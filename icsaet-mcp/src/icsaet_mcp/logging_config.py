"""Logging configuration for the MCP server."""

import atexit
import logging
import logging.handlers
import os
import queue
import sys
from pathlib import Path


def setup_logging():
    """Configure async logging with stderr output and optional file logging."""
    log_level_str = os.getenv("ICAET_LOG_LEVEL", "INFO").upper()
    log_level = getattr(logging, log_level_str, logging.INFO)
    
    log_format = "%(asctime)s %(levelname)s %(message)s"
    formatter = logging.Formatter(log_format, datefmt="%Y-%m-%d %H:%M:%S")
    
    stderr_handler = logging.StreamHandler(sys.stderr)
    stderr_handler.setFormatter(formatter)
    stderr_handler.setLevel(log_level)
    
    handlers = [stderr_handler]
    
    try:
        log_dir = Path.home() / ".icsaet-mcp" / "logs"
        log_dir.mkdir(parents=True, exist_ok=True)
        log_file = log_dir / "server.log"
        
        file_handler = logging.handlers.RotatingFileHandler(
            log_file, 
            maxBytes=10*1024*1024, 
            backupCount=5
        )
        file_handler.setFormatter(formatter)
        file_handler.setLevel(log_level)
        handlers.append(file_handler)
    except Exception:
        pass
    
    log_queue = queue.Queue(-1)
    queue_handler = logging.handlers.QueueHandler(log_queue)
    
    listener = logging.handlers.QueueListener(
        log_queue, 
        *handlers, 
        respect_handler_level=True
    )
    listener.start()
    atexit.register(listener.stop)
    
    logger = logging.getLogger()
    logger.setLevel(log_level)
    logger.addHandler(queue_handler)
    
    return logger

