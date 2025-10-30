"""Logging configuration for the coffee machine application."""
import logging
import sys
from pathlib import Path
from logging.handlers import RotatingFileHandler
import structlog


class LoggerSetup:
    """Configure application logging with structured logging support."""
    
    @staticmethod
    def setup_logging(log_level: str = "INFO", log_to_file: bool = True):
        """
        Configure application logging.
        
        Args:
            log_level: Logging level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
            log_to_file: Whether to write logs to file
            
        Returns:
            Configured structlog logger
        """
        # Create logs directory
        log_dir = Path("logs")
        log_dir.mkdir(exist_ok=True)
        
        # Configure standard logging
        log_format = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
        
        handlers = [logging.StreamHandler(sys.stdout)]
        
        if log_to_file:
            file_handler = RotatingFileHandler(
                log_dir / "app.log",
                maxBytes=10_000_000,  # 10MB
                backupCount=5
            )
            file_handler.setFormatter(logging.Formatter(log_format))
            handlers.append(file_handler)
        
        logging.basicConfig(
            level=getattr(logging, log_level.upper()),
            format=log_format,
            handlers=handlers
        )
        
        # Configure structlog for structured logging
        structlog.configure(
            processors=[
                structlog.stdlib.filter_by_level,
                structlog.stdlib.add_logger_name,
                structlog.stdlib.add_log_level,
                structlog.stdlib.PositionalArgumentsFormatter(),
                structlog.processors.TimeStamper(fmt="iso"),
                structlog.processors.StackInfoRenderer(),
                structlog.processors.format_exc_info,
                structlog.processors.UnicodeDecoder(),
                structlog.processors.JSONRenderer()
            ],
            context_class=dict,
            logger_factory=structlog.stdlib.LoggerFactory(),
            cache_logger_on_first_use=True,
        )
        
        return structlog.get_logger()


# Initialize logger with default settings
logger = LoggerSetup.setup_logging()

