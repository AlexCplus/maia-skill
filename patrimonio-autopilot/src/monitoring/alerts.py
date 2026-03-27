import json
import os
import smtplib
import urllib.parse
import urllib.request
from email.message import EmailMessage
from typing import Dict


def _missing_env_error(var_name: str) -> Dict[str, str]:
    return {
        "status": "error",
        "detail": f"Missing required environment variable: {var_name}",
    }


def send_test_telegram_alert(message: str = "patrimonio-autopilot test alert") -> Dict[str, str]:
    bot_token = os.environ.get("TELEGRAM_BOT_TOKEN", "").strip()
    chat_id = os.environ.get("TELEGRAM_CHAT_ID", "").strip()

    if not bot_token:
        return _missing_env_error("TELEGRAM_BOT_TOKEN")
    if not chat_id:
        return _missing_env_error("TELEGRAM_CHAT_ID")

    payload = urllib.parse.urlencode({"chat_id": chat_id, "text": message}).encode("utf-8")
    url = f"https://api.telegram.org/bot{bot_token}/sendMessage"
    request = urllib.request.Request(url=url, data=payload, method="POST")
    with urllib.request.urlopen(request, timeout=10) as response:
        body = response.read().decode("utf-8")

    data = json.loads(body)
    if not data.get("ok", False):
        return {"status": "error", "detail": f"Telegram API error: {body}"}
    return {"status": "pass", "detail": "Telegram test alert sent"}


def send_test_email_alert(subject: str = "patrimonio-autopilot test alert", body: str = "This is a test alert.") -> Dict[str, str]:
    required = [
        "SMTP_HOST",
        "SMTP_PORT",
        "SMTP_USERNAME",
        "SMTP_PASSWORD",
        "SMTP_FROM",
        "SMTP_TO",
    ]
    values = {key: os.environ.get(key, "").strip() for key in required}
    for key, value in values.items():
        if not value:
            return _missing_env_error(key)

    msg = EmailMessage()
    msg["Subject"] = subject
    msg["From"] = values["SMTP_FROM"]
    msg["To"] = values["SMTP_TO"]
    msg.set_content(body)

    with smtplib.SMTP(values["SMTP_HOST"], int(values["SMTP_PORT"]), timeout=10) as server:
        server.starttls()
        server.login(values["SMTP_USERNAME"], values["SMTP_PASSWORD"])
        server.send_message(msg)

    return {"status": "pass", "detail": "Email test alert sent"}
