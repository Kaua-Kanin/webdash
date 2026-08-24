"""Integração com a API pública CoinGecko (não exige chave de API)."""

import requests

PRICE_URL = "https://api.coingecko.com/api/v3/simple/price"

COINS = {"bitcoin": "Bitcoin", "ethereum": "Ethereum", "solana": "Solana"}


def get_crypto_prices(timeout: int = 8) -> list:
    resp = requests.get(
        PRICE_URL,
        params={"ids": ",".join(COINS), "vs_currencies": "usd,brl"},
        timeout=timeout,
    )
    resp.raise_for_status()
    data = resp.json()

    return [
        {
            "id": coin_id,
            "name": label,
            "usd": data.get(coin_id, {}).get("usd"),
            "brl": data.get(coin_id, {}).get("brl"),
        }
        for coin_id, label in COINS.items()
    ]
