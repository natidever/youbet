import logging
import sys
from logging.handlers import RotatingFileHandler
from pathlib import Path
import json
from datetime import datetime

# Log directory setup
LOG_DIR = Path("logs")
# LOG_DIR.mkdir(exist_ok=True)

# Current timestamp for log filename
CURRENT_TIME = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
# LOG_FILE = LOG_DIR / f"app_{CURRENT_TIME}.log"

# JSON formatter for structured logging
class JSONFormatter(logging.Formatter):
    def format(self, record):
        log_record = {
            "timestamp": datetime.now().isoformat(),
            "level": record.levelname,
            "message": record.getMessage(),
            "module": record.module,
            "function": record.funcName,
            "line": record.lineno,
        }
        if record.exc_info:
            log_record["exception"] = self.formatException(record.exc_info)
        return json.dumps(log_record)

# Configure the root logger
def setup_logging():
    logger = logging.getLogger()  # Root logger
    logger.setLevel(logging.INFO)  # Default log level

    # Console Handler (for development)
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(logging.DEBUG)
    console_formatter = logging.Formatter(
        "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    )
    console_handler.setFormatter(console_formatter)
    logger.addHandler(console_handler)

    # File Handler (for production)
    # file_handler = RotatingFileHandler(
    #     # LOG_FILE,
    #     maxBytes=10 * 1024 * 1024,  # 10 MB per file
    #     backupCount=5,  # Keep 5 backup logs
    #     encoding="utf-8",
    # )
    # file_handler.setLevel(logging.INFO)
    # file_handler.setFormatter(JSONFormatter())  # Structured logs
    # logger.addHandler(file_handler)

    # Suppress noisy library logs
    logging.getLogger("uvicorn").setLevel(logging.WARNING)
    logging.getLogger("sqlalchemy").setLevel(logging.ERROR)

    return logger

# Initialize logging when imported
logger = setup_logging()