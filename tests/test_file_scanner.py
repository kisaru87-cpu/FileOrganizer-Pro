import unittest
import os
import tempfile
from src.file_scanner import FileScanner

class TestFileScanner(unittest.TestCase):
    """Test file scanner functionality"""
    
    def setUp(self):
        """Set up test fixtures"""
        self.temp_dir = tempfile.mkdtemp()
        self.scanner = FileScanner()
        
        # Create test files
        with open(os.path.join(self.temp_dir, 'test.txt'), 'w') as f:
            f.write('test')
        with open(os.path.join(self.temp_dir, 'test.jpg'), 'wb') as f:
            f.write(b'\xff\xd8\xff')
    
    def tearDown(self):
        """Clean up test fixtures"""
        import shutil
        shutil.rmtree(self.temp_dir)
    
    def test_scan_directory(self):
        """Test directory scanning"""
        files = self.scanner.scan_directory(self.temp_dir, recursive=False)
        self.assertEqual(len(files), 2)
    
    def test_file_extension_detection(self):
        """Test file extension detection"""
        files = self.scanner.scan_directory(self.temp_dir, recursive=False)
        extensions = [f['extension'] for f in files]
        self.assertIn('.txt', extensions)
        self.assertIn('.jpg', extensions)

if __name__ == '__main__':
    unittest.main()
