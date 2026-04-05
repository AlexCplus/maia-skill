"use client"

import { useCallback, useEffect, useState } from "react"
import type { PerformanceSeriesResponse } from "@/types/performance"
import { getAuthHeader } from "@/lib/auth"

const DEFAULT_API_BASE = "http://127.0.0.1:8000"
const DEFAULT_PORTFOLIO_ID = 0
const DEFAULT_DAYS = 30

interface UsePerformanceDataParams {
  portfolioId: number
  days: number
}

export function usePerformanceData(params: UsePerformanceDataParams) {
  const [data, setData] = useState<PerformanceSeriesResponse | null>(null)
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
      setData(null)
      setLoading(false)
      setError("Missing NEXT_PUBLIC_AUTOPILOT_TOKEN")
      return () => controller.abort()
    }

    const envPortfolioId = DEFAULT_PORTFOLIO_ID
    const envDaysRaw = process.env.NEXT_PUBLIC_AUTOPILOT_PERFORMANCE_DAYS
    const envDays = Number(envDaysRaw ?? DEFAULT_DAYS)

    const effectivePortfolioId =
      Number.isFinite(params.portfolioId) && params.portfolioId > 0
        ? params.portfolioId
        : Number.isFinite(envPortfolioId) && envPortfolioId > 0
          ? envPortfolioId
          : DEFAULT_PORTFOLIO_ID

    const effectiveDays =
      Number.isFinite(params.days) && params.days > 0
        ? params.days
        : Number.isFinite(envDays) && envDays > 0
          ? envDays
          : DEFAULT_DAYS

    if (!Number.isFinite(effectivePortfolioId) || effectivePortfolioId <= 0) {
      setData(null)
      setLoading(false)
      setError(null)
      return () => controller.abort()
    }

    setLoading(true)
    setError(null)

    fetch(`${apiBase}/portfolios/${effectivePortfolioId}/analytics/performance`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        ...authHeader,
      },
      body: JSON.stringify({ days: effectiveDays }),
      signal: controller.signal,
    })
      .then((res) => {
        if (!res.ok) {
          throw new Error(`Failed to load performance data: ${res.status}`)
        }
        return res.json() as Promise<PerformanceSeriesResponse>
      })
      .then(setData)
      .catch((err: unknown) => {
        if (err instanceof Error && err.name === "AbortError") return
        const message = err instanceof Error ? err.message : "Unknown performance data error"
        setError(message)
      })
      .finally(() => setLoading(false))

    return () => controller.abort()
  }, [params.days, params.portfolioId, refreshToken])

  return { data, loading, error, refetch }
}

