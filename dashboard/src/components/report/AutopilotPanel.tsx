"use client"

import { useMemo, useState } from "react"
import { motion } from "framer-motion"
import { useLanguage } from "@/hooks/use-language"
import { useAuth } from "@/hooks/use-auth"
import { usePortfolios } from "@/hooks/use-portfolios"
import { getAuthHeader } from "@/lib/auth"
import type { AutopilotStatus } from "@/types/autopilot"
import { Button } from "@/components/ui/button"
import { Input } from "@/components/ui/input"

const DEFAULT_API_BASE = "http://127.0.0.1:8000"

interface ReportInfo {
  metadata: {
    generated_at: string
    model_used: string
    total_picks: number
    market_summary: string
  }
  total_picks: number
  buy_recommendations: number
  sell_recommendations: number
  hold_recommendations: number
  picks_preview: Array<{
    rank: number
    symbol: string
    name: string
    sector: string
    recommendation: string
    confidence: number
    risk_adjusted_score: number
  }>
}

export function AutopilotPanel() {
  const { lang } = useLanguage()
  const { token } = useAuth()
  const { data: portfolios, refetch: refetchPortfolios } = usePortfolios()
  const [portfolioId, setPortfolioId] = useState(0)
  const [intervalSeconds, setIntervalSeconds] = useState("60")
  const [watchlist, setWatchlist] = useState("")
  const [autoExecute, setAutoExecute] = useState(true)
  const [useReport, setUseReport] = useState(true)
  const [useRealPrices, setUseRealPrices] = useState(true)
  const [minConfidence, setMinConfidence] = useState("7")
  const [status, setStatus] = useState<AutopilotStatus | null>(null)
  const [reportInfo, setReportInfo] = useState<ReportInfo | null>(null)
  const [message, setMessage] = useState<string | null>(null)
  const [newPortfolioName, setNewPortfolioName] = useState("")
  const [showCreateForm, setShowCreateForm] = useState(false)

  const authHeader = getAuthHeader(token)
  const apiBase = process.env.NEXT_PUBLIC_AUTOPILOT_API_BASE_URL ?? DEFAULT_API_BASE

  const labels = useMemo(
    () => ({
      title: lang === "es" ? "Autopilot 24/7 (paper)" : "Autopilot 24/7 (paper)",
      start: lang === "es" ? "Iniciar" : "Start",
      stop: lang === "es" ? "Parar" : "Stop",
      refresh: lang === "es" ? "Estado" : "Status",
      interval: lang === "es" ? "Intervalo (s)" : "Interval (s)",
      watchlist: lang === "es" ? "Watchlist extra (sym:class)" : "Extra watchlist (sym:class)",
      auto: lang === "es" ? "Auto-ejecutar órdenes" : "Auto-execute orders",
      useReport: lang === "es" ? "Usar recomendaciones MAIA" : "Use MAIA recommendations",
      realPrices: lang === "es" ? "Precios reales (Yahoo/CoinGecko)" : "Real prices (Yahoo/CoinGecko)",
      minConf: lang === "es" ? "Confianza mín (1-10)" : "Min confidence (1-10)",
      loadReport: lang === "es" ? "Ver Report MAIA" : "Load MAIA Report",
      reportTitle: lang === "es" ? "Report MAIA Actual" : "Current MAIA Report",
      noPortfolios: lang === "es" ? "No tienes portfolios. Crea uno primero:" : "No portfolios found. Create one first:",
      createPortfolio: lang === "es" ? "Crear Portfolio" : "Create Portfolio",
      portfolioName: lang === "es" ? "Nombre del portfolio" : "Portfolio name",
      create: lang === "es" ? "Crear" : "Create",
      cancel: lang === "es" ? "Cancelar" : "Cancel",
    }),
    [lang]
  )

  const activePortfolio = portfolioId || portfolios[0]?.id || 0

  const createPortfolio = async () => {
    if (!authHeader || !newPortfolioName.trim()) return
    const res = await fetch(`${apiBase}/portfolios`, {
      method: "POST",
      headers: { "Content-Type": "application/json", ...authHeader },
      body: JSON.stringify({ name: newPortfolioName.trim(), base_currency: "USD" }),
    })
    if (!res.ok) {
      setMessage(`Error creating portfolio: ${res.status}`)
      return
    }
    setNewPortfolioName("")
    setShowCreateForm(false)
    refetchPortfolios()
    setMessage(lang === "es" ? "Portfolio creado!" : "Portfolio created!")
  }

  const fetchStatus = async () => {
    if (!authHeader || !activePortfolio) return
    const res = await fetch(`${apiBase}/autopilot/status/${activePortfolio}`, { headers: authHeader })
    if (!res.ok) {
      setMessage(`Status ${res.status}`)
      return
    }
    setStatus((await res.json()) as AutopilotStatus)
    setMessage(null)
  }

  const fetchReportInfo = async () => {
    if (!authHeader) return
    const res = await fetch(`${apiBase}/autopilot/report/info`, { headers: authHeader })
    if (!res.ok) {
      setMessage(`Report ${res.status}`)
      return
    }
    setReportInfo((await res.json()) as ReportInfo)
    setMessage(lang === "es" ? "Report cargado" : "Report loaded")
  }

  const start = async () => {
    if (!authHeader || !activePortfolio) return
    const parsedWatchlist = watchlist
      .split(",")
      .map((x) => x.trim())
      .filter(Boolean)
      .map((item) => {
        const [symbol, assetClass] = item.split(":")
        return { symbol: (symbol || "").toUpperCase(), asset_class: (assetClass || "stock").toLowerCase() }
      })
      .filter((x) => x.symbol.length > 0)
    const interval = Number(intervalSeconds)
    const minConf = Number(minConfidence)
    const res = await fetch(`${apiBase}/autopilot/start`, {
      method: "POST",
      headers: { "Content-Type": "application/json", ...authHeader },
      body: JSON.stringify({
        portfolio_id: activePortfolio,
        interval_seconds: Number.isFinite(interval) && interval >= 10 ? interval : 60,
        auto_execute: autoExecute,
        watchlist: parsedWatchlist,
        use_report: useReport,
        use_real_prices: useRealPrices,
        min_confidence: Number.isFinite(minConf) && minConf >= 1 && minConf <= 10 ? minConf : 7,
      }),
    })
    if (!res.ok) {
      setMessage(`Start ${res.status}`)
      return
    }
    setStatus((await res.json()) as AutopilotStatus)
    setMessage(lang === "es" ? "Autopilot iniciado." : "Autopilot started.")
  }

  const stop = async () => {
    if (!authHeader || !activePortfolio) return
    const res = await fetch(`${apiBase}/autopilot/stop/${activePortfolio}`, {
      method: "POST",
      headers: authHeader,
    })
    if (!res.ok) {
      setMessage(`Stop ${res.status}`)
      return
    }
    setStatus((await res.json()) as AutopilotStatus)
    setMessage(lang === "es" ? "Autopilot detenido." : "Autopilot stopped.")
  }

  return (
    <motion.section
      initial={{ opacity: 0, y: 8 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ delay: 0.78 }}
      className="rounded-xl border border-[#E6E6E4] bg-[#FCFCFB] p-5"
    >
      <h3 className="text-sm font-semibold text-[#252420]">{labels.title}</h3>
      
      {/* No portfolios warning */}
      {portfolios.length === 0 && (
        <div className="mt-3 rounded-lg border border-amber-200 bg-amber-50 p-3">
          <p className="text-sm text-amber-800">{labels.noPortfolios}</p>
          {!showCreateForm ? (
            <Button 
              variant="outline" 
              size="sm" 
              className="mt-2"
              onClick={() => setShowCreateForm(true)}
            >
              {labels.createPortfolio}
            </Button>
          ) : (
            <div className="mt-2 flex gap-2">
              <Input 
                value={newPortfolioName} 
                onChange={(e) => setNewPortfolioName(e.target.value)} 
                placeholder={labels.portfolioName}
                className="h-8"
              />
              <Button variant="default" size="sm" onClick={createPortfolio}>{labels.create}</Button>
              <Button variant="outline" size="sm" onClick={() => setShowCreateForm(false)}>{labels.cancel}</Button>
            </div>
          )}
        </div>
      )}
      
      {/* Main controls - only show if portfolios exist */}
      {portfolios.length > 0 && (
        <>
          <div className="mt-3 grid gap-2 sm:grid-cols-[1fr_1fr_2fr]">
            <select
              className="h-8 rounded-lg border border-input bg-transparent px-2.5 py-1 text-sm outline-none"
              value={String(activePortfolio)}
              onChange={(e) => setPortfolioId(Number(e.target.value))}
            >
              {portfolios.map((p) => (
                <option key={p.id} value={String(p.id)}>
                  {p.name} (#{p.id})
                </option>
              ))}
            </select>
            <Input value={intervalSeconds} onChange={(e) => setIntervalSeconds(e.target.value)} placeholder={labels.interval} />
            <Input value={watchlist} onChange={(e) => setWatchlist(e.target.value)} placeholder={labels.watchlist} />
          </div>
          
          {/* MAIA integration options */}
          <div className="mt-3 grid gap-2 sm:grid-cols-3">
            <label className="flex items-center gap-2 text-xs text-[#8B8B85]">
              <input type="checkbox" checked={useReport} onChange={(e) => setUseReport(e.target.checked)} />
              {labels.useReport}
            </label>
            <label className="flex items-center gap-2 text-xs text-[#8B8B85]">
              <input type="checkbox" checked={useRealPrices} onChange={(e) => setUseRealPrices(e.target.checked)} />
              {labels.realPrices}
            </label>
            <div className="flex items-center gap-2">
              <span className="text-xs text-[#8B8B85]">{labels.minConf}:</span>
              <Input 
                className="h-6 w-16 text-xs" 
                value={minConfidence} 
                onChange={(e) => setMinConfidence(e.target.value)} 
                type="number"
                min="1"
                max="10"
              />
            </div>
          </div>
          
          {/* Auto execute and action buttons */}
          <div className="mt-3 flex flex-wrap items-center gap-2">
            <label className="flex items-center gap-2 text-xs text-[#8B8B85]">
              <input type="checkbox" checked={autoExecute} onChange={(e) => setAutoExecute(e.target.checked)} />
              {labels.auto}
            </label>
            <div className="ml-auto flex gap-2">
              <Button variant="outline" size="sm" onClick={fetchReportInfo}>{labels.loadReport}</Button>
              <Button variant="outline" size="sm" onClick={start}>{labels.start}</Button>
              <Button variant="outline" size="sm" onClick={stop}>{labels.stop}</Button>
              <Button variant="outline" size="sm" onClick={fetchStatus}>{labels.refresh}</Button>
            </div>
          </div>
        </>
      )}
      
      {message && <p className="mt-2 text-xs text-[#8B8B85]">{message}</p>}
      
      {/* Status display */}
      {status && (
        <div className="mt-3 rounded-lg border border-[#E6E6E4] bg-white p-3 text-xs">
          <div className="grid gap-1 sm:grid-cols-2">
            <p><span className="font-medium">Running:</span> {String(status.running)} | <span className="font-medium">Ticks:</span> {status.ticks_total}</p>
            <p><span className="font-medium">Interval:</span> {status.interval_seconds}s | <span className="font-medium">Auto-exec:</span> {String(status.auto_execute)}</p>
            <p><span className="font-medium">Use Report:</span> {String(status.use_report)} | <span className="font-medium">Real Prices:</span> {String(status.use_real_prices)}</p>
            <p><span className="font-medium">Report Picks:</span> {status.report_picks_count} | <span className="font-medium">Min Conf:</span> {status.min_confidence}</p>
            <p><span className="font-medium">Last tick:</span> {status.last_tick_at ?? "-"}</p>
            <p><span className="font-medium">Report read:</span> {status.report_last_read ?? "-"}</p>
          </div>
          {status.last_error && <p className="mt-2 text-red-600"><span className="font-medium">Error:</span> {status.last_error}</p>}
        </div>
      )}
      
      {/* Report preview */}
      {reportInfo && (
        <div className="mt-3 rounded-lg border border-blue-200 bg-blue-50 p-3">
          <h4 className="text-xs font-semibold text-blue-800">{labels.reportTitle}</h4>
          <p className="mt-1 text-xs text-blue-700">
            Generated: {reportInfo.metadata.generated_at} | Model: {reportInfo.metadata.model_used}
          </p>
          <p className="text-xs text-blue-700">
            Buy: {reportInfo.buy_recommendations} | Hold: {reportInfo.hold_recommendations} | Sell: {reportInfo.sell_recommendations}
          </p>
          <div className="mt-2 max-h-40 overflow-auto">
            <table className="w-full text-xs">
              <thead>
                <tr className="border-b border-blue-200 text-left">
                  <th className="p-1">#</th>
                  <th className="p-1">Symbol</th>
                  <th className="p-1">Sector</th>
                  <th className="p-1">Action</th>
                  <th className="p-1">Conf</th>
                  <th className="p-1">Score</th>
                </tr>
              </thead>
              <tbody>
                {reportInfo.picks_preview.map((pick) => (
                  <tr key={pick.symbol} className="border-b border-blue-100">
                    <td className="p-1">{pick.rank}</td>
                    <td className="p-1 font-medium">{pick.symbol}</td>
                    <td className="p-1">{pick.sector}</td>
                    <td className={`p-1 ${pick.recommendation === 'buy' ? 'text-green-600' : pick.recommendation === 'sell' ? 'text-red-600' : 'text-gray-600'}`}>
                      {pick.recommendation.toUpperCase()}
                    </td>
                    <td className="p-1">{pick.confidence}/10</td>
                    <td className="p-1">{pick.risk_adjusted_score.toFixed(1)}</td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>
      )}
    </motion.section>
  )
}

