"use client"

import { useMemo, useState } from "react"
import { Button } from "@/components/ui/button"
import { Input } from "@/components/ui/input"
import { Alert, AlertDescription, AlertTitle } from "@/components/ui/alert"
import { useAuth } from "@/hooks/use-auth"
import { useLanguage } from "@/hooks/use-language"

export function AuthGate() {
  const { lang } = useLanguage()
  const { login, register, ready } = useAuth()
  const [mode, setMode] = useState<"login" | "register">("login")
  const [email, setEmail] = useState("")
  const [password, setPassword] = useState("")
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState<string | null>(null)

  const labels = useMemo(
    () => ({
      title: lang === "es" ? "Acceso a patrimonio" : "Portfolio Access",
      subtitle:
        lang === "es"
          ? "Inicia sesión o crea cuenta para operar y ver tu rendimiento."
          : "Sign in or create an account to trade and view your performance.",
      email: lang === "es" ? "Correo" : "Email",
      password: lang === "es" ? "Contraseña" : "Password",
      login: lang === "es" ? "Iniciar sesión" : "Sign in",
      register: lang === "es" ? "Crear cuenta" : "Create account",
      switchToRegister: lang === "es" ? "¿No tienes cuenta? Regístrate" : "No account? Register",
      switchToLogin: lang === "es" ? "¿Ya tienes cuenta? Inicia sesión" : "Already have an account? Sign in",
      loading: lang === "es" ? "Cargando..." : "Loading...",
    }),
    [lang]
  )

  const handleSubmit = async () => {
    setError(null)
    const normalizedEmail = email.trim().toLowerCase()
    if (!normalizedEmail || password.length < 8) {
      setError(lang === "es" ? "Correo válido y contraseña (8+)." : "Valid email and password (8+).")
      return
    }
    setLoading(true)
    try {
      if (mode === "login") {
        await login(normalizedEmail, password)
      } else {
        await register(normalizedEmail, password)
      }
    } catch (err: unknown) {
      setError(err instanceof Error ? err.message : "Authentication error")
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="rounded-xl border border-[#E6E6E4] bg-[#FCFCFB] p-5">
      <h3 className="text-sm font-semibold text-[#252420]">{labels.title}</h3>
      <p className="mt-1 text-xs text-[#8B8B85]">{labels.subtitle}</p>
      <div className="mt-3 grid gap-2">
        <Input
          placeholder={labels.email}
          value={email}
          onChange={(e) => setEmail(e.target.value)}
          type="email"
          autoComplete="email"
        />
        <Input
          placeholder={labels.password}
          value={password}
          onChange={(e) => setPassword(e.target.value)}
          type="password"
          autoComplete={mode === "login" ? "current-password" : "new-password"}
        />
      </div>
      <div className="mt-3 flex gap-2">
        <Button variant="outline" onClick={handleSubmit} disabled={!ready || loading}>
          {loading ? labels.loading : mode === "login" ? labels.login : labels.register}
        </Button>
        <Button
          variant="outline"
          onClick={() => setMode((prev) => (prev === "login" ? "register" : "login"))}
          disabled={loading}
        >
          {mode === "login" ? labels.switchToRegister : labels.switchToLogin}
        </Button>
      </div>
      {error && (
        <Alert variant="destructive" className="mt-3">
          <AlertTitle>Error</AlertTitle>
          <AlertDescription>{error}</AlertDescription>
        </Alert>
      )}
    </div>
  )
}

