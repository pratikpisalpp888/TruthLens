"""
TruthLens — Logging Configuration.

Configures structlog for JSON formatting, Request ID injection, and timing.
"""

import logging
import sys
import time
from typing import Any
import structlog
from fastapi import Request
from contextvars import ContextVar

from app.core.config import settings

request_id_var: ContextVar[str] = ContextVar("request_id", default="")
request_start_time_var: ContextVar[float] = ContextVar("request_start_time", default=0.0)

def add_request_context(logger: structlog.types.WrappedLogger, method_name: str, event_dict: structlog.types.EventDict) -> structlog.types.EventDict:
    """Injects request_id and performance timing into logs."""
    req_id = request_id_var.get()
    if req_id:
        event_dict["request_id"] = req_id
    
    start_time = request_start_time_var.get()
    if start_time:
        event_dict["elapsed_ms"] = round((time.time() - start_time) * 1000, 2)
        
    return event_dict

def configure_logging() -> None:
    """Configure structlog to output JSON with context."""
    log_level = getattr(logging, settings.LOG_LEVEL.upper(), logging.INFO)
    
    logging.basicConfig(
        format="%(message)s",
        stream=sys.stdout,
        level=log_level,
    )
    
    structlog.configure(
        processors=[
            structlog.contextvars.merge_contextvars,
            structlog.stdlib.add_log_level,
            structlog.stdlib.add_logger_name,
            structlog.processors.TimeStamper(fmt="iso"),
            add_request_context,
            structlog.processors.JSONRenderer(),
        ],
        wrapper_class=structlog.stdlib.BoundLogger,
        logger_factory=structlog.stdlib.LoggerFactory(),
        cache_logger_on_first_use=True,
    )
