from collections import defaultdict

from src.data.models import Position


def normalize_target_allocation(raw_target: dict[str, float]) -> dict[str, float]:
    cleaned: dict[str, float] = {}
    for asset_class, value in raw_target.items():
        if value <= 0:
            continue
        cleaned[asset_class.lower()] = float(value)
    total = sum(cleaned.values())
    if total <= 0:
        return {}
    return {key: value / total for key, value in cleaned.items()}


def compute_allocation_by_asset_class(
    positions: list[Position],
    current_prices: dict[str, float],
) -> tuple[dict[str, float], float]:
    by_asset_class_notional: dict[str, float] = defaultdict(float)
    total_market_value = 0.0
    for position in positions:
        symbol = position.symbol.upper()
        price = float(current_prices.get(symbol, position.avg_cost))
        notional = position.quantity * price
        asset_class = position.asset_class.lower()
        by_asset_class_notional[asset_class] += notional
        total_market_value += notional

    if total_market_value <= 0:
        return {}, 0.0

    current_allocation = {
        asset_class: notional / total_market_value
        for asset_class, notional in by_asset_class_notional.items()
    }
    return current_allocation, total_market_value


def suggest_rebalance_actions(
    current_allocation: dict[str, float],
    target_allocation: dict[str, float],
    total_market_value: float,
    min_trade_notional: float,
) -> list[dict[str, object]]:
    actions: list[dict[str, object]] = []
    all_asset_classes = set(current_allocation.keys()) | set(target_allocation.keys())
    for asset_class in sorted(all_asset_classes):
        current_weight = current_allocation.get(asset_class, 0.0)
        target_weight = target_allocation.get(asset_class, 0.0)
        diff = target_weight - current_weight
        notional = abs(diff) * total_market_value
        if notional < min_trade_notional:
            continue
        action = "buy" if diff > 0 else "sell"
        actions.append(
            {
                "asset_class": asset_class,
                "action": action,
                "notional": round(notional, 2),
                "symbol_hint": f"{asset_class.upper()}_BASKET",
            }
        )
    return actions

