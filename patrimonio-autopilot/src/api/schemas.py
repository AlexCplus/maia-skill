from datetime import datetime
from typing import Literal

from pydantic import BaseModel, ConfigDict, Field


class PortfolioCreate(BaseModel):
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


class RiskCheckRead(BaseModel):
    portfolio_id: int
    passed: bool
    max_open_positions: int
    max_daily_loss: float
    max_order_notional: float
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


class UserRegisterRequest(BaseModel):
    email: str = Field(min_length=3, max_length=256)
    password: str = Field(min_length=8, max_length=256)


class UserLoginRequest(BaseModel):
    email: str = Field(min_length=3, max_length=256)
    password: str = Field(min_length=8, max_length=256)


class AuthTokenRead(BaseModel):
    access_token: str
    token_type: str = "bearer"

