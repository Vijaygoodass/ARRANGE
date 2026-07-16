# 📁 ARRANGE - Professional File Organizer

**Desktop App + Android Mobile App** for automatic file organization

A powerful application that intelligently organizes files into categorized subfolders by format type. Supports **200+ file extensions** across **14 categories** with background scheduling on desktop and mobile-friendly UI on Android.

---

## 🌟 Features

### ✨ Desktop (Windows/Mac/Linux)
- ✅ Organize files into **14 main categories**
- ✅ **200+ file extension** support
- ✅ **Format-specific subfolders** (e.g., JPEG→Images/JPEG, MP3→Audio/MP3)
- ✅ **Background scheduler** - Runs automatically once per day
- ✅ **Interactive menu** - Easy configuration
- ✅ **Dry-run mode** - Preview before organizing
- ✅ **Multi-directory** - Organize multiple folders
- ✅ **Comprehensive logging** - Complete audit trail
- ✅ **Safe operation** - Skips existing files, no deletions

### 📱 Android Mobile App
- ✅ **Beautiful mobile UI** - Buttons, menus, real-time log
- ✅ **Add/Remove folders** - Manage watch directories
- ✅ **Organize on demand** - One-tap organizing
- ✅ **Real-time logging** - See every action
- ✅ **Settings dashboard** - View configuration
- ✅ **Works offline** - No internet needed
- ✅ **All 200+ file types** - Same comprehensive support

---

## 📊 Supported File Categories

### 1. 📄 Documents & Text
PDF, Word, Plain Text, RTF, OpenDocument, eBooks

### 2. 🖼️ Images
JPEG, PNG, GIF, BMP, WebP, HEIC/HEIF, SVG, Vector, 3D Models

### 3. 🎵 Audio
MP3, WAV, AAC, FLAC, M4A, WMA, OGG, Opus, ALAC, AIFF

### 4. 🎬 Video
MP4, MOV, MKV, AVI, WebM, WMV, FLV, 3GP, TS

### 5. 📊 Data & Spreadsheets
Excel, CSV, TSV, JSON, XML, SQL, YAML

### 6. 📦 Compressed & Archive
ZIP, RAR, 7Z, TAR, GZIP, BZ2, ISO, DMG

### 7. ⚙️ Executables & Installers
Windows (EXE, MSI), Android (APK, AAB), macOS (DMG, APP), iOS (IPA), Linux (DEB, RPM)

### 8. 🌐 Web
HTML, CSS, JavaScript, PHP, ASP, JSP

### 9. 💻 Code (25+ Languages)
Python, Java, C/C++, Go, Rust, Ruby, TypeScript, Swift, Kotlin, Scala, and more

### 10. ⚙️ Config & Settings
INI, CFG, CONF, Docker, Makefile, .env files

### 11. 🎨 Media & Design
3D Models (OBJ, FBX, GLTF), Design Files (AI, PSD, XD), CAD (DWG, DXF)

### 12. 📈 Office & Presentation
PPT, PPTX, XLS, XLSX, ODP, ODS

### 13. 🖥️ System & Backup
BAK, DLL, SO, VMDK, VDI, ISO

### 14. 🔤 Fonts & Special
TTF, OTF, WOFF, Markdown, LaTeX, AsciiDoc

---

## 🚀 Quick Start

### Desktop (Computer)

#### Installation
```bash
# Clone the repository
git clone https://github.com/Vijaygoodass/ARRANGE.git
cd ARRANGE

# No dependencies needed! Just Python 3.6+
python file_organizer.py
```

#### Usage
```bash
# Interactive mode (default)
python file_organizer.py

# Daemon mode (background)
python file_organizer.py --daemon

# Organize specific directory
python file_organizer.py /path/to/directory
```

#### Interactive Menu
```
1. Add directory to watch
2. Remove directory from watch
3. Set interval (hours) - default 24
4. Start background scheduler
5. Organize now (manual trigger)
6. View status
7. Exit
```

---

### 📱 Android Phone

#### Option 1: Download Pre-built APK (Easiest)
1. Download `arrange-1.0-debug.apk` from releases
2. Transfer to phone
3. Open file manager and tap APK
4. Install and grant permissions
5. Done! 🎉

#### Option 2: Build Your Own APK

See [BUILD_APK.md](BUILD_APK.md) for detailed instructions

**Quick version:**
```bash
# Install requirements
pip install -r requirements_android.txt

# Run quick build (Mac/Linux)
chmod +x QUICK_BUILD.sh
./QUICK_BUILD.sh

# Or on Windows
QUICK_BUILD.bat

# Find APK in: bin/arrange-1.0-debug.apk
```

See [ANDROID_SETUP.md](ANDROID_SETUP.md) for full Android guide

---

## 💾 Configuration Files

### Desktop
- `organizer_config.json` - Stores watched directories and interval
- `organizer_schedule.json` - Last run and next run times
- `file_organizer.log` - Complete operation history

### Android
- `organizer_config_mobile.json` - Stores configured directories
- `file_organizer_mobile.log` - All operations logged

---

## 📂 Example Organization

### Before
```
Downloads/
├── document.pdf
├── photo.jpg
├── video.mp4
├── song.mp3
├── script.py
├── data.xlsx
└── archive.zip
```

### After (Desktop)
```
Downloads/
├── Documents & Text/PDF/document.pdf
├── Images/JPEG/photo.jpg
├── Video/MP4/video.mp4
├── Audio/MP3/song.mp3
├── Code/Python/script.py
├── Data & Spreadsheets/Excel/data.xlsx
└── Compressed & Archive/ZIP/archive.zip
```

---

## 🎯 Common Use Cases

### 1. Organize Downloads Folder
```bash
python file_organizer.py ~/Downloads
```

### 2. Auto-Organize Multiple Folders Daily
1. Run interactive mode
2. Add folders
3. Set interval to 24 hours
4. Start background scheduler
5. ✅ Done! Runs automatically

### 3. On Android Phone
1. Open ARRANGE app
2. Add `/storage/emulated/0/Download`
3. Tap "Organize Now"
4. Watch files organize in real-time

### 4. Bulk Organization
```bash
python file_organizer.py /path/to/messy/folder
```

---

## 🔒 Security & Safety

✅ **Never Deletes Files**
- Files are only moved, never deleted
- Folder structure is preserved
- Existing files are never overwritten

✅ **Safe Operation**
- Dry-run mode to preview changes
- Permission checks before moving
- Comprehensive error handling
- Detailed logging of all operations

✅ **No Internet Needed**
- Works completely offline
- No data collection
- No cloud access required
- 100% local operation

---

## ⚙️ Advanced Usage

### Custom Intervals (Desktop)
```
Select option 3 in menu
Enter hours (1-168 or higher)
Default: 24 hours
```

### Recursive Organization
```python
from file_organizer import FileOrganizer

organizer = FileOrganizer('/path/to/folder')
organizer.organize_recursive(dry_run=False)
```

### Customize File Categories
Edit `file_organizer.py` to add more file types:
```python
'My Category': {
    'Subfolder': ['.ext1', '.ext2', '.ext3'],
}
```

---

## 🐛 Troubleshooting

### Desktop

**Problem: "Directory not found"**
```
Solution: Use absolute path or full path
❌ Wrong: ~/Downloads
✅ Right: /Users/username/Downloads
```

**Problem: Permission denied**
```
Solution: Run with appropriate permissions
sudo python file_organizer.py
```

**Problem: Background scheduler not working**
```
Solution: Keep terminal/command prompt open
Or use --daemon flag
```

### Android

**Problem: "Permission denied" when organizing**
```
Solution: 
1. Go to Settings > Apps > ARRANGE
2. Tap Permissions
3. Enable "Files and Media"
```

**Problem: Can't find directory path**
```
Solution: Use standard paths:
- /storage/emulated/0/Download
- /storage/emulated/0/Pictures
- /storage/emulated/0/Documents
```

**Problem: App won't install**
```
Solution:
1. Settings > Security > Unknown Sources
2. Enable "Allow installation from unknown sources"
3. Try again
```

---

## 📋 Requirements

### Desktop (Windows/Mac/Linux)
- **Python 3.6+** (no other dependencies!)
- **2GB disk space** minimum
- **100MB free space** for app
- Any OS: Windows, macOS, Linux

### Android
- **Android 5.0+** (API 21)
- **100MB disk space** minimum
- **1GB RAM** minimum (2GB recommended)
- Any brand: Samsung, OnePlus, Xiaomi, etc.

---

## 📦 Installation

### From Source
```bash
git clone https://github.com/Vijaygoodass/ARRANGE.git
cd ARRANGE
python file_organizer.py
```

### Pre-built APK (Android)
Download from GitHub Releases:
- `arrange-1.0-debug.apk` - Debug version
- `arrange-1.0-release.apk` - Production version

---

## 🤝 Contributing

Contributions are welcome! 

### To contribute:
1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

### Ideas for contributions:
- Add more file types
- Improve UI design
- Add scheduling features
- Localization/translations
- Bug fixes

---

## 📄 License

Apache License 2.0

See LICENSE file for details

---

## 👤 Author

**Vijaygoodass**
- GitHub: [@Vijaygoodass](https://github.com/Vijaygoodass)
- Project: [ARRANGE](https://github.com/Vijaygoodass/ARRANGE)

---

## 📚 Documentation

- [Desktop User Guide](README.md) - This file
- [Android Setup Guide](ANDROID_SETUP.md) - Mobile app instructions
- [Build APK Guide](BUILD_APK.md) - How to build from source

---

## 🐞 Issues & Bug Reports

Found a bug? Have a feature request?

[Open an issue](https://github.com/Vijaygoodass/ARRANGE/issues)

---

## 💡 Tips & Tricks

### Desktop
- Use dry-run mode first to preview changes
- Set multiple directories for background scheduler
- Check logs regularly for organization history
- Customize intervals based on your needs

### Android
- Grant all permissions for full functionality
- Use settings to view configured directories
- Clear log after each major organization
- Copy-paste paths to avoid typos

---

## 🎊 What's Next?

### Planned Features
- 🎨 Dark mode UI
- 🌍 Multi-language support
- 📊 Statistics dashboard
- ⏰ Scheduled notifications
- 🔄 Sync across devices
- 🌐 Cloud storage support

---

## ❓ FAQ

**Q: Can I organize my cloud storage?**
A: Currently supports local storage. Cloud support planned for v2.0

**Q: Will it delete any files?**
A: No! Files are only moved, never deleted.

**Q: Is my data safe?**
A: Yes! 100% local operation, no internet or data collection.

**Q: Can I organize multiple folders at once?**
A: Desktop: Yes, add multiple directories
   Android: Organize one at a time

**Q: How long does organization take?**
A: Depends on file count. Usually 1-10 seconds per 100 files.

**Q: Can I undo organization?**
A: Files are organized by moving, not copying. Paths are logged for reference.

---

## 🌟 Show Your Support

If ARRANGE helps you, please:
- ⭐ Star the repository
- 📢 Share with friends
- 💬 Provide feedback
- 🐛 Report bugs
- 💡 Suggest features

---

## 📞 Contact & Support

**GitHub Issues:** [Report a problem](https://github.com/Vijaygoodass/ARRANGE/issues)

**Email:** sonuraj1998ab@gmail.com

**Website:** [Vijaygoodass](https://github.com/Vijaygoodass)

---

**Built with ❤️ using Python and Kivy**

**Happy organizing! 📁✨**

git add .
git commit -m "Test auto-build"
git push origin Index
