"use client"

import { useCallback, useEffect, useState } from "react"
import type { PaperBalance, PositionSummary, OrderSummary } from "@/types/trading"

const DEFAULT_API_BASE = "http://127.0.0.1:8000"

interface UseTradingPanelParams {
  portfolioId: number
}

export function useTradingPanel(params: UseTradingPanelParams) {
  const [positions, setPositions] = useState<PositionSummary[]>([])
  const [orders, setOrders] = useState<OrderSummary[]>([])
  const [balance, setBalance] = useState<PaperBalance | null>(null)
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
    const portfolioId = params.portfolioId

    if (!token) {
      setPositions([])
      setOrders([])
      setBalance(null)
      setLoading(false)
      setError("Missing NEXT_PUBLIC_AUTOPILOT_TOKEN")
      return () => controller.abort()
    }

    if (!Number.isFinite(portfolioId) || portfolioId <= 0) {
      setPositions([])
      setOrders([])
      setBalance(null)
      setLoading(false)
      setError(null)
      return () => controller.abort()
    }

    setLoading(true)
    setError(null)

    Promise.all([
      fetch(`${apiBase}/portfolios/${portfolioId}/positions`, {
        signal: controller.signal,
        headers: { Authorization: `Bearer ${token}` },
      }),
      fetch(`${apiBase}/orders?portfolio_id=${portfolioId}`, {
        signal: controller.signal,
        headers: { Authorization: `Bearer ${token}` },
      }),
      fetch(`${apiBase}/orders/balance/${portfolioId}`, {
        signal: controller.signal,
        headers: { Authorization: `Bearer ${token}` },
      }),
    ])
      .then(async ([positionsRes, ordersRes, balanceRes]) => {
        if (!positionsRes.ok) throw new Error(`Failed positions: ${positionsRes.status}`)
        if (!ordersRes.ok) throw new Error(`Failed orders: ${ordersRes.status}`)
        if (!balanceRes.ok) throw new Error(`Failed balance: ${balanceRes.status}`)
        return Promise.all([
          positionsRes.json() as Promise<PositionSummary[]>,
          ordersRes.json() as Promise<OrderSummary[]>,
          balanceRes.json() as Promise<PaperBalance>,
        ])
      })
      .then(([positionsData, ordersData, balanceData]) => {
        setPositions(positionsData)
        setOrders(ordersData)
        setBalance(balanceData)
      })
      .catch((err: unknown) => {
        if (err instanceof Error && err.name === "AbortError") return
        const message = err instanceof Error ? err.message : "Unknown trading panel error"
        setError(message)
      })
      .finally(() => setLoading(false))

    return () => controller.abort()
  }, [params.portfolioId, refreshToken])

  return { positions, orders, balance, loading, error, refetch }
}

