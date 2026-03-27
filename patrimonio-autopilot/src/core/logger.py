import json
import logging
import sys
from datetime import datetime, timezone
from typing import Any, Dict, Optional


class JsonFormatter(logging.Formatter):
    def format(self, record: logging.LogRecord) -> str:
        payload: Dict[str, Any] = {
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "level": record.levelname,
            "message": record.getMessage(),
            "correlation_id": getattr(record, "correlation_id", None),
            "component": getattr(record, "component", record.name),
        }

        extra_fields = getattr(record, "extra_fields", None)
        if isinstance(extra_fields, dict):
            payload.update(extra_fields)

        return json.dumps(payload, ensure_ascii=True)


def get_logger(name: str, component: Optional[str] = None) -> logging.Logger:
    logger = logging.getLogger(name)
    if not logger.handlers:
        handler = logging.StreamHandler(sys.stdout)
        handler.setFormatter(JsonFormatter())
        logger.addHandler(handler)
        logger.setLevel(logging.INFO)
        logger.propagate = False

    if component:
        logger = logging.LoggerAdapter(logger, {"component": component})  # type: ignore[assignment]
    return logger


def log_event(
    logger: logging.Logger,
    level: str,
    message: str,
    correlation_id: str,
    component: str,
    **extra_fields: Any,
) -> None:
    logger.log(
        getattr(logging, level.upper(), logging.INFO),
        message,
        extra={
            "correlation_id": correlation_id,
            "component": component,
            "extra_fields": extra_fields,
        },
    )
