export interface AutopilotWatchItem {
  symbol: string
  asset_class: string
}

export interface AutopilotStatus {
  portfolio_id: number
  running: boolean
  interval_seconds: number
  auto_execute: boolean
  watchlist: AutopilotWatchItem[]
  use_report: boolean
  use_real_prices: boolean
  min_confidence: number
  report_picks_count: number
  report_last_read: string | null
  started_at: string
  last_tick_at: string | null
  ticks_total: number
  last_error: string | null
}

