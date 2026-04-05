from collections import defaultdict
from datetime import date, timedelta

from src.data.models import Order, Position


def compute_position_market_value(position: Position, current_price: float) -> float:
    return position.quantity * current_price


def compute_position_cost_value(position: Position) -> float:
    return position.quantity * position.avg_cost


def compute_position_unrealized_pnl(position: Position, current_price: float) -> float:
    return compute_position_market_value(position, current_price) - compute_position_cost_value(position)


def compute_realized_pnl_for_day(orders: list[Order], target_day: date) -> dict[str, float]:
    sorted_orders = sorted(orders, key=lambda x: x.executed_at)
    inventory: dict[str, dict[str, float]] = defaultdict(lambda: {"qty": 0.0, "avg_cost": 0.0})
    realized_total = 0.0
    trades_count = 0
    notional_bought = 0.0
    notional_sold = 0.0

    for order in sorted_orders:
        symbol = order.symbol.upper()
        side = order.side.lower()
        position = inventory[symbol]
        qty = position["qty"]
        avg_cost = position["avg_cost"]

        if side == "buy":
            new_qty = qty + order.quantity
            total_cost = (qty * avg_cost) + (order.quantity * order.price) + order.fee
            position["qty"] = new_qty
            position["avg_cost"] = total_cost / new_qty if new_qty > 0 else 0.0
            if order.executed_at.date() == target_day:
                trades_count += 1
                notional_bought += order.notional
            continue

        sell_qty = min(order.quantity, qty)
        if sell_qty <= 0:
            continue
        fee_alloc = order.fee * (sell_qty / order.quantity)
        proceeds = (sell_qty * order.price) - fee_alloc
        cost_basis = sell_qty * avg_cost
        trade_realized = proceeds - cost_basis

        remaining_qty = qty - sell_qty
        position["qty"] = remaining_qty
        if remaining_qty <= 0:
            position["avg_cost"] = 0.0

        if order.executed_at.date() == target_day:
            trades_count += 1
            notional_sold += sell_qty * order.price
            realized_total += trade_realized

    return {
        "realized_pnl_day": realized_total,
        "trades_count_day": float(trades_count),
        "notional_bought_day": notional_bought,
        "notional_sold_day": notional_sold,
    }


def compute_realized_pnl_timeseries(orders: list[Order], days: int, end_day: date | None = None) -> list[dict[str, float | str]]:
    last_day = end_day or date.today()
    start_day = last_day - timedelta(days=days - 1)
    points: list[dict[str, float | str]] = []
    cumulative = 0.0

    for offset in range(days):
        target_day = start_day + timedelta(days=offset)
        day_metrics = compute_realized_pnl_for_day(orders, target_day)
        realized = float(day_metrics["realized_pnl_day"])
        cumulative += realized
        points.append(
            {
                "day": target_day.isoformat(),
                "realized_pnl_day": round(realized, 4),
                "cumulative_realized_pnl": round(cumulative, 4),
                "trades_count_day": int(day_metrics["trades_count_day"]),
            }
        )
    return points

