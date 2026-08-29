import os
from typing import List, Dict
from src.file_scanner import FileScanner
from src.corruption_detector import CorruptionDetector
from src.organizer import FileOrganizer
from src.virtual_filesystem import VirtualFileSystem
from src.logger import log_info, log_error

class OrganizationManager:
    """Manages the entire organization workflow"""
    
    def __init__(self, vfs_root: str = '.fileorganizer'):
        self.scanner = FileScanner()
        self.detector = CorruptionDetector()
        self.organizer = FileOrganizer()
        self.vfs = VirtualFileSystem(vfs_root)
        self.scanned_files = []
        self.corruption_results = {}
        self.categorization = {}
    
    def full_organization_workflow(self, directory: str, scan_corruption: bool = True) -> Dict:
        """Execute complete organization workflow"""
        workflow_results = {
            'scan': None,
            'corruption': None,
            'vfs_structure': None,
            'status': 'pending'
        }
        
        log_info(f"Starting full organization workflow for {directory}")
        
        try:
            # Step 1: Scan files
            log_info("Step 1: Scanning files...")
            self.scanned_files = self.scanner.scan_directory(directory, recursive=True)
            workflow_results['scan'] = {
                'total_files': len(self.scanned_files),
                'total_size': self.scanner.total_size
            }
            
            # Step 2: Check for corruption (optional)
            if scan_corruption:
                log_info("Step 2: Scanning for corruption...")
                self.corruption_results = self.detector.scan_files(self.scanned_files)
                workflow_results['corruption'] = self.corruption_results
            
            # Step 3: Categorize files
            log_info("Step 3: Categorizing files...")
            for file_info in self.scanned_files:
                file_path = file_info['path']
                category = self.organizer.categorize_file(file_path)
                self.categorization[file_path] = category
            
            # Step 4: Create virtual file structure
            log_info("Step 4: Creating virtual file structure...")
            vfs_result = self.vfs.create_virtual_structure(self.scanned_files, self.categorization)
            workflow_results['vfs_structure'] = vfs_result
            
            workflow_results['status'] = 'success'
            log_info("Full organization workflow completed successfully")
            
        except Exception as e:
            workflow_results['status'] = 'failed'
            workflow_results['error'] = str(e)
            log_error(f"Organization workflow failed: {e}")
        
        return workflow_results
    
    def get_vfs_view(self) -> Dict:
        """Get current virtual file system view"""
        return self.vfs.get_vfs_structure()
    
    def mirror_vfs_to_disk(self, destination: str, overwrite: bool = False) -> Dict:
        """Mirror virtual file system to physical disk"""
        log_info(f"Mirroring VFS to {destination}")
        return self.vfs.mirror_to_disk(destination, overwrite)
    
    def get_category_files(self, category: str) -> List[Dict]:
        """Get all files in a category"""
        files_in_category = []
        
        for file_info in self.scanned_files:
            if self.categorization.get(file_info['path']) == category:
                files_in_category.append(file_info)
        
        return files_in_category
    
    def get_statistics(self) -> Dict:
        """Get organization statistics"""
        stats = {
            'total_files': len(self.scanned_files),
            'total_size': self.scanner.total_size,
            'categories': {},
            'corruption': {
                'corrupted_count': len(self.detector.corrupted_files),
                'suspicious_count': len(self.detector.suspicious_files),
                'healthy_count': len(self.scanned_files) - len(self.detector.corrupted_files) - len(self.detector.suspicious_files)
            }
        }
        
        # Calculate per-category statistics
        category_sizes = {}
        for file_info in self.scanned_files:
            category = self.categorization.get(file_info['path'], 'Unknown')
            if category not in category_sizes:
                category_sizes[category] = {'count': 0, 'size': 0}
            category_sizes[category]['count'] += 1
            category_sizes[category]['size'] += file_info['size']
        
        stats['categories'] = category_sizes
        
        return stats
