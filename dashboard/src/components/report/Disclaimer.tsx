"use client"

import { motion } from "framer-motion"
import { useLanguage } from "@/hooks/use-language"

export function Disclaimer() {
  const { t } = useLanguage()
  return (
    <motion.div initial={{ opacity: 0 }} animate={{ opacity: 1 }} transition={{ delay: 0.75 }} className="rounded-xl border border-[#E6E6E4] bg-[#FCFCFB] px-5 py-4 text-xs leading-relaxed text-[#8B8B85]">
      <strong className="text-[#37352F]">{t("disclaimer.label")}</strong> {t("disclaimer.text")}
    </motion.div>
  )
}
