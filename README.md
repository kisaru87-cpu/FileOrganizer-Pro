# FileOrganizer-Pro

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.8+](https://img.shields.io/badge/Python-3.8%2B-blue.svg)](https://www.python.org/downloads/)
[![Platform: Windows, macOS, Linux](https://img.shields.io/badge/Platform-Windows%20%7C%20macOS%20%7C%20Linux-lightgrey.svg)](#)

A cross-platform file organization software that categorizes all file types and scans for corrupted or potentially corrupted files. Features a **virtual file system** that organizes files without modifying the original structure.

## 🌟 Key Features

### Virtual File System (VFS)
- **Non-Destructive Organization**: Files remain in original locations while appearing organized in VFS
- **Symbolic Links**: Uses OS-level symlinks for instant organization (no copying)
- **Safe by Default**: 100% reversible - just delete `.fileorganizer` folder to undo
- **Cross-Platform**: Works on Windows, macOS, and Linux

### File Organization
- **Smart Categorization**: Automatically sorts 100+ file types into 9 categories
- **Corruption Detection**: Scans file headers and integrity
- **Recursive Scanning**: Includes all subfolders in one operation
- **Duplicate Handling**: Intelligently renames conflicting files

### Mirror & Export
- **Safe Mirroring**: Copy organized VFS structure to physical disk
- **Preserves Originals**: Original files never touched by mirror operation
- **Overwrite Control**: Choose to skip or replace existing files
- **Batch Operations**: Handle thousands of files efficiently

### Statistics & Insights
- **Real-Time Analytics**: View file distribution by category
- **Storage Analysis**: See how much space each category uses
- **Corruption Reports**: Identify problematic files before they become issues

## 📋 System Requirements

- **OS**: Windows 10+, macOS 10.14+, or Linux (Ubuntu 18.04+)
- **Python**: 3.8 or higher
- **RAM**: 512MB minimum
- **Disk Space**: 200MB for installation
- **Permissions**: Ability to create symlinks (admin on Windows)

## 🚀 Quick Start

### Installation

```bash
# Clone the repository
git clone https://github.com/kisaru87-cpu/FileOrganizer-Pro.git
cd FileOrganizer-Pro

# Install dependencies
pip install -r requirements.txt

# Run the application
python main.py
```

### Basic Workflow

1. **Scan Files**: Select a folder and click "Create Virtual File Structure"
2. **View Organization**: Browse files by category in the Virtual File Manager
3. **Mirror (Optional)**: Export organized structure to disk
4. **Analyze**: Review statistics and corruption reports

## 📁 Project Structure

```
FileOrganizer-Pro/
├── main.py                          # Application entry point
├── requirements.txt                 # Python dependencies
├── config/
│   ├── file_types.json            # File type categorization
│   └── settings.json              # Application settings
├── src/
│   ├── file_scanner.py            # Directory scanning engine
│   ├── corruption_detector.py     # File integrity checking
│   ├── organizer.py               # File categorization
│   ├── virtual_filesystem.py      # VFS management (symlinks)
│   ├── organization_manager.py    # Workflow orchestration
│   ├── utils.py                   # Utility functions
│   └── logger.py                  # Logging configuration
├── ui/
│   └── main_window.py             # PyQt6 GUI application
├── tests/
│   ├── test_file_scanner.py
│   ├── test_corruption_detector.py
│   └── test_organizer.py
├── docs/
│   ├── USER_GUIDE.md
│   └── DEVELOPER_GUIDE.md
└── logs/                          # Application logs (created at runtime)
```

## 🎯 Supported File Categories

| Category | Extensions |
|----------|------------|
| **Documents** | PDF, DOC, DOCX, TXT, XLSX, XLS, PPT, PPTX, OTF, RTF |
| **Images** | JPG, JPEG, PNG, GIF, BMP, SVG, WEBP, TIFF, ICO |
| **Videos** | MP4, AVI, MKV, MOV, FLV, WMV, WEBM, M4V, 3GP |
| **Audio** | MP3, WAV, FLAC, AAC, OGG, M4A, WMA, AIFF |
| **Archives** | ZIP, RAR, 7Z, TAR, GZ, BZ2, ISO, DMG |
| **Code** | PY, JS, TS, JAVA, CPP, C, H, CS, PHP, RB, GO, RS, SQL, HTML, CSS, JSON, XML, YAML, YML |
| **Executables** | EXE, MSI, APP, DMG, DEB, RPM, SH, BAT, CMD |
| **Fonts** | TTF, OTF, WOFF, WOFF2, EOT |
| **Database** | DB, SQLITE, SQLITE3, MDB, ACCDB, SQL |
| **Other** | Any unrecognized file type |

## 🔧 Virtual File System Explained

Unlike traditional file organizers that move or copy files:

```
Original Structure          Virtual Structure (.fileorganizer)
/Downloads                 ├── Documents
├── report.pdf       →      │   └── report.pdf -> /Downloads/report.pdf
├── photo.jpg              ├── Images
├── video.mp4              │   └── photo.jpg -> /Downloads/photo.jpg
└── script.py              ├── Videos
                           │   └── video.mp4 -> /Downloads/video.mp4
                           └── Code
                               └── script.py -> /Downloads/script.py
```

**Benefits:**
- ⚡ Instant organization (no copying)
- 💾 Zero additional disk space used
- 🔄 100% reversible
- 🛡️ Completely safe - originals never modified

## 🪞 Mirror to Disk

When you want actual organized files:

```bash
1. Create VFS (symbolic links organized by category)
2. Mirror to Disk (COPY files following VFS structure)
3. Result: Physical organized folder structure
```

## 📊 Corruption Detection

Automatic scanning for:
- ✗ Invalid file signatures (magic bytes)
- ✗ Unreadable files
- ✗ Empty files
- ✗ Suspicious file characteristics
- ✗ Inaccessible files

## 🧪 Running Tests

```bash
# Install test dependencies
pip install pytest pytest-cov

# Run all tests
python -m pytest tests/

# Run with coverage report
python -m pytest tests/ --cov=src --cov-report=html

# Run specific test
python -m pytest tests/test_file_scanner.py -v
```

## 📖 Documentation

- [User Guide](docs/USER_GUIDE.md) - How to use the application
- [Developer Guide](docs/DEVELOPER_GUIDE.md) - Contributing and extending

## 🐛 Troubleshooting

### Application won't start
```bash
# Verify Python version
python --version  # Must be 3.8+

# Reinstall dependencies
pip install --upgrade -r requirements.txt

# Check for errors
cat logs/fileorganizer.log
```

### Symlinks not working on Windows
- Windows 10+ requires admin privileges or Developer Mode
- Application automatically falls back to metadata references
- Try running as Administrator

### VFS not appearing
1. Ensure scan completed successfully
2. Check that `.fileorganizer` directory exists
3. Verify source directory has readable files
4. Check logs for errors

## 🤝 Contributing

Contributions welcome! Please:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit changes (`git commit -m 'Add AmazingFeature'`)
4. Push to branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙌 Acknowledgments

- PyQt6 for the GUI framework
- python-magic for file type detection
- tqdm for progress indicators
- All contributors and users

## 📞 Support

- 🐛 [Report a Bug](https://github.com/kisaru87-cpu/FileOrganizer-Pro/issues)
- 💡 [Request a Feature](https://github.com/kisaru87-cpu/FileOrganizer-Pro/issues)
- 📧 Email: support@fileorganizer-pro.dev

## 🗺️ Roadmap

- [ ] Cloud synchronization (Google Drive, OneDrive)
- [ ] Custom categorization rules (regex support)
- [ ] Scheduled automatic organization
- [ ] File preview in GUI
- [ ] Search functionality
- [ ] Undo/Redo operations
- [ ] Batch file operations (rename, delete, move)
- [ ] Plugin system for extensions

---

**Made with ❤️ for file organization enthusiasts**
