import os
import sys
from pathlib import Path
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QPushButton, QLabel, QLineEdit, QComboBox, QCheckBox, QTableWidget,
    QTableWidgetItem, QFileDialog, QMessageBox, QProgressBar, QTabWidget,
    QTreeWidget, QTreeWidgetItem, QSplitter, QSpinBox, QDialogButtonBox,
    QDialog
)
from PyQt6.QtCore import Qt, QThread, pyqtSignal, QSize
from PyQt6.QtGui import QIcon, QColor
from src.file_scanner import FileScanner
from src.corruption_detector import CorruptionDetector
from src.organizer import FileOrganizer
from src.organization_manager import OrganizationManager
from src.logger import log_info, log_error

class OrganizationThread(QThread):
    """Thread for full organization workflow"""
    progress = pyqtSignal(str)
    finished = pyqtSignal(dict)
    
    def __init__(self, directory, scan_corruption=True):
        super().__init__()
        self.directory = directory
        self.scan_corruption = scan_corruption
    
    def run(self):
        try:
            manager = OrganizationManager()
            self.progress.emit("Starting scan...")
            results = manager.full_organization_workflow(self.directory, self.scan_corruption)
            self.finished.emit(results)
        except Exception as e:
            self.finished.emit({'status': 'error', 'error': str(e)})

class MirrorThread(QThread):
    """Thread for mirroring VFS to disk"""
    progress = pyqtSignal(str)
    finished = pyqtSignal(dict)
    
    def __init__(self, manager, destination, overwrite=False):
        super().__init__()
        self.manager = manager
        self.destination = destination
        self.overwrite = overwrite
    
    def run(self):
        try:
            self.progress.emit(f"Mirroring to {self.destination}...")
            results = self.manager.mirror_vfs_to_disk(self.destination, self.overwrite)
            self.finished.emit(results)
        except Exception as e:
            self.finished.emit({'status': 'error', 'error': str(e)})

class FileOrganizerApp(QMainWindow):
    """Main application window with virtual file system support"""
    
    def __init__(self):
        super().__init__()
        self.setWindowTitle('FileOrganizer-Pro - Virtual File Manager')
        self.setGeometry(100, 100, 1400, 900)
        self.manager = OrganizationManager()
        self.init_ui()
    
    def init_ui(self):
        """Initialize user interface"""
        main_widget = QWidget()
        self.setCentralWidget(main_widget)
        
        layout = QVBoxLayout()
        
        # Tab widget
        tabs = QTabWidget()
        
        # Scanner & VFS tab
        scanner_tab = self.create_scanner_tab()
        tabs.addTab(scanner_tab, "Scanner & VFS")
        
        # Virtual File Manager tab
        vfs_tab = self.create_vfs_manager_tab()
        tabs.addTab(vfs_tab, "Virtual File Manager")
        
        # Mirror & Export tab
        mirror_tab = self.create_mirror_tab()
        tabs.addTab(mirror_tab, "Mirror to Disk")
        
        # Statistics tab
        stats_tab = self.create_statistics_tab()
        tabs.addTab(stats_tab, "Statistics")
        
        layout.addWidget(tabs)
        main_widget.setLayout(layout)
    
    def create_scanner_tab(self):
        """Create scanner and virtual file system creation tab"""
        tab = QWidget()
        layout = QVBoxLayout()
        
        # Directory selection
        dir_layout = QHBoxLayout()
        dir_layout.addWidget(QLabel("Source Directory:"))
        self.scanner_dir = QLineEdit()
        dir_layout.addWidget(self.scanner_dir)
        browse_btn = QPushButton("Browse")
        browse_btn.clicked.connect(self.browse_directory)
        dir_layout.addWidget(browse_btn)
        layout.addLayout(dir_layout)
        
        # Options
        options_layout = QHBoxLayout()
        self.corruption_check = QCheckBox("Scan for Corruption")
        self.corruption_check.setChecked(True)
        options_layout.addWidget(self.corruption_check)
        options_layout.addStretch()
        layout.addLayout(options_layout)
        
        # Scan button
        scan_btn = QPushButton("Create Virtual File Structure")
        scan_btn.setStyleSheet("background-color: #4CAF50; color: white; padding: 10px; font-weight: bold;")
        scan_btn.clicked.connect(self.start_organization)
        layout.addWidget(scan_btn)
        
        # Progress bar
        self.scan_progress = QProgressBar()
        layout.addWidget(self.scan_progress)
        
        # Status label
        self.status_label = QLabel("Ready to scan...")
        layout.addWidget(self.status_label)
        
        # Results table
        self.scanner_table = QTableWidget()
        self.scanner_table.setColumnCount(5)
        self.scanner_table.setHorizontalHeaderLabels(["Filename", "Size", "Extension", "Category", "Status"])
        layout.addWidget(self.scanner_table)
        
        tab.setLayout(layout)
        return tab
    
    def create_vfs_manager_tab(self):
        """Create virtual file manager tab"""
        tab = QWidget()
        layout = QVBoxLayout()
        
        # VFS Path display
        vfs_info_layout = QHBoxLayout()
        vfs_info_layout.addWidget(QLabel("Virtual File System Location:"))
        self.vfs_path_label = QLineEdit()
        self.vfs_path_label.setText(os.path.abspath('.fileorganizer'))
        self.vfs_path_label.setReadOnly(True)
        vfs_info_layout.addWidget(self.vfs_path_label)
        layout.addLayout(vfs_info_layout)
        
        # Refresh button
        refresh_btn = QPushButton("Refresh View")
        refresh_btn.clicked.connect(self.refresh_vfs_view)
        layout.addWidget(refresh_btn)
        
        # VFS Tree view
        self.vfs_tree = QTreeWidget()
        self.vfs_tree.setHeaderLabels(["Category", "Files", "Status"])
        layout.addWidget(self.vfs_tree)
        
        # Category details
        details_layout = QHBoxLayout()
        details_layout.addWidget(QLabel("Category Details:"))
        self.category_combo = QComboBox()
        self.category_combo.currentTextChanged.connect(self.on_category_selected)
        details_layout.addWidget(self.category_combo)
        layout.addLayout(details_layout)
        
        # Files in category
        self.category_files_table = QTableWidget()
        self.category_files_table.setColumnCount(4)
        self.category_files_table.setHorizontalHeaderLabels(["Filename", "Original Path", "Size", "Status"])
        layout.addWidget(self.category_files_table)
        
        tab.setLayout(layout)
        return tab
    
    def create_mirror_tab(self):
        """Create mirror to disk tab"""
        tab = QWidget()
        layout = QVBoxLayout()
        
        # Info box
        info_label = QLabel(
            "Mirror the virtual file structure to actual disk locations.\n"
            "This will COPY files to the destination while keeping originals intact."
        )
        info_label.setStyleSheet("background-color: #E3F2FD; padding: 10px; border-radius: 5px;")
        layout.addWidget(info_label)
        
        # Destination directory
        dest_layout = QHBoxLayout()
        dest_layout.addWidget(QLabel("Destination Directory:"))
        self.mirror_dest = QLineEdit()
        dest_layout.addWidget(self.mirror_dest)
        browse_dest_btn = QPushButton("Browse")
        browse_dest_btn.clicked.connect(self.browse_mirror_destination)
        dest_layout.addWidget(browse_dest_btn)
        layout.addLayout(dest_layout)
        
        # Options
        self.overwrite_check = QCheckBox("Overwrite Existing Files")
        self.overwrite_check.setChecked(False)
        layout.addWidget(self.overwrite_check)
        
        # Mirror button
        mirror_btn = QPushButton("Mirror Virtual Structure to Disk")
        mirror_btn.setStyleSheet("background-color: #2196F3; color: white; padding: 10px; font-weight: bold;")
        mirror_btn.clicked.connect(self.start_mirror)
        layout.addWidget(mirror_btn)
        
        # Progress bar
        self.mirror_progress = QProgressBar()
        layout.addWidget(self.mirror_progress)
        
        # Results table
        self.mirror_table = QTableWidget()
        self.mirror_table.setColumnCount(4)
        self.mirror_table.setHorizontalHeaderLabels(["Source File", "Destination", "Category", "Status"])
        layout.addWidget(self.mirror_table)
        
        tab.setLayout(layout)
        return tab
    
    def create_statistics_tab(self):
        """Create statistics tab"""
        tab = QWidget()
        layout = QVBoxLayout()
        
        # Overall statistics
        stats_layout = QHBoxLayout()
        
        # Total files
        self.total_files_label = QLabel("Total Files: 0")
        self.total_files_label.setStyleSheet("font-size: 12pt; font-weight: bold;")
        stats_layout.addWidget(self.total_files_label)
        
        # Total size
        self.total_size_label = QLabel("Total Size: 0 B")
        self.total_size_label.setStyleSheet("font-size: 12pt; font-weight: bold;")
        stats_layout.addWidget(self.total_size_label)
        
        # Corruption stats
        self.corruption_label = QLabel("Healthy: 0 | Suspicious: 0 | Corrupted: 0")
        self.corruption_label.setStyleSheet("font-size: 12pt; font-weight: bold;")
        stats_layout.addWidget(self.corruption_label)
        
        stats_layout.addStretch()
        layout.addLayout(stats_layout)
        
        # Category breakdown
        layout.addWidget(QLabel("Files by Category:"))
        self.stats_table = QTableWidget()
        self.stats_table.setColumnCount(4)
        self.stats_table.setHorizontalHeaderLabels(["Category", "File Count", "Total Size", "Percentage"])
        layout.addWidget(self.stats_table)
        
        tab.setLayout(layout)
        return tab
    
    def browse_directory(self):
        """Browse for directory"""
        directory = QFileDialog.getExistingDirectory(self, "Select Directory to Scan")
        if directory:
            self.scanner_dir.setText(directory)
    
    def browse_mirror_destination(self):
        """Browse for mirror destination"""
        directory = QFileDialog.getExistingDirectory(self, "Select Mirror Destination")
        if directory:
            self.mirror_dest.setText(directory)
    
    def start_organization(self):
        """Start full organization workflow"""
        directory = self.scanner_dir.text()
        if not directory or not os.path.isdir(directory):
            QMessageBox.warning(self, "Warning", "Please select a valid directory")
            return
        
        self.scan_progress.setValue(0)
        self.scanner_table.setRowCount(0)
        self.status_label.setText("Scanning and creating virtual structure...")
        
        self.org_thread = OrganizationThread(directory, self.corruption_check.isChecked())
        self.org_thread.progress.connect(self.on_progress_update)
        self.org_thread.finished.connect(self.on_organization_finished)
        self.org_thread.start()
    
    def on_progress_update(self, message):
        """Update progress message"""
        self.status_label.setText(message)
    
    def on_organization_finished(self, results):
        """Handle organization completion"""
        if results.get('status') == 'success':
            self.scan_progress.setValue(100)
            
            # Display VFS structure
            self.refresh_vfs_view()
            
            # Update statistics
            vfs_stats = self.manager.get_statistics()
            self.update_statistics_display(vfs_stats)
            
            scan_info = results.get('scan', {})
            msg = f"Virtual File Structure Created!\n\n" \
                  f"Total Files: {scan_info.get('total_files', 0)}\n" \
                  f"Operations: {results.get('vfs_structure', {}).get('linked', 0)} linked\n" \
                  f"Failed: {results.get('vfs_structure', {}).get('failed', 0)}"
            
            if results.get('corruption'):
                corrupt_info = results['corruption']
                msg += f"\n\nCorruption Scan:\n" \
                       f"Corrupted: {len(corrupt_info.get('corrupted', []))}\n" \
                       f"Suspicious: {len(corrupt_info.get('suspicious', []))}"
            
            QMessageBox.information(self, "Success", msg)
            self.status_label.setText("Virtual structure ready! Use 'Mirror to Disk' to export organized files.")
        else:
            QMessageBox.critical(self, "Error", f"Organization failed: {results.get('error')}")
    
    def refresh_vfs_view(self):
        """Refresh virtual file system view"""
        vfs_structure = self.manager.get_vfs_view()
        
        self.vfs_tree.clear()
        self.category_combo.clear()
        
        for category, cat_info in vfs_structure.items():
            item = QTreeWidgetItem([category, str(cat_info.get('file_count', 0)), "OK"])
            self.vfs_tree.addTopLevelItem(item)
            
            # Add files
            for file_name in cat_info.get('files', []):
                child = QTreeWidgetItem([file_name, "", "✓"])
                item.addChild(child)
            
            self.category_combo.addItem(category)
    
    def on_category_selected(self, category):
        """Handle category selection"""
        if not category:
            return
        
        files = self.manager.get_category_files(category)
        self.category_files_table.setRowCount(len(files))
        
        for row, file_info in enumerate(files):
            self.category_files_table.setItem(row, 0, QTableWidgetItem(file_info.get('name', 'N/A')))
            self.category_files_table.setItem(row, 1, QTableWidgetItem(file_info.get('path', 'N/A')))
            self.category_files_table.setItem(row, 2, QTableWidgetItem(self.format_size(file_info.get('size', 0))))
            self.category_files_table.setItem(row, 3, QTableWidgetItem("OK" if file_info.get('readable') else "Error"))
    
    def start_mirror(self):
        """Start mirroring to disk"""
        destination = self.mirror_dest.text()
        if not destination:
            QMessageBox.warning(self, "Warning", "Please select a destination directory")
            return
        
        if not os.path.isdir(destination):
            try:
                os.makedirs(destination, exist_ok=True)
            except Exception as e:
                QMessageBox.critical(self, "Error", f"Cannot create destination: {e}")
                return
        
        self.mirror_progress.setValue(0)
        self.mirror_table.setRowCount(0)
        
        self.mirror_thread = MirrorThread(self.manager, destination, self.overwrite_check.isChecked())
        self.mirror_thread.progress.connect(self.on_progress_update)
        self.mirror_thread.finished.connect(self.on_mirror_finished)
        self.mirror_thread.start()
    
    def on_mirror_finished(self, results):
        """Handle mirror completion"""
        self.mirror_progress.setValue(100)
        
        # Display results
        self.mirror_table.setRowCount(len(results.get('operations', [])))
        
        for row, op in enumerate(results.get('operations', [])):
            self.mirror_table.setItem(row, 0, QTableWidgetItem(op.get('source', 'N/A')))
            self.mirror_table.setItem(row, 1, QTableWidgetItem(op.get('destination', 'N/A')))
            self.mirror_table.setItem(row, 2, QTableWidgetItem(op.get('category', 'N/A')))
            status = op.get('status', 'unknown').upper()
            status_color = QColor('#4CAF50') if status == 'SUCCESS' else QColor('#F44336')
            item = QTableWidgetItem(status)
            item.setBackground(status_color)
            self.mirror_table.setItem(row, 3, item)
        
        msg = f"Mirror Complete!\n\n" \
              f"Total Files: {results.get('total_files', 0)}\n" \
              f"Copied: {results.get('copied', 0)}\n" \
              f"Failed: {results.get('failed', 0)}"
        
        QMessageBox.information(self, "Mirror Complete", msg)
    
    def update_statistics_display(self, stats):
        """Update statistics display"""
        # Overall statistics
        self.total_files_label.setText(f"Total Files: {stats.get('total_files', 0)}")
        self.total_size_label.setText(f"Total Size: {self.format_size(stats.get('total_size', 0))}")
        
        # Corruption statistics
        corruption = stats.get('corruption', {})
        self.corruption_label.setText(
            f"Healthy: {corruption.get('healthy_count', 0)} | "
            f"Suspicious: {corruption.get('suspicious_count', 0)} | "
            f"Corrupted: {corruption.get('corrupted_count', 0)}"
        )
        
        # Category breakdown
        categories = stats.get('categories', {})
        self.stats_table.setRowCount(len(categories))
        
        total_size = stats.get('total_size', 1)  # Avoid division by zero
        
        for row, (category, cat_stats) in enumerate(categories.items()):
            count = cat_stats.get('count', 0)
            size = cat_stats.get('size', 0)
            percentage = (size / total_size * 100) if total_size > 0 else 0
            
            self.stats_table.setItem(row, 0, QTableWidgetItem(category))
            self.stats_table.setItem(row, 1, QTableWidgetItem(str(count)))
            self.stats_table.setItem(row, 2, QTableWidgetItem(self.format_size(size)))
            self.stats_table.setItem(row, 3, QTableWidgetItem(f"{percentage:.1f}%"))
    
    @staticmethod
    def format_size(size):
        """Format file size"""
        for unit in ['B', 'KB', 'MB', 'GB']:
            if size < 1024:
                return f"{size:.2f} {unit}"
            size /= 1024
        return f"{size:.2f} TB"

def main():
    app = QApplication(sys.argv)
    window = FileOrganizerApp()
    window.show()
    sys.exit(app.exec())

if __name__ == '__main__':
    main()
