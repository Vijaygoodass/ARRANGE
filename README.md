# ARRANGE - File Organizer

A simple Python application that automatically organizes files into folders based on their file type.

## Features

✨ **Automatic File Classification** - Sorts files by type (Images, Documents, Videos, Audio, Archives, Code, etc.)

📁 **Organized Folder Structure** - Creates categorized folders and moves files accordingly

🔍 **Dry Run Mode** - Preview changes before actually moving files

⚠️ **Safe Operation** - Skips files that already exist to prevent overwrites

## Supported File Types

### Images
`.jpg`, `.jpeg`, `.png`, `.gif`, `.bmp`, `.svg`, `.webp`, `.ico`, `.tiff`

### Documents
`.pdf`, `.doc`, `.docx`, `.txt`, `.xls`, `.xlsx`, `.ppt`, `.pptx`, `.odt`

### Videos
`.mp4`, `.avi`, `.mov`, `.mkv`, `.flv`, `.wmv`, `.webm`, `.m4v`

### Audio
`.mp3`, `.wav`, `.flac`, `.aac`, `.wma`, `.ogg`, `.m4a`, `.alac`

### Archives
`.zip`, `.rar`, `.7z`, `.tar`, `.gz`, `.bz2`, `.iso`

### Code
`.py`, `.js`, `.ts`, `.java`, `.c`, `.cpp`, `.go`, `.rs`, `.rb`, `.php`, `.html`, `.css`

### Spreadsheets
`.csv`, `.tsv`

### Others
Any file type not listed above goes to the `Others` folder

## Installation

No external dependencies required! Just Python 3.6+

```bash
git clone https://github.com/Vijaygoodass/ARRANGE.git
cd ARRANGE
```

## Usage

### Basic Usage (Current Directory)

```bash
python file_organizer.py
```

### Specify Directory

```bash
python file_organizer.py /path/to/directory
```

Or on Windows:

```bash
python file_organizer.py C:\Users\YourName\Downloads
```

### Interactive Mode

1. Run the script
2. Enter the directory path when prompted (or press Enter for current directory)
3. Choose to run in dry-run mode first (recommended!)
4. Review the preview
5. Confirm to proceed with organization

## Example

**Before:**
```
Downloads/
├── document.pdf
├── photo.jpg
├── script.py
├── song.mp3
└── archive.zip
```

**After:**
```
Downloads/
├── Documents/
│   └── document.pdf
├── Images/
│   └── photo.jpg
├── Code/
│   └── script.py
├── Audio/
│   └── song.mp3
└── Archives/
    └── archive.zip
```

## Features

### Dry Run Mode (Recommended)
See what would be moved without actually moving files:
```
[DRY RUN] Would move: document.pdf → Documents/
[DRY RUN] Would move: photo.jpg → Images/
```

### Safe Operation
- Skips files that already exist in destination
- Creates folders only if needed
- No files are deleted

## Customization

To add more file types, edit the `FILE_CATEGORIES` dictionary in `file_organizer.py`:

```python
FILE_CATEGORIES = {
    'My Custom Category': ['.ext1', '.ext2', '.ext3'],
    # ... other categories
}
```

## How It Works

1. **Scans** the target directory for files
2. **Analyzes** each file's extension
3. **Categorizes** files based on type
4. **Creates** necessary folders
5. **Moves** files to appropriate folders
6. **Reports** what was organized

## License

Apache License 2.0

## Author

Vijaygoodass

---

**Happy Organizing!** 📁✨