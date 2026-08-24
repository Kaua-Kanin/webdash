"""Validação de entrada do usuário (defesa contra injeção/abuso)."""

import re

CITY_PATTERN = re.compile(r"^[A-Za-zÀ-ÿ\s\-']{2,60}$")


def is_valid_city(city: str) -> bool:
    return bool(CITY_PATTERN.match(city.strip()))
