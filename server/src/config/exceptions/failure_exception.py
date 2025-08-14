import logging
import os
from datetime import datetime
from enum import Enum
from pathlib import Path
from typing import Any, Optional


class ExceptionType(Enum):
    NONE = "NONE"
    VALIDATION = "VALIDATION"
    DATABASE = "DATABASE"
    NETWORK = "NETWORK"
    UNKNOWN = "UNKNOWN"


class LogLevel(Enum):
    IGNORE = "IGNORE"
    INFO = "INFO"
    WARNING = "WARNING"
    ERROR = "ERROR"
    NOT_FOUND = "NOT_FOUND"


# Initialize logger
logger = logging.getLogger("Artaban")
logger.setLevel(logging.DEBUG)
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.DEBUG)
formatter = logging.Formatter("[%(asctime)s] [%(levelname)s] %(message)s")
console_handler.setFormatter(formatter)
logger.addHandler(console_handler)


class FailureException(Exception):
    def __init__(
        self,
        type: ExceptionType = ExceptionType.NONE,
        level: LogLevel = LogLevel.IGNORE,
        message: Optional[str] = None,
        userMessage: Optional[str] = None,
        error: Optional[Any] = None,
    ):
        self.type = type
        self.level = level
        self.message = message
        self.user_message = userMessage or ""
        self.error = error
        self._logException()

    @property
    def isActive(self) -> bool:
        return not (
            self.type == ExceptionType.NONE
            and self.level == LogLevel.IGNORE
            and self.message is None
        )

    @property
    def hasError(self) -> bool:
        return (
            self.level == LogLevel.ERROR
            and self.message is not None
            and self.error is not None
        )

    @property
    def justMessage(self) -> bool:
        return (
            self.level == LogLevel.IGNORE
            or self.message is not None
            or self.user_message != ""
        )

    def _logException(self):
        logMessage = self._buildLogMessage()
        self._writeLogToFile(logMessage)

        if self.level == LogLevel.INFO:
            logger.info(self.message or "")
        elif self.level == LogLevel.NOT_FOUND:
            logger.debug(self.message or "")
        elif self.level == LogLevel.IGNORE:
            logger.debug(self.message or "")
        elif self.level == LogLevel.WARNING:
            logger.warning(self.message or "")
        elif self.level == LogLevel.ERROR:
            if isinstance(self.error, Exception):
                logger.error(f"{type(self.error).__name__} => {str(self.error)}")
            else:
                logger.error(self.message or "")

    def _buildLogMessage(self) -> str:
        timestamp = datetime.utcnow().isoformat()
        log = f"[{timestamp}] [{self.level.name}] Type: {self.type.name}"
        if self.message:
            log += f" - Message: {self.message}"
        if self.user_message:
            log += f" - User Message: {self.user_message}"
        if self.error:
            log += f" - Error: {self.error}"
        return log

    def _writeLogToFile(self, log_message: str):
        try:
            log_dir = Path.home() / ".Artaban"
            log_dir.mkdir(parents=True, exist_ok=True)
            log_filename = f"Artaban_logs_{datetime.now().date()}.txt"
            log_path = log_dir / log_filename

            self._manageLogFiles(log_dir)

            with open(log_path, "a", encoding="utf-8") as f:
                f.write(log_message + "\n")

        except Exception as e:
            logger.info(f"Failed to write log to file: {e}")

    def _manageLogFiles(self, log_dir: Path):
        max_log_files = 5
        log_files = sorted(
            log_dir.glob("Artaban_logs_*.txt"), key=lambda f: f.stat().st_mtime
        )
        if len(log_files) >= max_log_files:
            for file in log_files[: len(log_files) - (max_log_files - 1)]:
                try:
                    file.unlink()
                except Exception as e:
                    logger.info(f"Failed to delete old log file {file}: {e}")

    def __str__(self):
        return (
            f"FailureException(type: {self.type.name}, level: {self.level.name}, "
            f"message: {self.message}, error: {self.error})"
        )

    def toDict(self) -> dict:
        return {
            "type": self.type.name,
            "level": self.level.name,
            "message": self.message,
            "user_message": self.user_message,
            "error": str(self.error) if self.error else None,
        }

    def toJson(self) -> dict:
        return self.toDict()

    def out(self) -> dict:
        return self.toDict()
