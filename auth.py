"""Autenticação simples de um único usuário administrador.

A senha nunca é armazenada em texto puro: só guardamos o hash (gerado com
werkzeug.security.generate_password_hash) na variável de ambiente
DASHBOARD_PASSWORD_HASH.
"""

import os

from werkzeug.security import check_password_hash

USERNAME = os.environ.get("DASHBOARD_USERNAME", "admin")
PASSWORD_HASH = os.environ.get("DASHBOARD_PASSWORD_HASH", "")


def verify_credentials(username: str, password: str) -> bool:
    if not PASSWORD_HASH:
        return False
    return username == USERNAME and check_password_hash(PASSWORD_HASH, password)
