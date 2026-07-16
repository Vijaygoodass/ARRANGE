#!/usr/bin/env python3
"""
File Organizer Application
Automatically sorts and moves files into folders based on their file type
"""

import os
import shutil
from pathlib import Path
from collections import defaultdict


# File type to folder mapping
FILE_CATEGORIES = {
    # Images
    'Images': ['.jpg', '.jpeg', '.png', '.gif', '.bmp', '.svg', '.webp', '.ico', '.tiff'],
    
    # Documents
    'Documents': ['.pdf', '.doc', '.docx', '.txt', '.xls', '.xlsx', '.ppt', '.pptx', '.odt'],
    
    # Videos
    'Videos': ['.mp4', '.avi', '.mov', '.mkv', '.flv', '.wmv', '.webm', '.m4v'],
    
    # Audio
    'Audio': ['.mp3', '.wav', '.flac', '.aac', '.wma', '.ogg', '.m4a', '.alac'],
    
    # Archives
    'Archives': ['.zip', '.rar', '.7z', '.tar', '.gz', '.bz2', '.iso'],
    
    # Code
    'Code': ['.py', '.js', '.ts', '.java', '.c', '.cpp', '.go', '.rs', '.rb', '.php', '.html', '.css'],
    
    # Spreadsheets
    'Spreadsheets': ['.csv', '.tsv'],
}


class FileOrganizer:
    """Organizes files into folders based on their type"""
    
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
    
    def get_file_category(self, file_extension):
        """
        Determine the category of a file based on its extension
        
        Args:
            file_extension (str): File extension (e.g., '.pdf')
            
        Returns:
            str: Category folder name or 'Others' if not categorized
        """
        file_extension = file_extension.lower()
        
        for category, extensions in FILE_CATEGORIES.items():
            if file_extension in extensions:
                return category
        
        return 'Others'
    
    def organize_files(self, dry_run=False):
        """
        Organize files into folders based on their type
        
        Args:
            dry_run (bool): If True, show what would be moved without actually moving
        """
        file_stats = defaultdict(int)
        
        # Get all files in the directory (non-recursive)
        files = [f for f in self.source_dir.iterdir() if f.is_file()]
        
        if not files:
            print(f"No files found in {self.source_dir}")
            return
        
        print(f"Found {len(files)} file(s) to organize\n")
        
        for file_path in files:
            file_extension = file_path.suffix
            category = self.get_file_category(file_extension)
            
            # Create category folder if it doesn't exist
            category_folder = self.source_dir / category
            
            if not category_folder.exists() and not dry_run:
                category_folder.mkdir(parents=True, exist_ok=True)
                print(f"✓ Created folder: {category}/")
            
            # Move file to category folder
            destination = category_folder / file_path.name
            
            if dry_run:
                print(f"[DRY RUN] Would move: {file_path.name} → {category}/")
            else:
                if destination.exists():
                    print(f"⚠ File already exists: {category}/{file_path.name} (skipping)")
                else:
                    shutil.move(str(file_path), str(destination))
                    print(f"✓ Moved: {file_path.name} → {category}/")
            
            file_stats[category] += 1
        
        print("\n" + "="*50)
        print("ORGANIZATION SUMMARY")
        print("="*50)
        
        for category in sorted(file_stats.keys()):
            print(f"{category}: {file_stats[category]} file(s)")
        
        print("="*50)
    
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


def main():
    """Main entry point"""
    import sys
    
    print("=" * 50)
    print("FILE ORGANIZER APPLICATION")
    print("=" * 50)
    print("\nThis app organizes files into folders by type:\n")
    
    for category, extensions in FILE_CATEGORIES.items():
        print(f"  {category}: {', '.join(extensions[:3])}...")
    
    print("\n")
    
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
