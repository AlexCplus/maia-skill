export interface PerformancePoint {
  day: string
  realized_pnl_day: number
  cumulative_realized_pnl: number
  trades_count_day: number
}

export interface PerformanceSeriesResponse {
  portfolio_id: number
  days: number
  series: PerformancePoint[]
  win_rate_pct: number
  profit_factor: number
  max_drawdown: number
  max_drawdown_pct: number
}

