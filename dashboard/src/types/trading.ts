export interface PositionSummary {
  id: number
  portfolio_id: number
  symbol: string
  quantity: number
  avg_cost: number
  asset_class: string
}

export interface OrderSummary {
  order_id: string
  portfolio_id: number
  symbol: string
  side: "buy" | "sell"
  quantity: number
  price: number
  fee: number
  notional: number
  status: "filled"
}

export interface PaperBalance {
  portfolio_id: number
  initial_cash: number
  cash_balance: number
  invested_notional: number
  position_market_value: number
  equity_estimate: number
}

