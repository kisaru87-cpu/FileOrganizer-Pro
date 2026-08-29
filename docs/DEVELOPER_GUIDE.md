# FileOrganizer-Pro - Developer Guide

## Architecture

### Core Modules

#### file_scanner.py
Responsible for:
- Scanning directories recursively or non-recursively
- Collecting file metadata (size, extension, dates)
- Generating scan summaries

Key Classes:
- `FileScanner`: Main scanning engine

#### corruption_detector.py
Responsible for:
- Checking file signatures (magic bytes)
- Detecting corrupted or suspicious files
- Verifying file integrity

Key Classes:
- `CorruptionDetector`: File integrity checking engine

#### organizer.py
Responsible for:
- Categorizing files by type
- Organizing files into category folders
- Handling file conflicts and duplicates

Key Classes:
- `FileOrganizer`: File organization engine

#### utils.py
Utility functions:
- `FileUtils`: File operations (move, copy, hash)
- `ConfigManager`: Configuration management

#### logger.py
Centralized logging:
- File and console logging
- Log rotation
- Multiple log levels

### UI Components

#### main_window.py
- PyQt6 based GUI
- Three tabs: Scanner, Corruption Detector, Organizer
- Thread-based operations for responsiveness

## Development Setup

```bash
# Clone repository
git clone https://github.com/kisaru87-cpu/FileOrganizer-Pro.git
cd FileOrganizer-Pro

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install development dependencies
pip install -r requirements.txt
pip install pytest pytest-cov
```

## Running Tests

```bash
# Run all tests
python -m pytest tests/

# Run with coverage
python -m pytest tests/ --cov=src

# Run specific test
python -m pytest tests/test_file_scanner.py
```

## Adding New File Types

Edit `config/file_types.json`:

```json
"MyCategory": {
  "extensions": [".ext1", ".ext2"],
  "mime_types": ["type/subtype"],
  "icon": "📁"
}
```

## Adding File Signature Detection

Edit `src/corruption_detector.py`:

```python
FILE_SIGNATURES = {
    '.newext': b'SIGNATURE_BYTES',
    '.complex': [b'SIG1', b'SIG2']
}
```

## Code Style

- Follow PEP 8
- Use type hints
- Document functions with docstrings
- Add unit tests for new functionality

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests
5. Submit a pull request

## Performance Optimization

- Use threading for I/O operations
- Batch file operations
- Cache file metadata
- Implement progressive scanning

## License

MIT License - See LICENSE file
