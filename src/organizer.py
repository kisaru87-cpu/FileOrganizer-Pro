import os
import json
import shutil
from pathlib import Path
from typing import List, Dict
from src.logger import log_info, log_error, log_warning
from src.utils import FileUtils

class FileOrganizer:
    """Organize files into categories"""
    
    def __init__(self, file_types_config: str = 'config/file_types.json'):
        self.file_types = self._load_file_types(file_types_config)
        self.organization_log = []
    
    def _load_file_types(self, config_file: str) -> Dict:
        """Load file type configuration"""
        try:
            with open(config_file, 'r') as f:
                return json.load(f)
        except (IOError, json.JSONDecodeError):
            log_error(f"Could not load file types config: {config_file}")
            return {}
    
    def categorize_file(self, file_path: str) -> str:
        """Categorize a file based on extension"""
        ext = FileUtils.get_file_extension(file_path)
        
        for category, data in self.file_types.items():
            if ext in data.get('extensions', []):
                return category
        
        return 'Other'
    
    def organize_files(self, files: List[Dict], base_directory: str, dry_run: bool = True, move: bool = True) -> Dict:
        """Organize files into category folders"""
        log_info(f"Starting file organization (dry_run={dry_run})")
        
        results = {
            'total_files': len(files),
            'organized': 0,
            'failed': 0,
            'skipped': 0,
            'operations': []
        }
        
        for file_info in files:
            file_path = file_info['path']
            category = self.categorize_file(file_path)
            
            # Create destination path
            dest_dir = os.path.join(base_directory, category)
            dest_path = os.path.join(dest_dir, os.path.basename(file_path))
            
            # Handle file already in correct location
            if os.path.dirname(file_path) == dest_dir:
                results['skipped'] += 1
                continue
            
            # Handle duplicate files
            if os.path.exists(dest_path):
                dest_path = self._generate_unique_filename(dest_path)
            
            # Log operation
            operation = {
                'source': file_path,
                'destination': dest_path,
                'category': category,
                'status': 'pending'
            }
            
            if not dry_run:
                # Perform the actual operation
                if move:
                    success = FileUtils.safe_move_file(file_path, dest_path)
                else:
                    success = FileUtils.safe_copy_file(file_path, dest_path)
                
                if success:
                    operation['status'] = 'success'
                    results['organized'] += 1
                    log_info(f"{'Moved' if move else 'Copied'} {file_path} -> {dest_path}")
                else:
                    operation['status'] = 'failed'
                    results['failed'] += 1
                    log_error(f"Failed to {'move' if move else 'copy'} {file_path}")
            else:
                operation['status'] = 'preview'
                results['organized'] += 1
            
            results['operations'].append(operation)
        
        log_info(f"Organization complete: {results['organized']} organized, {results['failed']} failed")
        return results
    
    def _generate_unique_filename(self, file_path: str) -> str:
        """Generate unique filename if file already exists"""
        if not os.path.exists(file_path):
            return file_path
        
        base, ext = os.path.splitext(file_path)
        directory = os.path.dirname(file_path)
        counter = 1
        
        while True:
            new_path = os.path.join(directory, f"{base}_{counter}{ext}")
            if not os.path.exists(new_path):
                return new_path
            counter += 1
    
    def get_organization_log(self) -> List[Dict]:
        """Get organization log"""
        return self.organization_log
