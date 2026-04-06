"""
MAIA Analysis Runner - Ejecuta los agentes de análisis y actualiza el report.

Este script invoca el skill de MAIA para generar un nuevo report_v2.json
con recomendaciones actualizadas del mercado.

Uso:
  python -m src.autopilot.run_analysis [--output OUTPUT_PATH]

El report generado es leído automáticamente por el autopilot si use_report=True.
"""
from __future__ import annotations

import argparse
import json
import os
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path


# Paths
PROJECT_ROOT = Path(__file__).parent.parent.parent.parent
DASHBOARD_DATA = PROJECT_ROOT / "dashboard" / "public" / "data"
DEFAULT_OUTPUT = DASHBOARD_DATA / "report_v2.json"
SKILL_PATH = PROJECT_ROOT / "SKILL.md"


def check_skill_exists() -> bool:
    """Verify MAIA skill file exists."""
    return SKILL_PATH.exists()


def run_maia_analysis(output_path: Path | None = None) -> dict:
    """
    Execute MAIA analysis skill.
    
    This requires the GitHub Copilot CLI to be available and configured.
    The skill reads market data and generates investment recommendations.
    
    Returns:
        Dict with execution result
    """
    output = output_path or DEFAULT_OUTPUT
    
    if not check_skill_exists():
        return {
            "success": False,
            "error": "SKILL.md not found. MAIA skill is not configured.",
        }
    
    # For now, return instructions since we can't auto-invoke the CLI
    return {
        "success": True,
        "message": "MAIA analysis ready to run",
        "instructions": [
            "To update the analysis report, run the MAIA skill using GitHub Copilot CLI:",
            "  copilot chat --skill maia-skill",
            "Or use VS Code with Copilot to invoke the skill.",
            f"The report will be saved to: {output}",
        ],
        "skill_path": str(SKILL_PATH),
        "output_path": str(output),
        "last_report": get_report_timestamp(output),
    }


def get_report_timestamp(path: Path) -> str | None:
    """Get the generation timestamp from existing report."""
    if not path.exists():
        return None
    try:
        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)
        return data.get("generated_at", "unknown")
    except Exception:
        return None


def create_manual_report_from_template() -> dict:
    """
    Create a basic report structure when no agent analysis is available.
    This provides a template that can be manually updated.
    """
    template = {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "model_used": "manual",
        "market_summary": {
            "summary_text": "Manual analysis template - please update with current market conditions",
            "key_events": [],
        },
        "risk_adjusted_picks": [
            {
                "rank": 1,
                "name": "Example Asset",
                "symbol": "EXAMPLE",
                "sector": "stocks",
                "confidence": 5,
                "risk_score": 5,
                "risk_adjusted_score": 5,
                "recommendation": "hold",
                "reasoning": "This is a template entry. Replace with real analysis.",
                "position_size": "5%",
            }
        ],
        "sector_analysis": {},
    }
    return template


def main():
    parser = argparse.ArgumentParser(description="Run MAIA market analysis")
    parser.add_argument(
        "--output",
        type=Path,
        default=DEFAULT_OUTPUT,
        help="Output path for report",
    )
    parser.add_argument(
        "--create-template",
        action="store_true",
        help="Create a template report for manual editing",
    )
    args = parser.parse_args()
    
    if args.create_template:
        template = create_manual_report_from_template()
        args.output.parent.mkdir(parents=True, exist_ok=True)
        with open(args.output, "w", encoding="utf-8") as f:
            json.dump(template, f, indent=2)
        print(f"Template created at: {args.output}")
        return
    
    result = run_maia_analysis(args.output)
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
