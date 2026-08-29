import os
import json
import shutil
from pathlib import Path
from typing import List, Dict, Optional, Tuple
from datetime import datetime
from src.logger import log_info, log_error, log_warning
from src.utils import FileUtils

class VirtualFileSystem:
    """Virtual file system for organizing files without modifying the original structure"""
    
    def __init__(self, vfs_root: str = '.fileorganizer'):
        self.vfs_root = vfs_root
        self.file_index = {}  # Maps original path to VFS path
        self.category_structure = {}  # Category -> list of files
        self._initialize_vfs()
    
    def _initialize_vfs(self):
        """Initialize virtual file system"""
        os.makedirs(self.vfs_root, exist_ok=True)
        log_info(f"Virtual file system initialized at {self.vfs_root}")
    
    def create_virtual_structure(self, files: List[Dict], categorization: Dict[str, str]) -> Dict:
        """Create virtual file structure using symlinks/shortcuts without moving files"""
        results = {
            'total_files': len(files),
            'linked': 0,
            'failed': 0,
            'operations': []
        }
        
        # Clear existing virtual structure
        self._clear_vfs()
        
        for file_info in files:
            file_path = file_info['path']
            category = categorization.get(file_path, 'Other')
            
            # Create category folder in VFS
            category_dir = os.path.join(self.vfs_root, category)
            os.makedirs(category_dir, exist_ok=True)
            
            # Create symbolic link or shortcut
            vfs_link_path = os.path.join(category_dir, os.path.basename(file_path))
            
            operation = {
                'original': file_path,
                'vfs_link': vfs_link_path,
                'category': category,
                'status': 'pending'
            }
            
            try:
                # Handle duplicate filenames
                vfs_link_path = self._get_unique_vfs_path(vfs_link_path)
                
                # Create symlink (cross-platform)
                self._create_link(file_path, vfs_link_path)
                
                # Update indices
                self.file_index[file_path] = vfs_link_path
                if category not in self.category_structure:
                    self.category_structure[category] = []
                self.category_structure[category].append(file_path)
                
                operation['status'] = 'success'
                operation['vfs_link'] = vfs_link_path
                results['linked'] += 1
                log_info(f"Linked {file_path} -> {vfs_link_path}")
                
            except Exception as e:
                operation['status'] = 'failed'
                operation['error'] = str(e)
                results['failed'] += 1
                log_error(f"Failed to link {file_path}: {e}")
            
            results['operations'].append(operation)
        
        # Save index
        self._save_index()
        
        log_info(f"Virtual structure created: {results['linked']} linked, {results['failed']} failed")
        return results
    
    def _create_link(self, original_path: str, link_path: str):
        """Create a symbolic link or shortcut (cross-platform)"""
        original_path = os.path.abspath(original_path)
        
        if os.path.exists(link_path):
            os.remove(link_path)
        
        try:
            # Try symbolic link first (Unix/Linux/macOS and Windows 10+)
            os.symlink(original_path, link_path)
        except (OSError, NotImplementedError):
            # Fallback for Windows without admin privileges
            if os.name == 'nt':
                self._create_windows_shortcut(original_path, link_path)
            else:
                raise
    
    def _create_windows_shortcut(self, target: str, shortcut_path: str):
        """Create Windows .lnk shortcut file"""
        try:
            import win32com.client
            shell = win32com.client.Dispatch("WScript.Shell")
            
            # Remove .lnk if target doesn't have it, add it to shortcut path
            if not shortcut_path.endswith('.lnk'):
                shortcut_path += '.lnk'
            
            shortcut = shell.CreateShortCut(shortcut_path)
            shortcut.TargetPath = target
            shortcut.save()
        except ImportError:
            # If pywin32 not available, copy file metadata instead
            log_warning(f"Cannot create .lnk shortcut, using metadata copy instead")
            with open(shortcut_path + '.json', 'w') as f:
                json.dump({'target': target, 'type': 'reference'}, f)
    
    def _get_unique_vfs_path(self, path: str) -> str:
        """Get unique path if file already exists"""
        if not os.path.exists(path):
            return path
        
        base, ext = os.path.splitext(path)
        counter = 1
        
        while True:
            new_path = f"{base}_{counter}{ext}"
            if not os.path.exists(new_path):
                return new_path
            counter += 1
    
    def _clear_vfs(self):
        """Clear virtual file system"""
        if os.path.exists(self.vfs_root):
            for item in os.listdir(self.vfs_root):
                item_path = os.path.join(self.vfs_root, item)
                if os.path.isdir(item_path):
                    shutil.rmtree(item_path)
                else:
                    os.remove(item_path)
    
    def _save_index(self):
        """Save file index to disk"""
        index_file = os.path.join(self.vfs_root, '.index.json')
        try:
            with open(index_file, 'w') as f:
                json.dump({
                    'file_index': self.file_index,
                    'category_structure': self.category_structure,
                    'created_at': datetime.now().isoformat()
                }, f, indent=2)
        except IOError as e:
            log_error(f"Failed to save index: {e}")
    
    def _load_index(self):
        """Load file index from disk"""
        index_file = os.path.join(self.vfs_root, '.index.json')
        try:
            if os.path.exists(index_file):
                with open(index_file, 'r') as f:
                    data = json.load(f)
                    self.file_index = data.get('file_index', {})
                    self.category_structure = data.get('category_structure', {})
        except IOError as e:
            log_error(f"Failed to load index: {e}")
    
    def get_vfs_structure(self) -> Dict:
        """Get the current virtual file structure"""
        structure = {}
        
        if os.path.exists(self.vfs_root):
            for category in os.listdir(self.vfs_root):
                category_path = os.path.join(self.vfs_root, category)
                if os.path.isdir(category_path):
                    files = os.listdir(category_path)
                    structure[category] = {
                        'path': category_path,
                        'file_count': len(files),
                        'files': files
                    }
        
        return structure
    
    def mirror_to_disk(self, destination: str, overwrite: bool = False) -> Dict:
        """Mirror virtual file structure to actual disk by copying files"""
        results = {
            'total_files': 0,
            'copied': 0,
            'failed': 0,
            'operations': []
        }
        
        log_info(f"Mirroring virtual structure to {destination}")
        
        for category, file_list in self.category_structure.items():
            dest_category = os.path.join(destination, category)
            os.makedirs(dest_category, exist_ok=True)
            
            for original_file in file_list:
                results['total_files'] += 1
                
                if not os.path.exists(original_file):
                    log_warning(f"Original file not found: {original_file}")
                    continue
                
                dest_file = os.path.join(dest_category, os.path.basename(original_file))
                
                # Handle duplicates
                if os.path.exists(dest_file) and not overwrite:
                    dest_file = self._get_unique_vfs_path(dest_file)
                
                operation = {
                    'source': original_file,
                    'destination': dest_file,
                    'category': category,
                    'status': 'pending'
                }
                
                try:
                    shutil.copy2(original_file, dest_file)
                    operation['status'] = 'success'
                    results['copied'] += 1
                    log_info(f"Copied {original_file} -> {dest_file}")
                except Exception as e:
                    operation['status'] = 'failed'
                    operation['error'] = str(e)
                    results['failed'] += 1
                    log_error(f"Failed to copy {original_file}: {e}")
                
                results['operations'].append(operation)
        
        log_info(f"Mirror complete: {results['copied']} copied, {results['failed']} failed")
        return results
