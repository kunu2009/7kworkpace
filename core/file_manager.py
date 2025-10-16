"""
File Manager - Handle file operations and scanning
"""

import os
import json
from pathlib import Path
from datetime import datetime
from typing import List, Dict


class FileManager:
    def __init__(self):
        self.files_cache = []
        self.config_file = Path.home() / ".workspace_organizer" / "config.json"
        self.load_config()
    
    def load_config(self):
        """Load configuration"""
        self.config_file.parent.mkdir(parents=True, exist_ok=True)
        if self.config_file.exists():
            with open(self.config_file, 'r') as f:
                self.config = json.load(f)
        else:
            self.config = {"watched_folders": []}
    
    def save_config(self):
        """Save configuration"""
        with open(self.config_file, 'w') as f:
            json.dump(self.config, f, indent=2)
    
    def scan_folder(self, folder_path: str, max_depth: int = 3) -> List[str]:
        """Scan folder for all files"""
        files = []
        try:
            for root, dirs, filenames in os.walk(folder_path):
                depth = root.replace(folder_path, '').count(os.sep)
                if depth > max_depth:
                    dirs.clear()
                    continue
                
                for filename in filenames:
                    file_path = os.path.join(root, filename)
                    files.append(file_path)
            
            self.files_cache = files
            return files
        except Exception as e:
            print(f"Error scanning folder: {e}")
            return []
    
    def get_recent_files(self, limit: int = 20) -> List[str]:
        """Get recently modified files"""
        if not self.files_cache:
            return []
        
        try:
            recent = sorted(
                self.files_cache,
                key=lambda x: os.path.getmtime(x),
                reverse=True
            )
            return recent[:limit]
        except:
            return self.files_cache[:limit]
    
    def get_total_storage(self) -> str:
        """Get total storage size"""
        if not self.files_cache:
            return "0 B"
        
        try:
            total_size = sum(
                os.path.getsize(f) for f in self.files_cache
                if os.path.exists(f)
            )
            
            for unit in ['B', 'KB', 'MB', 'GB']:
                if total_size < 1024:
                    return f"{total_size:.1f} {unit}"
                total_size /= 1024
            
            return f"{total_size:.1f} TB"
        except:
            return "Unknown"
    
    def categorize_files(self) -> Dict[str, List[str]]:
        """Categorize files by type"""
        categories = {
            'Documents': [],
            'Images': [],
            'Videos': [],
            'Audio': [],
            'Archives': [],
            'Other': []
        }
        
        doc_ext = {'.pdf', '.doc', '.docx', '.txt', '.xlsx', '.xls', '.ppt', '.pptx'}
        img_ext = {'.jpg', '.jpeg', '.png', '.gif', '.bmp', '.svg', '.ico'}
        video_ext = {'.mp4', '.avi', '.mkv', '.mov', '.wmv', '.flv'}
        audio_ext = {'.mp3', '.wav', '.flac', '.aac', '.ogg', '.m4a'}
        arch_ext = {'.zip', '.rar', '.7z', '.tar', '.gz', '.bz2'}
        
        for file_path in self.files_cache:
            ext = Path(file_path).suffix.lower()
            
            if ext in doc_ext:
                categories['Documents'].append(file_path)
            elif ext in img_ext:
                categories['Images'].append(file_path)
            elif ext in video_ext:
                categories['Videos'].append(file_path)
            elif ext in audio_ext:
                categories['Audio'].append(file_path)
            elif ext in arch_ext:
                categories['Archives'].append(file_path)
            else:
                categories['Other'].append(file_path)
        
        return categories
    
    def search_files(self, query: str) -> List[str]:
        """Search files by name"""
        query = query.lower()
        return [f for f in self.files_cache if query in Path(f).name.lower()]
    
    def organize_by_type(self, folder_path: str) -> int:
        """Organize files into folders by type"""
        organized_count = 0
        categorized = self.categorize_files()
        
        base_path = Path(folder_path)
        
        for category, files in categorized.items():
            if not files:
                continue
            
            # Create category folder
            category_folder = base_path / category
            category_folder.mkdir(exist_ok=True)
            
            # Move files
            for file_path in files:
                try:
                    file_obj = Path(file_path)
                    if file_obj.parent != category_folder:
                        shutil.move(str(file_obj), str(category_folder / file_obj.name))
                        organized_count += 1
                except:
                    pass
        
        return organized_count
    
    def organize_by_date(self, folder_path: str) -> int:
        """Organize files into folders by date"""
        organized_count = 0
        base_path = Path(folder_path)
        
        for file_path in self.files_cache:
            try:
                file_obj = Path(file_path)
                mod_time = datetime.fromtimestamp(os.path.getmtime(file_path))
                
                # Create date folder (YYYY/MM/DD)
                date_folder = base_path / str(mod_time.year) / f"{mod_time.month:02d}" / f"{mod_time.day:02d}"
                date_folder.mkdir(parents=True, exist_ok=True)
                
                if file_obj.parent != date_folder:
                    shutil.move(str(file_obj), str(date_folder / file_obj.name))
                    organized_count += 1
            except:
                pass
        
        return organized_count
    
    def find_duplicates(self, files: List[str]) -> Dict[str, List[str]]:
        """Find duplicate files by size and hash"""
        import hashlib
        
        duplicates = {}
        size_map = {}
        
        # Group by size first
        for file_path in files:
            try:
                size = os.path.getsize(file_path)
                if size not in size_map:
                    size_map[size] = []
                size_map[size].append(file_path)
            except:
                pass
        
        # Check files with same size for hash
        for size, file_list in size_map.items():
            if len(file_list) < 2:
                continue
            
            hash_map = {}
            for file_path in file_list:
                try:
                    with open(file_path, 'rb') as f:
                        file_hash = hashlib.md5(f.read()).hexdigest()
                    
                    if file_hash not in hash_map:
                        hash_map[file_hash] = []
                    hash_map[file_hash].append(file_path)
                except:
                    pass
            
            # Store duplicates
            for file_hash, dup_list in hash_map.items():
                if len(dup_list) > 1:
                    duplicates[file_hash] = dup_list
        
        return duplicates
    
    def cleanup_empty_folders(self, folder_path: str) -> int:
        """Remove empty folders"""
        removed_count = 0
        base_path = Path(folder_path)
        
        for root, dirs, files in os.walk(base_path, topdown=False):
            for dir_name in dirs:
                dir_path = Path(root) / dir_name
                try:
                    if not os.listdir(dir_path):
                        os.rmdir(dir_path)
                        removed_count += 1
                except:
                    pass
        
        return removed_count
