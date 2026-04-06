"""
Bridge between MAIA report (report_v2.json) and autopilot signals.
Reads AI-generated recommendations from the agents and converts them to trading signals.
"""
from __future__ import annotations

import json
import os
from dataclasses import dataclass
from pathlib import Path
from typing import Any


# Default path relative to project root
DEFAULT_REPORT_PATH = Path(__file__).parent.parent.parent.parent / "dashboard" / "public" / "data" / "report_v2.json"


@dataclass
class ReportPick:
    """A single recommendation from the MAIA report."""
    rank: int
    name: str
    symbol: str
    sector: str
    confidence: float
    risk_score: float
    risk_adjusted_score: float
    recommendation: str  # buy, sell, hold
    reasoning: str
    position_size: str  # e.g., "8-10%"


def _parse_position_size(size_str: str) -> tuple[float, float]:
    """Parse position size like '8-10%' into min/max percentages."""
    try:
        clean = size_str.replace("%", "").strip()
        if "-" in clean:
            parts = clean.split("-")
            return float(parts[0]), float(parts[1])
        return float(clean), float(clean)
    except (ValueError, IndexError):
        return 5.0, 10.0  # default


def load_report(report_path: Path | str | None = None) -> dict[str, Any]:
    """Load the full MAIA report JSON."""
    path = Path(report_path) if report_path else DEFAULT_REPORT_PATH
    env_path = os.environ.get("MAIA_REPORT_PATH")
    if env_path:
        path = Path(env_path)
    
    if not path.exists():
        return {}
    
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def get_picks(
    report_path: Path | str | None = None,
    min_confidence: float = 7.0,
    recommendation_filter: str | None = "buy",
    max_picks: int = 10,
) -> list[ReportPick]:
    """
    Extract risk-adjusted picks from the report.
    
    Args:
        report_path: Path to report_v2.json (uses default if not provided)
        min_confidence: Minimum confidence score to include (1-10)
        recommendation_filter: Only include picks with this recommendation (None for all)
        max_picks: Maximum number of picks to return
    
    Returns:
        List of ReportPick objects sorted by risk_adjusted_score descending
    """
    report = load_report(report_path)
    raw_picks = report.get("risk_adjusted_picks", [])
    
    picks = []
    for item in raw_picks:
        pick = ReportPick(
            rank=item.get("rank", 0),
            name=item.get("name", ""),
            symbol=item.get("symbol", ""),
            sector=item.get("sector", ""),
            confidence=item.get("confidence", 0),
            risk_score=item.get("risk_score", 5),
            risk_adjusted_score=item.get("risk_adjusted_score", 0),
            recommendation=item.get("recommendation", "hold").lower(),
            reasoning=item.get("reasoning", ""),
            position_size=item.get("position_size", "5%"),
        )
        
        # Apply filters
        if pick.confidence < min_confidence:
            continue
        if recommendation_filter and pick.recommendation != recommendation_filter.lower():
            continue
        
        picks.append(pick)
    
    # Sort by risk-adjusted score
    picks.sort(key=lambda p: p.risk_adjusted_score, reverse=True)
    return picks[:max_picks]


def picks_to_watchlist(picks: list[ReportPick]) -> list[dict[str, str]]:
    """
    Convert report picks to autopilot watchlist format.
    
    Returns list of {"symbol": "BTC", "asset_class": "crypto"}
    """
    sector_to_class = {
        "crypto": "crypto",
        "stocks": "stock",
        "materials": "commodity",
        "currencies": "forex",
        "energy": "commodity",
        "etf": "etf",
    }
    
    return [
        {
            "symbol": pick.symbol,
            "asset_class": sector_to_class.get(pick.sector.lower(), "stock"),
        }
        for pick in picks
    ]


def pick_to_signal_params(pick: ReportPick, current_price: float, portfolio_value: float) -> dict:
    """
    Convert a single pick to signal parameters for order creation.
    
    Args:
        pick: The report pick
        current_price: Current market price of the asset
        portfolio_value: Total portfolio value (cash + positions)
    
    Returns:
        Dict with signal parameters: symbol, side, confidence, reason, suggested_price, suggested_quantity
    """
    min_pct, max_pct = _parse_position_size(pick.position_size)
    # Use midpoint of suggested position size
    target_pct = (min_pct + max_pct) / 2 / 100
    target_value = portfolio_value * target_pct
    
    suggested_qty = target_value / current_price if current_price > 0 else 0
    
    sector_to_class = {
        "crypto": "crypto",
        "stocks": "stock",
        "materials": "commodity",
        "currencies": "forex",
        "energy": "commodity",
        "etf": "etf",
    }
    
    return {
        "symbol": pick.symbol,
        "asset_class": sector_to_class.get(pick.sector.lower(), "stock"),
        "side": pick.recommendation,
        "confidence": pick.confidence / 10.0,  # Convert 1-10 to 0-1
        "reason": f"[MAIA Report] {pick.reasoning}",
        "suggested_price": current_price,
        "suggested_quantity": round(suggested_qty, 8),
    }


def get_report_metadata(report_path: Path | str | None = None) -> dict[str, Any]:
    """Get metadata about the report: generated date, model used, etc."""
    report = load_report(report_path)
    return {
        "generated_at": report.get("generated_at", "unknown"),
        "model_used": report.get("model_used", "unknown"),
        "total_picks": len(report.get("risk_adjusted_picks", [])),
        "market_summary": report.get("market_summary", {}).get("summary_text", ""),
    }
