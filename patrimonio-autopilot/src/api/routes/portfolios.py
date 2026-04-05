from pathlib import Path
from datetime import date

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from src.api.auth import get_current_user
from src.api.schemas import (
    DailySummaryRead,
    DailySummaryRequest,
    PerformanceRead,
    PerformanceRequest,
    PerformancePointRead,
    PnLRequest,
    PortfolioPnLRead,
    PortfolioCreate,
    PortfolioRead,
    PositionCreate,
    RebalanceRead,
    RebalanceRequest,
    RiskCheckRead,
    RiskCheckRequest,
    PositionRead,
    PositionPnLRead,
    TransactionCreate,
    TransactionRead,
)
from src.data.database import get_db
from src.data.models import User
from src.data.repositories import (
    create_portfolio,
    create_position,
    create_transaction,
    get_portfolio,
    list_orders_for_portfolio,
    list_portfolios,
    list_positions,
    list_transactions,
)
from src.risk.limits import load_risk_limits
from src.strategy.analytics import (
    compute_position_cost_value,
    compute_position_market_value,
    compute_realized_pnl_for_day,
    compute_realized_pnl_timeseries,
    compute_position_unrealized_pnl,
)
from src.strategy.rebalancer import (
    compute_allocation_by_asset_class,
    normalize_target_allocation,
    suggest_rebalance_actions,
)


router = APIRouter(prefix="/portfolios", tags=["portfolios"])


@router.get("", response_model=list[PortfolioRead])
def get_portfolios(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> list[PortfolioRead]:
    return list_portfolios(db, owner_id=current_user.id)


@router.post("", response_model=PortfolioRead, status_code=status.HTTP_201_CREATED)
def post_portfolio(
    payload: PortfolioCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> PortfolioRead:
    return create_portfolio(db, owner_id=current_user.id, name=payload.name, base_currency=payload.base_currency.upper())


@router.get("/{portfolio_id}", response_model=PortfolioRead)
def get_portfolio_by_id(
    portfolio_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> PortfolioRead:
    portfolio = get_portfolio(db, portfolio_id, owner_id=current_user.id)
    if portfolio is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Portfolio not found")
    return portfolio


@router.get("/{portfolio_id}/positions", response_model=list[PositionRead])
def get_positions(
    portfolio_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> list[PositionRead]:
    portfolio = get_portfolio(db, portfolio_id, owner_id=current_user.id)
    if portfolio is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Portfolio not found")
    return list_positions(db, portfolio_id=portfolio_id)


@router.post("/{portfolio_id}/positions", response_model=PositionRead, status_code=status.HTTP_201_CREATED)
def post_position(
    portfolio_id: int,
    payload: PositionCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> PositionRead:
    portfolio = get_portfolio(db, portfolio_id, owner_id=current_user.id)
    if portfolio is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Portfolio not found")
    return create_position(
        db,
        portfolio_id=portfolio_id,
        symbol=payload.symbol,
        quantity=payload.quantity,
        avg_cost=payload.avg_cost,
        asset_class=payload.asset_class,
    )


@router.get("/{portfolio_id}/transactions", response_model=list[TransactionRead])
def get_transactions(
    portfolio_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> list[TransactionRead]:
    portfolio = get_portfolio(db, portfolio_id, owner_id=current_user.id)
    if portfolio is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Portfolio not found")
    return list_transactions(db, portfolio_id=portfolio_id)


@router.post(
    "/{portfolio_id}/transactions",
    response_model=TransactionRead,
    status_code=status.HTTP_201_CREATED,
)
def post_transaction(
    portfolio_id: int,
    payload: TransactionCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> TransactionRead:
    portfolio = get_portfolio(db, portfolio_id, owner_id=current_user.id)
    if portfolio is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Portfolio not found")
    return create_transaction(
        db,
        portfolio_id=portfolio_id,
        symbol=payload.symbol,
        side=payload.side,
        quantity=payload.quantity,
        price=payload.price,
        fee=payload.fee,
    )


@router.post("/{portfolio_id}/analytics/pnl", response_model=PortfolioPnLRead)
def get_portfolio_pnl(
    portfolio_id: int,
    payload: PnLRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> PortfolioPnLRead:
    portfolio = get_portfolio(db, portfolio_id, owner_id=current_user.id)
    if portfolio is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Portfolio not found")

    positions = list_positions(db, portfolio_id=portfolio_id)
    rows: list[PositionPnLRead] = []
    total_cost = 0.0
    total_market = 0.0

    for position in positions:
        symbol = position.symbol.upper()
        current_price = float(payload.current_prices.get(symbol, position.avg_cost))
        cost_value = compute_position_cost_value(position)
        market_value = compute_position_market_value(position, current_price)
        unrealized_pnl = compute_position_unrealized_pnl(position, current_price)
        pnl_pct = (unrealized_pnl / cost_value * 100) if cost_value > 0 else 0.0
        total_cost += cost_value
        total_market += market_value
        rows.append(
            PositionPnLRead(
                symbol=position.symbol,
                asset_class=position.asset_class,
                quantity=position.quantity,
                avg_cost=position.avg_cost,
                current_price=current_price,
                cost_value=round(cost_value, 4),
                market_value=round(market_value, 4),
                unrealized_pnl=round(unrealized_pnl, 4),
                unrealized_pnl_pct=round(pnl_pct, 4),
            )
        )

    total_unrealized = total_market - total_cost
    total_unrealized_pct = (total_unrealized / total_cost * 100) if total_cost > 0 else 0.0
    return PortfolioPnLRead(
        portfolio_id=portfolio_id,
        total_cost_value=round(total_cost, 4),
        total_market_value=round(total_market, 4),
        total_unrealized_pnl=round(total_unrealized, 4),
        total_unrealized_pnl_pct=round(total_unrealized_pct, 4),
        positions=rows,
    )


@router.post("/{portfolio_id}/risk/check", response_model=RiskCheckRead)
def check_portfolio_risk(
    portfolio_id: int,
    payload: RiskCheckRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> RiskCheckRead:
    portfolio = get_portfolio(db, portfolio_id, owner_id=current_user.id)
    if portfolio is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Portfolio not found")

    project_root = Path(__file__).resolve().parents[3]
    limits = load_risk_limits(project_root)
    positions = list_positions(db, portfolio_id=portfolio_id)
    open_positions = len(positions)
    daily_loss = max(0.0, -float(payload.daily_realized_pnl))
    violations: list[str] = []

    if open_positions > limits.max_open_positions:
        violations.append("max_open_positions_exceeded")
    if payload.proposed_order_notional > limits.max_order_notional:
        violations.append("max_order_notional_exceeded")
    if daily_loss > limits.max_daily_loss:
        violations.append("max_daily_loss_exceeded")

    return RiskCheckRead(
        portfolio_id=portfolio_id,
        passed=len(violations) == 0,
        max_open_positions=limits.max_open_positions,
        max_daily_loss=limits.max_daily_loss,
        max_order_notional=limits.max_order_notional,
        open_positions=open_positions,
        daily_loss=round(daily_loss, 4),
        proposed_order_notional=round(payload.proposed_order_notional, 4),
        violations=violations,
    )


@router.post("/{portfolio_id}/strategy/rebalance", response_model=RebalanceRead)
def rebalance_portfolio(
    portfolio_id: int,
    payload: RebalanceRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> RebalanceRead:
    portfolio = get_portfolio(db, portfolio_id, owner_id=current_user.id)
    if portfolio is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Portfolio not found")

    positions = list_positions(db, portfolio_id=portfolio_id)
    normalized_target = normalize_target_allocation(payload.target_allocation)
    if not normalized_target:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="target_allocation must contain positive weights")

    current_allocation, total_market_value = compute_allocation_by_asset_class(
        positions=positions,
        current_prices=payload.current_prices,
    )
    actions = suggest_rebalance_actions(
        current_allocation=current_allocation,
        target_allocation=normalized_target,
        total_market_value=total_market_value,
        min_trade_notional=payload.min_trade_notional,
    )
    return RebalanceRead(
        portfolio_id=portfolio_id,
        total_market_value=round(total_market_value, 4),
        current_allocation={k: round(v, 6) for k, v in current_allocation.items()},
        target_allocation={k: round(v, 6) for k, v in normalized_target.items()},
        actions=actions,
    )


@router.post("/{portfolio_id}/analytics/daily-summary", response_model=DailySummaryRead)
def get_daily_summary(
    portfolio_id: int,
    payload: DailySummaryRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> DailySummaryRead:
    portfolio = get_portfolio(db, portfolio_id, owner_id=current_user.id)
    if portfolio is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Portfolio not found")

    summary_day = date.fromisoformat(payload.day) if payload.day else date.today()
    orders = list_orders_for_portfolio(db, portfolio_id=portfolio_id, owner_id=current_user.id)
    realized = compute_realized_pnl_for_day(orders=orders, target_day=summary_day)

    positions = list_positions(db, portfolio_id=portfolio_id)
    unrealized_total = 0.0
    for position in positions:
        symbol = position.symbol.upper()
        current_price = float(payload.current_prices.get(symbol, position.avg_cost))
        unrealized_total += compute_position_unrealized_pnl(position, current_price)

    realized_total = float(realized["realized_pnl_day"])
    return DailySummaryRead(
        portfolio_id=portfolio_id,
        day=summary_day.isoformat(),
        trades_count_day=int(realized["trades_count_day"]),
        notional_bought_day=round(float(realized["notional_bought_day"]), 4),
        notional_sold_day=round(float(realized["notional_sold_day"]), 4),
        realized_pnl_day=round(realized_total, 4),
        unrealized_pnl_snapshot=round(unrealized_total, 4),
        total_pnl_snapshot=round(realized_total + unrealized_total, 4),
    )


@router.post("/{portfolio_id}/analytics/performance", response_model=PerformanceRead)
def get_performance_series(
    portfolio_id: int,
    payload: PerformanceRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> PerformanceRead:
    portfolio = get_portfolio(db, portfolio_id, owner_id=current_user.id)
    if portfolio is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Portfolio not found")

    orders = list_orders_for_portfolio(db, portfolio_id=portfolio_id, owner_id=current_user.id)
    series_raw = compute_realized_pnl_timeseries(orders=orders, days=payload.days)
    return PerformanceRead(
        portfolio_id=portfolio_id,
        days=payload.days,
        series=[
            PerformancePointRead(
                day=str(row["day"]),
                realized_pnl_day=float(row["realized_pnl_day"]),
                cumulative_realized_pnl=float(row["cumulative_realized_pnl"]),
                trades_count_day=int(row["trades_count_day"]),
            )
            for row in series_raw
        ],
    )

