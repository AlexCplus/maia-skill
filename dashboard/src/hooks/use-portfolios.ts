"use client"

import { useCallback, useEffect, useState } from "react"
import type { PortfolioSummary } from "@/types/portfolio"
import { getAuthHeader } from "@/lib/auth"

const DEFAULT_API_BASE = "http://127.0.0.1:8000"

export function usePortfolios() {
  const [data, setData] = useState<PortfolioSummary[]>([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)
  const [refreshToken, setRefreshToken] = useState(0)

  const refetch = useCallback(() => {
    setRefreshToken((prev) => prev + 1)
  }, [])

  useEffect(() => {
    const controller = new AbortController()
    const apiBase = process.env.NEXT_PUBLIC_AUTOPILOT_API_BASE_URL ?? DEFAULT_API_BASE
    const token = process.env.NEXT_PUBLIC_AUTOPILOT_TOKEN
    const authHeader = getAuthHeader(token)

    if (!authHeader) {
      setData([])
      setLoading(false)
      setError("Missing NEXT_PUBLIC_AUTOPILOT_TOKEN")
      return () => controller.abort()
    }

    setLoading(true)
    setError(null)

    fetch(`${apiBase}/portfolios`, {
      signal: controller.signal,
      headers: authHeader,
    })
      .then((res) => {
        if (!res.ok) {
          throw new Error(`Failed to load portfolios: ${res.status}`)
        }
        return res.json() as Promise<PortfolioSummary[]>
      })
      .then(setData)
      .catch((err: unknown) => {
        if (err instanceof Error && err.name === "AbortError") return
        const message = err instanceof Error ? err.message : "Unknown portfolios error"
        setError(message)
      })
      .finally(() => setLoading(false))

    return () => controller.abort()
  }, [refreshToken])

  return { data, loading, error, refetch }
}

