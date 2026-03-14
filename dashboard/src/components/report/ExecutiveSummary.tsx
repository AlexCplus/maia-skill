"use client"

import { motion } from "framer-motion"

export function ExecutiveSummary({ summary }: { summary: string }) {
  return (
    <motion.section
      initial={{ opacity: 0, y: 10 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ delay: 0.2 }}
      className="rounded-xl border border-[#E6E6E4] bg-[#FCFCFB] p-6"
    >
      <p className="mb-2 text-xs font-semibold uppercase tracking-[0.16em] text-[#8B8B85]">
        Executive Summary
      </p>
      <p className="text-[15px] leading-7 text-[#4D4A44]">{summary}</p>
    </motion.section>
  )
}
