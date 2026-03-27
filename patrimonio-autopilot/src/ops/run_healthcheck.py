import argparse
import sys
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[2]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from src.monitoring.alerts import send_test_email_alert, send_test_telegram_alert
from src.monitoring.healthcheck import run_healthcheck


def main() -> int:
    parser = argparse.ArgumentParser(description="Run basic system healthcheck")
    parser.add_argument(
        "--test-alert",
        choices=["telegram", "email"],
        help="Trigger an alert plumbing test",
    )
    args = parser.parse_args()

    result = run_healthcheck(PROJECT_ROOT)
    total_config = len(result["config"])
    failed_config = sum(1 for x in result["config"] if x["status"] == "fail")
    total_env = len(result["env"])
    failed_env = sum(1 for x in result["env"] if x["status"] == "fail")

    print(f"Healthcheck: {'PASS' if result['passed'] else 'FAIL'}")
    print(f"Config files: {total_config - failed_config}/{total_config} ok")
    print(f"Env vars: {total_env - failed_env}/{total_env} ok")

    if failed_config:
        missing_cfg = [x["name"] for x in result["config"] if x["status"] == "fail"]
        print("Missing config:", ", ".join(missing_cfg))

    if failed_env:
        missing_env = [x["name"] for x in result["env"] if x["status"] == "fail"]
        print("Missing env:", ", ".join(missing_env))

    if args.test_alert:
        if args.test_alert == "telegram":
            alert_result = send_test_telegram_alert()
        else:
            alert_result = send_test_email_alert()
        print(f"Alert test ({args.test_alert}): {alert_result['status']} - {alert_result['detail']}")
        if alert_result["status"] != "pass":
            return 1

    return 0 if result["passed"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
