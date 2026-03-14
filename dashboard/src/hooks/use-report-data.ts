"use client"

import { useState, useEffect } from "react"
import type { ReportData } from "@/types/report"

export function useReportData() {
  const [data, setData] = useState<ReportData | null>(null)
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)

  useEffect(() => {
    fetch("/data/report.json")
      .then((res) => {
        if (!res.ok) throw new Error(`Failed to load report data: ${res.status}`)
        return res.json()
      })
      .then(setData)
      .catch((err) => setError(err.message))
      .finally(() => setLoading(false))
  }, [])

  return { data, loading, error }
}
