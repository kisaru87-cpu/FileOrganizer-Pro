import os
import json
import hashlib
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Tuple

class FileUtils:
    """Utility functions for file operations"""
    
    @staticmethod
    def get_file_size(file_path: str) -> int:
        """Get file size in bytes"""
        try:
            return os.path.getsize(file_path)
        except OSError:
            return 0
    
    @staticmethod
    def get_file_extension(file_path: str) -> str:
        """Get file extension"""
        return os.path.splitext(file_path)[1].lower()
    
    @staticmethod
    def get_file_creation_date(file_path: str) -> datetime:
        """Get file creation date"""
        try:
            timestamp = os.path.getctime(file_path)
            return datetime.fromtimestamp(timestamp)
        except OSError:
            return None
    
    @staticmethod
    def get_file_modification_date(file_path: str) -> datetime:
        """Get file modification date"""
        try:
            timestamp = os.path.getmtime(file_path)
            return datetime.fromtimestamp(timestamp)
        except OSError:
            return None
    
    @staticmethod
    def calculate_file_hash(file_path: str, algorithm='sha256') -> str:
        """Calculate file hash (MD5, SHA1, SHA256)"""
        hash_func = hashlib.new(algorithm)
        try:
            with open(file_path, 'rb') as f:
                for chunk in iter(lambda: f.read(4096), b''):
                    hash_func.update(chunk)
            return hash_func.hexdigest()
        except (IOError, OSError):
            return None
    
    @staticmethod
    def is_file_readable(file_path: str) -> bool:
        """Check if file is readable"""
        return os.access(file_path, os.R_OK)
    
    @staticmethod
    def is_file_writable(file_path: str) -> bool:
        """Check if file is writable"""
        return os.access(file_path, os.W_OK)
    
    @staticmethod
    def safe_move_file(source: str, destination: str, overwrite=False) -> bool:
        """Safely move a file"""
        try:
            if os.path.exists(destination) and not overwrite:
                return False
            
            os.makedirs(os.path.dirname(destination), exist_ok=True)
            os.rename(source, destination)
            return True
        except (OSError, IOError):
            return False
    
    @staticmethod
    def safe_copy_file(source: str, destination: str, overwrite=False) -> bool:
        """Safely copy a file"""
        try:
            if os.path.exists(destination) and not overwrite:
                return False
            
            os.makedirs(os.path.dirname(destination), exist_ok=True)
            with open(source, 'rb') as src, open(destination, 'wb') as dst:
                dst.write(src.read())
            return True
        except (OSError, IOError):
            return False

class ConfigManager:
    """Manage application configuration"""
    
    def __init__(self, config_file='config/settings.json'):
        self.config_file = config_file
        self.config = self._load_config()
    
    def _load_config(self) -> Dict:
        """Load configuration from JSON file"""
        try:
            with open(self.config_file, 'r') as f:
                return json.load(f)
        except (IOError, json.JSONDecodeError):
            return {}
    
    def get(self, key: str, default=None):
        """Get configuration value"""
        keys = key.split('.')
        value = self.config
        for k in keys:
            if isinstance(value, dict):
                value = value.get(k)
            else:
                return default
        return value if value is not None else default
    
    def set(self, key: str, value):
        """Set configuration value"""
        keys = key.split('.')
        config = self.config
        for k in keys[:-1]:
            if k not in config:
                config[k] = {}
            config = config[k]
        config[keys[-1]] = value
    
    def save(self):
        """Save configuration to file"""
        try:
            with open(self.config_file, 'w') as f:
                json.dump(self.config, f, indent=2)
            return True
        except IOError:
            return False
