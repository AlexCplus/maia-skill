# patrimonio-autopilot

Sistema de paper trading automatizado que complementa el análisis MAIA.

## Características

- **Autopilot 24/7**: Loop automático que analiza y ejecuta trades
- **Integración MAIA**: Lee recomendaciones del `report_v2.json` generado por los agentes
- **Precios reales**: Soporte para Yahoo Finance y CoinGecko (con fallback a simulación)
- **Gestión de riesgo**: Límites configurables por símbolo/clase de activo
- **Multi-usuario**: Auth JWT con portfolios separados por usuario

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

## Run API

```bash
uvicorn src.api.main:app --reload --port 8000
```

## MAIA Integration

El autopilot puede usar las recomendaciones del sistema MAIA automáticamente:

1. **Report Bridge**: Lee `dashboard/public/data/report_v2.json`
2. **Picks to Watchlist**: Convierte recomendaciones BUY en watchlist automática
3. **Position Sizing**: Usa el `position_size` del report para calcular cantidades

### Configuración Autopilot

```json
POST /autopilot/start
{
  "portfolio_id": 1,
  "interval_seconds": 60,
  "auto_execute": true,
  "watchlist": [],  // Opcional: símbolos extra
  "use_report": true,  // Usar recomendaciones MAIA
  "use_real_prices": true,  // Yahoo Finance / CoinGecko
  "min_confidence": 7.0  // Solo picks con confianza >= 7
}
```

### Endpoints del Report

- `GET /autopilot/report/info` - Metadata del report actual
- `GET /autopilot/report/picks?min_confidence=7&recommendation=buy` - Lista de picks
- `GET /autopilot/prices/check` - Proveedores de precio disponibles
- `GET /autopilot/prices/{symbol}` - Precio actual de un símbolo
- `GET /autopilot/analysis/status` - Estado del skill MAIA

### Actualizar el Análisis MAIA

Para regenerar el report con nuevas recomendaciones:

```bash
# Usando GitHub Copilot CLI
copilot chat --skill maia-skill

# O invoca el skill desde VS Code Copilot
```

El report se guarda en `dashboard/public/data/report_v2.json` y es leído automáticamente por el autopilot en el siguiente tick.

## API Endpoints

### Auth
- `POST /auth/register` - Crear usuario
- `POST /auth/login` - Login (devuelve JWT)

### Portfolios
- `GET /portfolios`
- `POST /portfolios`
- `GET /portfolios/{id}`
- `PUT /portfolios/{id}`
- `DELETE /portfolios/{id}`

### Positions & Transactions
- `GET /portfolios/{id}/positions`
- `POST /portfolios/{id}/positions`
- `GET /portfolios/{id}/transactions`
- `POST /portfolios/{id}/transactions`

### Analytics
- `POST /portfolios/{id}/analytics/pnl`
- `POST /portfolios/{id}/analytics/daily-summary`
- `POST /portfolios/{id}/analytics/performance`

### Risk & Strategy
- `POST /portfolios/{id}/risk/check`
- `POST /portfolios/{id}/strategy/rebalance`

### Orders (Paper Trading)
- `POST /orders`
- `GET /orders`
- `GET /orders/balance/{portfolio_id}`

### AI Signals
- `POST /signals/generate`
- `GET /signals/{portfolio_id}`

### Autopilot
- `POST /autopilot/start`
- `POST /autopilot/stop/{portfolio_id}`
- `GET /autopilot/status/{portfolio_id}`
- `GET /autopilot/status`
- `GET /autopilot/report/info`
- `GET /autopilot/report/picks`
- `GET /autopilot/prices/check`
- `GET /autopilot/prices/{symbol}`
- `GET /autopilot/analysis/status`

## Configuración de Riesgo

Edita `config/risk.limits.yaml`:

```yaml
max_daily_loss: 500
max_open_positions: 10
max_order_notional: 5000
max_order_notional_by_asset_class:
  crypto: 10000
  stock: 5000
max_order_notional_by_symbol:
  BTC: 20000
```

## Migración de DB Legacy

Si tenías una DB antes del soporte multi-usuario:

```bash
python src/ops/migrate_auth_schema.py
```
