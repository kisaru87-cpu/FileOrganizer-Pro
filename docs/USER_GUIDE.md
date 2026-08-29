# FileOrganizer-Pro - User Guide

## Getting Started

### Installation

1. Clone the repository:
```bash
git clone https://github.com/kisaru87-cpu/FileOrganizer-Pro.git
cd FileOrganizer-Pro
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Run the application:
```bash
python main.py
```

## Features Guide

### File Scanner

1. **Select Directory**: Click "Browse" to select the folder you want to scan
2. **Recursive Scan**: Check "Recursive Scan" to include subfolders
3. **Start Scan**: Click "Start Scan" to begin
4. **View Results**: Files are displayed in the table with details

### Corruption Detector

1. **Prerequisites**: Must scan files first using the File Scanner
2. **Scan**: Click "Scan for Corruption" to check files
3. **Results**: 
   - CORRUPTED: Files that are definitely corrupted
   - SUSPICIOUS: Files with potential issues
   - HEALTHY: Files that are OK

### File Organizer

1. **Select Destination**: Choose where to organize files
2. **Options**:
   - **Move Files**: Move files instead of copying
   - **Preview Mode**: Preview changes without applying them
3. **Organize**: Click "Organize Files" to start
4. **Review**: Check the results table for operation status

## Supported File Types

- **Documents**: PDF, DOC, DOCX, TXT, XLSX, PPT, etc.
- **Images**: JPG, PNG, GIF, BMP, SVG, WEBP, TIFF, ICO
- **Videos**: MP4, AVI, MKV, MOV, FLV, WMV, WEBM
- **Audio**: MP3, WAV, FLAC, AAC, OGG, M4A, WMA, AIFF
- **Archives**: ZIP, RAR, 7Z, TAR, GZ, BZ2, ISO, DMG
- **Code**: Python, JavaScript, Java, C++, etc.
- **Executables**: EXE, MSI, APP, DEB, RPM, SH, BAT
- **Fonts**: TTF, OTF, WOFF, WOFF2, EOT
- **Database**: DB, SQLITE, MDB, ACCDB, SQL
- **Other**: All other file types

## Tips & Best Practices

1. Always use Preview Mode first to review changes
2. Backup important files before organizing
3. Run corruption scan regularly to maintain file health
4. Check logs in the logs directory for detailed information
5. Use safe mode for critical operations

## Troubleshooting

### Issue: Application won't start
- Ensure Python 3.8+ is installed
- Verify all dependencies are installed: `pip install -r requirements.txt`
- Check the logs directory for error messages

### Issue: Slow scanning on large directories
- Try organizing by smaller subfolders
- Increase thread count in settings.json
- Exclude network drives if possible

### Issue: Files not organizing correctly
- Verify the destination directory has write permissions
- Check that files are not currently in use
- Review the operation details in the results table

## Support

For more help, visit: https://github.com/kisaru87-cpu/FileOrganizer-Pro
