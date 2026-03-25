from __future__ import annotations

from datetime import datetime, timezone

import pandas as pd
import requests

from utils import DATA_PROCESSED_DIR, DATA_RAW_DIR, load_json, save_json

COINGECKO_URL = "https://api.coingecko.com/api/v3/simple/price"
FRANKFURTER_URL = "https://api.frankfurter.dev/v1/latest?base=GBP&symbols=USD"

HEADERS = {
    "accept": "application/json",
    "user-agent": "daily-fintech-signal-tracker/1.0",
}


def fetch_crypto_prices() -> dict:
    params = {
        "ids": "bitcoin,ethereum",
        "vs_currencies": "usd",
        "include_24hr_change": "true",
        "include_last_updated_at": "true",
    }
    response = requests.get(COINGECKO_URL, params=params, headers=HEADERS, timeout=30)
    response.raise_for_status()
    return response.json()


def fetch_fx_rate() -> dict:
    response = requests.get(FRANKFURTER_URL, headers=HEADERS, timeout=30)
    response.raise_for_status()
    return response.json()


def main() -> None:
    now = datetime.now(timezone.utc)
    today = now.date().isoformat()
    raw_file = DATA_RAW_DIR / f"{today}.json"
    history_file = DATA_PROCESSED_DIR / "history.csv"

    crypto = fetch_crypto_prices()
    fx = fetch_fx_rate()

    payload = {
        "date": today,
        "generated_at_utc": now.isoformat(),
        "signals": {
            "btc_usd": {
                "price": crypto["bitcoin"]["usd"],
                "change_24h_pct": crypto["bitcoin"].get("usd_24h_change"),
                "last_updated_at": crypto["bitcoin"].get("last_updated_at"),
            },
            "eth_usd": {
                "price": crypto["ethereum"]["usd"],
                "change_24h_pct": crypto["ethereum"].get("usd_24h_change"),
                "last_updated_at": crypto["ethereum"].get("last_updated_at"),
            },
            "gbp_usd": {
                "price": fx["rates"]["USD"],
                "source_date": fx.get("date"),
            },
        },
    }

    previous_payload = load_json(raw_file)
    if previous_payload != payload:
        save_json(raw_file, payload)

    row = {
        "date": today,
        "generated_at_utc": now.isoformat(),
        "btc_usd": payload["signals"]["btc_usd"]["price"],
        "btc_24h_change_pct": payload["signals"]["btc_usd"]["change_24h_pct"],
        "eth_usd": payload["signals"]["eth_usd"]["price"],
        "eth_24h_change_pct": payload["signals"]["eth_usd"]["change_24h_pct"],
        "gbp_usd": payload["signals"]["gbp_usd"]["price"],
    }

    if history_file.exists():
        df = pd.read_csv(history_file)
        df = df[df["date"] != today]
        df = pd.concat([df, pd.DataFrame([row])], ignore_index=True)
    else:
        df = pd.DataFrame([row])

    df = df.sort_values("date").reset_index(drop=True)
    df.to_csv(history_file, index=False)


if __name__ == "__main__":
    main()
