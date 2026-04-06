from pathlib import Path

from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from src.api.schemas import OrderCreate, OrderRead
from src.data.repositories import (
    create_order,
    create_transaction,
    get_position_by_symbol,
    get_portfolio,
    list_positions,
    upsert_position_after_fill,
)
from src.execution.paper_broker import PaperBroker
from src.risk.limits import load_risk_limits


def execute_paper_order(db: Session, payload: OrderCreate, owner_id: int) -> OrderRead:
    portfolio = get_portfolio(db, payload.portfolio_id, owner_id=owner_id)
    if portfolio is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Portfolio not found")

    limits = load_risk_limits(Path(__file__).resolve().parents[2])
    notional = payload.quantity * payload.price
    open_positions = len(list_positions(db, portfolio_id=payload.portfolio_id))
    daily_loss = max(0.0, -float(payload.daily_realized_pnl))
    symbol = payload.symbol.strip().upper()
    asset_class = payload.asset_class.strip().lower()
    current_symbol_position = get_position_by_symbol(
        db, portfolio_id=payload.portfolio_id, symbol=symbol
    )

    violations: list[str] = []
    if notional > limits.max_order_notional:
        violations.append("max_order_notional_exceeded")
    symbol_limit = limits.max_order_notional_by_symbol.get(symbol)
    if symbol_limit is not None and notional > symbol_limit:
        violations.append("max_order_notional_by_symbol_exceeded")
    asset_class_limit = limits.max_order_notional_by_asset_class.get(asset_class)
    if asset_class_limit is not None and notional > asset_class_limit:
        violations.append("max_order_notional_by_asset_class_exceeded")
    if daily_loss > limits.max_daily_loss:
        violations.append("max_daily_loss_exceeded")
    if (
        payload.side == "buy"
        and current_symbol_position is None
        and open_positions >= limits.max_open_positions
    ):
        violations.append("max_open_positions_exceeded")
    if violations:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={"message": "Risk limits violation", "violations": violations},
        )

    if payload.side == "sell":
        if current_symbol_position is None:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Cannot sell a symbol without an open position")
        if payload.quantity > current_symbol_position.quantity:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Sell quantity exceeds current position quantity")

    broker = PaperBroker()
    filled = broker.submit_market_order(
        symbol=payload.symbol,
        side=payload.side,
        quantity=payload.quantity,
        price=payload.price,
        fee=payload.fee,
    )

    create_transaction(
        db,
        portfolio_id=payload.portfolio_id,
        symbol=filled.symbol,
        side=filled.side,
        quantity=filled.quantity,
        price=filled.price,
        fee=filled.fee,
    )
    create_order(
        db,
        order_id=filled.order_id,
        portfolio_id=payload.portfolio_id,
        symbol=filled.symbol,
        side=filled.side,
        quantity=filled.quantity,
        price=filled.price,
        fee=filled.fee,
        notional=filled.notional,
        status=filled.status,
    )

    upsert_position_after_fill(
        db,
        portfolio_id=payload.portfolio_id,
        symbol=filled.symbol,
        side=filled.side,
        quantity=filled.quantity,
        price=filled.price,
        asset_class=payload.asset_class,
    )

    return OrderRead(
        order_id=filled.order_id,
        portfolio_id=payload.portfolio_id,
        symbol=filled.symbol,
        side=filled.side,
        quantity=filled.quantity,
        price=filled.price,
        fee=filled.fee,
        notional=filled.notional,
        status=filled.status,
    )

