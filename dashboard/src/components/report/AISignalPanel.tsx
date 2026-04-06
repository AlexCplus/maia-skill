"use client"

import { useMemo, useState } from "react"
import { motion } from "framer-motion"
import { useLanguage } from "@/hooks/use-language"
import { useAuth } from "@/hooks/use-auth"
import { usePortfolios } from "@/hooks/use-portfolios"
import { useAISignals } from "@/hooks/use-ai-signals"
import { getAuthHeader } from "@/lib/auth"
import type { AISignalGenerateResponse } from "@/types/signals"
import { Button } from "@/components/ui/button"
import { Input } from "@/components/ui/input"

const DEFAULT_API_BASE = "http://127.0.0.1:8000"

export function AISignalPanel() {
  const { lang } = useLanguage()
  const { token } = useAuth()
  const { data: portfolios } = usePortfolios()
  const [portfolioId, setPortfolioId] = useState(0)
  const [symbol, setSymbol] = useState("AAPL")
  const [assetClass, setAssetClass] = useState("stock")
  const [prices, setPrices] = useState("100,102,101,104,106,108,107")
  const [autoExecute, setAutoExecute] = useState(false)
  const [status, setStatus] = useState<string | null>(null)
  const { signals, refetch } = useAISignals(portfolioId)
  const authHeader = getAuthHeader(token)
  const apiBase = process.env.NEXT_PUBLIC_AUTOPILOT_API_BASE_URL ?? DEFAULT_API_BASE

  const labels = useMemo(
    () => ({
      title: lang === "es" ? "Motor IA (simulado)" : "AI Signal Engine (simulated)",
      generate: lang === "es" ? "Generar señal" : "Generate signal",
      autoExecute: lang === "es" ? "Auto-ejecutar paper order" : "Auto-execute paper order",
      portfolio: lang === "es" ? "Portfolio" : "Portfolio",
      symbol: lang === "es" ? "Símbolo" : "Symbol",
      prices: lang === "es" ? "Precios (coma)" : "Prices (comma separated)",
      assetClass: lang === "es" ? "Clase activo" : "Asset class",
      noData: lang === "es" ? "Sin señales." : "No signals yet.",
    }),
    [lang]
  )

  const runSignal = async () => {
    if (!authHeader) {
      setStatus(lang === "es" ? "Inicia sesión." : "Sign in first.")
      return
    }
    const parsed = prices
      .split(",")
      .map((x) => Number(x.trim()))
      .filter((x) => Number.isFinite(x) && x > 0)
    if (parsed.length < 2) {
      setStatus(lang === "es" ? "Necesitas al menos 2 precios." : "At least 2 prices required.")
      return
    }
    const id = portfolioId || portfolios[0]?.id || 0
    if (!id) {
      setStatus(lang === "es" ? "Crea/selecciona portfolio." : "Create/select a portfolio.")
      return
    }

    const res = await fetch(`${apiBase}/signals/generate`, {
      method: "POST",
      headers: { "Content-Type": "application/json", ...authHeader },
      body: JSON.stringify({
        portfolio_id: id,
        symbol,
        asset_class: assetClass,
        prices: parsed,
        auto_execute: autoExecute,
      }),
    })
    if (!res.ok) {
      setStatus(`Error ${res.status}`)
      return
    }
    const payload = (await res.json()) as AISignalGenerateResponse
    setStatus(
      payload.executed_order
        ? `${payload.signal.side.toUpperCase()} executed (#${payload.executed_order.order_id})`
        : `${payload.signal.side.toUpperCase()} suggested`
    )
    setPortfolioId(id)
    refetch()
  }

  return (
    <motion.section
      initial={{ opacity: 0, y: 8 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ delay: 0.76 }}
      className="rounded-xl border border-[#E6E6E4] bg-[#FCFCFB] p-5"
    >
      <h3 className="text-sm font-semibold text-[#252420]">{labels.title}</h3>

      <div className="mt-3 grid gap-2 sm:grid-cols-[1fr_1fr_1fr_2fr_auto]">
        <select
          className="h-8 rounded-lg border border-input bg-transparent px-2.5 py-1 text-sm outline-none"
          value={String(portfolioId || portfolios[0]?.id || 0)}
          onChange={(e) => setPortfolioId(Number(e.target.value))}
        >
          {portfolios.map((p) => (
            <option key={p.id} value={String(p.id)}>
              {labels.portfolio}: {p.name} (#{p.id})
            </option>
          ))}
        </select>
        <Input value={symbol} onChange={(e) => setSymbol(e.target.value.toUpperCase())} placeholder={labels.symbol} />
        <Input value={assetClass} onChange={(e) => setAssetClass(e.target.value.toLowerCase())} placeholder={labels.assetClass} />
        <Input value={prices} onChange={(e) => setPrices(e.target.value)} placeholder={labels.prices} />
        <Button variant="outline" onClick={runSignal}>
          {labels.generate}
        </Button>
      </div>

      <label className="mt-2 flex items-center gap-2 text-xs text-[#8B8B85]">
        <input type="checkbox" checked={autoExecute} onChange={(e) => setAutoExecute(e.target.checked)} />
        {labels.autoExecute}
      </label>

      {status && <p className="mt-2 text-xs text-[#8B8B85]">{status}</p>}

      <div className="mt-3 rounded-lg border border-[#E6E6E4] bg-white p-3 text-sm">
        {signals.length === 0 ? (
          <p className="text-xs text-[#8B8B85]">{labels.noData}</p>
        ) : (
          signals.slice(0, 10).map((s) => (
            <p key={s.id} className="text-xs">
              #{s.id} {s.symbol} {s.side.toUpperCase()} conf={s.confidence.toFixed(2)} status={s.status}
            </p>
          ))
        )}
      </div>
    </motion.section>
  )
}

