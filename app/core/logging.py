import logging
import os
from logging.handlers import RotatingFileHandler
from typing import Optional

def setup_logger(
    name: str = "app",
    log_level: int = logging.INFO,
    log_file: Optional[str] = "app.log",
    max_bytes: int = 1024 * 1024,  # 1MB
    backup_count: int = 5
) -> logging.Logger:
    """
    Configure and return a logger instance with both console and file handlers.
    
    Args:
        name: Logger name
        log_level: Logging level (default: INFO)
        log_file: Log file path (default: app.log)
        max_bytes: Maximum size of log file before rotation
        backup_count: Number of backup files to keep
    
    Returns:
        Configured logger instance
    """
    # Create logger
    logger = logging.getLogger(name)
    logger.setLevel(log_level)
    
    # Prevent adding handlers multiple times
    if logger.handlers:
        return logger
        
    # Create formatters
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    
    # Console handler
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)
    
    # File handler (if log_file is specified)
    if log_file:
        # Ensure log directory exists
        log_dir = os.path.dirname(log_file)
        if log_dir and not os.path.exists(log_dir):
            os.makedirs(log_dir)
            
        file_handler = RotatingFileHandler(
            log_file,
            maxBytes=max_bytes,
            backupCount=backup_count
        )
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)
    
    return logger

# Default logger instance
logger = setup_logger()

