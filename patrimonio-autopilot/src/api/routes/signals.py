from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from src.api.auth import get_current_user
from src.api.schemas import AISignalGenerateRequest, AISignalGenerateResponse, AISignalRead, OrderCreate, OrderRead
from src.data.database import get_db
from src.data.models import User
from src.data.repositories import (
    create_ai_signal,
    get_portfolio,
    list_ai_signals,
    list_positions,
    mark_ai_signal_executed,
)
from src.execution.order_service import execute_paper_order
from src.strategy.signal_engine import suggest_trade_from_prices


router = APIRouter(prefix="/signals", tags=["signals"])


@router.post("/generate", response_model=AISignalGenerateResponse, status_code=status.HTTP_201_CREATED)
def generate_signal(
    payload: AISignalGenerateRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> AISignalGenerateResponse:
    portfolio = get_portfolio(db, payload.portfolio_id, owner_id=current_user.id)
    if portfolio is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Portfolio not found")

    positions = list_positions(db, portfolio_id=payload.portfolio_id)
    suggestion = suggest_trade_from_prices(
        symbol=payload.symbol,
        asset_class=payload.asset_class,
        prices=payload.prices,
        current_positions=positions,
    )

    signal = create_ai_signal(
        db=db,
        portfolio_id=payload.portfolio_id,
        symbol=str(suggestion["symbol"]),
        asset_class=str(suggestion["asset_class"]),
        side=str(suggestion["side"]),
        confidence=float(suggestion["confidence"]),
        reason=str(suggestion["reason"]),
        suggested_price=float(suggestion["suggested_price"]),
        suggested_quantity=float(suggestion["suggested_quantity"]),
    )
    signal_read = AISignalRead(
        id=signal.id,
        portfolio_id=signal.portfolio_id,
        symbol=signal.symbol,
        asset_class=signal.asset_class,
        side=signal.side,
        confidence=signal.confidence,
        reason=signal.reason,
        suggested_price=signal.suggested_price,
        suggested_quantity=signal.suggested_quantity,
        status=signal.status,
        executed_order_id=signal.executed_order_id,
    )

    if (not payload.auto_execute) or signal.side == "hold" or signal.suggested_quantity <= 0:
        return AISignalGenerateResponse(signal=signal_read, executed_order=None)

    order = execute_paper_order(
        db=db,
        payload=OrderCreate(
            portfolio_id=payload.portfolio_id,
            symbol=signal.symbol,
            side=signal.side,
            quantity=signal.suggested_quantity,
            price=signal.suggested_price,
            fee=0,
            asset_class=signal.asset_class,
            daily_realized_pnl=0,
        ),
        owner_id=current_user.id,
    )
    mark_ai_signal_executed(db, signal_id=signal.id, order_id=order.order_id)
    return AISignalGenerateResponse(
        signal=AISignalRead(
            id=signal.id,
            portfolio_id=signal.portfolio_id,
            symbol=signal.symbol,
            asset_class=signal.asset_class,
            side=signal.side,
            confidence=signal.confidence,
            reason=signal.reason,
            suggested_price=signal.suggested_price,
            suggested_quantity=signal.suggested_quantity,
            status="executed",
            executed_order_id=order.order_id,
        ),
        executed_order=OrderRead(
            order_id=order.order_id,
            portfolio_id=order.portfolio_id,
            symbol=order.symbol,
            side=order.side,
            quantity=order.quantity,
            price=order.price,
            fee=order.fee,
            notional=order.notional,
            status=order.status,
        ),
    )


@router.get("/{portfolio_id}", response_model=list[AISignalRead])
def get_signals(
    portfolio_id: int,
    limit: int = 50,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> list[AISignalRead]:
    portfolio = get_portfolio(db, portfolio_id, owner_id=current_user.id)
    if portfolio is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Portfolio not found")
    rows = list_ai_signals(db, portfolio_id=portfolio_id, owner_id=current_user.id, limit=max(1, min(limit, 200)))
    return [
        AISignalRead(
            id=row.id,
            portfolio_id=row.portfolio_id,
            symbol=row.symbol,
            asset_class=row.asset_class,
            side=row.side,
            confidence=row.confidence,
            reason=row.reason,
            suggested_price=row.suggested_price,
            suggested_quantity=row.suggested_quantity,
            status=row.status,
            executed_order_id=row.executed_order_id,
        )
        for row in rows
    ]

