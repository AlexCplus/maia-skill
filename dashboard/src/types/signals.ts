export interface AISignal {
  id: number
  portfolio_id: number
  symbol: string
  asset_class: string
  side: "buy" | "sell" | "hold"
  confidence: number
  reason: string
  suggested_price: number
  suggested_quantity: number
  status: "suggested" | "executed"
  executed_order_id: string | null
}

export interface AISignalGenerateResponse {
  signal: AISignal
  executed_order: {
    order_id: string
    portfolio_id: number
    symbol: string
    side: "buy" | "sell"
    quantity: number
    price: number
    fee: number
    notional: number
    status: "filled"
  } | null
}

