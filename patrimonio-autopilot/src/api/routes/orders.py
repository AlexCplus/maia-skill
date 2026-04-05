from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from src.api.auth import get_current_user
from src.api.schemas import OrderCreate, OrderRead, PaperBalanceRead
from src.data.database import get_db
from src.data.models import User
from src.data.repositories import get_portfolio, list_orders, list_positions
from src.execution.order_service import execute_paper_order


router = APIRouter(prefix="/orders", tags=["orders"])


@router.post("", response_model=OrderRead, status_code=status.HTTP_201_CREATED)
def post_order(
    payload: OrderCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> OrderRead:
    return execute_paper_order(db, payload, owner_id=current_user.id)


@router.get("", response_model=list[OrderRead])
def get_orders(
    portfolio_id: int | None = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> list[OrderRead]:
    items = list_orders(db, owner_id=current_user.id, portfolio_id=portfolio_id)
    return [
        OrderRead(
            order_id=o.order_id,
            portfolio_id=o.portfolio_id,
            symbol=o.symbol,
            side=o.side,
            quantity=o.quantity,
            price=o.price,
            fee=o.fee,
            notional=o.notional,
            status=o.status,
        )
        for o in items
    ]


@router.get("/balance/{portfolio_id}", response_model=PaperBalanceRead)
def get_paper_balance(
    portfolio_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> PaperBalanceRead:
    portfolio = get_portfolio(db, portfolio_id, owner_id=current_user.id)
    if portfolio is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Portfolio not found")

    initial_cash = 100_000.0
    orders = list_orders(db, owner_id=current_user.id, portfolio_id=portfolio_id)
    positions = list_positions(db, portfolio_id=portfolio_id)

    net_cash_flow = 0.0
    for order in orders:
        gross = order.quantity * order.price
        if order.side == "buy":
            net_cash_flow -= gross + order.fee
        else:
            net_cash_flow += gross - order.fee

    cash_balance = initial_cash + net_cash_flow
    position_market_value = sum(p.quantity * p.avg_cost for p in positions)
    invested_notional = max(0.0, initial_cash - cash_balance)
    equity_estimate = cash_balance + position_market_value

    return PaperBalanceRead(
        portfolio_id=portfolio_id,
        initial_cash=round(initial_cash, 4),
        cash_balance=round(cash_balance, 4),
        invested_notional=round(invested_notional, 4),
        position_market_value=round(position_market_value, 4),
        equity_estimate=round(equity_estimate, 4),
    )

