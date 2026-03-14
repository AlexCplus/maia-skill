"use client"

import { AnimatePresence } from "framer-motion"
import { motion } from "framer-motion"
import type { RiskAdjustedPick, SectorData } from "@/types/report"
import { PickCard } from "./PickCard"

interface TopPicksGridProps {
  picks: RiskAdjustedPick[]
  sectors: Record<string, SectorData>
  filter: string
  searchQuery: string
}

export function TopPicksGrid({ picks, sectors, filter, searchQuery }: TopPicksGridProps) {
  const filtered = picks.filter((pick) => {
    const matchesFilter = filter === "all" || pick.recommendation === filter
    const matchesSearch =
      !searchQuery ||
      pick.name.toLowerCase().includes(searchQuery.toLowerCase()) ||
      pick.symbol.toLowerCase().includes(searchQuery.toLowerCase())
    return matchesFilter && matchesSearch
  })

  return (
    <motion.section
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ delay: 0.6 }}
    >
      <h2 className="mb-5 font-display text-[1.4rem] font-bold">
        Risk-Adjusted Top Picks
      </h2>
      <div
        className="grid gap-[18px]"
        style={{ gridTemplateColumns: "repeat(auto-fit, minmax(300px, 1fr))" }}
      >
        <AnimatePresence mode="popLayout">
          {filtered.map((pick) => (
            <PickCard key={pick.symbol} pick={pick} sectors={sectors} />
          ))}
        </AnimatePresence>
      </div>
      {filtered.length === 0 && (
        <p className="py-9 text-center text-[0.9rem] italic text-brand-text-muted">
          No picks match the current filter.
        </p>
      )}
    </motion.section>
  )
}
