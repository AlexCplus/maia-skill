# patrimonio-autopilot

D1 foundation scaffold for a Python project.

## Setup

1. Create and activate a virtual environment.
2. Install dependencies:

```bash
pip install -r requirements.txt
```

3. Copy environment template and fill values:

```bash
copy .env.example .env
```

## Run smoke checks

From project root:

```bash
python -m compileall src
python src/ops/run_healthcheck.py
```

Optional alert plumbing test:

```bash
python src/ops/run_healthcheck.py --test-alert telegram
python src/ops/run_healthcheck.py --test-alert email
```

Notes:
- Healthcheck verifies required config files and environment variables.
- Alert tests fail explicitly when required environment values are missing.

## Run API (MVP patrimonio)

From project root:

```bash
uvicorn src.api.main:app --reload --port 8000
```

Main endpoints:
- `GET /health`
- `GET /portfolios`
- `POST /portfolios`
- `GET /portfolios/{portfolio_id}`
- `GET /portfolios/{portfolio_id}/positions`
- `POST /portfolios/{portfolio_id}/positions`
- `GET /portfolios/{portfolio_id}/transactions`
- `POST /portfolios/{portfolio_id}/transactions`
- `POST /portfolios/{portfolio_id}/analytics/pnl`
- `POST /portfolios/{portfolio_id}/analytics/daily-summary`
- `POST /portfolios/{portfolio_id}/analytics/performance`
- `POST /portfolios/{portfolio_id}/risk/check`
- `POST /portfolios/{portfolio_id}/strategy/rebalance`
- `POST /orders` (paper trading, con validación de riesgo)
- `GET /orders` (historial de órdenes, `?portfolio_id=` opcional)
- `GET /orders/balance/{portfolio_id}` (balance paper)

Example payloads:

```json
{
  "current_prices": {
    "AAPL": 212.35,
    "BTC": 68000
  }
}
```

```json
{
  "portfolio_id": 1,
  "symbol": "MSFT",
  "side": "buy",
  "quantity": 2,
  "price": 300,
  "fee": 1,
  "asset_class": "stock",
  "daily_realized_pnl": 0
}
```

```json
{
  "proposed_order_notional": 12000,
  "daily_realized_pnl": -350
}
```

```json
{
  "current_prices": {
    "AAPL": 212.35,
    "BTC": 68000
  },
  "target_allocation": {
    "stock": 0.6,
    "crypto": 0.4
  },
  "min_trade_notional": 25
}
```
