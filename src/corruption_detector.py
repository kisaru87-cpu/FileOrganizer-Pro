import os
import struct
import hashlib
from typing import List, Dict, Tuple
from src.logger import log_info, log_error, log_warning

class CorruptionDetector:
    """Detect corrupted or potentially corrupted files"""
    
    # File signatures (magic bytes)
    FILE_SIGNATURES = {
        '.pdf': b'%PDF',
        '.jpg': [b'\xff\xd8\xff', b'\xff\xd8\xff\xe0', b'\xff\xd8\xff\xe1'],
        '.png': b'\x89PNG',
        '.gif': [b'GIF87a', b'GIF89a'],
        '.zip': b'PK\x03\x04',
        '.rar': b'Rar!',
        '.7z': b'7z\xbc\xaf\x27\x1c',
        '.exe': b'MZ',
        '.mp3': b'ID3',
        '.mp4': None,  # Complex format
        '.avi': b'RIFF',
        '.wav': b'RIFF',
        '.bmp': b'BM',
        '.tar': None,  # Usually uncompressed
        '.gz': b'\x1f\x8b'
    }
    
    def __init__(self):
        self.corrupted_files = []
        self.suspicious_files = []
    
    def scan_files(self, files: List[Dict]) -> Dict:
        """Scan files for corruption"""
        log_info(f"Starting corruption scan for {len(files)} files")
        self.corrupted_files = []
        self.suspicious_files = []
        
        results = {
            'total_scanned': len(files),
            'corrupted': [],
            'suspicious': [],
            'healthy': 0
        }
        
        for file_info in files:
            file_path = file_info['path']
            
            # Check if file is readable
            if not file_info.get('readable', True):
                results['suspicious'].append({
                    'path': file_path,
                    'reason': 'File is not readable'
                })
                continue
            
            # Check file integrity
            integrity_issues = self._check_file_integrity(file_path)
            if integrity_issues['is_corrupted']:
                results['corrupted'].append({
                    'path': file_path,
                    'issues': integrity_issues['issues']
                })
                self.corrupted_files.append(file_path)
            elif integrity_issues['warnings']:
                results['suspicious'].append({
                    'path': file_path,
                    'reason': ', '.join(integrity_issues['warnings'])
                })
                self.suspicious_files.append(file_path)
            else:
                results['healthy'] += 1
        
        log_info(f"Corruption scan complete: {len(results['corrupted'])} corrupted, {len(results['suspicious'])} suspicious")
        return results
    
    def _check_file_integrity(self, file_path: str) -> Dict:
        """Check file integrity"""
        issues = {
            'is_corrupted': False,
            'issues': [],
            'warnings': []
        }
        
        try:
            # Check if file exists and is accessible
            if not os.path.exists(file_path):
                issues['is_corrupted'] = True
                issues['issues'].append('File does not exist')
                return issues
            
            # Check file size
            try:
                file_size = os.path.getsize(file_path)
                if file_size == 0:
                    issues['warnings'].append('File is empty')
            except OSError:
                issues['is_corrupted'] = True
                issues['issues'].append('Cannot read file size')
                return issues
            
            # Check file signature
            ext = os.path.splitext(file_path)[1].lower()
            if ext in self.FILE_SIGNATURES:
                signature_valid = self._check_file_signature(file_path, ext)
                if not signature_valid:
                    issues['is_corrupted'] = True
                    issues['issues'].append('Invalid file signature/header')
            
            # Try to read file
            try:
                with open(file_path, 'rb') as f:
                    # Try to read first chunk
                    chunk = f.read(1024)
                    if not chunk and file_size > 0:
                        issues['is_corrupted'] = True
                        issues['issues'].append('Cannot read file content')
            except (IOError, OSError):
                issues['is_corrupted'] = True
                issues['issues'].append('File access error')
                return issues
            
            # Check for suspicious characteristics
            if file_size > 5 * 1024 * 1024 * 1024:  # > 5GB
                issues['warnings'].append('Very large file size')
            
        except Exception as e:
            issues['is_corrupted'] = True
            issues['issues'].append(f'Unexpected error: {str(e)}')
        
        return issues
    
    def _check_file_signature(self, file_path: str, extension: str) -> bool:
        """Check file signature (magic bytes)"""
        signatures = self.FILE_SIGNATURES.get(extension)
        
        if signatures is None:
            return True  # Unknown format, assume valid
        
        if not isinstance(signatures, list):
            signatures = [signatures]
        
        try:
            with open(file_path, 'rb') as f:
                header = f.read(16)
                
                for sig in signatures:
                    if header.startswith(sig):
                        return True
                
                return False
        except (IOError, OSError):
            return False
    
    def get_corrupted_files(self) -> List[str]:
        """Get list of corrupted files"""
        return self.corrupted_files
    
    def get_suspicious_files(self) -> List[str]:
        """Get list of suspicious files"""
        return self.suspicious_files
