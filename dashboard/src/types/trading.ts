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

export interface RiskCheckSummary {
  portfolio_id: number
  passed: boolean
  max_open_positions: number
  max_daily_loss: number
  max_order_notional: number
  max_order_notional_by_asset_class: Record<string, number>
  max_order_notional_by_symbol: Record<string, number>
  open_positions: number
  daily_loss: number
  proposed_order_notional: number
  violations: string[]
}

