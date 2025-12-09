import logging
from logging import Logger
import os
from datetime import datetime

def generate_run_id() -> str:
    now = datetime.now()
    return now.strftime("%Y-%m-%d_%H-%M-%S-") + f"{int(now.microsecond/1000):03d}"


def create_logs_path(run_id: str) -> str:
    log_dir = os.path.join("logs", run_id)
    os.makedirs(log_dir, exist_ok=True)
    return log_dir

def get_log_path(logger: logging.Logger):
    paths = []
    for handler in logger.handlers:
        if isinstance(handler, logging.FileHandler):
            paths.append(handler.baseFilename)
    return paths[0]

def get_log_folder(logger: logging.Logger):
    return os.path.dirname(get_log_path(logger))

def init_device_logger(log_dir: str, device_serial: str) -> Logger:
    log_path = os.path.join(log_dir, f"{device_serial}.log")

    formatter = logging.Formatter(
        "%(asctime)s | %(levelname)-8s | %(name)s | %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S"
    )

    logger = logging.getLogger(device_serial)
    logger.setLevel(logging.DEBUG)

    for h in logger.handlers:
        if isinstance(h, logging.FileHandler) and h.baseFilename == log_path:
            return logger

    handler = logging.FileHandler(log_path)
    handler.setFormatter(formatter)
    logger.addHandler(handler)

    return logger
