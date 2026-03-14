"use client"

import { useState, useCallback } from "react"
import { motion } from "framer-motion"
import type { SectorData, Asset } from "@/types/report"
import { SECTOR_COLORS, SECTOR_NAMES, SECTORS } from "@/lib/constants"

function parseNumeric(val: string): number {
  return parseFloat(val.replace(/[^0-9.\-]/g, "")) || 0
}

function ChangeCell({ value }: { value: string }) {
  const isPositive = value.startsWith("+")
  const isNegative = value.startsWith("-")
  return (
    <span className={isPositive ? "text-green-600" : isNegative ? "text-red-600" : "text-[#8B8B85]"}>
      {value || "-"}
    </span>
  )
}

type SortKey = "name" | "price" | "24h" | "7d" | "30d" | "ytd" | "signal"
type SortDir = "asc" | "desc"

const colAccessor: Record<SortKey, (a: Asset) => string | number> = {
  name: (a) => a.name,
  price: (a) => parseNumeric(a.current_price),
  "24h": (a) => parseFloat(a.change_24h) || 0,
  "7d": (a) => parseFloat(a.change_7d) || 0,
  "30d": (a) => parseFloat(a.change_30d) || 0,
  ytd: (a) => parseFloat(a.ytd_change) || 0,
  signal: (a) => ({ buy: 3, hold: 2, sell: 1 }[a.recommendation] ?? 0),
}

function SortableTable({ assets }: { assets: Asset[] }) {
  const [sortKey, setSortKey] = useState<SortKey>("name")
  const [sortDir, setSortDir] = useState<SortDir>("asc")

  const handleSort = useCallback(
    (key: SortKey) => {
      if (sortKey === key) setSortDir((d) => (d === "asc" ? "desc" : "asc"))
      else { setSortKey(key); setSortDir("asc") }
    },
    [sortKey]
  )

  const sorted = [...assets].sort((a, b) => {
    const va = colAccessor[sortKey](a)
    const vb = colAccessor[sortKey](b)
    const cmp = typeof va === "number" && typeof vb === "number" ? va - vb : String(va).localeCompare(String(vb))
    return sortDir === "desc" ? -cmp : cmp
  })

  const ThSort = ({ label, col }: { label: string; col: SortKey }) => (
    <th
      className="cursor-pointer select-none whitespace-nowrap border-b-2 border-[#E6E6E4] px-3 py-2 text-left text-[11px] font-semibold uppercase tracking-wider text-[#8B8B85] transition-colors hover:text-[#37352F]"
      onClick={(e) => { e.stopPropagation(); handleSort(col) }}
      aria-sort={sortKey === col ? (sortDir === "asc" ? "ascending" : "descending") : "none"}
    >
      {label}{" "}
      <span className={`text-[10px] ${sortKey === col ? "text-[#fa8625]" : "opacity-30"}`}>
        {sortKey === col && sortDir === "desc" ? "\u25BC" : "\u25B2"}
      </span>
    </th>
  )

  const badge = (value: string, type: "source" | "buzz" | "rec") => {
    const styles: Record<string, Record<string, string>> = {
      source: { high: "bg-green-50 text-green-700", medium: "bg-amber-50 text-amber-700", low: "bg-red-50 text-red-700" },
      buzz: { high: "bg-red-50 text-red-600", medium: "bg-amber-50 text-amber-700", low: "bg-zinc-100 text-zinc-500" },
      rec: { buy: "bg-green-50 text-green-700", hold: "bg-amber-50 text-amber-700", sell: "bg-red-50 text-red-700" },
    }
    return `inline-block rounded-full px-2 py-0.5 text-[10px] font-semibold ${styles[type][value] ?? "bg-zinc-100 text-zinc-500"}`
  }

  return (
    <div className="overflow-x-auto">
      <table className="mb-4 w-full border-collapse text-sm">
        <thead>
          <tr>
            <ThSort label="Asset" col="name" />
            <ThSort label="Price" col="price" />
            <ThSort label="24h" col="24h" />
            <ThSort label="7d" col="7d" />
            <ThSort label="30d" col="30d" />
            <ThSort label="YTD" col="ytd" />
            <th className="whitespace-nowrap border-b-2 border-[#E6E6E4] px-3 py-2 text-left text-[11px] font-semibold uppercase tracking-wider text-[#8B8B85]">52w H/L</th>
            <th className="whitespace-nowrap border-b-2 border-[#E6E6E4] px-3 py-2 text-left text-[11px] font-semibold uppercase tracking-wider text-[#8B8B85]">Sources</th>
            <th className="whitespace-nowrap border-b-2 border-[#E6E6E4] px-3 py-2 text-left text-[11px] font-semibold uppercase tracking-wider text-[#8B8B85]">Social</th>
            <ThSort label="Signal" col="signal" />
          </tr>
        </thead>
        <tbody>
          {sorted.map((a) => (
            <tr key={a.symbol} className="transition-colors hover:bg-[#F7F7F5]">
              <td className="whitespace-nowrap border-b border-[#F0F0ED] px-3 py-2.5">
                <strong className="text-[#252420]">{a.name}</strong>
                <br />
                <span className="text-xs text-[#8B8B85]">{a.symbol}</span>
              </td>
              <td className="whitespace-nowrap border-b border-[#F0F0ED] px-3 py-2.5 font-medium">{a.current_price || "N/A"}</td>
              <td className="whitespace-nowrap border-b border-[#F0F0ED] px-3 py-2.5 text-xs"><ChangeCell value={a.change_24h} /></td>
              <td className="whitespace-nowrap border-b border-[#F0F0ED] px-3 py-2.5 text-xs"><ChangeCell value={a.change_7d} /></td>
              <td className="whitespace-nowrap border-b border-[#F0F0ED] px-3 py-2.5 text-xs"><ChangeCell value={a.change_30d} /></td>
              <td className="whitespace-nowrap border-b border-[#F0F0ED] px-3 py-2.5 text-xs"><ChangeCell value={a.ytd_change} /></td>
              <td className="whitespace-nowrap border-b border-[#F0F0ED] px-3 py-2.5 text-xs text-[#8B8B85]">{a.week_52_high} / {a.week_52_low}</td>
              <td className="whitespace-nowrap border-b border-[#F0F0ED] px-3 py-2.5"><span className={badge(a.source_agreement, "source")}>{a.source_agreement}</span></td>
              <td className="whitespace-nowrap border-b border-[#F0F0ED] px-3 py-2.5"><span className={badge(a.social_buzz, "buzz")}>{a.social_sentiment} ({a.social_buzz})</span></td>
              <td className="whitespace-nowrap border-b border-[#F0F0ED] px-3 py-2.5"><span className={badge(a.recommendation, "rec")}>{a.recommendation}</span></td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  )
}

interface DetailedAnalysisProps {
  sectors: Record<string, SectorData>
  openSectors?: string[]
}

export function DetailedAnalysis({ sectors, openSectors = [] }: DetailedAnalysisProps) {
  const [openKeys, setOpenKeys] = useState<Set<string>>(new Set(openSectors))
  const toggle = useCallback((key: string) => {
    setOpenKeys((prev) => { const next = new Set(prev); if (next.has(key)) next.delete(key); else next.add(key); return next })
  }, [])

  const effectiveOpen = new Set([...openKeys, ...openSectors])

  return (
    <motion.section
      initial={{ opacity: 0, y: 10 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ delay: 0.55 }}
    >
      <p className="mb-2 text-xs font-semibold uppercase tracking-[0.16em] text-[#8B8B85]">Analysis</p>
      <h2 className="mb-4 text-2xl font-bold tracking-tight text-[#252420]">Detailed Breakdown</h2>
      <div className="space-y-3">
        {SECTORS.map((key) => {
          const s = sectors[key]
          if (!s || s.data_unavailable) return null
          const isOpen = effectiveOpen.has(key)

          const newsItems = (s.assets || []).flatMap((a) => (a.key_news || []).map((n) => n))
          const socialItems = (s.assets || []).flatMap((a) => (a.social_highlights || []).map((h) => h))

          return (
            <div key={key} id={`sector-${key}`} className="overflow-hidden rounded-xl border border-[#E6E6E4] bg-[#FCFCFB]">
              <div
                className="flex cursor-pointer select-none items-center justify-between px-5 py-4 transition-colors hover:bg-[#F7F7F5]"
                onClick={() => toggle(key)}
              >
                <h3 className="flex items-center gap-2.5 text-sm font-semibold text-[#252420]">
                  <span className="inline-block h-2.5 w-2.5 rounded-full" style={{ backgroundColor: SECTOR_COLORS[key] }} />
                  {SECTOR_NAMES[key]}
                </h3>
                <span className="text-sm text-[#8B8B85] transition-transform duration-300" style={{ transform: isOpen ? "rotate(180deg)" : "rotate(0)" }}>
                  &#9660;
                </span>
              </div>
              <div className="overflow-hidden transition-all duration-300 ease-in-out" style={{ maxHeight: isOpen ? "3000px" : "0" }}>
                <div className="border-t border-[#E6E6E4] px-5 pb-5 pt-4" onClick={(e) => e.stopPropagation()}>
                  <SortableTable assets={s.assets} />
                  <div className="mt-4 grid gap-4 sm:grid-cols-2">
                    {newsItems.length > 0 && (
                      <div>
                        <h4 className="mb-2 text-xs font-semibold uppercase tracking-wider text-[#8B8B85]">Key News</h4>
                        {newsItems.slice(0, 8).map((n, i) => (
                          <div key={i} className="border-b border-[#F0F0ED] py-1.5 text-sm text-[#4D4A44]">{n}</div>
                        ))}
                      </div>
                    )}
                    {socialItems.length > 0 && (
                      <div>
                        <h4 className="mb-2 text-xs font-semibold uppercase tracking-wider text-[#8B8B85]">Social Highlights</h4>
                        {socialItems.slice(0, 6).map((h, i) => (
                          <div key={i} className="border-b border-[#F0F0ED] py-1.5 text-sm italic text-[#8B8B85]">{h}</div>
                        ))}
                      </div>
                    )}
                  </div>
                </div>
              </div>
            </div>
          )
        })}
      </div>
    </motion.section>
  )
}
