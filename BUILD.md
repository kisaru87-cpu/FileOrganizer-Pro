# FileOrganizer-Pro Build Instructions

## Building the .exe Executable

### Prerequisites

1. **Python 3.8+** installed
2. **PyInstaller** installed
3. All dependencies installed

### Quick Start

#### On Windows (using Command Prompt or PowerShell):

```batch
# Install dependencies
pip install -r requirements.txt

# Run build script
python build.py
```

Or use the batch file:
```batch
build.bat
```

#### On macOS/Linux:

```bash
# Install dependencies
pip install -r requirements.txt

# Run build script
python build.py
```

### Build Output

After building, you'll find:

```
dist/FileOrganizer-Pro/
├── FileOrganizer-Pro.exe          # Main executable
├── config/                         # Configuration files
├── docs/                          # Documentation
├── _internal/                     # Dependencies (PyQt6, etc.)
└── ... (other runtime files)
```

### Running the .exe

1. Navigate to `dist/FileOrganizer-Pro/`
2. Double-click `FileOrganizer-Pro.exe`
3. Application starts - no Python installation needed!

### Distribution

**To distribute:**
- Compress the entire `dist/FileOrganizer-Pro/` folder
- Share the .zip file with users
- Users extract and run `FileOrganizer-Pro.exe`

### Creating a Windows Installer (Optional)

For a professional installer:

1. Install NSIS: https://nsis.sourceforge.io/
2. Create `installer.nsi` (example below)
3. Run: `makensis installer.nsi`

**Example NSIS installer script:**

```nsis
; FileOrganizer-Pro Installer
!include "MUI2.nsh"

Name "FileOrganizer-Pro"
OutFile "FileOrganizer-Pro-Installer.exe"
InstallDir "$PROGRAMFILES\FileOrganizer-Pro"

!insertmacro MUI_PAGE_WELCOME
!insertmacro MUI_PAGE_DIRECTORY
!insertmacro MUI_PAGE_INSTFILES
!insertmacro MUI_PAGE_FINISH

!insertmacro MUI_LANGUAGE "English"

Section "Install"
  SetOutPath "$INSTDIR"
  File /r "dist\FileOrganizer-Pro\*.*"
  
  CreateDirectory "$SMPROGRAMS\FileOrganizer-Pro"
  CreateShortCut "$SMPROGRAMS\FileOrganizer-Pro\FileOrganizer-Pro.lnk" "$INSTDIR\FileOrganizer-Pro.exe"
  CreateShortCut "$DESKTOP\FileOrganizer-Pro.lnk" "$INSTDIR\FileOrganizer-Pro.exe"
SectionEnd

Section "Uninstall"
  RMDir /r "$INSTDIR"
  Delete "$SMPROGRAMS\FileOrganizer-Pro\FileOrganizer-Pro.lnk"
  Delete "$DESKTOP\FileOrganizer-Pro.lnk"
SectionEnd
```

## Troubleshooting

### "PyInstaller not found"
```bash
pip install PyInstaller
```

### "Module not found" errors
- Make sure all dependencies are installed: `pip install -r requirements.txt`
- Check hidden imports in `FileOrganizer-Pro.spec`

### .exe file is very large (300+ MB)
- This is normal - includes all Python libraries and PyQt6
- Use `upx` to compress further (optional)

### .exe won't run
1. Check Windows Defender doesn't quarantine it
2. Ensure you have write permissions in the directory
3. Try running as Administrator
4. Check the logs folder for error messages

## File Size Optimization

To reduce executable size:

1. **Enable UPX compression** (add to spec file)
2. **Exclude unused modules** (update hiddenimports)
3. **Remove debug symbols** (already done in spec)

## Performance Tips

- First run may be slower as PyInstaller extracts runtime files
- Subsequent runs are faster (cached)
- For production, create installer with proper shortcuts

## Support

For issues with PyInstaller, see: https://pyinstaller.org/
