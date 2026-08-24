"""Dashboard web: clima + criptomoedas, com login e boas práticas de segurança."""

import os
import secrets
from functools import wraps

import requests
from dotenv import load_dotenv
from flask import Flask, jsonify, redirect, render_template, request, session, url_for
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

from auth import verify_credentials
from services.crypto import get_crypto_prices
from services.weather import CityNotFoundError, get_weather
from validation import is_valid_city

load_dotenv()

app = Flask(__name__)
app.config.update(
    SECRET_KEY=os.environ.get("FLASK_SECRET_KEY") or secrets.token_hex(32),
    SESSION_COOKIE_HTTPONLY=True,
    SESSION_COOKIE_SAMESITE="Lax",
    SESSION_COOKIE_SECURE=os.environ.get("FLASK_ENV") == "production",
)

limiter = Limiter(get_remote_address, app=app, default_limits=["200 per hour"])


@app.after_request
def set_security_headers(response):
    response.headers["X-Frame-Options"] = "DENY"
    response.headers["X-Content-Type-Options"] = "nosniff"
    response.headers["Referrer-Policy"] = "no-referrer"
    response.headers["Content-Security-Policy"] = "default-src 'self'; style-src 'self' 'unsafe-inline'"
    return response


def login_required(view):
    @wraps(view)
    def wrapped(*args, **kwargs):
        if not session.get("user"):
            return redirect(url_for("login"))
        return view(*args, **kwargs)
    return wrapped


@app.route("/login", methods=["GET", "POST"])
@limiter.limit("5 per minute")
def login():
    error = None
    if request.method == "POST":
        username = request.form.get("username", "")
        password = request.form.get("password", "")
        if verify_credentials(username, password):
            session.clear()
            session["user"] = username
            return redirect(url_for("dashboard"))
        error = "Usuário ou senha inválidos."
    return render_template("login.html", error=error)


@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("login"))


@app.route("/")
@login_required
def dashboard():
    return render_template("dashboard.html", username=session["user"])


@app.route("/api/weather")
@login_required
@limiter.limit("20 per minute")
def api_weather():
    city = request.args.get("city", "").strip()
    if not is_valid_city(city):
        return jsonify({"error": "Nome de cidade inválido."}), 400
    try:
        data = get_weather(city)
    except CityNotFoundError:
        return jsonify({"error": "Cidade não encontrada."}), 404
    except requests.RequestException:
        return jsonify({"error": "Erro ao consultar a previsão do tempo."}), 502
    return jsonify(data)


@app.route("/api/crypto")
@login_required
@limiter.limit("20 per minute")
def api_crypto():
    try:
        data = get_crypto_prices()
    except requests.RequestException:
        return jsonify({"error": "Erro ao consultar preços de criptomoedas."}), 502
    return jsonify(data)


if __name__ == "__main__":
    app.run(debug=os.environ.get("FLASK_DEBUG") == "1")
