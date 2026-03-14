"use client"

import { motion } from "framer-motion"

export function Disclaimer() {
  return (
    <motion.div
      initial={{ opacity: 0 }}
      animate={{ opacity: 1 }}
      transition={{ delay: 0.75 }}
      className="rounded-xl border border-[#E6E6E4] bg-[#FCFCFB] px-5 py-4 text-xs leading-relaxed text-[#8B8B85]"
    >
      <strong className="text-[#37352F]">Disclaimer:</strong> This report is generated
      by an AI-powered multi-agent research system and is for{" "}
      <strong>informational and educational purposes only</strong>. It does{" "}
      <strong>not</strong> constitute financial advice, investment recommendations, or
      solicitation to buy or sell any securities, cryptocurrencies, or commodities.
      Always consult a qualified financial advisor. Past performance is not indicative
      of future results.{" "}
      <strong>Tododeia and its creators assume no liability for investment losses.</strong>
    </motion.div>
  )
}
