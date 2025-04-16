# pipeline_debugger/logger.py

import logging

def init_logging(level: str = "INFO", log_file: str = None):
    """
    Initialize logging configuration. If log_file is provided, log to that file as well as console.
    """
    log_level = getattr(logging, level.upper(), logging.INFO)
    logging.basicConfig(level=log_level,
                        format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
                        datefmt="%Y-%m-%d %H:%M:%S")
    if log_file:
        file_handler = logging.FileHandler(log_file)
        file_handler.setLevel(log_level)
        file_formatter = logging.Formatter("%(asctime)s [%(levelname)s] %(name)s: %(message)s")
        file_handler.setFormatter(file_formatter)
        logging.getLogger().addHandler(file_handler)
