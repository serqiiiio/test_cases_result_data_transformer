import logging
import os
from datetime import datetime
import sys


def setup_logger(name: str = __name__) -> logging.Logger:
    """
    Creates a configured logger instance with logs directory in parent directory

    Args:
        name: Logger name (usually __name__)

    Returns:
        Configured Logger instance
    """
    logger = logging.getLogger(name)

    if not logger.hasHandlers():
        logger.setLevel(logging.DEBUG)

        current_dir = os.path.dirname(os.path.abspath(__file__))
        parent_dir = os.path.dirname(current_dir)
        log_dir = os.path.join(parent_dir, "logs")
        os.makedirs(log_dir, exist_ok=True)

        # Create formatters
        console_format = logging.Formatter(
            "%(asctime)s | %(levelname)-8s | %(filename)s:%(lineno)d | %(message)s",
            datefmt="%H:%M:%S"
        )

        file_format = logging.Formatter(
            "%(asctime)s | %(levelname)-8s | %(name)s | %(filename)s:%(lineno)d | %(funcName)s | %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S"
        )

        # Console handler (warnings and above)
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setLevel(logging.WARNING)
        console_handler.setFormatter(console_format)

        # File handler (all debug messages)
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        log_file = os.path.join(log_dir, f"{timestamp}.log")
        file_handler = logging.FileHandler(log_file)
        file_handler.setLevel(logging.DEBUG)
        file_handler.setFormatter(file_format)

        # Add handlers
        logger.addHandler(console_handler)
        logger.addHandler(file_handler)

        logger.info(f"Logger initialized. Log file: {log_file}")

    return logger


if __name__ == "__main__":
    logger = setup_logger(__name__)

    logger.debug("This is a debug message (only in file)")
    logger.info("Process started")
    logger.warning("This is a warning (console and file)")
    logger.error("An error occurred!", exc_info=True)
    logger.critical("Critical failure!")

    try:
        1 / 0
    except ZeroDivisionError:
        logger.exception("Exception example:")