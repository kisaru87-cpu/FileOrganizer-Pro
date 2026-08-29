import unittest
from src.organizer import FileOrganizer
import tempfile
import os

class TestFileOrganizer(unittest.TestCase):
    """Test file organization functionality"""
    
    def setUp(self):
        """Set up test fixtures"""
        self.organizer = FileOrganizer()
        self.temp_dir = tempfile.mkdtemp()
    
    def tearDown(self):
        """Clean up test fixtures"""
        import shutil
        shutil.rmtree(self.temp_dir)
    
    def test_file_categorization(self):
        """Test file categorization"""
        category = self.organizer.categorize_file('document.pdf')
        self.assertEqual(category, 'Documents')
        
        category = self.organizer.categorize_file('image.jpg')
        self.assertEqual(category, 'Images')
        
        category = self.organizer.categorize_file('script.py')
        self.assertEqual(category, 'Code')
    
    def test_unknown_extension_categorization(self):
        """Test unknown extension categorization"""
        category = self.organizer.categorize_file('unknown.xyz')
        self.assertEqual(category, 'Other')

if __name__ == '__main__':
    unittest.main()
