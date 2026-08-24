"""Integração com a API pública Open-Meteo (não exige chave de API)."""

import requests

GEOCODING_URL = "https://geocoding-api.open-meteo.com/v1/search"
FORECAST_URL = "https://api.open-meteo.com/v1/forecast"


class CityNotFoundError(Exception):
    pass


def get_weather(city: str, timeout: int = 8) -> dict:
    geo_resp = requests.get(
        GEOCODING_URL,
        params={"name": city, "count": 1, "language": "pt", "format": "json"},
        timeout=timeout,
    )
    geo_resp.raise_for_status()
    results = geo_resp.json().get("results")
    if not results:
        raise CityNotFoundError(f"Cidade não encontrada: {city}")

    place = results[0]

    forecast_resp = requests.get(
        FORECAST_URL,
        params={
            "latitude": place["latitude"],
            "longitude": place["longitude"],
            "current": "temperature_2m,relative_humidity_2m,wind_speed_10m",
            "timezone": "auto",
        },
        timeout=timeout,
    )
    forecast_resp.raise_for_status()
    current = forecast_resp.json()["current"]

    return {
        "city": place["name"],
        "country": place.get("country", ""),
        "temperature_c": current["temperature_2m"],
        "humidity_pct": current["relative_humidity_2m"],
        "wind_kmh": current["wind_speed_10m"],
    }
