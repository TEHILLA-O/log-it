from __future__ import annotations

import pandas as pd

from utils import DATA_PROCESSED_DIR, REPORTS_DIR, safe_pct_change

HISTORY_FILE = DATA_PROCESSED_DIR / "history.csv"
REPORT_FILE = REPORTS_DIR / "latest.md"


def format_change(value: float | None) -> str:
    if value is None:
        return "N/A"
    return f"{value:+.2f}%"


def direction_word(value: float | None) -> str:
    if value is None:
        return "was unavailable"
    if value > 0:
        return "rose"
    if value < 0:
        return "fell"
    return "was flat"


def main() -> None:
    if not HISTORY_FILE.exists():
        raise FileNotFoundError("history.csv not found. Run fetch_data.py first.")

    df = pd.read_csv(HISTORY_FILE).sort_values("date").reset_index(drop=True)
    latest = df.iloc[-1]
    previous = df.iloc[-2] if len(df) > 1 else None

    btc_day_change = None if previous is None else safe_pct_change(latest["btc_usd"], previous["btc_usd"])
    eth_day_change = None if previous is None else safe_pct_change(latest["eth_usd"], previous["eth_usd"])
    fx_day_change = None if previous is None else safe_pct_change(latest["gbp_usd"], previous["gbp_usd"])

    report = f"""# Daily FinTech Signal Tracker — {latest['date']}

## Snapshot
- BTC/USD: {latest['btc_usd']:.2f}
- ETH/USD: {latest['eth_usd']:.2f}
- GBP/USD: {latest['gbp_usd']:.4f}

## Day-over-day movement
- BTC/USD: {format_change(btc_day_change)}
- ETH/USD: {format_change(eth_day_change)}
- GBP/USD: {format_change(fx_day_change)}

## 24-hour crypto movement
- BTC 24h: {format_change(latest['btc_24h_change_pct'])}
- ETH 24h: {format_change(latest['eth_24h_change_pct'])}

## Brief interpretation
Bitcoin {direction_word(btc_day_change)} day over day, Ethereum {direction_word(eth_day_change)}, and GBP/USD {direction_word(fx_day_change)}. This update is generated automatically from the project pipeline and committed by GitHub Actions.

## Files updated
- data/processed/history.csv
- reports/latest.md
"""

    REPORT_FILE.write_text(report, encoding="utf-8")


if __name__ == "__main__":
    main()
