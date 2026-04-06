"use client"

import { createContext, useCallback, useContext, useEffect, useMemo, useState, type ReactNode } from "react"

const DEFAULT_API_BASE = "http://127.0.0.1:8000"
const TOKEN_STORAGE_KEY = "autopilot-token-v1"
const EMAIL_STORAGE_KEY = "autopilot-email-v1"

interface AuthContextValue {
  token: string | null
  email: string | null
  ready: boolean
  isAuthenticated: boolean
  login: (email: string, password: string) => Promise<void>
  register: (email: string, password: string) => Promise<void>
  logout: () => void
}

const AuthContext = createContext<AuthContextValue | null>(null)

async function authenticate(
  mode: "login" | "register",
  email: string,
  password: string
): Promise<{ access_token: string }> {
  const apiBase = process.env.NEXT_PUBLIC_AUTOPILOT_API_BASE_URL ?? DEFAULT_API_BASE
  const endpoint = mode === "login" ? "/auth/login" : "/auth/register"
  const res = await fetch(`${apiBase}${endpoint}`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ email, password }),
  })
  if (!res.ok) {
    const detail = await res.text()
    throw new Error(detail || `Auth failed (${res.status})`)
  }
  return (await res.json()) as { access_token: string }
}

export function AuthProvider({ children }: { children: ReactNode }) {
  const [token, setToken] = useState<string | null>(null)
  const [email, setEmail] = useState<string | null>(null)
  const [ready, setReady] = useState(false)

  useEffect(() => {
    const storedToken = localStorage.getItem(TOKEN_STORAGE_KEY)
    const storedEmail = localStorage.getItem(EMAIL_STORAGE_KEY)
    const envToken = process.env.NEXT_PUBLIC_AUTOPILOT_TOKEN ?? null
    setToken((storedToken ?? envToken)?.trim() || null)
    setEmail(storedEmail || null)
    setReady(true)
  }, [])

  const login = useCallback(async (rawEmail: string, rawPassword: string) => {
    const normalizedEmail = rawEmail.trim().toLowerCase()
    const payload = await authenticate("login", normalizedEmail, rawPassword)
    setToken(payload.access_token)
    setEmail(normalizedEmail)
    localStorage.setItem(TOKEN_STORAGE_KEY, payload.access_token)
    localStorage.setItem(EMAIL_STORAGE_KEY, normalizedEmail)
  }, [])

  const register = useCallback(async (rawEmail: string, rawPassword: string) => {
    const normalizedEmail = rawEmail.trim().toLowerCase()
    const payload = await authenticate("register", normalizedEmail, rawPassword)
    setToken(payload.access_token)
    setEmail(normalizedEmail)
    localStorage.setItem(TOKEN_STORAGE_KEY, payload.access_token)
    localStorage.setItem(EMAIL_STORAGE_KEY, normalizedEmail)
  }, [])

  const logout = useCallback(() => {
    setToken(null)
    setEmail(null)
    localStorage.removeItem(TOKEN_STORAGE_KEY)
    localStorage.removeItem(EMAIL_STORAGE_KEY)
  }, [])

  const value = useMemo<AuthContextValue>(
    () => ({
      token,
      email,
      ready,
      isAuthenticated: !!token,
      login,
      register,
      logout,
    }),
    [email, login, logout, ready, register, token]
  )

  return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>
}

export function useAuth(): AuthContextValue {
  const ctx = useContext(AuthContext)
  if (!ctx) {
    throw new Error("useAuth must be used within an AuthProvider")
  }
  return ctx
}

