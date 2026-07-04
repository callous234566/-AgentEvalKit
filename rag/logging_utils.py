"""
项目日志配置工具。
"""

import logging
from contextvars import ContextVar
from logging.handlers import RotatingFileHandler
from pathlib import Path

import config

_REQUEST_ID: ContextVar[str] = ContextVar("request_id", default="-")
class RequestIdFilter(logging.Filter):
    """Attach the current request id to every log record."""

    def filter(self, record: logging.LogRecord) -> bool:
        record.request_id = get_request_id()
        return True


def set_request_id(value: str):
    """Set the current request id and return a token for reset."""
    return _REQUEST_ID.set(str(value or "-"))


def reset_request_id(token) -> None:
    """Reset request id context using the token returned by set_request_id."""
    _REQUEST_ID.reset(token)


def get_request_id() -> str:
    """Return the request id for the current logging context."""
    return _REQUEST_ID.get() or "-"


def _ensure_request_id_filter(handler: logging.Handler) -> None:
    if not any(isinstance(item, RequestIdFilter) for item in handler.filters):
        handler.addFilter(RequestIdFilter())


def _ensure_request_id_record_factory() -> None:
    current_factory = logging.getLogRecordFactory()
    if getattr(current_factory, "_rag_request_id_factory", False):
        return

    def record_factory(*args, **kwargs):
        record = current_factory(*args, **kwargs)
        record.request_id = get_request_id()
        return record

    record_factory._rag_request_id_factory = True
    logging.setLogRecordFactory(record_factory)


def setup_logging() -> None:
    """配置控制台日志和滚动文件日志。"""
    log_dir = Path(config.LOG_DIR)
    log_dir.mkdir(parents=True, exist_ok=True)
    log_path = log_dir / config.LOG_FILE

    formatter = logging.Formatter(
        "%(asctime)s - request_id=%(request_id)s - %(name)s - %(levelname)s - %(message)s"
    )
    root_logger = logging.getLogger()
    root_logger.setLevel(logging.INFO)
    _ensure_request_id_record_factory()

    if not any(isinstance(handler, logging.StreamHandler) for handler in root_logger.handlers):
        stream_handler = logging.StreamHandler()
        stream_handler.setFormatter(formatter)
        _ensure_request_id_filter(stream_handler)
        root_logger.addHandler(stream_handler)

    resolved_log_path = str(log_path.resolve())
    for handler in root_logger.handlers:
        _ensure_request_id_filter(handler)
        if isinstance(handler, RotatingFileHandler) and handler.baseFilename == resolved_log_path:
            handler.setFormatter(formatter)
            return

    file_handler = RotatingFileHandler(
        resolved_log_path,
        maxBytes=config.LOG_MAX_BYTES,
        backupCount=config.LOG_BACKUP_COUNT,
        encoding="utf-8",
    )
    file_handler.setFormatter(formatter)
    _ensure_request_id_filter(file_handler)
    root_logger.addHandler(file_handler)
