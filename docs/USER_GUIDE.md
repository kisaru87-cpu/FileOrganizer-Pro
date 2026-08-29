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

## How It Works

### Virtual File System (VFS)

FileOrganizer-Pro uses a **virtual file system** to organize your files WITHOUT modifying the original file structure:

1. **VFS Storage**: A hidden `.fileorganizer` directory stores symbolic links to your files organized by category
2. **Original Files**: Your original files remain untouched in their original locations
3. **Mirror to Disk**: Optional feature to create actual organized copies on disk

### Workflow

#### Step 1: Create Virtual File Structure

1. Open the "Scanner & VFS" tab
2. Click "Browse" and select the folder containing files to organize
3. Optionally check "Scan for Corruption" to detect file issues
4. Click "Create Virtual File Structure"
5. Wait for the process to complete

#### Step 2: View Virtual Organization

1. Go to the "Virtual File Manager" tab
2. You'll see your files organized by category in the tree view
3. Select a category to view files in detail
4. Original file paths are displayed for reference

#### Step 3: Mirror to Disk (Optional)

1. Navigate to the "Mirror to Disk" tab
2. Select a destination directory
3. Optionally check "Overwrite Existing Files"
4. Click "Mirror Virtual Structure to Disk"
5. Files will be COPIED (not moved) to the new organized location

## Features

### Scanner & VFS Creation

- **Recursive Scanning**: Includes all subfolders automatically
- **Corruption Detection**: Checks file headers and integrity
- **Automatic Categorization**: Files sorted into 9+ categories
- **Progress Tracking**: Real-time status updates

### Virtual File Manager

- **Non-Destructive**: Original files remain completely untouched
- **Fast Organization**: Uses symbolic links (instant access)
- **Category Browsing**: Easy navigation by file type
- **File Details**: View original paths and file properties

### Mirror to Disk

- **Safe Copying**: Creates organized copies without moving originals
- **Duplicate Handling**: Automatically renames conflicting files
- **Selective Export**: Mirror all or specific categories
- **Overwrite Control**: Option to replace or keep existing files

### Statistics

- **Overall Statistics**: Total files, size, and corruption status
- **Category Breakdown**: Files and sizes per category
- **Percentage Distribution**: Visual representation of storage usage

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

1. **Always Start with VFS**: Use the virtual file system first to preview organization
2. **Check Statistics**: Review the statistics tab to understand your file distribution
3. **Test Corruption Scanning**: Identify damaged files before mirroring
4. **Mirror to External Drive**: Create organized backups on separate storage
5. **Keep Original Structure**: Original files are never modified by VFS
6. **Multiple VFS Instances**: Run multiple scans in different directories

## Key Differences from Traditional Organizers

| Feature | FileOrganizer-Pro VFS | Traditional Organizers |
|---------|----------------------|------------------------|
| Modify Original Files | ❌ No | ✅ Yes (risk) |
| Organization Speed | ✅ Instant (symlinks) | Slow (copying) |
| Disk Space Used | ✅ Minimal | More (full copies) |
| Reversible | ✅ Yes (delete .fileorganizer) | Risky |
| Safe to Try | ✅ 100% safe | Potentially risky |

## Troubleshooting

### Issue: Application won't start
- Ensure Python 3.8+ is installed
- Verify all dependencies: `pip install -r requirements.txt`
- Check logs directory for errors

### Issue: VFS not showing files
- Ensure you've created the virtual structure first
- Check that the source directory has readable files
- Verify `.fileorganizer` directory exists and has contents

### Issue: Mirror operation slow
- Large file counts or file sizes take time
- Check available disk space
- Consider mirroring to faster storage (SSD)

### Issue: Symlinks not working on Windows
- Windows 10+ supports symlinks with proper permissions
- Falls back to metadata shortcuts automatically
- Try running as Administrator

## Support

For issues and feature requests: https://github.com/kisaru87-cpu/FileOrganizer-Pro
