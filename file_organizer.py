#!/usr/bin/env python3
"""
File Organizer Application - Background Scheduler
Automatically sorts and moves files into folders based on their file type
Creates subfolders for each specific format within main categories
Runs in background and organizes files once per day
"""

import os
import shutil
import time
import sys
import signal
import logging
from pathlib import Path
from collections import defaultdict
from datetime import datetime, timedelta
from threading import Thread
import json


# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('file_organizer.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)


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
        'Other Docs': ['.log', '.dat', '.msg', '.eml'],
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
        try:
            files = [f for f in self.source_dir.iterdir() if f.is_file()]
        except PermissionError:
            logger.error(f"Permission denied accessing {self.source_dir}")
            return
        
        if not files:
            logger.info(f"No files found in {self.source_dir}")
            return
        
        logger.info(f"Found {len(files)} file(s) to organize")
        
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
                try:
                    target_folder.mkdir(parents=True, exist_ok=True)
                    logger.info(f"✓ Created folder: {destination_display}/")
                except PermissionError:
                    logger.error(f"Permission denied creating {destination_display}/")
                    continue
            
            # Move file to target folder
            destination = target_folder / file_path.name
            
            if dry_run:
                logger.info(f"[DRY RUN] Would move: {file_path.name} → {destination_display}/")
            else:
                if destination.exists():
                    logger.warning(f"⚠ File already exists: {destination_display}/{file_path.name} (skipping)")
                else:
                    try:
                        shutil.move(str(file_path), str(destination))
                        logger.info(f"✓ Moved: {file_path.name} → {destination_display}/")
                    except (PermissionError, shutil.Error) as e:
                        logger.error(f"Error moving {file_path.name}: {e}")
                        continue
            
            file_stats[category][subfolder] += 1
        
        logger.info("="*80)
        logger.info("ORGANIZATION SUMMARY")
        logger.info("="*80)
        
        total_files = sum(sum(subf.values()) for subf in file_stats.values())
        logger.info(f"Total files organized: {total_files}\n")
        
        for category in sorted(file_stats.keys()):
            total_in_category = sum(file_stats[category].values())
            logger.info(f"📁 {category} ({total_in_category} file(s)):")
            for subfolder, count in sorted(file_stats[category].items()):
                if subfolder:
                    logger.info(f"   └─ {subfolder}: {count} file(s)")
                else:
                    logger.info(f"   {count} file(s)")
        
        logger.info("="*80)


class ScheduledOrganizer:
    """Manages scheduled file organization in background"""
    
    CONFIG_FILE = 'organizer_config.json'
    SCHEDULE_FILE = 'organizer_schedule.json'
    
    def __init__(self):
        self.running = False
        self.directories = []
        self.interval_hours = 24  # Default: organize once per day
        self.load_config()
    
    def load_config(self):
        """Load configuration from file"""
        if os.path.exists(self.CONFIG_FILE):
            try:
                with open(self.CONFIG_FILE, 'r') as f:
                    config = json.load(f)
                    self.directories = config.get('directories', [])
                    self.interval_hours = config.get('interval_hours', 24)
                    logger.info(f"Loaded config: {len(self.directories)} directories, interval: {self.interval_hours}h")
            except Exception as e:
                logger.error(f"Error loading config: {e}")
        else:
            logger.warning("Config file not found. Using default settings.")
    
    def save_config(self):
        """Save configuration to file"""
        config = {
            'directories': self.directories,
            'interval_hours': self.interval_hours,
            'created_at': datetime.now().isoformat()
        }
        try:
            with open(self.CONFIG_FILE, 'w') as f:
                json.dump(config, f, indent=4)
                logger.info(f"Config saved: {len(self.directories)} directories")
        except Exception as e:
            logger.error(f"Error saving config: {e}")
    
    def add_directory(self, directory_path):
        """Add directory to organization list"""
        directory_path = str(Path(directory_path).resolve())
        if directory_path not in self.directories:
            self.directories.append(directory_path)
            self.save_config()
            logger.info(f"Added directory: {directory_path}")
            return True
        return False
    
    def remove_directory(self, directory_path):
        """Remove directory from organization list"""
        directory_path = str(Path(directory_path).resolve())
        if directory_path in self.directories:
            self.directories.remove(directory_path)
            self.save_config()
            logger.info(f"Removed directory: {directory_path}")
            return True
        return False
    
    def organize_now(self):
        """Organize all directories immediately"""
        logger.info("Starting manual organization...")
        for directory in self.directories:
            if not os.path.exists(directory):
                logger.warning(f"Directory not found: {directory}")
                continue
            
            try:
                organizer = FileOrganizer(directory)
                organizer.organize_files(dry_run=False)
            except Exception as e:
                logger.error(f"Error organizing {directory}: {e}")
        
        self.update_last_run_time()
    
    def update_last_run_time(self):
        """Update the last run time"""
        schedule = {
            'last_run': datetime.now().isoformat(),
            'next_run': (datetime.now() + timedelta(hours=self.interval_hours)).isoformat()
        }
        try:
            with open(self.SCHEDULE_FILE, 'w') as f:
                json.dump(schedule, f, indent=4)
        except Exception as e:
            logger.error(f"Error updating schedule: {e}")
    
    def get_next_run_time(self):
        """Get the next scheduled run time"""
        if os.path.exists(self.SCHEDULE_FILE):
            try:
                with open(self.SCHEDULE_FILE, 'r') as f:
                    schedule = json.load(f)
                    return schedule.get('next_run', 'Unknown')
            except Exception as e:
                logger.error(f"Error reading schedule: {e}")
        return 'Not scheduled'
    
    def scheduler_loop(self):
        """Background scheduler loop"""
        logger.info(f"Scheduler started - will organize every {self.interval_hours} hours")
        
        last_run = datetime.now() - timedelta(hours=self.interval_hours)  # Run immediately on start
        
        while self.running:
            now = datetime.now()
            time_since_last_run = (now - last_run).total_seconds() / 3600  # Convert to hours
            
            if time_since_last_run >= self.interval_hours:
                logger.info(f"\n{'='*80}")
                logger.info(f"🔄 Scheduled organization triggered at {now.strftime('%Y-%m-%d %H:%M:%S')}")
                logger.info(f"{'='*80}\n")
                
                self.organize_now()
                last_run = now
                
                next_run = now + timedelta(hours=self.interval_hours)
                logger.info(f"\n✅ Next organization scheduled for: {next_run.strftime('%Y-%m-%d %H:%M:%S')}\n")
            
            # Check every 60 seconds
            time.sleep(60)
    
    def start_background(self):
        """Start the scheduler in background thread"""
        if self.running:
            logger.warning("Scheduler is already running")
            return False
        
        if not self.directories:
            logger.error("No directories configured. Add directories first.")
            return False
        
        self.running = True
        scheduler_thread = Thread(target=self.scheduler_loop, daemon=True)
        scheduler_thread.start()
        logger.info("Background scheduler started")
        return True
    
    def stop_background(self):
        """Stop the background scheduler"""
        self.running = False
        logger.info("Background scheduler stopped")


def signal_handler(sig, frame):
    """Handle Ctrl+C gracefully"""
    logger.info("\nShutdown signal received")
    sys.exit(0)


def interactive_menu(organizer):
    """Interactive menu for user"""
    while True:
        print("\n" + "="*80)
        print("FILE ORGANIZER - BACKGROUND SCHEDULER")
        print("="*80)
        print("\n1. Add directory to watch")
        print("2. Remove directory from watch")
        print("3. Set interval (hours)")
        print("4. Start background scheduler")
        print("5. Organize now")
        print("6. View status")
        print("7. Exit")
        print("\nConfigured directories:")
        for i, d in enumerate(organizer.directories, 1):
            print(f"  {i}. {d}")
        
        choice = input("\nSelect option (1-7): ").strip()
        
        if choice == '1':
            path = input("Enter directory path: ").strip()
            if organizer.add_directory(path):
                print(f"✓ Added: {path}")
            else:
                print(f"⚠ Directory already added")
        
        elif choice == '2':
            if not organizer.directories:
                print("No directories configured")
                continue
            path = input("Enter directory path to remove: ").strip()
            if organizer.remove_directory(path):
                print(f"✓ Removed: {path}")
            else:
                print(f"⚠ Directory not found")
        
        elif choice == '3':
            try:
                hours = int(input("Enter interval in hours (default 24): ").strip() or "24")
                organizer.interval_hours = max(1, hours)
                organizer.save_config()
                print(f"✓ Interval set to {organizer.interval_hours} hours")
            except ValueError:
                print("Invalid input")
        
        elif choice == '4':
            if organizer.start_background():
                print("✓ Background scheduler started")
                print("The app will now run in the background")
            else:
                print("⚠ Could not start scheduler")
        
        elif choice == '5':
            print("\n🔄 Organizing now...")
            organizer.organize_now()
            print("✓ Organization complete")
        
        elif choice == '6':
            print("\n" + "-"*80)
            print("STATUS")
            print("-"*80)
            print(f"Running: {organizer.running}")
            print(f"Interval: {organizer.interval_hours} hours")
            print(f"Directories: {len(organizer.directories)}")
            print(f"Next run: {organizer.get_next_run_time()}")
            print("-"*80)
        
        elif choice == '7':
            print("Exiting...")
            break
        
        else:
            print("Invalid option")


def main():
    """Main entry point"""
    signal.signal(signal.SIGINT, signal_handler)
    
    print("="*80)
    print("FILE ORGANIZER - BACKGROUND SCHEDULER")
    print("="*80)
    print("\n✨ Professional file organization with background scheduling")
    print("🔄 Organizes files once per day automatically")
    print("📁 Supports 200+ file extensions\n")
    
    organizer = ScheduledOrganizer()
    
    # If running as daemon/background (with --daemon flag)
    if len(sys.argv) > 1 and sys.argv[1] == '--daemon':
        if not organizer.directories:
            print("Error: No directories configured. Configure first with --setup")
            sys.exit(1)
        
        print("Starting in daemon mode...")
        if organizer.start_background():
            logger.info("Daemon started - running in background")
            try:
                while True:
                    time.sleep(1)
            except KeyboardInterrupt:
                logger.info("Daemon stopped")
    else:
        # Interactive mode
        interactive_menu(organizer)


if __name__ == "__main__":
    main()
