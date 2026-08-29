import os
import sys
from pathlib import Path
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QPushButton, QLabel, QLineEdit, QComboBox, QCheckBox, QTableWidget,
    QTableWidgetItem, QFileDialog, QMessageBox, QProgressBar, QTabWidget
)
from PyQt6.QtCore import Qt, QThread, pyqtSignal
from src.file_scanner import FileScanner
from src.corruption_detector import CorruptionDetector
from src.organizer import FileOrganizer
from src.logger import log_info, log_error

class ScannerThread(QThread):
    """Thread for file scanning operations"""
    progress = pyqtSignal(int)
    finished = pyqtSignal(list)
    
    def __init__(self, directory, recursive=True):
        super().__init__()
        self.directory = directory
        self.recursive = recursive
    
    def run(self):
        scanner = FileScanner()
        files = scanner.scan_directory(self.directory, self.recursive)
        self.finished.emit(files)

class CorruptionScanThread(QThread):
    """Thread for corruption scanning"""
    progress = pyqtSignal(int)
    finished = pyqtSignal(dict)
    
    def __init__(self, files):
        super().__init__()
        self.files = files
    
    def run(self):
        detector = CorruptionDetector()
        results = detector.scan_files(self.files)
        self.finished.emit(results)

class FileOrganizerApp(QMainWindow):
    """Main application window"""
    
    def __init__(self):
        super().__init__()
        self.setWindowTitle('FileOrganizer-Pro')
        self.setGeometry(100, 100, 1200, 800)
        self.scanned_files = []
        self.init_ui()
    
    def init_ui(self):
        """Initialize user interface"""
        main_widget = QWidget()
        self.setCentralWidget(main_widget)
        
        layout = QVBoxLayout()
        
        # Tab widget
        tabs = QTabWidget()
        
        # Scanner tab
        scanner_tab = self.create_scanner_tab()
        tabs.addTab(scanner_tab, "File Scanner")
        
        # Corruption tab
        corruption_tab = self.create_corruption_tab()
        tabs.addTab(corruption_tab, "Corruption Detector")
        
        # Organizer tab
        organizer_tab = self.create_organizer_tab()
        tabs.addTab(organizer_tab, "File Organizer")
        
        layout.addWidget(tabs)
        main_widget.setLayout(layout)
    
    def create_scanner_tab(self):
        """Create file scanner tab"""
        tab = QWidget()
        layout = QVBoxLayout()
        
        # Directory selection
        dir_layout = QHBoxLayout()
        dir_layout.addWidget(QLabel("Directory:"))
        self.scanner_dir = QLineEdit()
        dir_layout.addWidget(self.scanner_dir)
        browse_btn = QPushButton("Browse")
        browse_btn.clicked.connect(self.browse_directory)
        dir_layout.addWidget(browse_btn)
        layout.addLayout(dir_layout)
        
        # Options
        self.recursive_check = QCheckBox("Recursive Scan")
        self.recursive_check.setChecked(True)
        layout.addWidget(self.recursive_check)
        
        # Scan button
        scan_btn = QPushButton("Start Scan")
        scan_btn.clicked.connect(self.start_scan)
        layout.addWidget(scan_btn)
        
        # Progress bar
        self.scan_progress = QProgressBar()
        layout.addWidget(self.scan_progress)
        
        # Results table
        self.scanner_table = QTableWidget()
        self.scanner_table.setColumnCount(5)
        self.scanner_table.setHorizontalHeaderLabels(["Filename", "Size", "Extension", "Path", "Status"])
        layout.addWidget(self.scanner_table)
        
        tab.setLayout(layout)
        return tab
    
    def create_corruption_tab(self):
        """Create corruption detector tab"""
        tab = QWidget()
        layout = QVBoxLayout()
        
        # Scan button
        scan_corruption_btn = QPushButton("Scan for Corruption")
        scan_corruption_btn.clicked.connect(self.start_corruption_scan)
        layout.addWidget(scan_corruption_btn)
        
        # Progress bar
        self.corruption_progress = QProgressBar()
        layout.addWidget(self.corruption_progress)
        
        # Results table
        self.corruption_table = QTableWidget()
        self.corruption_table.setColumnCount(3)
        self.corruption_table.setHorizontalHeaderLabels(["File", "Status", "Issue"])
        layout.addWidget(self.corruption_table)
        
        tab.setLayout(layout)
        return tab
    
    def create_organizer_tab(self):
        """Create file organizer tab"""
        tab = QWidget()
        layout = QVBoxLayout()
        
        # Destination directory
        dest_layout = QHBoxLayout()
        dest_layout.addWidget(QLabel("Destination:"))
        self.organizer_dest = QLineEdit()
        dest_layout.addWidget(self.organizer_dest)
        browse_dest_btn = QPushButton("Browse")
        browse_dest_btn.clicked.connect(self.browse_destination)
        dest_layout.addWidget(browse_dest_btn)
        layout.addLayout(dest_layout)
        
        # Options
        self.move_check = QCheckBox("Move Files (instead of Copy)")
        self.move_check.setChecked(True)
        layout.addWidget(self.move_check)
        
        self.dry_run_check = QCheckBox("Preview Mode (Dry Run)")
        self.dry_run_check.setChecked(True)
        layout.addWidget(self.dry_run_check)
        
        # Organize button
        organize_btn = QPushButton("Organize Files")
        organize_btn.clicked.connect(self.start_organization)
        layout.addWidget(organize_btn)
        
        # Results table
        self.organizer_table = QTableWidget()
        self.organizer_table.setColumnCount(4)
        self.organizer_table.setHorizontalHeaderLabels(["Source", "Destination", "Category", "Status"])
        layout.addWidget(self.organizer_table)
        
        tab.setLayout(layout)
        return tab
    
    def browse_directory(self):
        """Browse for directory"""
        directory = QFileDialog.getExistingDirectory(self, "Select Directory")
        if directory:
            self.scanner_dir.setText(directory)
    
    def browse_destination(self):
        """Browse for destination directory"""
        directory = QFileDialog.getExistingDirectory(self, "Select Destination")
        if directory:
            self.organizer_dest.setText(directory)
    
    def start_scan(self):
        """Start file scanning"""
        directory = self.scanner_dir.text()
        if not directory:
            QMessageBox.warning(self, "Warning", "Please select a directory")
            return
        
        self.scan_progress.setValue(0)
        self.scanner_table.setRowCount(0)
        
        self.scanner_thread = ScannerThread(directory, self.recursive_check.isChecked())
        self.scanner_thread.finished.connect(self.on_scan_finished)
        self.scanner_thread.start()
    
    def on_scan_finished(self, files):
        """Handle scan completion"""
        self.scanned_files = files
        self.scan_progress.setValue(100)
        
        # Populate table
        self.scanner_table.setRowCount(len(files))
        for row, file_info in enumerate(files):
            self.scanner_table.setItem(row, 0, QTableWidgetItem(file_info['name']))
            self.scanner_table.setItem(row, 1, QTableWidgetItem(self.format_size(file_info['size'])))
            self.scanner_table.setItem(row, 2, QTableWidgetItem(file_info['extension']))
            self.scanner_table.setItem(row, 3, QTableWidgetItem(file_info['path']))
            self.scanner_table.setItem(row, 4, QTableWidgetItem("OK" if file_info['readable'] else "Error"))
        
        QMessageBox.information(self, "Success", f"Found {len(files)} files")
    
    def start_corruption_scan(self):
        """Start corruption scan"""
        if not self.scanned_files:
            QMessageBox.warning(self, "Warning", "Please scan files first")
            return
        
        self.corruption_progress.setValue(0)
        self.corruption_table.setRowCount(0)
        
        self.corruption_thread = CorruptionScanThread(self.scanned_files)
        self.corruption_thread.finished.connect(self.on_corruption_scan_finished)
        self.corruption_thread.start()
    
    def on_corruption_scan_finished(self, results):
        """Handle corruption scan completion"""
        self.corruption_progress.setValue(100)
        
        # Populate results
        row = 0
        for corrupted in results['corrupted']:
            self.corruption_table.insertRow(row)
            self.corruption_table.setItem(row, 0, QTableWidgetItem(corrupted['path']))
            self.corruption_table.setItem(row, 1, QTableWidgetItem("CORRUPTED"))
            self.corruption_table.setItem(row, 2, QTableWidgetItem(", ".join(corrupted['issues'])))
            row += 1
        
        for suspicious in results['suspicious']:
            self.corruption_table.insertRow(row)
            self.corruption_table.setItem(row, 0, QTableWidgetItem(suspicious['path']))
            self.corruption_table.setItem(row, 1, QTableWidgetItem("SUSPICIOUS"))
            self.corruption_table.setItem(row, 2, QTableWidgetItem(suspicious['reason']))
            row += 1
        
        msg = f"Scan Complete:\n- Corrupted: {len(results['corrupted'])}\n- Suspicious: {len(results['suspicious'])}\n- Healthy: {results['healthy']}"
        QMessageBox.information(self, "Results", msg)
    
    def start_organization(self):
        """Start file organization"""
        if not self.scanned_files:
            QMessageBox.warning(self, "Warning", "Please scan files first")
            return
        
        destination = self.organizer_dest.text()
        if not destination:
            QMessageBox.warning(self, "Warning", "Please select a destination directory")
            return
        
        organizer = FileOrganizer()
        results = organizer.organize_files(
            self.scanned_files,
            destination,
            dry_run=self.dry_run_check.isChecked(),
            move=self.move_check.isChecked()
        )
        
        # Populate results
        self.organizer_table.setRowCount(len(results['operations']))
        for row, op in enumerate(results['operations']):
            self.organizer_table.setItem(row, 0, QTableWidgetItem(op['source']))
            self.organizer_table.setItem(row, 1, QTableWidgetItem(op['destination']))
            self.organizer_table.setItem(row, 2, QTableWidgetItem(op['category']))
            self.organizer_table.setItem(row, 3, QTableWidgetItem(op['status'].upper()))
        
        msg = f"Organization Complete:\n- Organized: {results['organized']}\n- Failed: {results['failed']}\n- Skipped: {results['skipped']}"
        QMessageBox.information(self, "Results", msg)
    
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
