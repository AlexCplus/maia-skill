"""
Fetches real-time prices from Yahoo Finance (stocks) and CoinGecko (crypto).
Falls back to simulated prices if APIs fail.
"""
from __future__ import annotations

import logging
from typing import TYPE_CHECKING

import httpx

if TYPE_CHECKING:
    pass

logger = logging.getLogger(__name__)

_COINGECKO_IDS: dict[str, str] = {
    "BTC": "bitcoin",
    "ETH": "ethereum",
    "SOL": "solana",
    "XRP": "ripple",
    "ADA": "cardano",
    "DOGE": "dogecoin",
    "DOT": "polkadot",
    "AVAX": "avalanche-2",
    "MATIC": "matic-network",
    "LINK": "chainlink",
    "UNI": "uniswap",
    "ATOM": "cosmos",
    "LTC": "litecoin",
    "SHIB": "shiba-inu",
    "TRX": "tron",
    "NEAR": "near",
    "APT": "aptos",
    "ARB": "arbitrum",
    "OP": "optimism",
}


def _fetch_crypto_price_coingecko(symbol: str, timeout: float = 10.0) -> float | None:
    """Fetch crypto price from CoinGecko API (free, no key required)."""
    coin_id = _COINGECKO_IDS.get(symbol.upper())
    if coin_id is None:
        return None
    url = f"https://api.coingecko.com/api/v3/simple/price?ids={coin_id}&vs_currencies=usd"
    try:
        with httpx.Client(timeout=timeout) as client:
            resp = client.get(url)
            resp.raise_for_status()
            data = resp.json()
            price = data.get(coin_id, {}).get("usd")
            return float(price) if price is not None else None
    except Exception as e:
        logger.warning(f"CoinGecko fetch failed for {symbol}: {e}")
        return None


def _fetch_stock_price_yahoo(symbol: str, timeout: float = 10.0) -> float | None:
    """Fetch stock price using yfinance (Yahoo Finance)."""
    try:
        import yfinance as yf
        ticker = yf.Ticker(symbol)
        hist = ticker.history(period="1d")
        if hist.empty:
            return None
        return float(hist["Close"].iloc[-1])
    except Exception as e:
        logger.warning(f"Yahoo Finance fetch failed for {symbol}: {e}")
        return None


def _fetch_commodity_price(symbol: str, timeout: float = 10.0) -> float | None:
    """Fetch commodity prices (gold, oil, etc.) via Yahoo Finance tickers."""
    commodity_tickers = {
        "GOLD": "GC=F",
        "XAU": "GC=F",
        "OIL": "CL=F",
        "WTI": "CL=F",
        "SILVER": "SI=F",
        "XAG": "SI=F",
        "COPPER": "HG=F",
        "HG": "HG=F",
        "NATGAS": "NG=F",
        "NG": "NG=F",
    }
    ticker_symbol = commodity_tickers.get(symbol.upper())
    if ticker_symbol is None:
        return None
    return _fetch_stock_price_yahoo(ticker_symbol, timeout)


def _fetch_forex_price(symbol: str, timeout: float = 10.0) -> float | None:
    """Fetch forex pair via Yahoo Finance."""
    symbol_clean = symbol.upper().replace("/", "").replace("-", "")
    if len(symbol_clean) == 6:
        yahoo_symbol = f"{symbol_clean}=X"
    elif symbol_clean == "DXY":
        yahoo_symbol = "DX-Y.NYB"
    else:
        yahoo_symbol = f"{symbol_clean}=X"
    return _fetch_stock_price_yahoo(yahoo_symbol, timeout)


def fetch_price(symbol: str, asset_class: str, timeout: float = 10.0) -> float | None:
    """
    Fetch real price for a symbol based on asset class.
    Returns None if fetch fails.
    """
    asset_lower = asset_class.lower()
    symbol_upper = symbol.upper()

    if asset_lower == "crypto":
        return _fetch_crypto_price_coingecko(symbol_upper, timeout)
    elif asset_lower in {"stock", "stocks", "equity"}:
        return _fetch_stock_price_yahoo(symbol_upper, timeout)
    elif asset_lower in {"commodity", "commodities", "materials"}:
        return _fetch_commodity_price(symbol_upper, timeout)
    elif asset_lower in {"forex", "currency", "currencies"}:
        return _fetch_forex_price(symbol_upper, timeout)
    else:
        price = _fetch_stock_price_yahoo(symbol_upper, timeout)
        if price is None:
            price = _fetch_crypto_price_coingecko(symbol_upper, timeout)
        return price


def fetch_prices_batch(items: list[tuple[str, str]], timeout: float = 10.0) -> dict[str, float | None]:
    """
    Fetch prices for multiple (symbol, asset_class) pairs.
    Returns dict mapping symbol to price (or None if failed).
    """
    result: dict[str, float | None] = {}
    for symbol, asset_class in items:
        result[symbol.upper()] = fetch_price(symbol, asset_class, timeout)
    return result
