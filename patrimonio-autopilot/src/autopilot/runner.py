from __future__ import annotations

import os
from collections import defaultdict, deque
from dataclasses import dataclass, field
from datetime import datetime, timezone
from threading import Event, Lock, Thread
import random
import logging

from sqlalchemy.orm import Session, sessionmaker

from src.api.schemas import OrderCreate
from src.data.repositories import (
    create_ai_signal,
    get_portfolio,
    list_positions,
    mark_ai_signal_executed,
)
from src.execution.order_service import execute_paper_order
from src.strategy.signal_engine import suggest_trade_from_prices
from src.autopilot.report_bridge import get_picks, picks_to_watchlist, pick_to_signal_params, get_report_metadata
from src.autopilot.price_feed import get_price, PriceFeedError

logger = logging.getLogger(__name__)


def utcnow() -> datetime:
    return datetime.now(timezone.utc)


@dataclass(frozen=True)
class WatchItem:
    symbol: str
    asset_class: str


@dataclass
class AutopilotJob:
    owner_id: int
    portfolio_id: int
    interval_seconds: int
    auto_execute: bool
    watchlist: list[WatchItem]
    use_report: bool = True  # Use MAIA report recommendations
    use_real_prices: bool = True  # Use real price feeds (fallback to simulation)
    min_confidence: float = 7.0  # Minimum confidence from report
    running: bool = True
    started_at: datetime = field(default_factory=utcnow)
    last_tick_at: datetime | None = None
    ticks_total: int = 0
    last_error: str | None = None
    report_last_read: datetime | None = None
    report_picks_count: int = 0
    history: dict[str, deque[float]] = field(default_factory=lambda: defaultdict(lambda: deque(maxlen=30)))
    stop_event: Event = field(default_factory=Event)
    thread: Thread | None = None


_JOBS: dict[tuple[int, int], AutopilotJob] = {}
_LOCK = Lock()


def _initial_price(symbol: str, asset_class: str) -> float:
    upper = symbol.upper()
    if upper in {"BTC", "ETH"} or asset_class.lower() == "crypto":
        return 60000.0 if upper == "BTC" else 3000.0
    return 100.0


def _next_price(previous: float, asset_class: str) -> float:
    volatility = 0.035 if asset_class.lower() == "crypto" else 0.012
    drift = random.uniform(-volatility, volatility)
    next_value = previous * (1 + drift)
    return max(0.01, round(next_value, 4))


def _get_current_price(symbol: str, asset_class: str, history: deque[float], use_real: bool) -> float:
    """Get current price from real feed or simulation."""
    if use_real:
        try:
            price_data = get_price(symbol, asset_class, use_simulation=True)
            return price_data.price
        except PriceFeedError:
            logger.warning(f"Price feed failed for {symbol}, using simulation")
    
    # Fallback to simulation with history tracking
    if not history:
        history.extend([_initial_price(symbol, asset_class), _initial_price(symbol, asset_class) * 1.001])
    history.append(_next_price(history[-1], asset_class))
    return history[-1]


def _run_tick(job: AutopilotJob, session_factory: sessionmaker[Session]) -> None:
    db = session_factory()
    try:
        portfolio = get_portfolio(db, portfolio_id=job.portfolio_id, owner_id=job.owner_id)
        if portfolio is None:
            job.last_error = "Portfolio not found"
            return

        positions = list_positions(db, portfolio_id=job.portfolio_id)
        
        # Calculate portfolio value for position sizing
        portfolio_value = float(portfolio.initial_cash)
        for pos in positions:
            portfolio_value += float(pos.quantity) * float(pos.avg_price)
        
        # Determine watchlist: from MAIA report or manual
        effective_watchlist = list(job.watchlist)
        
        if job.use_report:
            try:
                picks = get_picks(min_confidence=job.min_confidence, recommendation_filter="buy")
                if picks:
                    job.report_picks_count = len(picks)
                    job.report_last_read = utcnow()
                    # Add picks to watchlist (avoiding duplicates)
                    existing_symbols = {w.symbol.upper() for w in effective_watchlist}
                    for item in picks_to_watchlist(picks):
                        if item["symbol"].upper() not in existing_symbols:
                            effective_watchlist.append(WatchItem(symbol=item["symbol"], asset_class=item["asset_class"]))
                            existing_symbols.add(item["symbol"].upper())
            except Exception as e:
                logger.warning(f"Failed to read MAIA report: {e}")
        
        # Process each symbol
        for item in effective_watchlist:
            key = item.symbol.upper()
            history = job.history[key]
            
            # Get current price (real or simulated)
            current_price = _get_current_price(key, item.asset_class, history, job.use_real_prices)
            
            # Check if this symbol has a report recommendation
            report_pick = None
            if job.use_report:
                try:
                    picks = get_picks(min_confidence=job.min_confidence)
                    for p in picks:
                        if p.symbol.upper() == key:
                            report_pick = p
                            break
                except Exception:
                    pass
            
            if report_pick:
                # Use MAIA report recommendation
                signal_params = pick_to_signal_params(report_pick, current_price, portfolio_value)
            else:
                # Fall back to momentum-based signal
                if not history:
                    history.extend([current_price * 0.999, current_price])
                else:
                    history.append(current_price)
                prices = list(history)
                signal_params = suggest_trade_from_prices(
                    symbol=key,
                    asset_class=item.asset_class,
                    prices=prices,
                    current_positions=positions,
                )
            
            signal = create_ai_signal(
                db=db,
                portfolio_id=job.portfolio_id,
                symbol=str(signal_params["symbol"]),
                asset_class=str(signal_params["asset_class"]),
                side=str(signal_params["side"]),
                confidence=float(signal_params["confidence"]),
                reason=str(signal_params["reason"]),
                suggested_price=float(signal_params["suggested_price"]),
                suggested_quantity=float(signal_params["suggested_quantity"]),
            )

            if job.auto_execute and signal.side in {"buy", "sell"} and signal.suggested_quantity > 0:
                order = execute_paper_order(
                    db=db,
                    payload=OrderCreate(
                        portfolio_id=job.portfolio_id,
                        symbol=signal.symbol,
                        side=signal.side,
                        quantity=signal.suggested_quantity,
                        price=signal.suggested_price,
                        fee=0,
                        asset_class=signal.asset_class,
                        daily_realized_pnl=0,
                    ),
                    owner_id=job.owner_id,
                )
                mark_ai_signal_executed(db, signal_id=signal.id, order_id=order.order_id)

        job.last_tick_at = utcnow()
        job.ticks_total += 1
        job.last_error = None
    except Exception as e:
        job.last_error = str(e)
        logger.error(f"Autopilot tick error: {e}")
    finally:
        db.close()


def _worker(job: AutopilotJob, session_factory: sessionmaker[Session]) -> None:
    while not job.stop_event.is_set():
        _run_tick(job, session_factory)
        if job.stop_event.wait(job.interval_seconds):
            break
    job.running = False


def start_job(
    owner_id: int,
    portfolio_id: int,
    interval_seconds: int,
    auto_execute: bool,
    watchlist: list[WatchItem],
    session_factory: sessionmaker[Session],
    use_report: bool = True,
    use_real_prices: bool = True,
    min_confidence: float = 7.0,
) -> AutopilotJob:
    key = (owner_id, portfolio_id)
    with _LOCK:
        existing = _JOBS.get(key)
        if existing is not None and existing.running:
            raise ValueError("Autopilot already running for this portfolio")
        job = AutopilotJob(
            owner_id=owner_id,
            portfolio_id=portfolio_id,
            interval_seconds=interval_seconds,
            auto_execute=auto_execute,
            watchlist=watchlist,
            use_report=use_report,
            use_real_prices=use_real_prices,
            min_confidence=min_confidence,
        )
        thread = Thread(target=_worker, args=(job, session_factory), daemon=True, name=f"autopilot-{owner_id}-{portfolio_id}")
        job.thread = thread
        _JOBS[key] = job
        thread.start()
        return job


def stop_job(owner_id: int, portfolio_id: int) -> AutopilotJob | None:
    key = (owner_id, portfolio_id)
    with _LOCK:
        job = _JOBS.get(key)
    if job is None:
        return None
    job.stop_event.set()
    return job


def get_job(owner_id: int, portfolio_id: int) -> AutopilotJob | None:
    with _LOCK:
        return _JOBS.get((owner_id, portfolio_id))


def list_jobs(owner_id: int) -> list[AutopilotJob]:
    with _LOCK:
        return [job for (job_owner, _), job in _JOBS.items() if job_owner == owner_id]


def stop_all_jobs() -> None:
    with _LOCK:
        jobs = list(_JOBS.values())
    for job in jobs:
        job.stop_event.set()
