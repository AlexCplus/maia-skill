from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from src.api.auth import get_current_user
from src.api.schemas import (
    AutopilotStartRequest,
    AutopilotStatusRead,
    AutopilotWatchItem,
)
from src.autopilot.runner import WatchItem, get_job, list_jobs, start_job, stop_job
from src.autopilot.report_bridge import get_picks, get_report_metadata, picks_to_watchlist
from src.autopilot.price_feed import get_price, check_price_feed_availability
from src.data.database import SessionLocal, get_db
from src.data.models import User
from src.data.repositories import get_portfolio


router = APIRouter(prefix="/autopilot", tags=["autopilot"])


def _to_status(job) -> AutopilotStatusRead:
    return AutopilotStatusRead(
        portfolio_id=job.portfolio_id,
        running=job.running,
        interval_seconds=job.interval_seconds,
        auto_execute=job.auto_execute,
        watchlist=[AutopilotWatchItem(symbol=w.symbol, asset_class=w.asset_class) for w in job.watchlist],
        use_report=job.use_report,
        use_real_prices=job.use_real_prices,
        min_confidence=job.min_confidence,
        report_picks_count=job.report_picks_count,
        report_last_read=job.report_last_read.isoformat() if job.report_last_read else None,
        started_at=job.started_at.isoformat(),
        last_tick_at=job.last_tick_at.isoformat() if job.last_tick_at else None,
        ticks_total=job.ticks_total,
        last_error=job.last_error,
    )


@router.post("/start", response_model=AutopilotStatusRead, status_code=status.HTTP_201_CREATED)
def start_autopilot(
    payload: AutopilotStartRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> AutopilotStatusRead:
    portfolio = get_portfolio(db, portfolio_id=payload.portfolio_id, owner_id=current_user.id)
    if portfolio is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Portfolio not found")
    try:
        job = start_job(
            owner_id=current_user.id,
            portfolio_id=payload.portfolio_id,
            interval_seconds=payload.interval_seconds,
            auto_execute=payload.auto_execute,
            watchlist=[WatchItem(symbol=w.symbol.upper(), asset_class=w.asset_class.lower()) for w in payload.watchlist],
            session_factory=SessionLocal,
            use_report=payload.use_report,
            use_real_prices=payload.use_real_prices,
            min_confidence=payload.min_confidence,
        )
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(exc)) from exc
    return _to_status(job)


@router.post("/stop/{portfolio_id}", response_model=AutopilotStatusRead)
def stop_autopilot(
    portfolio_id: int,
    current_user: User = Depends(get_current_user),
) -> AutopilotStatusRead:
    job = stop_job(owner_id=current_user.id, portfolio_id=portfolio_id)
    if job is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Autopilot job not found")
    return _to_status(job)


@router.get("/status/{portfolio_id}", response_model=AutopilotStatusRead)
def autopilot_status(
    portfolio_id: int,
    current_user: User = Depends(get_current_user),
) -> AutopilotStatusRead:
    job = get_job(owner_id=current_user.id, portfolio_id=portfolio_id)
    if job is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Autopilot job not found")
    return _to_status(job)


@router.get("/status", response_model=list[AutopilotStatusRead])
def autopilot_status_all(current_user: User = Depends(get_current_user)) -> list[AutopilotStatusRead]:
    return [_to_status(job) for job in list_jobs(owner_id=current_user.id)]


@router.get("/report/info")
def report_info(current_user: User = Depends(get_current_user)) -> dict:
    """Get metadata about the current MAIA report."""
    meta = get_report_metadata()
    picks = get_picks(min_confidence=0)  # Get all picks
    return {
        "metadata": meta,
        "total_picks": len(picks),
        "buy_recommendations": len([p for p in picks if p.recommendation == "buy"]),
        "sell_recommendations": len([p for p in picks if p.recommendation == "sell"]),
        "hold_recommendations": len([p for p in picks if p.recommendation == "hold"]),
        "picks_preview": [
            {
                "rank": p.rank,
                "symbol": p.symbol,
                "name": p.name,
                "sector": p.sector,
                "recommendation": p.recommendation,
                "confidence": p.confidence,
                "risk_adjusted_score": p.risk_adjusted_score,
            }
            for p in picks[:10]
        ],
    }


@router.get("/report/picks")
def report_picks(
    min_confidence: float = 7.0,
    recommendation: str | None = None,
    current_user: User = Depends(get_current_user),
) -> dict:
    """Get picks from MAIA report with optional filters."""
    picks = get_picks(min_confidence=min_confidence, recommendation_filter=recommendation)
    return {
        "count": len(picks),
        "picks": [
            {
                "rank": p.rank,
                "symbol": p.symbol,
                "name": p.name,
                "sector": p.sector,
                "recommendation": p.recommendation,
                "confidence": p.confidence,
                "risk_score": p.risk_score,
                "risk_adjusted_score": p.risk_adjusted_score,
                "reasoning": p.reasoning,
                "position_size": p.position_size,
            }
            for p in picks
        ],
        "watchlist_format": picks_to_watchlist(picks),
    }


@router.get("/prices/check")
def check_prices(current_user: User = Depends(get_current_user)) -> dict:
    """Check which price feed providers are available."""
    return check_price_feed_availability()


@router.get("/prices/{symbol}")
def get_current_price(
    symbol: str,
    asset_class: str = "stock",
    current_user: User = Depends(get_current_user),
) -> dict:
    """Get current price for a symbol."""
    try:
        price_data = get_price(symbol, asset_class, use_simulation=True)
        return {
            "symbol": price_data.symbol,
            "price": price_data.price,
            "currency": price_data.currency,
            "source": price_data.source,
            "timestamp": price_data.timestamp.isoformat(),
            "change_24h": price_data.change_24h,
            "volume_24h": price_data.volume_24h,
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/analysis/status")
def analysis_status(current_user: User = Depends(get_current_user)) -> dict:
    """Get status of MAIA analysis and instructions to run it."""
    from src.autopilot.run_analysis import run_maia_analysis, check_skill_exists
    
    return {
        "skill_available": check_skill_exists(),
        "analysis_info": run_maia_analysis(),
    }

