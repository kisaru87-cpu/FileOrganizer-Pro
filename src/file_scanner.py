import os
import json
from pathlib import Path
from typing import List, Dict, Generator
from tqdm import tqdm
from src.logger import log_info, log_error, log_warning

class FileScanner:
    """Scan directories for files"""
    
    def __init__(self, max_file_size=None):
        self.max_file_size = max_file_size
        self.files_found = []
        self.total_size = 0
    
    def scan_directory(self, directory: str, recursive: bool = True, extensions: List[str] = None) -> List[Dict]:
        """Scan directory for files"""
        if not os.path.isdir(directory):
            log_error(f"Invalid directory: {directory}")
            return []
        
        log_info(f"Starting scan of directory: {directory}")
        self.files_found = []
        self.total_size = 0
        
        if recursive:
            for root, dirs, files in os.walk(directory):
                for file in files:
                    file_path = os.path.join(root, file)
                    if extensions is None or self._has_valid_extension(file_path, extensions):
                        file_info = self._get_file_info(file_path)
                        if file_info:
                            self.files_found.append(file_info)
                            self.total_size += file_info['size']
        else:
            for file in os.listdir(directory):
                file_path = os.path.join(directory, file)
                if os.path.isfile(file_path):
                    if extensions is None or self._has_valid_extension(file_path, extensions):
                        file_info = self._get_file_info(file_path)
                        if file_info:
                            self.files_found.append(file_info)
                            self.total_size += file_info['size']
        
        log_info(f"Scan complete: Found {len(self.files_found)} files, Total size: {self._format_size(self.total_size)}")
        return self.files_found
    
    def _get_file_info(self, file_path: str) -> Dict:
        """Get file information"""
        try:
            stat = os.stat(file_path)
            return {
                'path': file_path,
                'name': os.path.basename(file_path),
                'extension': os.path.splitext(file_path)[1].lower(),
                'size': stat.st_size,
                'created': stat.st_ctime,
                'modified': stat.st_mtime,
                'readable': os.access(file_path, os.R_OK)
            }
        except (OSError, IOError) as e:
            log_warning(f"Could not access file {file_path}: {e}")
            return None
    
    def _has_valid_extension(self, file_path: str, extensions: List[str]) -> bool:
        """Check if file has valid extension"""
        ext = os.path.splitext(file_path)[1].lower()
        return ext in extensions
    
    def _format_size(self, size: int) -> str:
        """Format file size to human readable format"""
        for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
            if size < 1024:
                return f"{size:.2f} {unit}"
            size /= 1024
        return f"{size:.2f} PB"
    
    def get_summary(self) -> Dict:
        """Get scan summary"""
        return {
            'total_files': len(self.files_found),
            'total_size': self.total_size,
            'formatted_size': self._format_size(self.total_size),
            'files': self.files_found
        }
