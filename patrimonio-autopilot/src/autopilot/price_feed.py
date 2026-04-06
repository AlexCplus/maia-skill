"""
Price feed module for real market data.
Supports multiple providers with fallback: Yahoo Finance, CoinGecko, simulation.
"""
from __future__ import annotations

import os
import time
from dataclasses import dataclass
from datetime import datetime, timezone
from typing import Any
import random


@dataclass
class PriceData:
    """Standardized price data."""
    symbol: str
    price: float
    currency: str
    source: str
    timestamp: datetime
    change_24h: float | None = None
    volume_24h: float | None = None


# Symbol mappings for different providers
YAHOO_SYMBOL_MAP = {
    "BTC": "BTC-USD",
    "ETH": "ETH-USD",
    "SOL": "SOL-USD",
    "AVAX": "AVAX-USD",
    "HG": "HG=F",  # Copper futures
    "GC": "GC=F",  # Gold futures
    "CL": "CL=F",  # Crude oil futures
    "USD/MXN": "MXN=X",
    "EUR/USD": "EURUSD=X",
}

COINGECKO_IDS = {
    "BTC": "bitcoin",
    "ETH": "ethereum",
    "SOL": "solana",
    "AVAX": "avalanche-2",
    "DOGE": "dogecoin",
    "XRP": "ripple",
}


class PriceFeedError(Exception):
    """Raised when price cannot be fetched."""


def _try_yfinance(symbol: str) -> PriceData | None:
    """Try to get price from Yahoo Finance."""
    try:
        import yfinance as yf
        
        ticker_symbol = YAHOO_SYMBOL_MAP.get(symbol.upper(), symbol.upper())
        ticker = yf.Ticker(ticker_symbol)
        
        # Try fast_info first (faster)
        try:
            price = ticker.fast_info.last_price
            if price and price > 0:
                return PriceData(
                    symbol=symbol.upper(),
                    price=float(price),
                    currency="USD",
                    source="yahoo_finance",
                    timestamp=datetime.now(timezone.utc),
                )
        except Exception:
            pass
        
        # Fallback to history
        hist = ticker.history(period="1d")
        if not hist.empty:
            price = float(hist["Close"].iloc[-1])
            return PriceData(
                symbol=symbol.upper(),
                price=price,
                currency="USD",
                source="yahoo_finance",
                timestamp=datetime.now(timezone.utc),
            )
    except ImportError:
        pass  # yfinance not installed
    except Exception:
        pass  # Any other error
    
    return None


def _try_coingecko(symbol: str) -> PriceData | None:
    """Try to get price from CoinGecko (free, no API key)."""
    try:
        import urllib.request
        import json
        
        coin_id = COINGECKO_IDS.get(symbol.upper())
        if not coin_id:
            return None
        
        url = f"https://api.coingecko.com/api/v3/simple/price?ids={coin_id}&vs_currencies=usd&include_24hr_change=true&include_24hr_vol=true"
        
        req = urllib.request.Request(url, headers={"Accept": "application/json"})
        with urllib.request.urlopen(req, timeout=10) as response:
            data = json.loads(response.read().decode())
        
        if coin_id in data:
            coin_data = data[coin_id]
            return PriceData(
                symbol=symbol.upper(),
                price=float(coin_data["usd"]),
                currency="USD",
                source="coingecko",
                timestamp=datetime.now(timezone.utc),
                change_24h=coin_data.get("usd_24h_change"),
                volume_24h=coin_data.get("usd_24h_vol"),
            )
    except Exception:
        pass
    
    return None


def _simulate_price(symbol: str, asset_class: str) -> PriceData:
    """Generate simulated price (fallback)."""
    base_prices = {
        "BTC": 67000,
        "ETH": 3500,
        "SOL": 150,
        "VRT": 85,
        "LITE": 95,
        "HG": 4.5,
        "GC": 2350,
        "USD/MXN": 17.2,
    }
    
    base = base_prices.get(symbol.upper(), 100)
    # Add small random variation
    variation = random.uniform(-0.02, 0.02)
    price = base * (1 + variation)
    
    return PriceData(
        symbol=symbol.upper(),
        price=round(price, 4),
        currency="USD",
        source="simulation",
        timestamp=datetime.now(timezone.utc),
    )


# Rate limiting for API calls
_last_call_time: dict[str, float] = {}
MIN_CALL_INTERVAL = 1.0  # seconds between calls to same provider


def _rate_limit(provider: str) -> None:
    """Simple rate limiting."""
    last = _last_call_time.get(provider, 0)
    elapsed = time.time() - last
    if elapsed < MIN_CALL_INTERVAL:
        time.sleep(MIN_CALL_INTERVAL - elapsed)
    _last_call_time[provider] = time.time()


def get_price(
    symbol: str,
    asset_class: str = "stock",
    use_simulation: bool = True,
) -> PriceData:
    """
    Get current price for a symbol.
    
    Tries providers in order:
    1. Yahoo Finance (for stocks, ETFs, forex, commodities, crypto)
    2. CoinGecko (for crypto)
    3. Simulation (if use_simulation=True)
    
    Args:
        symbol: Trading symbol (e.g., "BTC", "AAPL", "VRT")
        asset_class: Asset type for simulation fallback
        use_simulation: Whether to fall back to simulated prices
    
    Returns:
        PriceData with current price
    
    Raises:
        PriceFeedError if price cannot be obtained and simulation disabled
    """
    # Check environment for forcing simulation mode
    if os.environ.get("PRICE_FEED_SIMULATION", "").lower() == "true":
        return _simulate_price(symbol, asset_class)
    
    # Try Yahoo Finance
    _rate_limit("yahoo")
    result = _try_yfinance(symbol)
    if result:
        return result
    
    # Try CoinGecko for crypto
    if asset_class.lower() == "crypto" or symbol.upper() in COINGECKO_IDS:
        _rate_limit("coingecko")
        result = _try_coingecko(symbol)
        if result:
            return result
    
    # Fallback to simulation
    if use_simulation:
        return _simulate_price(symbol, asset_class)
    
    raise PriceFeedError(f"Could not get price for {symbol}")


def get_prices_batch(symbols: list[dict[str, str]], use_simulation: bool = True) -> dict[str, PriceData]:
    """
    Get prices for multiple symbols.
    
    Args:
        symbols: List of {"symbol": "BTC", "asset_class": "crypto"}
        use_simulation: Whether to fall back to simulated prices
    
    Returns:
        Dict mapping symbol to PriceData
    """
    results = {}
    for item in symbols:
        symbol = item.get("symbol", "")
        asset_class = item.get("asset_class", "stock")
        try:
            results[symbol] = get_price(symbol, asset_class, use_simulation)
        except PriceFeedError:
            pass
    return results


def check_price_feed_availability() -> dict[str, bool]:
    """Check which price feed providers are available."""
    available = {
        "yfinance": False,
        "coingecko": False,
        "simulation": True,
    }
    
    try:
        import yfinance
        available["yfinance"] = True
    except ImportError:
        pass
    
    # CoinGecko is always available (just HTTP requests)
    available["coingecko"] = True
    
    return available
