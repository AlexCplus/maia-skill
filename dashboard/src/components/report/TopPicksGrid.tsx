"use client"

import { AnimatePresence, motion } from "framer-motion"
import { useLanguage } from "@/hooks/use-language"
import type { RiskAdjustedPick, SectorData } from "@/types/report"
import { PickCard } from "./PickCard"

interface TopPicksGridProps {
  picks: RiskAdjustedPick[]
  sectors: Record<string, SectorData>
  filter: string
  searchQuery: string
}

export function TopPicksGrid({ picks, sectors, filter, searchQuery }: TopPicksGridProps) {
  const { t } = useLanguage()
  const filtered = picks.filter((pick) => {
    const matchesFilter = filter === "all" || pick.recommendation === filter
    const matchesSearch = !searchQuery || pick.name.toLowerCase().includes(searchQuery.toLowerCase()) || pick.symbol.toLowerCase().includes(searchQuery.toLowerCase())
    return matchesFilter && matchesSearch
  })

  return (
    <motion.section initial={{ opacity: 0, y: 10 }} animate={{ opacity: 1, y: 0 }} transition={{ delay: 0.45 }}>
      <h2 className="mb-5 text-2xl font-bold tracking-tight text-[#252420]">{t("picks.title")}</h2>
      <div className="grid gap-[18px]" style={{ gridTemplateColumns: "repeat(auto-fit, minmax(300px, 1fr))" }}>
        <AnimatePresence mode="popLayout">
          {filtered.map((pick) => <PickCard key={pick.symbol} pick={pick} sectors={sectors} />)}
        </AnimatePresence>
      </div>
      {filtered.length === 0 && <p className="py-9 text-center text-sm italic text-[#8B8B85]">{t("picks.empty")}</p>}
    </motion.section>
  )
}
