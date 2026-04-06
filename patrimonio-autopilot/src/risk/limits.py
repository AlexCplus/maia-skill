from dataclasses import dataclass
from pathlib import Path

import yaml


@dataclass(frozen=True)
class RiskLimits:
    max_daily_loss: float
    max_open_positions: int
    max_order_notional: float
    max_order_notional_by_asset_class: dict[str, float]
    max_order_notional_by_symbol: dict[str, float]
    kill_switch_enabled: bool


def load_risk_limits(project_root: Path) -> RiskLimits:
    limits_path = project_root / "config" / "risk.limits.yaml"
    with limits_path.open("r", encoding="utf-8") as fh:
        data = yaml.safe_load(fh) or {}
    risk_cfg = data.get("risk", {})
    return RiskLimits(
        max_daily_loss=float(risk_cfg.get("max_daily_loss", 0)),
        max_open_positions=int(risk_cfg.get("max_open_positions", 0)),
        max_order_notional=float(risk_cfg.get("max_order_notional", 0)),
        max_order_notional_by_asset_class={
            str(k).strip().lower(): float(v)
            for k, v in (risk_cfg.get("max_order_notional_by_asset_class", {}) or {}).items()
        },
        max_order_notional_by_symbol={
            str(k).strip().upper(): float(v)
            for k, v in (risk_cfg.get("max_order_notional_by_symbol", {}) or {}).items()
        },
        kill_switch_enabled=bool(risk_cfg.get("kill_switch_enabled", False)),
    )

