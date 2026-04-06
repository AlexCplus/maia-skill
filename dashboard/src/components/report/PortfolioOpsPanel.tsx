"use client"

import { useEffect, useMemo, useState } from "react"
import { motion } from "framer-motion"
import { useLanguage } from "@/hooks/use-language"
import { usePortfolios } from "@/hooks/use-portfolios"
import { useTradingPanel } from "@/hooks/use-trading-panel"
import { useAuth } from "@/hooks/use-auth"
import { getAuthHeader } from "@/lib/auth"
import type { RiskCheckSummary } from "@/types/trading"
import { Input } from "@/components/ui/input"
import { Button } from "@/components/ui/button"
import { Alert, AlertDescription, AlertTitle } from "@/components/ui/alert"
import {
  Table,
  TableBody,
  TableCell,
  TableHead,
  TableHeader,
  TableRow,
} from "@/components/ui/table"

const DEFAULT_API_BASE = "http://127.0.0.1:8000"

export function PortfolioOpsPanel() {
  const { lang } = useLanguage()
  const { token } = useAuth()
  const { data: portfolios, loading: portfoliosLoading, refetch: refetchPortfolios } = usePortfolios()
  const [selectedPortfolioId, setSelectedPortfolioId] = useState<number>(0)
  const [createName, setCreateName] = useState("")
  const [createCurrency, setCreateCurrency] = useState("USD")
  const [editName, setEditName] = useState("")
  const [editCurrency, setEditCurrency] = useState("USD")
  const [busyAction, setBusyAction] = useState<"create" | "update" | "delete" | "order" | "risk" | null>(null)
  const [orderSymbol, setOrderSymbol] = useState("AAPL")
  const [orderSide, setOrderSide] = useState<"buy" | "sell">("buy")
  const [orderQty, setOrderQty] = useState("1")
  const [orderPrice, setOrderPrice] = useState("100")
  const [orderAssetClass, setOrderAssetClass] = useState("stock")
  const [orderFilterSide, setOrderFilterSide] = useState<"all" | "buy" | "sell">("all")
  const [orderFilterSymbol, setOrderFilterSymbol] = useState("")
  const [message, setMessage] = useState<string | null>(null)
  const [messageError, setMessageError] = useState(false)
  const [riskPreview, setRiskPreview] = useState<RiskCheckSummary | null>(null)

  const { positions, orders, balance, loading, error, refetch } = useTradingPanel({
    portfolioId: selectedPortfolioId,
  })

  const apiBase = process.env.NEXT_PUBLIC_AUTOPILOT_API_BASE_URL ?? DEFAULT_API_BASE
  const authHeader = getAuthHeader(token)

  const labels = useMemo(
    () => ({
      title: lang === "es" ? "Operación de Portafolio" : "Portfolio Operations",
      subtitle:
        lang === "es"
          ? "Gestión rápida: crear portfolio, lanzar órdenes paper y revisar estado"
          : "Quick operations: create portfolio, place paper orders, and review state",
      createPortfolio: lang === "es" ? "Crear Portfolio" : "Create Portfolio",
      updatePortfolio: lang === "es" ? "Guardar cambios" : "Save changes",
      deletePortfolio: lang === "es" ? "Eliminar portfolio" : "Delete portfolio",
      placeOrder: lang === "es" ? "Enviar Orden" : "Place Order",
      validateRisk: lang === "es" ? "Validar riesgo" : "Validate risk",
      refresh: lang === "es" ? "Refrescar" : "Refresh",
      symbol: lang === "es" ? "Símbolo" : "Symbol",
      quantity: lang === "es" ? "Cantidad" : "Quantity",
      price: lang === "es" ? "Precio" : "Price",
      assetClass: lang === "es" ? "Clase activo" : "Asset class",
      balance: lang === "es" ? "Balance" : "Balance",
      positions: lang === "es" ? "Posiciones" : "Positions",
      orders: lang === "es" ? "Órdenes" : "Orders",
      buy: lang === "es" ? "Compra" : "Buy",
      sell: lang === "es" ? "Venta" : "Sell",
      all: lang === "es" ? "Todas" : "All",
      filterSide: lang === "es" ? "Filtrar lado" : "Filter side",
      filterSymbol: lang === "es" ? "Filtrar símbolo" : "Filter symbol",
      noData: lang === "es" ? "Sin datos." : "No data.",
      noPortfolios: lang === "es" ? "Crea un portfolio para empezar." : "Create a portfolio to start.",
      portfolioName: lang === "es" ? "Nombre portfolio" : "Portfolio name",
      currency: lang === "es" ? "Moneda" : "Currency",
      confirmDelete:
        lang === "es"
          ? "¿Eliminar este portfolio y todos sus datos? Esta acción no se puede deshacer."
          : "Delete this portfolio and all its data? This cannot be undone.",
      missingToken:
        lang === "es"
          ? "Inicia sesión para operar."
          : "Sign in to trade.",
      riskCheck: lang === "es" ? "Pre-check riesgo" : "Risk pre-check",
      riskViolations: lang === "es" ? "Violaciones de riesgo" : "Risk violations",
      riskOk: lang === "es" ? "Riesgo OK para la orden." : "Risk check passed.",
      riskBlocked: lang === "es" ? "Orden bloqueada por riesgo." : "Order blocked by risk.",
      violation_max_order_notional_exceeded:
        lang === "es" ? "Supera el límite global por orden." : "Exceeds global max order notional.",
      violation_max_daily_loss_exceeded:
        lang === "es" ? "Supera la pérdida diaria máxima." : "Exceeds max daily loss.",
      violation_max_open_positions_exceeded:
        lang === "es" ? "Supera el máximo de posiciones abiertas." : "Exceeds max open positions.",
      violation_max_order_notional_by_symbol_exceeded:
        lang === "es" ? "Supera el límite por símbolo." : "Exceeds symbol-specific notional limit.",
      violation_max_order_notional_by_asset_class_exceeded:
        lang === "es" ? "Supera el límite por clase de activo." : "Exceeds asset-class notional limit.",
      unknownViolation: lang === "es" ? "Violación de riesgo desconocida." : "Unknown risk violation.",
    }),
    [lang]
  )

  const setStatus = (text: string, isError = false) => {
    setMessage(text)
    setMessageError(isError)
  }

  const selectedPortfolioExists = portfolios.some((p) => p.id === selectedPortfolioId)

  useEffect(() => {
    if (portfolios.length === 0) return
    if (!selectedPortfolioExists) {
      setSelectedPortfolioId(portfolios[0].id)
    }
  }, [portfolios, selectedPortfolioExists])

  useEffect(() => {
    const selected = portfolios.find((p) => p.id === selectedPortfolioId)
    if (!selected) {
      setEditName("")
      setEditCurrency("USD")
      return
    }
    setEditName(selected.name)
    setEditCurrency(selected.base_currency)
  }, [portfolios, selectedPortfolioId])

  const createPortfolio = async () => {
    setBusyAction("create")
    setMessage(null)
    if (!authHeader) {
      setStatus(labels.missingToken, true)
      setBusyAction(null)
      return
    }
    const name = createName.trim()
    const currency = createCurrency.trim().toUpperCase()
    if (!name) {
      setStatus(lang === "es" ? "Nombre requerido." : "Name required.", true)
      setBusyAction(null)
      return
    }
    if (currency.length < 3 || currency.length > 8) {
      setStatus(lang === "es" ? "Moneda inválida." : "Invalid currency.", true)
      setBusyAction(null)
      return
    }
    const res = await fetch(`${apiBase}/portfolios`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        ...authHeader,
      },
      body: JSON.stringify({ name, base_currency: currency }),
    })
    if (!res.ok) {
      setStatus(`${lang === "es" ? "Error creando portfolio" : "Error creating portfolio"}: ${res.status}`, true)
      setBusyAction(null)
      return
    }
    const created = (await res.json()) as { id: number; name: string }
    setCreateName("")
    setSelectedPortfolioId(created.id)
    setStatus(`${lang === "es" ? "Portfolio creado" : "Portfolio created"}: ${created.name} (#${created.id})`)
    refetchPortfolios()
    refetch()
    setBusyAction(null)
  }

  const updateSelectedPortfolio = async () => {
    setBusyAction("update")
    setMessage(null)
    if (!authHeader) {
      setStatus(labels.missingToken, true)
      setBusyAction(null)
      return
    }
    if (!selectedPortfolioExists) {
      setStatus(lang === "es" ? "Selecciona un portfolio válido." : "Select a valid portfolio.", true)
      setBusyAction(null)
      return
    }
    const name = editName.trim()
    const currency = editCurrency.trim().toUpperCase()
    if (!name) {
      setStatus(lang === "es" ? "Nombre requerido." : "Name required.", true)
      setBusyAction(null)
      return
    }
    if (currency.length < 3 || currency.length > 8) {
      setStatus(lang === "es" ? "Moneda inválida." : "Invalid currency.", true)
      setBusyAction(null)
      return
    }
    const res = await fetch(`${apiBase}/portfolios/${selectedPortfolioId}`, {
      method: "PUT",
      headers: {
        "Content-Type": "application/json",
        ...authHeader,
      },
      body: JSON.stringify({ name, base_currency: currency }),
    })
    if (!res.ok) {
      setStatus(`${lang === "es" ? "Error actualizando portfolio" : "Error updating portfolio"}: ${res.status}`, true)
      setBusyAction(null)
      return
    }
    setStatus(lang === "es" ? "Portfolio actualizado." : "Portfolio updated.")
    refetchPortfolios()
    refetch()
    setBusyAction(null)
  }

  const deleteSelectedPortfolio = async () => {
    setBusyAction("delete")
    setMessage(null)
    if (!authHeader) {
      setStatus(labels.missingToken, true)
      setBusyAction(null)
      return
    }
    if (!selectedPortfolioExists) {
      setStatus(lang === "es" ? "Selecciona un portfolio válido." : "Select a valid portfolio.", true)
      setBusyAction(null)
      return
    }
    if (!window.confirm(labels.confirmDelete)) {
      setBusyAction(null)
      return
    }
    const deletingId = selectedPortfolioId
    const res = await fetch(`${apiBase}/portfolios/${deletingId}`, {
      method: "DELETE",
      headers: {
        ...authHeader,
      },
    })
    if (!res.ok) {
      setStatus(`${lang === "es" ? "Error eliminando portfolio" : "Error deleting portfolio"}: ${res.status}`, true)
      setBusyAction(null)
      return
    }
    setStatus(lang === "es" ? "Portfolio eliminado." : "Portfolio deleted.")
    const remaining = portfolios.filter((p) => p.id !== deletingId)
    setSelectedPortfolioId(remaining[0]?.id ?? 0)
    refetchPortfolios()
    refetch()
    setBusyAction(null)
  }

  const runRiskCheck = async (): Promise<RiskCheckSummary | null> => {
    if (!authHeader) {
      setStatus(labels.missingToken, true)
      return null
    }
    if (!selectedPortfolioExists) {
      setStatus(lang === "es" ? "Selecciona un portfolio válido." : "Select a valid portfolio.", true)
      return null
    }
    const symbol = orderSymbol.trim().toUpperCase()
    const assetClass = orderAssetClass.trim().toLowerCase()
    const quantity = Number(orderQty)
    const price = Number(orderPrice)
    if (!symbol) {
      setStatus(lang === "es" ? "Símbolo requerido." : "Symbol required.", true)
      return null
    }
    if (!assetClass) {
      setStatus(lang === "es" ? "Clase de activo requerida." : "Asset class required.", true)
      return null
    }
    if (!Number.isFinite(quantity) || quantity <= 0 || !Number.isFinite(price) || price <= 0) {
      setStatus(lang === "es" ? "Cantidad o precio inválidos." : "Invalid quantity or price.", true)
      return null
    }
    const notional = quantity * price
    const riskRes = await fetch(`${apiBase}/portfolios/${selectedPortfolioId}/risk/check`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        ...authHeader,
      },
      body: JSON.stringify({
        proposed_order_notional: notional,
        daily_realized_pnl: 0,
        symbol,
        asset_class: assetClass,
      }),
    })
    if (!riskRes.ok) {
      setStatus(`${lang === "es" ? "Error pre-check riesgo" : "Risk pre-check error"}: ${riskRes.status}`, true)
      return null
    }
    const riskPayload = (await riskRes.json()) as RiskCheckSummary
    setRiskPreview(riskPayload)
    if (!riskPayload.passed) {
      setStatus(
        `${labels.riskBlocked} ${labels.riskViolations}: ${
          riskPayload.violations.map(explainViolation).join(" | ") || "-"
        }`,
        true
      )
      return riskPayload
    }
    setStatus(labels.riskOk, false)
    return riskPayload
  }

  const validateRiskOnly = async () => {
    setBusyAction("risk")
    setMessage(null)
    await runRiskCheck()
    setBusyAction(null)
  }

  const placeOrder = async () => {
    setBusyAction("order")
    setMessage(null)
    const symbol = orderSymbol.trim().toUpperCase()
    const assetClass = orderAssetClass.trim().toLowerCase()
    const quantity = Number(orderQty)
    const price = Number(orderPrice)
    const riskPayload = await runRiskCheck()
    if (!riskPayload) {
      setBusyAction(null)
      return
    }
    if (!riskPayload.passed) {
      setBusyAction(null)
      return
    }

    const res = await fetch(`${apiBase}/orders`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        ...authHeader,
      },
      body: JSON.stringify({
        portfolio_id: selectedPortfolioId,
        symbol,
        side: orderSide,
        quantity,
        price,
        fee: 0,
        asset_class: assetClass,
        daily_realized_pnl: 0,
      }),
    })
    if (!res.ok) {
      const body = await res.text()
      setStatus(`${lang === "es" ? "Orden rechazada" : "Order rejected"}: ${body}`, true)
      setBusyAction(null)
      return
    }
    setStatus(`${lang === "es" ? "Orden ejecutada." : "Order filled."} ${labels.riskOk}`)
    refetch()
    setBusyAction(null)
  }

  const filteredOrders = useMemo(() => {
    const symbolNeedle = orderFilterSymbol.trim().toUpperCase()
    return orders.filter((o) => {
      const sideOk = orderFilterSide === "all" ? true : o.side === orderFilterSide
      const symbolOk = symbolNeedle ? o.symbol.includes(symbolNeedle) : true
      return sideOk && symbolOk
    })
  }, [orderFilterSide, orderFilterSymbol, orders])

  const explainViolation = (code: string) => {
    switch (code) {
      case "max_order_notional_exceeded":
        return labels.violation_max_order_notional_exceeded
      case "max_daily_loss_exceeded":
        return labels.violation_max_daily_loss_exceeded
      case "max_open_positions_exceeded":
        return labels.violation_max_open_positions_exceeded
      case "max_order_notional_by_symbol_exceeded":
        return labels.violation_max_order_notional_by_symbol_exceeded
      case "max_order_notional_by_asset_class_exceeded":
        return labels.violation_max_order_notional_by_asset_class_exceeded
      default:
        return `${labels.unknownViolation} (${code})`
    }
  }

  return (
    <motion.section
      initial={{ opacity: 0, y: 8 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ delay: 0.74 }}
      className="rounded-xl border border-[#E6E6E4] bg-[#FCFCFB] p-5"
    >
      <h3 className="text-sm font-semibold text-[#252420]">{labels.title}</h3>
      <p className="mt-1 text-xs text-[#8B8B85]">{labels.subtitle}</p>

      <div className="mt-3 grid gap-2 sm:grid-cols-[2fr_1fr_auto]">
        <Input value={createName} onChange={(e) => setCreateName(e.target.value)} placeholder={labels.portfolioName} />
        <Input value={createCurrency} onChange={(e) => setCreateCurrency(e.target.value)} placeholder={labels.currency} />
        <Button variant="outline" onClick={createPortfolio} disabled={busyAction !== null}>
          {labels.createPortfolio}
        </Button>
      </div>

      <div className="mt-3 grid gap-2 sm:grid-cols-[2fr_1fr_auto_auto]">
        <Input value={editName} onChange={(e) => setEditName(e.target.value)} placeholder={labels.portfolioName} />
        <Input value={editCurrency} onChange={(e) => setEditCurrency(e.target.value)} placeholder={labels.currency} />
        <Button variant="outline" onClick={updateSelectedPortfolio} disabled={busyAction !== null || !selectedPortfolioExists}>
          {labels.updatePortfolio}
        </Button>
        <Button variant="outline" onClick={deleteSelectedPortfolio} disabled={busyAction !== null || !selectedPortfolioExists}>
          {labels.deletePortfolio}
        </Button>
      </div>

      <div className="mt-3 grid gap-2 sm:grid-cols-[2fr_1fr_1fr_1fr_1fr_1fr_auto_auto]">
        <select
          className="h-8 rounded-lg border border-input bg-transparent px-2.5 py-1 text-sm outline-none"
          disabled={portfoliosLoading}
          value={String(selectedPortfolioId)}
          onChange={(e) => setSelectedPortfolioId(Number(e.target.value))}
        >
          {portfolios.length === 0 ? (
            <option value="0">{labels.noPortfolios}</option>
          ) : (
            portfolios.map((p) => (
              <option key={p.id} value={String(p.id)}>
                {p.name} (#{p.id})
              </option>
            ))
          )}
        </select>
        <Input value={orderSymbol} onChange={(e) => setOrderSymbol(e.target.value)} placeholder={labels.symbol} />
        <select
          className="h-8 rounded-lg border border-input bg-transparent px-2.5 py-1 text-sm outline-none"
          value={orderSide}
          onChange={(e) => setOrderSide(e.target.value as "buy" | "sell")}
        >
          <option value="buy">{labels.buy}</option>
          <option value="sell">{labels.sell}</option>
        </select>
        <Input value={orderQty} onChange={(e) => setOrderQty(e.target.value)} placeholder={labels.quantity} />
        <Input value={orderPrice} onChange={(e) => setOrderPrice(e.target.value)} placeholder={labels.price} />
        <Input value={orderAssetClass} onChange={(e) => setOrderAssetClass(e.target.value)} placeholder={labels.assetClass} />
        <Button variant="outline" onClick={validateRiskOnly} disabled={busyAction !== null}>
          {labels.validateRisk}
        </Button>
        <Button variant="outline" onClick={placeOrder} disabled={busyAction !== null}>
          {labels.placeOrder}
        </Button>
      </div>

      <div className="mt-3 flex gap-2">
        <Button variant="outline" onClick={refetch} disabled={busyAction !== null}>
          {labels.refresh}
        </Button>
      </div>

      {(message || error) && (
        <Alert variant={messageError || !!error ? "destructive" : "default"} className="mt-3">
          <AlertTitle>{messageError || !!error ? "Error" : "Info"}</AlertTitle>
          <AlertDescription>{message ?? error}</AlertDescription>
        </Alert>
      )}

      {riskPreview && (
        <div
          className={`mt-3 rounded-lg border p-3 text-sm ${
            riskPreview.passed
              ? "border-[#D4E8D4] bg-[#F6FFF6]"
              : "border-[#F3C6C6] bg-[#FFF6F6]"
          }`}
        >
          <p className="text-xs text-[#8B8B85]">{labels.riskCheck}</p>
          <p>
            {riskPreview.passed
              ? labels.riskOk
              : `${labels.riskViolations}: ${riskPreview.violations.map(explainViolation).join(" | ")}`}
          </p>
          <p className="text-xs text-[#8B8B85]">
            max_order_notional={riskPreview.max_order_notional} | open_positions={riskPreview.open_positions}
          </p>
        </div>
      )}

      <div className="mt-4 grid gap-3 md:grid-cols-3">
        <div className="rounded-lg border border-[#E6E6E4] bg-white p-3 text-sm">
          <p className="text-xs text-[#8B8B85]">{labels.balance}</p>
          <p>Cash: {balance?.cash_balance?.toFixed(2) ?? "-"}</p>
          <p>Equity: {balance?.equity_estimate?.toFixed(2) ?? "-"}</p>
        </div>
        <div className="rounded-lg border border-[#E6E6E4] bg-white p-3 text-sm">
          <p className="text-xs text-[#8B8B85]">{labels.positions}</p>
          <p>{loading ? "..." : positions.length}</p>
        </div>
        <div className="rounded-lg border border-[#E6E6E4] bg-white p-3 text-sm">
          <p className="text-xs text-[#8B8B85]">{labels.orders}</p>
          <p>{loading ? "..." : orders.length}</p>
        </div>
      </div>

      <div className="mt-4 grid gap-4 lg:grid-cols-2">
        <div className="rounded-lg border border-[#E6E6E4] bg-white p-3">
          <p className="mb-2 text-xs font-semibold uppercase tracking-[0.12em] text-[#8B8B85]">{labels.positions}</p>
          <Table>
            <TableHeader>
              <TableRow>
                <TableHead>{labels.symbol}</TableHead>
                <TableHead>{labels.quantity}</TableHead>
                <TableHead>{labels.price}</TableHead>
                <TableHead>{labels.assetClass}</TableHead>
              </TableRow>
            </TableHeader>
            <TableBody>
              {positions.length === 0 ? (
                <TableRow>
                  <TableCell colSpan={4} className="text-xs text-[#8B8B85]">{labels.noData}</TableCell>
                </TableRow>
              ) : (
                positions.map((p) => (
                  <TableRow key={p.id}>
                    <TableCell>{p.symbol}</TableCell>
                    <TableCell>{p.quantity}</TableCell>
                    <TableCell>{p.avg_cost.toFixed(2)}</TableCell>
                    <TableCell>{p.asset_class}</TableCell>
                  </TableRow>
                ))
              )}
            </TableBody>
          </Table>
        </div>

        <div className="rounded-lg border border-[#E6E6E4] bg-white p-3">
          <p className="mb-2 text-xs font-semibold uppercase tracking-[0.12em] text-[#8B8B85]">{labels.orders}</p>
          <div className="mb-2 grid gap-2 sm:grid-cols-2">
            <select
              className="h-8 rounded-lg border border-input bg-transparent px-2.5 py-1 text-sm outline-none"
              value={orderFilterSide}
              onChange={(e) => setOrderFilterSide(e.target.value as "all" | "buy" | "sell")}
            >
              <option value="all">{labels.filterSide}: {labels.all}</option>
              <option value="buy">{labels.filterSide}: {labels.buy}</option>
              <option value="sell">{labels.filterSide}: {labels.sell}</option>
            </select>
            <Input
              value={orderFilterSymbol}
              onChange={(e) => setOrderFilterSymbol(e.target.value)}
              placeholder={labels.filterSymbol}
            />
          </div>
          <Table>
            <TableHeader>
              <TableRow>
                <TableHead>{labels.symbol}</TableHead>
                <TableHead>{labels.buy}/{labels.sell}</TableHead>
                <TableHead>{labels.quantity}</TableHead>
                <TableHead>{labels.price}</TableHead>
              </TableRow>
            </TableHeader>
            <TableBody>
              {filteredOrders.length === 0 ? (
                <TableRow>
                  <TableCell colSpan={4} className="text-xs text-[#8B8B85]">{labels.noData}</TableCell>
                </TableRow>
              ) : (
                filteredOrders.slice().reverse().map((o) => (
                  <TableRow key={o.order_id}>
                    <TableCell>{o.symbol}</TableCell>
                    <TableCell>{o.side}</TableCell>
                    <TableCell>{o.quantity}</TableCell>
                    <TableCell>{o.price.toFixed(2)}</TableCell>
                  </TableRow>
                ))
              )}
            </TableBody>
          </Table>
        </div>
      </div>
    </motion.section>
  )
}

