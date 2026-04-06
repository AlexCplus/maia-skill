from datetime import datetime
from typing import Literal

from pydantic import BaseModel, ConfigDict, Field


class PortfolioCreate(BaseModel):
    name: str = Field(min_length=1, max_length=128)
    base_currency: str = Field(default="USD", min_length=3, max_length=8)


class PortfolioUpdate(BaseModel):
    name: str = Field(min_length=1, max_length=128)
    base_currency: str = Field(default="USD", min_length=3, max_length=8)


class PortfolioRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
    base_currency: str
    created_at: datetime
    updated_at: datetime


class PositionCreate(BaseModel):
    symbol: str = Field(min_length=1, max_length=32)
    quantity: float = Field(gt=0)
    avg_cost: float = Field(gt=0)
    asset_class: str = Field(default="stock", min_length=1, max_length=32)


class PositionRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    portfolio_id: int
    symbol: str
    quantity: float
    avg_cost: float
    asset_class: str
    created_at: datetime
    updated_at: datetime


class TransactionCreate(BaseModel):
    symbol: str = Field(min_length=1, max_length=32)
    side: Literal["buy", "sell"]
    quantity: float = Field(gt=0)
    price: float = Field(gt=0)
    fee: float = Field(default=0, ge=0)


class TransactionRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    portfolio_id: int
    symbol: str
    side: str
    quantity: float
    price: float
    fee: float
    executed_at: datetime


class PnLRequest(BaseModel):
    current_prices: dict[str, float] = Field(default_factory=dict)


class PositionPnLRead(BaseModel):
    symbol: str
    asset_class: str
    quantity: float
    avg_cost: float
    current_price: float
    cost_value: float
    market_value: float
    unrealized_pnl: float
    unrealized_pnl_pct: float


class PortfolioPnLRead(BaseModel):
    portfolio_id: int
    total_cost_value: float
    total_market_value: float
    total_unrealized_pnl: float
    total_unrealized_pnl_pct: float
    positions: list[PositionPnLRead]


class RiskCheckRequest(BaseModel):
    proposed_order_notional: float = Field(default=0, ge=0)
    daily_realized_pnl: float = 0
    symbol: str | None = None
    asset_class: str | None = None


class RiskCheckRead(BaseModel):
    portfolio_id: int
    passed: bool
    max_open_positions: int
    max_daily_loss: float
    max_order_notional: float
    max_order_notional_by_asset_class: dict[str, float]
    max_order_notional_by_symbol: dict[str, float]
    open_positions: int
    daily_loss: float
    proposed_order_notional: float
    violations: list[str]


class RebalanceRequest(BaseModel):
    current_prices: dict[str, float] = Field(default_factory=dict)
    target_allocation: dict[str, float] = Field(default_factory=dict)
    min_trade_notional: float = Field(default=10, gt=0)


class RebalanceActionRead(BaseModel):
    asset_class: str
    action: Literal["buy", "sell"]
    notional: float
    symbol_hint: str


class RebalanceRead(BaseModel):
    portfolio_id: int
    total_market_value: float
    current_allocation: dict[str, float]
    target_allocation: dict[str, float]
    actions: list[RebalanceActionRead]


class OrderCreate(BaseModel):
    portfolio_id: int = Field(gt=0)
    symbol: str = Field(min_length=1, max_length=32)
    side: Literal["buy", "sell"]
    quantity: float = Field(gt=0)
    price: float = Field(gt=0)
    fee: float = Field(default=0, ge=0)
    asset_class: str = Field(default="stock", min_length=1, max_length=32)
    daily_realized_pnl: float = 0


class OrderRead(BaseModel):
    order_id: str
    portfolio_id: int
    symbol: str
    side: Literal["buy", "sell"]
    quantity: float
    price: float
    fee: float
    notional: float
    status: Literal["filled"]


class PaperBalanceRead(BaseModel):
    portfolio_id: int
    initial_cash: float
    cash_balance: float
    invested_notional: float
    position_market_value: float
    equity_estimate: float


class DailySummaryRequest(BaseModel):
    current_prices: dict[str, float] = Field(default_factory=dict)
    day: str | None = None


class DailySummaryRead(BaseModel):
    portfolio_id: int
    day: str
    trades_count_day: int
    notional_bought_day: float
    notional_sold_day: float
    realized_pnl_day: float
    unrealized_pnl_snapshot: float
    total_pnl_snapshot: float


class PerformanceRequest(BaseModel):
    days: int = Field(default=30, ge=1, le=3650)


class PerformancePointRead(BaseModel):
    day: str
    realized_pnl_day: float
    cumulative_realized_pnl: float
    trades_count_day: int


class PerformanceRead(BaseModel):
    portfolio_id: int
    days: int
    series: list[PerformancePointRead]
    win_rate_pct: float
    profit_factor: float
    max_drawdown: float
    max_drawdown_pct: float


class UserRegisterRequest(BaseModel):
    email: str = Field(min_length=3, max_length=256)
    password: str = Field(min_length=8, max_length=256)


class UserLoginRequest(BaseModel):
    email: str = Field(min_length=3, max_length=256)
    password: str = Field(min_length=8, max_length=256)


class AuthTokenRead(BaseModel):
    access_token: str
    token_type: str = "bearer"


class AISignalGenerateRequest(BaseModel):
    portfolio_id: int = Field(gt=0)
    symbol: str = Field(min_length=1, max_length=32)
    asset_class: str = Field(default="stock", min_length=1, max_length=32)
    prices: list[float] = Field(default_factory=list, min_length=2)
    auto_execute: bool = False


class AISignalRead(BaseModel):
    id: int
    portfolio_id: int
    symbol: str
    asset_class: str
    side: Literal["buy", "sell", "hold"]
    confidence: float
    reason: str
    suggested_price: float
    suggested_quantity: float
    status: Literal["suggested", "executed"]
    executed_order_id: str | None = None


class AISignalGenerateResponse(BaseModel):
    signal: AISignalRead
    executed_order: OrderRead | None = None


class AutopilotWatchItem(BaseModel):
    symbol: str = Field(min_length=1, max_length=32)
    asset_class: str = Field(default="stock", min_length=1, max_length=32)


class AutopilotStartRequest(BaseModel):
    portfolio_id: int = Field(gt=0)
    interval_seconds: int = Field(default=60, ge=10, le=3600)
    auto_execute: bool = True
    watchlist: list[AutopilotWatchItem] = Field(default_factory=list)
    use_report: bool = Field(default=True, description="Use MAIA report recommendations")
    use_real_prices: bool = Field(default=True, description="Use real price feeds (with simulation fallback)")
    min_confidence: float = Field(default=7.0, ge=1.0, le=10.0, description="Minimum confidence from report (1-10)")


class AutopilotStatusRead(BaseModel):
    portfolio_id: int
    running: bool
    interval_seconds: int
    auto_execute: bool
    watchlist: list[AutopilotWatchItem]
    use_report: bool = True
    use_real_prices: bool = True
    min_confidence: float = 7.0
    report_picks_count: int = 0
    report_last_read: str | None = None
    started_at: str
    last_tick_at: str | None = None
    ticks_total: int
    last_error: str | None = None

