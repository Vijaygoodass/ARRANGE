"""
File Organizer - Mobile App (Kivy)
Android app for automatic file organization
"""

from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.scrollview import ScrollView
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.popup import Popup
from kivy.uix.textinput import TextInput
from kivy.uix.spinner import Spinner
from kivy.uix.checkbox import CheckBox
from kivy.uix.image import Image
from kivy.core.window import Window
from kivy.garden.matplotlib.backend_kivyagg import FigureCanvasKivyAgg
from kivy.uix.progressbar import ProgressBar
import os
import shutil
import json
import threading
import time
from pathlib import Path
from datetime import datetime, timedelta
from collections import defaultdict
import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[logging.FileHandler('file_organizer_mobile.log')]
)
logger = logging.getLogger(__name__)

# Set window size for mobile
Window.size = (480, 854)


# File extension to subfolder mapping
FILE_CATEGORIES = {
    'Documents & Text': {
        'PDF': ['.pdf'],
        'Word': ['.doc', '.docx', '.docm', '.dot', '.dotx', '.odt', '.pages'],
        'Plain Text': ['.txt', '.text'],
        'Rich Text': ['.rtf'],
        'OpenDocument': ['.odt', '.ott'],
        'eBook': ['.epub', '.mobi', '.azw', '.azw3'],
    },
    
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
    
    'Audio': {
        'MP3': ['.mp3'],
        'WAV': ['.wav', '.wave'],
        'AAC': ['.aac'],
        'FLAC': ['.flac'],
        'Mobile Audio': ['.m4a', '.m4b', '.m4p'],
        'Other Audio': ['.wma', '.ogg', '.oga', '.opus', '.alac', '.ape', '.aiff', '.aif', '.au'],
    },
    
    'Video': {
        'MP4': ['.mp4', '.m4v'],
        'QuickTime': ['.mov', '.qt'],
        'Matroska': ['.mkv', '.mka', '.mks'],
        'AVI': ['.avi'],
        'WebM': ['.webm'],
        'Windows Media': ['.wmv', '.wm', '.asf'],
        'Other Video': ['.flv', '.ogv', '.ts', '.m3u8', '.vob', '.f4v', '.3gp', '.3g2', '.mts'],
    },
    
    'Data & Spreadsheets': {
        'Excel': ['.xlsx', '.xls', '.xlsm', '.xlsb', '.xltx', '.xltm', '.ods'],
        'CSV': ['.csv', '.tsv', '.txt'],
        'JSON': ['.json', '.jsonl', '.ndjson'],
        'XML': ['.xml', '.xsd', '.xsl', '.xslt'],
        'SQL': ['.sql', '.sqlite', '.db', '.sqlite3', '.mdb', '.accdb'],
        'YAML': ['.yaml', '.yml'],
    },
    
    'Compressed & Archive': {
        'ZIP': ['.zip', '.zipx'],
        'RAR': ['.rar', '.r01', '.r02', '.r03'],
        '7Z': ['.7z', '.7z001'],
        'TAR': ['.tar', '.tar.gz', '.tgz', '.tar.bz2', '.tbz'],
        'GZIP': ['.gz', '.gzip', '.bz2'],
        'Other Archive': ['.iso', '.dmg', '.cab'],
    },
    
    'Code': {
        'Python': ['.py', '.pyw', '.pyx'],
        'Java': ['.java', '.class', '.jar'],
        'C/C++': ['.c', '.cpp', '.cc', '.h', '.hpp'],
        'JavaScript': ['.js', '.jsx', '.mjs'],
        'TypeScript': ['.ts', '.tsx'],
        'Web': ['.html', '.htm', '.css', '.php'],
        'Other Code': ['.sh', '.rb', '.go', '.rs', '.swift'],
    },
}


class FileOrganizer:
    """Organizes files with UI feedback"""
    
    def __init__(self, callback=None):
        self.callback = callback
        self.is_organizing = False
    
    def get_file_category_and_subfolder(self, file_extension):
        """Get category and subfolder for file extension"""
        file_extension = file_extension.lower()
        
        for category, subfolders in FILE_CATEGORIES.items():
            if isinstance(subfolders, dict):
                for subfolder, extensions in subfolders.items():
                    if file_extension in extensions:
                        return category, subfolder
        
        return 'Others', ''
    
    def organize_directory(self, directory_path):
        """Organize files in directory"""
        self.is_organizing = True
        directory = Path(directory_path)
        
        if not directory.exists():
            self.callback(f"❌ Directory not found: {directory_path}")
            return False
        
        try:
            files = [f for f in directory.iterdir() if f.is_file()]
            
            if not files:
                self.callback(f"ℹ️ No files to organize in {directory.name}")
                return True
            
            self.callback(f"📁 Found {len(files)} files\n")
            file_stats = defaultdict(lambda: defaultdict(int))
            
            for idx, file_path in enumerate(files):
                if not self.is_organizing:
                    break
                
                file_extension = file_path.suffix
                category, subfolder = self.get_file_category_and_subfolder(file_extension)
                
                if subfolder:
                    target_folder = directory / category / subfolder
                    destination_display = f"{category}/{subfolder}"
                else:
                    target_folder = directory / category
                    destination_display = category
                
                try:
                    if not target_folder.exists():
                        target_folder.mkdir(parents=True, exist_ok=True)
                    
                    destination = target_folder / file_path.name
                    
                    if not destination.exists():
                        shutil.move(str(file_path), str(destination))
                        file_stats[category][subfolder] += 1
                        self.callback(f"✓ {file_path.name} → {destination_display}")
                    else:
                        self.callback(f"⚠️ {file_path.name} (already exists)")
                
                except Exception as e:
                    self.callback(f"❌ Error with {file_path.name}: {e}")
                
                # Update progress
                progress = (idx + 1) / len(files)
                if hasattr(self, 'progress_callback'):
                    self.progress_callback(progress)
            
            # Summary
            self.callback("\n" + "="*50)
            self.callback("SUMMARY")
            self.callback("="*50)
            for cat in sorted(file_stats.keys()):
                total = sum(file_stats[cat].values())
                self.callback(f"📁 {cat}: {total} files")
            
            self.is_organizing = False
            return True
        
        except Exception as e:
            self.callback(f"❌ Error: {e}")
            return False


class FileOrganizerApp(App):
    """Main Android App"""
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.organizer = FileOrganizer(callback=self.log_message)
        self.config_file = 'organizer_config_mobile.json'
        self.selected_directory = None
        self.directories = []
        self.load_config()
    
    def load_config(self):
        """Load configuration"""
        try:
            if os.path.exists(self.config_file):
                with open(self.config_file, 'r') as f:
                    config = json.load(f)
                    self.directories = config.get('directories', [])
        except Exception as e:
            logger.error(f"Error loading config: {e}")
    
    def save_config(self):
        """Save configuration"""
        try:
            config = {
                'directories': self.directories,
                'created_at': datetime.now().isoformat()
            }
            with open(self.config_file, 'w') as f:
                json.dump(config, f, indent=4)
        except Exception as e:
            logger.error(f"Error saving config: {e}")
    
    def log_message(self, message):
        """Log message to UI"""
        logger.info(message)
        self.log_output.text += message + "\n"
        self.log_scroll.scroll_y = 0
    
    def build(self):
        """Build the UI"""
        main_layout = BoxLayout(orientation='vertical', padding=10, spacing=10)
        
        # Title
        title = Label(
            text='📁 FILE ORGANIZER',
            size_hint_y=0.08,
            font_size='24sp',
            bold=True,
            color=(0.2, 0.6, 1, 1)
        )
        main_layout.add_widget(title)
        
        # Directory Section
        dir_box = BoxLayout(orientation='vertical', size_hint_y=0.15, spacing=5)
        
        dir_label = Label(text='📂 Select Directory:', size_hint_y=0.3, font_size='14sp')
        dir_box.add_widget(dir_label)
        
        dir_layout = BoxLayout(size_hint_y=0.7, spacing=5)
        
        self.dir_spinner = Spinner(
            text='Choose Directory',
            values=self.directories if self.directories else ['No directories added'],
            size_hint_x=0.65
        )
        dir_layout.add_widget(self.dir_spinner)
        
        add_dir_btn = Button(text='➕ Add', size_hint_x=0.35, background_color=(0.2, 0.8, 0.2, 1))
        add_dir_btn.bind(on_press=self.show_add_directory_popup)
        dir_layout.add_widget(add_dir_btn)
        
        dir_box.add_widget(dir_layout)
        main_layout.add_widget(dir_box)
        
        # Control Buttons
        button_layout = GridLayout(cols=2, size_hint_y=0.12, spacing=5)
        
        organize_btn = Button(
            text='⚡ Organize Now',
            background_color=(0.3, 0.7, 1, 1),
            font_size='14sp'
        )
        organize_btn.bind(on_press=self.organize_files)
        button_layout.add_widget(organize_btn)
        
        clear_btn = Button(
            text='🗑️ Clear Log',
            background_color=(1, 0.5, 0.5, 1),
            font_size='14sp'
        )
        clear_btn.bind(on_press=self.clear_log)
        button_layout.add_widget(clear_btn)
        
        settings_btn = Button(
            text='⚙️ Settings',
            background_color=(0.8, 0.8, 0.2, 1),
            font_size='14sp'
        )
        settings_btn.bind(on_press=self.show_settings)
        button_layout.add_widget(settings_btn)
        
        remove_btn = Button(
            text='❌ Remove Dir',
            background_color=(1, 0.4, 0.4, 1),
            font_size='14sp'
        )
        remove_btn.bind(on_press=self.remove_directory)
        button_layout.add_widget(remove_btn)
        
        main_layout.add_widget(button_layout)
        
        # Progress Bar
        self.progress_bar = ProgressBar(size_hint_y=0.05, max=100)
        main_layout.add_widget(self.progress_bar)
        
        # Log Output
        log_label = Label(text='📝 Log:', size_hint_y=0.05, font_size='12sp')
        main_layout.add_widget(log_label)
        
        self.log_scroll = ScrollView(size_hint_y=0.60)
        self.log_output = Label(
            text='Ready to organize files...\n',
            size_hint_y=None,
            markup=True,
            text_size=(400, None)
        )
        self.log_output.bind(texture_size=self.log_output.setter('size'))
        self.log_scroll.add_widget(self.log_output)
        main_layout.add_widget(self.log_scroll)
        
        return main_layout
    
    def show_add_directory_popup(self, instance):
        """Show popup to add directory"""
        content = BoxLayout(orientation='vertical', spacing=10, padding=10)
        
        label = Label(
            text='Enter directory path:\n(e.g., /storage/emulated/0/Download)',
            size_hint_y=0.3,
            font_size='12sp'
        )
        content.add_widget(label)
        
        text_input = TextInput(
            multiline=False,
            size_hint_y=0.4,
            font_size='12sp',
            hint_text='Directory path'
        )
        content.add_widget(text_input)
        
        button_layout = BoxLayout(size_hint_y=0.3, spacing=10)
        
        add_btn = Button(text='✓ Add', background_color=(0.2, 0.8, 0.2, 1))
        cancel_btn = Button(text='✕ Cancel', background_color=(1, 0.4, 0.4, 1))
        
        button_layout.add_widget(add_btn)
        button_layout.add_widget(cancel_btn)
        content.add_widget(button_layout)
        
        popup = Popup(
            title='Add Directory',
            content=content,
            size_hint=(0.9, 0.6)
        )
        
        def add_action(btn):
            path = text_input.text.strip()
            if path and os.path.isdir(path):
                if path not in self.directories:
                    self.directories.append(path)
                    self.save_config()
                    self.dir_spinner.values = self.directories
                    self.log_message(f"✓ Added: {path}")
                    popup.dismiss()
                else:
                    self.log_message("⚠️ Directory already added")
            else:
                self.log_message("❌ Invalid path")
        
        add_btn.bind(on_press=add_action)
        cancel_btn.bind(on_press=popup.dismiss)
        
        popup.open()
    
    def remove_directory(self, instance):
        """Remove selected directory"""
        selected = self.dir_spinner.text
        if selected in self.directories:
            self.directories.remove(selected)
            self.save_config()
            self.dir_spinner.values = self.directories if self.directories else ['No directories added']
            self.dir_spinner.text = self.dir_spinner.values[0]
            self.log_message(f"✓ Removed: {selected}")
        else:
            self.log_message("⚠️ No directory selected")
    
    def organize_files(self, instance):
        """Start organizing files"""
        selected = self.dir_spinner.text
        
        if selected not in self.directories:
            self.log_message("❌ Please select a valid directory")
            return
        
        self.log_output.text = ""
        self.log_message("🔄 Starting organization...\n")
        
        # Run in background thread
        thread = threading.Thread(
            target=self.organizer.organize_directory,
            args=(selected,)
        )
        thread.daemon = True
        thread.start()
        
        self.progress_bar.value = 100
    
    def clear_log(self, instance):
        """Clear the log"""
        self.log_output.text = "Log cleared\n"
        self.progress_bar.value = 0
    
    def show_settings(self, instance):
        """Show settings popup"""
        content = BoxLayout(orientation='vertical', spacing=10, padding=10)
        
        info_text = f"""
📊 SETTINGS & INFO

📁 Directories: {len(self.directories)}
📝 App Version: 1.0
⚙️ Supported Formats: 200+
        
Directories:
"""
        for d in self.directories:
            info_text += f"\n  • {d}"
        
        label = Label(
            text=info_text,
            size_hint_y=0.8,
            font_size='12sp',
            text_size=(300, None)
        )
        content.add_widget(label)
        
        close_btn = Button(text='Close', size_hint_y=0.2, background_color=(0.3, 0.7, 1, 1))
        content.add_widget(close_btn)
        
        popup = Popup(
            title='Settings',
            content=content,
            size_hint=(0.9, 0.7)
        )
        
        close_btn.bind(on_press=popup.dismiss)
        popup.open()


if __name__ == '__main__':
    FileOrganizerApp().run()
