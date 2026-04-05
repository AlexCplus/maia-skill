from fastapi.testclient import TestClient

from src.api.main import app
from src.data import init_db


def _auth_headers(client: TestClient, email: str = "user@example.com", password: str = "secret1234") -> dict[str, str]:
    register_resp = client.post("/auth/register", json={"email": email, "password": password})
    if register_resp.status_code not in (201, 409):
        raise AssertionError(register_resp.text)
    login_resp = client.post("/auth/login", json={"email": email, "password": password})
    assert login_resp.status_code == 200
    token = login_resp.json()["access_token"]
    return {"Authorization": f"Bearer {token}"}


def test_portfolio_crud_basics() -> None:
    init_db()
    client = TestClient(app)
    headers = _auth_headers(client)

    create_resp = client.post("/portfolios", json={"name": "Core Portfolio", "base_currency": "usd"}, headers=headers)
    assert create_resp.status_code == 201
    created = create_resp.json()
    assert created["name"] == "Core Portfolio"
    assert created["base_currency"] == "USD"
    portfolio_id = created["id"]

    list_resp = client.get("/portfolios", headers=headers)
    assert list_resp.status_code == 200
    items = list_resp.json()
    assert any(item["id"] == portfolio_id for item in items)

    get_resp = client.get(f"/portfolios/{portfolio_id}", headers=headers)
    assert get_resp.status_code == 200
    assert get_resp.json()["id"] == portfolio_id


def test_positions_and_transactions_flow() -> None:
    init_db()
    client = TestClient(app)
    headers = _auth_headers(client, email="positions@example.com")

    created = client.post("/portfolios", json={"name": "Tactical", "base_currency": "EUR"}, headers=headers).json()
    portfolio_id = created["id"]

    position_resp = client.post(
        f"/portfolios/{portfolio_id}/positions",
        json={"symbol": "aapl", "quantity": 5, "avg_cost": 180.5, "asset_class": "stock"},
        headers=headers,
    )
    assert position_resp.status_code == 201
    assert position_resp.json()["symbol"] == "AAPL"

    tx_resp = client.post(
        f"/portfolios/{portfolio_id}/transactions",
        json={"symbol": "aapl", "side": "buy", "quantity": 5, "price": 180.5, "fee": 1.2},
        headers=headers,
    )
    assert tx_resp.status_code == 201
    assert tx_resp.json()["side"] == "buy"

    list_positions_resp = client.get(f"/portfolios/{portfolio_id}/positions", headers=headers)
    assert list_positions_resp.status_code == 200
    assert len(list_positions_resp.json()) >= 1

    list_tx_resp = client.get(f"/portfolios/{portfolio_id}/transactions", headers=headers)
    assert list_tx_resp.status_code == 200
    assert len(list_tx_resp.json()) >= 1


def test_pnl_risk_and_rebalance_endpoints() -> None:
    init_db()
    client = TestClient(app)
    headers = _auth_headers(client, email="analytics@example.com")

    created = client.post("/portfolios", json={"name": "Balanced", "base_currency": "USD"}, headers=headers).json()
    portfolio_id = created["id"]

    client.post(
        f"/portfolios/{portfolio_id}/positions",
        json={"symbol": "AAPL", "quantity": 10, "avg_cost": 100, "asset_class": "stock"},
        headers=headers,
    )
    client.post(
        f"/portfolios/{portfolio_id}/positions",
        json={"symbol": "BTC", "quantity": 1, "avg_cost": 20000, "asset_class": "crypto"},
        headers=headers,
    )

    pnl_resp = client.post(
        f"/portfolios/{portfolio_id}/analytics/pnl",
        json={"current_prices": {"AAPL": 110, "BTC": 25000}},
        headers=headers,
    )
    assert pnl_resp.status_code == 200
    pnl_data = pnl_resp.json()
    assert pnl_data["total_unrealized_pnl"] > 0
    assert len(pnl_data["positions"]) == 2

    risk_resp = client.post(
        f"/portfolios/{portfolio_id}/risk/check",
        json={"proposed_order_notional": 1000, "daily_realized_pnl": -100},
        headers=headers,
    )
    assert risk_resp.status_code == 200
    assert risk_resp.json()["passed"] is True

    rebalance_resp = client.post(
        f"/portfolios/{portfolio_id}/strategy/rebalance",
        json={
            "current_prices": {"AAPL": 110, "BTC": 25000},
            "target_allocation": {"stock": 0.5, "crypto": 0.5},
            "min_trade_notional": 1,
        },
        headers=headers,
    )
    assert rebalance_resp.status_code == 200
    rebalance_data = rebalance_resp.json()
    assert "actions" in rebalance_data


def test_order_flow_updates_transactions_and_positions() -> None:
    init_db()
    client = TestClient(app)
    headers = _auth_headers(client, email="orders@example.com")

    created = client.post("/portfolios", json={"name": "Execution", "base_currency": "USD"}, headers=headers).json()
    portfolio_id = created["id"]

    buy_resp = client.post(
        "/orders",
        json={
            "portfolio_id": portfolio_id,
            "symbol": "MSFT",
            "side": "buy",
            "quantity": 2,
            "price": 300,
            "fee": 1,
            "asset_class": "stock",
            "daily_realized_pnl": 0,
        },
        headers=headers,
    )
    assert buy_resp.status_code == 201
    assert buy_resp.json()["status"] == "filled"

    positions_resp = client.get(f"/portfolios/{portfolio_id}/positions", headers=headers)
    assert positions_resp.status_code == 200
    positions = positions_resp.json()
    assert any(p["symbol"] == "MSFT" and p["quantity"] == 2 for p in positions)

    tx_resp = client.get(f"/portfolios/{portfolio_id}/transactions", headers=headers)
    assert tx_resp.status_code == 200
    assert any(t["symbol"] == "MSFT" and t["side"] == "buy" for t in tx_resp.json())

    sell_resp = client.post(
        "/orders",
        json={
            "portfolio_id": portfolio_id,
            "symbol": "MSFT",
            "side": "sell",
            "quantity": 1,
            "price": 310,
            "fee": 1,
            "asset_class": "stock",
            "daily_realized_pnl": 0,
        },
        headers=headers,
    )
    assert sell_resp.status_code == 201

    positions_after_sell = client.get(f"/portfolios/{portfolio_id}/positions", headers=headers).json()
    msft = [p for p in positions_after_sell if p["symbol"] == "MSFT"][0]
    assert msft["quantity"] == 1


def test_order_risk_validation_blocks_large_order() -> None:
    init_db()
    client = TestClient(app)
    headers = _auth_headers(client, email="risk@example.com")

    created = client.post("/portfolios", json={"name": "Risk", "base_currency": "USD"}, headers=headers).json()
    portfolio_id = created["id"]

    blocked_resp = client.post(
        "/orders",
        json={
            "portfolio_id": portfolio_id,
            "symbol": "SPY",
            "side": "buy",
            "quantity": 1000,
            "price": 100,
            "fee": 0,
            "asset_class": "stock",
            "daily_realized_pnl": 0,
        },
        headers=headers,
    )
    assert blocked_resp.status_code == 400


def test_orders_list_and_paper_balance() -> None:
    init_db()
    client = TestClient(app)
    headers = _auth_headers(client, email="ledger@example.com")

    portfolio = client.post("/portfolios", json={"name": "Ledger", "base_currency": "USD"}, headers=headers).json()
    portfolio_id = portfolio["id"]

    client.post(
        "/orders",
        json={
            "portfolio_id": portfolio_id,
            "symbol": "NVDA",
            "side": "buy",
            "quantity": 1,
            "price": 500,
            "fee": 1,
            "asset_class": "stock",
            "daily_realized_pnl": 0,
        },
        headers=headers,
    )
    client.post(
        "/orders",
        json={
            "portfolio_id": portfolio_id,
            "symbol": "NVDA",
            "side": "sell",
            "quantity": 0.5,
            "price": 550,
            "fee": 1,
            "asset_class": "stock",
            "daily_realized_pnl": 0,
        },
        headers=headers,
    )

    orders_all = client.get("/orders", headers=headers)
    assert orders_all.status_code == 200
    assert len(orders_all.json()) >= 2

    orders_portfolio = client.get(f"/orders?portfolio_id={portfolio_id}", headers=headers)
    assert orders_portfolio.status_code == 200
    assert len(orders_portfolio.json()) == 2

    balance_resp = client.get(f"/orders/balance/{portfolio_id}", headers=headers)
    assert balance_resp.status_code == 200
    balance = balance_resp.json()
    assert balance["initial_cash"] == 100000.0
    assert balance["cash_balance"] < 100000.0


def test_daily_summary_includes_realized_and_unrealized_pnl() -> None:
    init_db()
    client = TestClient(app)
    headers = _auth_headers(client, email="summary@example.com")

    portfolio = client.post("/portfolios", json={"name": "Summary", "base_currency": "USD"}, headers=headers).json()
    portfolio_id = portfolio["id"]

    client.post(
        "/orders",
        json={
            "portfolio_id": portfolio_id,
            "symbol": "TSLA",
            "side": "buy",
            "quantity": 2,
            "price": 100,
            "fee": 0,
            "asset_class": "stock",
            "daily_realized_pnl": 0,
        },
        headers=headers,
    )
    client.post(
        "/orders",
        json={
            "portfolio_id": portfolio_id,
            "symbol": "TSLA",
            "side": "sell",
            "quantity": 1,
            "price": 120,
            "fee": 0,
            "asset_class": "stock",
            "daily_realized_pnl": 0,
        },
        headers=headers,
    )

    summary_resp = client.post(
        f"/portfolios/{portfolio_id}/analytics/daily-summary",
        json={"current_prices": {"TSLA": 130}},
        headers=headers,
    )
    assert summary_resp.status_code == 200
    summary = summary_resp.json()
    assert summary["trades_count_day"] >= 2
    assert summary["realized_pnl_day"] > 0
    assert summary["unrealized_pnl_snapshot"] > 0


def test_performance_timeseries_endpoint_returns_expected_points() -> None:
    init_db()
    client = TestClient(app)
    headers = _auth_headers(client, email="perf@example.com")

    portfolio = client.post("/portfolios", json={"name": "Perf", "base_currency": "USD"}, headers=headers).json()
    portfolio_id = portfolio["id"]

    client.post(
        "/orders",
        json={
            "portfolio_id": portfolio_id,
            "symbol": "AMD",
            "side": "buy",
            "quantity": 2,
            "price": 100,
            "fee": 0,
            "asset_class": "stock",
            "daily_realized_pnl": 0,
        },
        headers=headers,
    )
    client.post(
        "/orders",
        json={
            "portfolio_id": portfolio_id,
            "symbol": "AMD",
            "side": "sell",
            "quantity": 1,
            "price": 110,
            "fee": 0,
            "asset_class": "stock",
            "daily_realized_pnl": 0,
        },
        headers=headers,
    )

    perf_resp = client.post(
        f"/portfolios/{portfolio_id}/analytics/performance",
        json={"days": 7},
        headers=headers,
    )
    assert perf_resp.status_code == 200
    payload = perf_resp.json()
    assert payload["portfolio_id"] == portfolio_id
    assert payload["days"] == 7
    assert len(payload["series"]) == 7


def test_order_sell_without_position_is_rejected() -> None:
    init_db()
    client = TestClient(app)
    headers = _auth_headers(client, email="sellwithout@example.com")

    created = client.post("/portfolios", json={"name": "SellCheck", "base_currency": "USD"}, headers=headers).json()
    portfolio_id = created["id"]

    resp = client.post(
        "/orders",
        json={
            "portfolio_id": portfolio_id,
            "symbol": "QQQ",
            "side": "sell",
            "quantity": 1,
            "price": 400,
            "fee": 0,
            "asset_class": "stock",
            "daily_realized_pnl": 0,
        },
        headers=headers,
    )
    assert resp.status_code == 400


def test_order_oversell_is_rejected() -> None:
    init_db()
    client = TestClient(app)
    headers = _auth_headers(client, email="oversell@example.com")

    created = client.post("/portfolios", json={"name": "OverSell", "base_currency": "USD"}, headers=headers).json()
    portfolio_id = created["id"]

    client.post(
        "/orders",
        json={
            "portfolio_id": portfolio_id,
            "symbol": "META",
            "side": "buy",
            "quantity": 1,
            "price": 300,
            "fee": 0,
            "asset_class": "stock",
            "daily_realized_pnl": 0,
        },
        headers=headers,
    )
    resp = client.post(
        "/orders",
        json={
            "portfolio_id": portfolio_id,
            "symbol": "META",
            "side": "sell",
            "quantity": 2,
            "price": 320,
            "fee": 0,
            "asset_class": "stock",
            "daily_realized_pnl": 0,
        },
        headers=headers,
    )
    assert resp.status_code == 400


def test_order_blocks_when_daily_loss_exceeded() -> None:
    init_db()
    client = TestClient(app)
    headers = _auth_headers(client, email="lossguard@example.com")

    created = client.post("/portfolios", json={"name": "LossGuard", "base_currency": "USD"}, headers=headers).json()
    portfolio_id = created["id"]

    resp = client.post(
        "/orders",
        json={
            "portfolio_id": portfolio_id,
            "symbol": "DIA",
            "side": "buy",
            "quantity": 1,
            "price": 100,
            "fee": 0,
            "asset_class": "stock",
            "daily_realized_pnl": -2000,
        },
        headers=headers,
    )
    assert resp.status_code == 400


def test_multiuser_portfolio_isolation() -> None:
    init_db()
    client = TestClient(app)

    headers_a = _auth_headers(client, email="alice@example.com")
    headers_b = _auth_headers(client, email="bob@example.com")

    created = client.post("/portfolios", json={"name": "AliceOnly", "base_currency": "USD"}, headers=headers_a).json()
    portfolio_id = created["id"]

    bob_read = client.get(f"/portfolios/{portfolio_id}", headers=headers_b)
    assert bob_read.status_code == 404

