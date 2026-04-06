from statistics import mean

from src.data.models import Position


def _simple_signal_from_prices(prices: list[float]) -> tuple[str, float]:
    if len(prices) < 2:
        return "hold", 0.0
    short_window = prices[-3:] if len(prices) >= 3 else prices
    long_window = prices[-7:] if len(prices) >= 7 else prices
    short_ma = mean(short_window)
    long_ma = mean(long_window)
    if long_ma <= 0:
        return "hold", 0.0
    diff_ratio = (short_ma - long_ma) / long_ma
    confidence = min(abs(diff_ratio) * 100, 95.0)
    if diff_ratio > 0.01:
        return "buy", round(confidence, 4)
    if diff_ratio < -0.01:
        return "sell", round(confidence, 4)
    return "hold", round(confidence, 4)


def suggest_trade_from_prices(
    symbol: str,
    asset_class: str,
    prices: list[float],
    current_positions: list[Position],
) -> dict[str, float | str]:
    side, confidence = _simple_signal_from_prices(prices)
    if side == "hold":
        return {
            "symbol": symbol.upper(),
            "asset_class": asset_class.lower(),
            "side": "hold",
            "confidence": confidence,
            "reason": "No clear momentum edge in moving-average spread",
            "suggested_price": float(prices[-1]) if prices else 0.0,
            "suggested_quantity": 0.0,
        }

    last_price = float(prices[-1])
    existing = next((p for p in current_positions if p.symbol.upper() == symbol.upper()), None)
    if side == "sell" and (existing is None or existing.quantity <= 0):
        return {
            "symbol": symbol.upper(),
            "asset_class": asset_class.lower(),
            "side": "hold",
            "confidence": confidence,
            "reason": "Sell signal ignored because there is no open position",
            "suggested_price": last_price,
            "suggested_quantity": 0.0,
        }

    base_notional = 1000.0
    risk_scale = max(0.2, min(confidence / 100.0, 1.0))
    target_notional = base_notional * risk_scale
    qty = round(target_notional / last_price, 6) if last_price > 0 else 0.0
    if side == "sell" and existing is not None:
        qty = min(qty, float(existing.quantity))
    if qty <= 0:
        side = "hold"

    return {
        "symbol": symbol.upper(),
        "asset_class": asset_class.lower(),
        "side": side,
        "confidence": confidence,
        "reason": "Signal based on short-vs-long moving-average momentum",
        "suggested_price": last_price,
        "suggested_quantity": float(qty),
    }

