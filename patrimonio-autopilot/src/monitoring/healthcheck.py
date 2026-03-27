import os
from pathlib import Path
from typing import Dict, List


REQUIRED_CONFIG_FILES = [
    "config/app.settings.yaml",
    "config/risk.limits.yaml",
    "config/alerts.yaml",
    "config/brokers/paper.yaml",
    "config/brokers/live.yaml",
]

REQUIRED_ENV_VARS = [
    "TELEGRAM_BOT_TOKEN",
    "TELEGRAM_CHAT_ID",
    "SMTP_HOST",
    "SMTP_PORT",
    "SMTP_USERNAME",
    "SMTP_PASSWORD",
    "SMTP_FROM",
    "SMTP_TO",
    "DB_URL",
]


def check_config_files(project_root: Path) -> List[Dict[str, str]]:
    results: List[Dict[str, str]] = []
    for relative_path in REQUIRED_CONFIG_FILES:
        full_path = project_root / relative_path
        exists = full_path.exists()
        results.append(
            {
                "name": relative_path,
                "status": "pass" if exists else "fail",
                "detail": "found" if exists else "missing",
            }
        )
    return results


def check_env_vars(env: Dict[str, str] = None) -> List[Dict[str, str]]:
    active_env = env if env is not None else dict(os.environ)
    results: List[Dict[str, str]] = []
    for key in REQUIRED_ENV_VARS:
        value = active_env.get(key, "")
        present = bool(str(value).strip())
        results.append(
            {
                "name": key,
                "status": "pass" if present else "fail",
                "detail": "set" if present else "missing",
            }
        )
    return results


def run_healthcheck(project_root: Path) -> Dict[str, object]:
    config_results = check_config_files(project_root)
    env_results = check_env_vars()
    combined = config_results + env_results
    passed = all(item["status"] == "pass" for item in combined)
    return {
        "passed": passed,
        "config": config_results,
        "env": env_results,
    }
