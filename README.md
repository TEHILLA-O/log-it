# Daily FinTech Signal Tracker

An automated Python project that collects selected financial signals each day, stores historical observations, generates a markdown market summary, and publishes updates through GitHub Actions.

## Signals tracked
- BTC/USD
- ETH/USD
- GBP/USD

## Why this project exists
This project demonstrates:
- API integration
- lightweight data engineering
- scheduled automation
- historical logging
- reproducible reporting
- GitHub Actions workflow design

## Stack
- Python
- requests
- pandas
- GitHub Actions

## Output
The pipeline updates:
- `data/raw/YYYY-MM-DD.json`
- `data/processed/history.csv`
- `reports/latest.md`

## Automation
The workflow runs daily on a GitHub Actions schedule and can also be triggered manually.

## Future improvements
- Add equities, rates, or volatility proxies
- Add simple anomaly detection
- Add charts
- Publish a small dashboard
