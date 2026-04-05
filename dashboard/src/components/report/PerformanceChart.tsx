"use client"

import { useEffect, useState } from "react"
import { motion } from "framer-motion"
import {
  CartesianGrid,
  Line,
  LineChart,
  ResponsiveContainer,
  Tooltip,
  XAxis,
  YAxis,
} from "recharts"
import { useLanguage } from "@/hooks/use-language"
import { usePerformanceData } from "@/hooks/use-performance-data"
import { usePortfolios } from "@/hooks/use-portfolios"
import { Input } from "@/components/ui/input"
import { Button } from "@/components/ui/button"

const DEFAULT_PORTFOLIO_ID = 0
const DEFAULT_DAYS = Number(process.env.NEXT_PUBLIC_AUTOPILOT_PERFORMANCE_DAYS ?? 30)

function formatDay(value: string): string {
  if (typeof value !== "string" || value.length < 10) return value
  return value.slice(5)
}

export function PerformanceChart() {
  const { lang } = useLanguage()
  const { data: portfolios, loading: portfoliosLoading } = usePortfolios()
  const [portfolioInput, setPortfolioInput] = useState(String(DEFAULT_PORTFOLIO_ID))
  const [daysInput, setDaysInput] = useState(String(DEFAULT_DAYS))
  const [query, setQuery] = useState({ portfolioId: DEFAULT_PORTFOLIO_ID, days: DEFAULT_DAYS })
  const { data, loading, error, refetch } = usePerformanceData(query)

  const title = lang === "es" ? "Rendimiento (PnL realizado)" : "Performance (Realized PnL)"
  const subtitle =
    lang === "es"
      ? "Serie diaria para conectar con la evolución de cartera"
      : "Daily timeseries to track portfolio evolution"
  const loadingLabel = lang === "es" ? "Cargando rendimiento..." : "Loading performance..."
  const unavailableLabel = lang === "es" ? "Rendimiento no disponible." : "Performance unavailable."
  const pnlLabel = lang === "es" ? "PnL acumulado" : "Cumulative PnL"
  const portfolioLabel = lang === "es" ? "Portfolio ID" : "Portfolio ID"
  const portfolioSelectLabel = lang === "es" ? "Portfolio" : "Portfolio"
  const daysLabel = lang === "es" ? "Días" : "Days"
  const applyLabel = lang === "es" ? "Aplicar" : "Apply"
  const refreshLabel = lang === "es" ? "Refrescar" : "Refresh"
  const loadingPortfoliosLabel = lang === "es" ? "Cargando portfolios..." : "Loading portfolios..."
  const noPortfoliosLabel = lang === "es" ? "Sin portfolios" : "No portfolios"
  const missingTokenLabel =
    lang === "es"
      ? "Falta NEXT_PUBLIC_AUTOPILOT_TOKEN en dashboard/.env.local"
      : "Missing NEXT_PUBLIC_AUTOPILOT_TOKEN in dashboard/.env.local"
  const manualHint =
    lang === "es"
      ? "Si no aparece en la lista, puedes usar Portfolio ID manual."
      : "If not listed, you can use manual Portfolio ID."

  useEffect(() => {
    if (portfolios.length === 0) return
    const hasCurrent = portfolios.some((p) => String(p.id) === portfolioInput)
    if (!hasCurrent) {
      const firstId = String(portfolios[0].id)
      setPortfolioInput(firstId)
      setQuery((prev) => ({ ...prev, portfolioId: Number(firstId) }))
    }
  }, [portfolioInput, portfolios])

  const applyQuery = () => {
    const portfolioId = Number(portfolioInput)
    const days = Number(daysInput)
    const safePortfolioId = Number.isFinite(portfolioId) && portfolioId > 0 ? portfolioId : 0
    const safeDays = Number.isFinite(days) && days > 0 ? days : 30
    setQuery({ portfolioId: safePortfolioId, days: safeDays })
  }

  return (
    <motion.section
      initial={{ opacity: 0, y: 8 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ delay: 0.72 }}
      className="rounded-xl border border-[#E6E6E4] bg-[#FCFCFB] p-5"
    >
      <h3 className="text-sm font-semibold text-[#252420]">{title}</h3>
      <p className="mt-1 text-xs text-[#8B8B85]">{subtitle}</p>

      <div className="mt-3 grid gap-2 sm:grid-cols-[1fr_1fr_1fr_auto_auto]">
        <div>
          <p className="mb-1 text-[11px] text-[#8B8B85]">{portfolioSelectLabel}</p>
          <select
            className="h-8 w-full min-w-0 rounded-lg border border-input bg-transparent px-2.5 py-1 text-sm outline-none"
            disabled={portfoliosLoading || portfolios.length === 0}
            value={portfolioInput}
            onChange={(e) => setPortfolioInput(e.target.value)}
          >
            {portfoliosLoading ? (
              <option value={portfolioInput}>{loadingPortfoliosLabel}</option>
            ) : portfolios.length === 0 ? (
              <option value={portfolioInput}>{noPortfoliosLabel}</option>
            ) : (
              portfolios.map((p) => (
                <option key={p.id} value={String(p.id)}>
                  {p.name} (#{p.id})
                </option>
              ))
            )}
          </select>
        </div>
        <div>
          <p className="mb-1 text-[11px] text-[#8B8B85]">{portfolioLabel}</p>
          <Input
            value={portfolioInput}
            onChange={(e) => setPortfolioInput(e.target.value)}
            inputMode="numeric"
          />
        </div>
        <div>
          <p className="mb-1 text-[11px] text-[#8B8B85]">{daysLabel}</p>
          <Input
            value={daysInput}
            onChange={(e) => setDaysInput(e.target.value)}
            inputMode="numeric"
          />
        </div>
        <div className="flex items-end">
          <Button variant="outline" onClick={applyQuery}>
            {applyLabel}
          </Button>
        </div>
        <div className="flex items-end">
          <Button variant="outline" onClick={refetch}>
            {refreshLabel}
          </Button>
        </div>
      </div>
      <p className="mt-1 text-[11px] text-[#8B8B85]">
        {process.env.NEXT_PUBLIC_AUTOPILOT_TOKEN ? manualHint : missingTokenLabel}
      </p>

      <div className="mt-4 h-[260px]">
        {loading ? (
          <div className="flex h-full items-center justify-center text-sm text-[#8B8B85]">{loadingLabel}</div>
        ) : error || !data || data.series.length === 0 ? (
          <div className="flex h-full items-center justify-center text-sm text-[#8B8B85]">
            {error ?? unavailableLabel}
          </div>
        ) : (
          <ResponsiveContainer width="100%" height="100%">
            <LineChart data={data.series} margin={{ top: 10, right: 12, left: 6, bottom: 10 }}>
              <CartesianGrid stroke="#F0F0ED" />
              <XAxis dataKey="day" tickFormatter={formatDay} tick={{ fill: "#8B8B85", fontSize: 10 }} />
              <YAxis tick={{ fill: "#8B8B85", fontSize: 10 }} />
              <Tooltip
                contentStyle={{ border: "1px solid #E6E6E4", borderRadius: "0.75rem" }}
                labelFormatter={(value) => String(value)}
                formatter={(value: number) => [value.toFixed(2), pnlLabel]}
              />
              <Line
                type="monotone"
                dataKey="cumulative_realized_pnl"
                stroke="#fa8625"
                strokeWidth={2.5}
                dot={false}
              />
            </LineChart>
          </ResponsiveContainer>
        )}
      </div>
    </motion.section>
  )
}

