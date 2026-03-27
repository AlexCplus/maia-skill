"use client"

import { useState, useEffect } from "react"
import type { ReportData } from "@/types/report"
import type { Language } from "@/lib/translations"

export function useReportData(lang: Language = "en") {
  const [data, setData] = useState<ReportData | null>(null)
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)

  useEffect(() => {
    setLoading(true)
    setError(null)

    const file = lang === "es" ? "/data/report-es_v2.json" : "/data/report_v2.json"

    fetch(file)
      .then((res) => {
        if (!res.ok) {
          if (lang === "es" && res.status === 404) {
            // Fallback to English if Spanish file doesn't exist
            return fetch("/data/report.json").then((fallback) => {
              if (!fallback.ok) throw new Error(`Failed to load report data: ${fallback.status}`)
              return fallback.json()
            })
          }
          throw new Error(`Failed to load report data: ${res.status}`)
        }
        return res.json()
      })
      .then(setData)
      .catch((err) => setError(err.message))
      .finally(() => setLoading(false))
  }, [lang])

  return { data, loading, error }
}
