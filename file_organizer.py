#!/usr/bin/env python3
"""
File Organizer Application
Automatically sorts and moves files into folders based on their file type
Creates subfolders for each specific format within main categories
Comprehensive extension support for all major file types
"""

import os
import shutil
from pathlib import Path
from collections import defaultdict


# File extension to subfolder mapping (Category -> Subfolder -> Extensions)
FILE_CATEGORIES = {
    # Documents & Text
    'Documents & Text': {
        'PDF': ['.pdf'],
        'Word': ['.doc', '.docx', '.docm', '.dot', '.dotx', '.odt', '.pages'],
        'Plain Text': ['.txt', '.text'],
        'Rich Text': ['.rtf'],
        'OpenDocument': ['.odt', '.ott'],
        'eBook': ['.epub', '.mobi', '.azw', '.azw3'],
    },
    
    # Images
    'Images': {
        'JPEG': ['.jpg', '.jpeg', '.jpe'],
        'PNG': ['.png'],
        'GIF': ['.gif'],
        'BMP': ['.bmp', '.dib'],
        'WebP': ['.webp'],
        'Mobile Images': ['.heic', '.heif'],
        'Vector': ['.svg', '.eps', '.ai'],
        'Other Images': ['.tiff', '.tif', '.ico', '.icns', '.jp2', '.jpx', '.pcx', '.psd', '.psb'],
    },
    
    # Audio
    'Audio': {
        'MP3': ['.mp3'],
        'WAV': ['.wav', '.wave'],
        'AAC': ['.aac'],
        'FLAC': ['.flac'],
        'Mobile Audio': ['.m4a', '.m4b', '.m4p'],
        'Other Audio': ['.wma', '.ogg', '.oga', '.opus', '.alac', '.ape', '.aiff', '.aif', '.au', '.flv'],
    },
    
    # Video
    'Video': {
        'MP4': ['.mp4', '.m4v'],
        'QuickTime': ['.mov', '.qt'],
        'Matroska': ['.mkv', '.mka', '.mks'],
        'AVI': ['.avi'],
        'WebM': ['.webm'],
        'Windows Media': ['.wmv', '.wm', '.asf'],
        'Other Video': ['.flv', '.ogv', '.ts', '.m3u8', '.vob', '.f4v', '.3gp', '.3g2', '.mts', '.m2ts', '.mxf', '.mpg', '.mpeg', '.m2v'],
    },
    
    # Data & Spreadsheets
    'Data & Spreadsheets': {
        'Excel': ['.xlsx', '.xls', '.xlsm', '.xlsb', '.xltx', '.xltm', '.ods', '.gnumeric'],
        'CSV': ['.csv', '.tsv', '.txt'],
        'JSON': ['.json', '.jsonl', '.ndjson'],
        'XML': ['.xml', '.xsd', '.xsl', '.xslt'],
        'SQL': ['.sql', '.sqlite', '.db', '.sqlite3', '.mdb', '.accdb'],
        'YAML': ['.yaml', '.yml'],
        'Other Data': ['.dat', '.data', '.ini', '.cfg', '.conf'],
    },
    
    # Compressed & Archive
    'Compressed & Archive': {
        'ZIP': ['.zip', '.zipx'],
        'RAR': ['.rar', '.r01', '.r02', '.r03', '.r99'],
        '7Z': ['.7z', '.7z001'],
        'TAR': ['.tar', '.tar.gz', '.tgz', '.tar.bz2', '.tbz', '.tar.xz', '.txz'],
        'GZIP': ['.gz', '.gzip', '.bz2'],
        'Other Archive': ['.iso', '.dmg', '.cab', '.lzh', '.ace', '.arc', '.arj', '.b64'],
    },
    
    # Executables & Installers
    'Executables & Installers': {
        'Windows': ['.exe', '.msi', '.msu', '.scr', '.bat', '.cmd', '.com'],
        'Android': ['.apk', '.aab', '.xapk'],
        'macOS': ['.dmg', '.app', '.pkg', '.mpkg'],
        'iOS': ['.ipa'],
        'Linux': ['.deb', '.rpm', '.run', '.sh'],
        'Other Installers': ['.bin', '.jar'],
    },
    
    # Web
    'Web': {
        'HTML': ['.html', '.htm', '.xhtml', '.xht', '.mhtml', '.mht'],
        'CSS': ['.css', '.scss', '.sass', '.less'],
        'JavaScript': ['.js', '.jsx', '.mjs', '.cjs', '.ts', '.tsx'],
        'Web Data': ['.json', '.jsonp', '.xml', '.wsdl', '.soap'],
        'PHP': ['.php', '.php3', '.php4', '.php5', '.phtml', '.pht', '.phps'],
        'ASP': ['.asp', '.aspx', '.asax', '.ascx', '.asmx', '.ashx'],
        'JSP': ['.jsp', '.jspx', '.jsw', '.jsv', '.jspf'],
        'Other Web': ['.pl', '.cgi', '.cfm', '.cfc', '.erb', '.rhtml'],
    },
    
    # Code - Programming Languages
    'Code': {
        'Python': ['.py', '.pyw', '.pyx', '.pyc', '.pyo', '.egg'],
        'Java': ['.java', '.class', '.jar', '.war', '.ear'],
        'C/C++': ['.c', '.cpp', '.cc', '.cxx', '.c++', '.h', '.hpp', '.hxx', '.h++', '.ii', '.ipp'],
        'C#': ['.cs', '.csproj', '.sln'],
        'Go': ['.go'],
        'Rust': ['.rs'],
        'Ruby': ['.rb', '.erb', '.gemspec', '.Rakefile'],
        'TypeScript': ['.ts', '.tsx', '.d.ts'],
        'JSX': ['.jsx'],
        'Shell Script': ['.sh', '.bash', '.zsh', '.fish', '.ksh'],
        'Lua': ['.lua'],
        'Swift': ['.swift', '.playground'],
        'Kotlin': ['.kt', '.kts'],
        'Scala': ['.scala', '.sc'],
        'R': ['.r', '.R', '.Rdata', '.rds'],
        'MATLAB': ['.m', '.mat'],
        'Perl': ['.pl', '.pm', '.t'],
        'VB/VBA': ['.vb', '.vbs', '.bas', '.frm', '.cls'],
        'Pascal': ['.pas', '.pp'],
        'Delphi': ['.dpr', '.dfm'],
        'Objective-C': ['.m', '.mm', '.h'],
        'Groovy': ['.groovy', '.gradle'],
        'Clojure': ['.clj', '.cljs', '.cljc'],
        'Elixir': ['.ex', '.exs'],
        'Erlang': ['.erl', '.hrl'],
        'Haskell': ['.hs', '.lhs'],
        'Lisp': ['.lisp', '.lsp', '.cl', '.el'],
        'Scheme': ['.scm', '.ss'],
        'Prolog': ['.pl', '.pro'],
        'COBOL': ['.cbl', '.cobol', '.cob'],
        'Fortran': ['.f', '.f90', '.f95', '.f03', '.f08', '.for'],
        'Other Code': ['.ada', '.adb', '.asm', '.s', '.s79'],
    },
    
    # Configuration & Settings
    'Config & Settings': {
        'Configuration': ['.ini', '.cfg', '.conf', '.config', '.properties', '.env'],
        'Docker': ['.dockerfile', 'Dockerfile', '.dockerignore'],
        'Build Files': ['.cmake', '.make', '.Makefile', '.gradle', '.maven', '.sbt'],
        'Package': ['.package', '.lock', '.json', '.yaml', '.yml'],
        'Other Config': ['.gitignore', '.editorconfig', '.htaccess'],
    },
    
    # Media - 3D & Design
    'Media & Design': {
        '3D Models': ['.obj', '.fbx', '.gltf', '.glb', '.blend', '.max', '.ma', '.mb', '.c4d', '.dae', '.ply', '.stl'],
        'Design Files': ['.ai', '.psd', '.psb', '.xd', '.fig', '.sketch', '.drawio'],
        'CAD': ['.dwg', '.dxf', '.igs', '.iges', '.step', '.stp'],
        'Other Media': ['.swf', '.flv'],
    },
    
    # Documents - Office & Presentation
    'Office & Presentation': {
        'Presentations': ['.ppt', '.pptx', '.pptm', '.pot', '.potx', '.odp'],
        'Spreadsheets': ['.xls', '.xlsx', '.xlsm', '.ods', '.numbers'],
        'Documents': ['.doc', '.docx', '.docm', '.odt', '.pages'],
        'Other Office': ['.pub', '.one', '.vsd', '.visio'],
    },
    
    # System & Backup
    'System & Backup': {
        'Backup': ['.bak', '.backup', '.old', '.tmp', '.temp'],
        'System': ['.sys', '.dll', '.so', '.dylib', '.a', '.lib'],
        'Virtual Machine': ['.vmdk', '.vdi', '.qcow', '.qcow2', '.vhd', '.vhdx'],
        'Disk Image': ['.iso', '.img', '.dmg', '.toast'],
    },
    
    # Fonts
    'Fonts': {
        'TrueType': ['.ttf'],
        'OpenType': ['.otf', '.otc'],
        'Web Fonts': ['.woff', '.woff2', '.eot'],
        'Other Fonts': ['.fon', '.fnt', '.pfm', '.pfb'],
    },
    
    # Documents - Special
    'Documents - Special': {
        'Markdown': ['.md', '.markdown', '.mdown', '.mkd'],
        'LaTeX': ['.tex', '.latex', '.ltx', '.aux', '.bbl', '.bib'],
        'ReStructuredText': ['.rst', '.rest'],
        'AsciiDoc': ['.adoc', '.asciidoc'],
        'Other Docs': ['.log', '.dat', '.dat', '.msg', '.eml'],
    },
}


class FileOrganizer:
    """Organizes files into folders based on their type with subfolders per format"""
    
    def __init__(self, source_directory):
        """
        Initialize the organizer with a source directory
        
        Args:
            source_directory (str): Path to the directory containing files to organize
        """
        self.source_dir = Path(source_directory)
        
        if not self.source_dir.exists():
            raise FileNotFoundError(f"Directory not found: {source_directory}")
        
        if not self.source_dir.is_dir():
            raise NotADirectoryError(f"Path is not a directory: {source_directory}")
    
    def get_file_category_and_subfolder(self, file_extension):
        """
        Determine the category and subfolder of a file based on its extension
        
        Args:
            file_extension (str): File extension (e.g., '.pdf')
            
        Returns:
            tuple: (category_folder, subfolder_name) or ('Others', '') if not categorized
        """
        file_extension = file_extension.lower()
        
        for category, subfolders in FILE_CATEGORIES.items():
            if isinstance(subfolders, dict):
                for subfolder, extensions in subfolders.items():
                    if file_extension in extensions:
                        return category, subfolder
        
        return 'Others', ''
    
    def organize_files(self, dry_run=False):
        """
        Organize files into folders and subfolders based on their type
        
        Args:
            dry_run (bool): If True, show what would be moved without actually moving
        """
        file_stats = defaultdict(lambda: defaultdict(int))
        
        # Get all files in the directory (non-recursive)
        files = [f for f in self.source_dir.iterdir() if f.is_file()]
        
        if not files:
            print(f"No files found in {self.source_dir}")
            return
        
        print(f"Found {len(files)} file(s) to organize\n")
        
        for file_path in files:
            file_extension = file_path.suffix
            category, subfolder = self.get_file_category_and_subfolder(file_extension)
            
            # Create category folder structure
            if subfolder:
                # Create: Category/Subfolder/
                target_folder = self.source_dir / category / subfolder
                destination_display = f"{category}/{subfolder}"
            else:
                # Create: Others/
                target_folder = self.source_dir / category
                destination_display = category
            
            if not target_folder.exists() and not dry_run:
                target_folder.mkdir(parents=True, exist_ok=True)
                if subfolder:
                    print(f"✓ Created folder: {destination_display}/")
            
            # Move file to target folder
            destination = target_folder / file_path.name
            
            if dry_run:
                print(f"[DRY RUN] Would move: {file_path.name} → {destination_display}/")
            else:
                if destination.exists():
                    print(f"⚠ File already exists: {destination_display}/{file_path.name} (skipping)")
                else:
                    shutil.move(str(file_path), str(destination))
                    print(f"✓ Moved: {file_path.name} → {destination_display}/")
            
            file_stats[category][subfolder] += 1
        
        print("\n" + "="*80)
        print("ORGANIZATION SUMMARY")
        print("="*80)
        
        total_files = sum(sum(subf.values()) for subf in file_stats.values())
        print(f"\nTotal files organized: {total_files}\n")
        
        for category in sorted(file_stats.keys()):
            total_in_category = sum(file_stats[category].values())
            print(f"📁 {category} ({total_in_category} file(s)):")
            for subfolder, count in sorted(file_stats[category].items()):
                if subfolder:
                    print(f"   └─ {subfolder}: {count} file(s)")
                else:
                    print(f"   {count} file(s)")
        
        print("\n" + "="*80)
    
    def organize_recursive(self, dry_run=False):
        """
        Recursively organize files in subdirectories
        
        Args:
            dry_run (bool): If True, show what would be moved without actually moving
        """
        for directory in self.source_dir.rglob('.'):
            if directory.is_dir():
                organizer = FileOrganizer(str(directory))
                files_in_dir = [f for f in directory.iterdir() if f.is_file()]
                
                if files_in_dir:
                    print(f"\nOrganizing: {directory}")
                    organizer.organize_files(dry_run=dry_run)


def print_categories():
    """Print available categories and subfolders"""
    print("\n" + "="*80)
    print("SUPPORTED FILE TYPES - COMPREHENSIVE EXTENSION LIST")
    print("="*80)
    
    total_extensions = 0
    for category, subfolders in FILE_CATEGORIES.items():
        if isinstance(subfolders, dict):
            category_ext_count = sum(len(exts) for exts in subfolders.values())
            total_extensions += category_ext_count
    
    print(f"\nTotal Categories: {len(FILE_CATEGORIES)}")
    print(f"Total Extensions Supported: {total_extensions}\n")
    
    for category, subfolders in FILE_CATEGORIES.items():
        total_in_category = sum(len(exts) for exts in subfolders.values())
        print(f"📁 {category}/ ({total_in_category} extensions)")
        if isinstance(subfolders, dict):
            items = list(subfolders.items())
            for idx, (subfolder, extensions) in enumerate(items):
                is_last = idx == len(items) - 1
                prefix = "   └─ " if is_last else "   ├─ "
                ext_list = ', '.join(extensions)
                print(f"{prefix}{subfolder}: {ext_list}")
        print()


def main():
    """Main entry point"""
    import sys
    
    print("=" * 80)
    print("FILE ORGANIZER - PROFESSIONAL EDITION (COMPREHENSIVE)")
    print("=" * 80)
    print("\n✨ Organizes ALL file types into categorized subfolders by format")
    print("🎯 Supports 200+ file extensions across 14 categories")
    print("🔒 Smart organization with dry-run preview\n")
    
    print_categories()
    
    # Get directory from user or use current directory
    if len(sys.argv) > 1:
        target_dir = sys.argv[1]
    else:
        target_dir = input("Enter directory path (default: current directory): ").strip()
        if not target_dir:
            target_dir = "."
    
    try:
        organizer = FileOrganizer(target_dir)
        
        # Ask for dry run
        dry_run_input = input("\nRun in dry-run mode first? (y/n, default: y): ").strip().lower()
        dry_run = dry_run_input != 'n'
        
        if dry_run:
            print("\n[DRY RUN MODE] Preview of changes:\n")
        
        organizer.organize_files(dry_run=dry_run)
        
        if dry_run:
            proceed = input("\nProceed with organizing files? (y/n): ").strip().lower()
            if proceed == 'y':
                print("\nExecuting organization...\n")
                organizer.organize_files(dry_run=False)
            else:
                print("Operation cancelled.")
    
    except (FileNotFoundError, NotADirectoryError) as e:
        print(f"Error: {e}")
        sys.exit(1)
    except KeyboardInterrupt:
        print("\nOperation cancelled by user.")
        sys.exit(0)


if __name__ == "__main__":
    main()
