import unittest
from src.corruption_detector import CorruptionDetector
import tempfile
import os

class TestCorruptionDetector(unittest.TestCase):
    """Test corruption detection functionality"""
    
    def setUp(self):
        """Set up test fixtures"""
        self.detector = CorruptionDetector()
        self.temp_dir = tempfile.mkdtemp()
    
    def tearDown(self):
        """Clean up test fixtures"""
        import shutil
        shutil.rmtree(self.temp_dir)
    
    def test_valid_file_signature(self):
        """Test valid file signature detection"""
        # Create a valid PNG file
        png_file = os.path.join(self.temp_dir, 'test.png')
        with open(png_file, 'wb') as f:
            f.write(b'\x89PNG\r\n\x1a\n')
        
        result = self.detector._check_file_integrity(png_file)
        self.assertFalse(result['is_corrupted'])
    
    def test_invalid_file_signature(self):
        """Test invalid file signature detection"""
        # Create an invalid PNG file
        png_file = os.path.join(self.temp_dir, 'test.png')
        with open(png_file, 'wb') as f:
            f.write(b'INVALID')
        
        result = self.detector._check_file_integrity(png_file)
        self.assertTrue(result['is_corrupted'])
    
    def test_empty_file_detection(self):
        """Test empty file detection"""
        empty_file = os.path.join(self.temp_dir, 'empty.txt')
        with open(empty_file, 'wb') as f:
            pass
        
        result = self.detector._check_file_integrity(empty_file)
        self.assertIn('File is empty', result['warnings'])

if __name__ == '__main__':
    unittest.main()
