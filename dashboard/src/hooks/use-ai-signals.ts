"use client"

import { useCallback, useEffect, useState } from "react"
import { useAuth } from "@/hooks/use-auth"
import { getAuthHeader } from "@/lib/auth"
import type { AISignal } from "@/types/signals"

const DEFAULT_API_BASE = "http://127.0.0.1:8000"

export function useAISignals(portfolioId: number) {
  const [signals, setSignals] = useState<AISignal[]>([])
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState<string | null>(null)
  const [refreshToken, setRefreshToken] = useState(0)
  const { token, ready } = useAuth()

  const refetch = useCallback(() => {
    setRefreshToken((prev) => prev + 1)
  }, [])

  useEffect(() => {
    const controller = new AbortController()
    const apiBase = process.env.NEXT_PUBLIC_AUTOPILOT_API_BASE_URL ?? DEFAULT_API_BASE
    const authHeader = getAuthHeader(token)

    if (!ready || !authHeader || !Number.isFinite(portfolioId) || portfolioId <= 0) {
      setSignals([])
      setLoading(false)
      setError(null)
      return () => controller.abort()
    }

    setLoading(true)
    setError(null)
    fetch(`${apiBase}/signals/${portfolioId}?limit=50`, {
      signal: controller.signal,
      headers: authHeader,
    })
      .then((res) => {
        if (!res.ok) throw new Error(`Failed signals: ${res.status}`)
        return res.json() as Promise<AISignal[]>
      })
      .then(setSignals)
      .catch((err: unknown) => {
        if (err instanceof Error && err.name === "AbortError") return
        setError(err instanceof Error ? err.message : "Unknown signals error")
      })
      .finally(() => setLoading(false))

    return () => controller.abort()
  }, [portfolioId, ready, refreshToken, token])

  return { signals, loading, error, refetch }
}

