import logging
import os
from logging.handlers import RotatingFileHandler
import json

class Logger:
    """Centralized logging configuration"""
    
    def __init__(self, log_file='logs/fileorganizer.log', level=logging.INFO):
        self.log_file = log_file
        self.level = level
        self.logger = self._setup_logger()
    
    def _setup_logger(self):
        """Configure logging with file and console handlers"""
        os.makedirs(os.path.dirname(self.log_file), exist_ok=True)
        
        logger = logging.getLogger('FileOrganizer')
        logger.setLevel(self.level)
        
        # File handler with rotation
        file_handler = RotatingFileHandler(
            self.log_file,
            maxBytes=10*1024*1024,  # 10MB
            backupCount=5
        )
        file_handler.setLevel(self.level)
        
        # Console handler
        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.INFO)
        
        # Formatter
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        file_handler.setFormatter(formatter)
        console_handler.setFormatter(formatter)
        
        logger.addHandler(file_handler)
        logger.addHandler(console_handler)
        
        return logger
    
    def get_logger(self):
        return self.logger

# Global logger instance
_logger_instance = Logger().get_logger()

def log_info(message):
    _logger_instance.info(message)

def log_error(message):
    _logger_instance.error(message)

def log_warning(message):
    _logger_instance.warning(message)

def log_debug(message):
    _logger_instance.debug(message)
