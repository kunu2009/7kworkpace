"""
Workspace Organizer - Productivity Dashboard
A beautiful desktop application for organizing files, notes, and tracking productivity
Now with Dark Mode and Full Functionality!
"""

import sys
import os
from datetime import datetime
from pathlib import Path
import json
import traceback

try:
    from PyQt6.QtWidgets import (
        QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
        QGridLayout, QLabel, QLineEdit, QPushButton, QFileDialog, QScrollArea,
        QFrame, QListWidget, QListWidgetItem, QTextEdit, QCalendarWidget,
        QTabWidget, QPlainTextEdit, QMessageBox, QComboBox, QMenuBar, QMenu
    )
    from PyQt6.QtCore import Qt, QDate, QSize, QTimer, pyqtSignal
    from PyQt6.QtGui import QIcon, QFont, QColor, QPixmap, QImage, QLinearGradient
except ImportError as e:
    print("❌ Error: PyQt6 is not installed!")
    print("   Please run: python -m pip install -r requirements.txt")
    sys.exit(1)

try:
    from ui.styles import get_stylesheet
    from core.file_manager import FileManager
    from core.notes_manager import NotesManager
except ImportError as e:
    print(f"❌ Error importing modules: {e}")
    print("   Make sure all files are in correct folders")
    traceback.print_exc()
    sys.exit(1)


class WorkspaceOrganizer(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Workspace Organizer - Productivity Dashboard")
        self.setGeometry(100, 100, 1400, 900)
        self.setMinimumSize(800, 600)
        
        # Initialize managers
        self.file_manager = FileManager()
        self.notes_manager = NotesManager()
        
        # Theme state
        self.dark_mode = False
        self.current_folder = None
        
        # Setup UI
        self.setup_menu_bar()
        self.setup_ui()
        self.apply_styles()
        
        # Load initial data
        self.refresh_dashboard()
        
        # Start time updater
        self.setup_timers()
        
    def setup_menu_bar(self):
        """Setup the menu bar with File and View options"""
        menubar = self.menuBar()
        
        # File menu
        file_menu = menubar.addMenu("📁 File")
        
        scan_action = file_menu.addAction("Scan Folder")
        scan_action.triggered.connect(self.scan_folder)
        scan_action.setShortcut("Ctrl+O")
        
        file_menu.addSeparator()
        
        exit_action = file_menu.addAction("Exit")
        exit_action.triggered.connect(self.close)
        exit_action.setShortcut("Ctrl+Q")
        
        # View menu
        view_menu = menubar.addMenu("👁️ View")
        
        theme_action = view_menu.addAction("Toggle Dark Mode")
        theme_action.triggered.connect(self.toggle_dark_mode)
        theme_action.setShortcut("Ctrl+D")
        
        # Help menu
        help_menu = menubar.addMenu("❓ Help")
        about_action = help_menu.addAction("About")
        about_action.triggered.connect(self.show_about)
        
    def setup_timers(self):
        """Setup timers for periodic updates"""
        # Update time every second
        timer = QTimer()
        timer.timeout.connect(self.update_time)
        timer.start(1000)
        
    def toggle_dark_mode(self):
        """Toggle between light and dark mode"""
        self.dark_mode = not self.dark_mode
        self.apply_styles()
        
    def setup_ui(self):
        """Setup the main UI layout"""
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # Main layout
        main_layout = QHBoxLayout(central_widget)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)
        
        # Left sidebar
        left_sidebar = self.create_left_sidebar()
        main_layout.addWidget(left_sidebar, 2)
        
        # Right content area
        right_content = self.create_right_content()
        main_layout.addWidget(right_content, 5)
        
    def create_left_sidebar(self):
        """Create the left sidebar with date/time and quick stats"""
        frame = QFrame()
        if self.dark_mode:
            frame.setStyleSheet("""
                QFrame {
                    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                    border-right: 2px solid rgba(0,0,0,0.3);
                }
            """)
        else:
            frame.setStyleSheet("""
                QFrame {
                    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                    border-right: 2px solid rgba(0,0,0,0.1);
                }
            """)
        layout = QVBoxLayout(frame)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(20)
        
        # App title
        title = QLabel("Workspace\nOrganizer")
        title.setStyleSheet("color: white; font-size: 22px; font-weight: bold;")
        layout.addWidget(title)
        
        # Date and time display
        date_label = QLabel(f"{datetime.now().strftime('%B %d, %Y')}")
        date_label.setStyleSheet("color: white; font-size: 14px; font-weight: bold; margin-top: 10px;")
        layout.addWidget(date_label)
        
        # Current time
        self.time_label = QLabel(datetime.now().strftime('%H:%M'))
        self.time_label.setStyleSheet("color: rgba(255,255,255,0.9); font-size: 18px; font-weight: bold;")
        layout.addWidget(self.time_label)
        
        # Quick stats section
        layout.addSpacing(30)
        
        stats_label = QLabel("📊 Quick Stats")
        stats_label.setStyleSheet("color: white; font-size: 12px; font-weight: bold;")
        layout.addWidget(stats_label)
        
        # File count
        self.file_count_label = QLabel("📁 Files: 0")
        self.file_count_label.setStyleSheet("color: rgba(255,255,255,0.9); font-size: 11px;")
        layout.addWidget(self.file_count_label)
        
        # Storage info
        self.storage_label = QLabel("💾 Storage: 0 B")
        self.storage_label.setStyleSheet("color: rgba(255,255,255,0.9); font-size: 11px;")
        layout.addWidget(self.storage_label)
        
        # Notes count
        self.notes_count_label = QLabel("📝 Notes: 0")
        self.notes_count_label.setStyleSheet("color: rgba(255,255,255,0.9); font-size: 11px;")
        layout.addWidget(self.notes_count_label)
        
        layout.addStretch()
        
        # Action buttons
        scan_btn = QPushButton("🔍 Scan Folder")
        scan_btn.setStyleSheet("""
            QPushButton {
                background-color: rgba(255,255,255,0.2);
                color: white;
                border: 2px solid white;
                border-radius: 20px;
                padding: 12px;
                font-weight: bold;
                font-size: 11px;
            }
            QPushButton:hover {
                background-color: rgba(255,255,255,0.3);
            }
        """)
        scan_btn.clicked.connect(self.scan_folder)
        layout.addWidget(scan_btn)
        
        return frame
    
    def create_right_content(self):
        """Create the right content area with tabs"""
        frame = QFrame()
        if self.dark_mode:
            frame.setStyleSheet("QFrame { background-color: #1e1e1e; }")
        else:
            frame.setStyleSheet("QFrame { background-color: #f5f7fa; }")
        layout = QVBoxLayout(frame)
        layout.setContentsMargins(10, 10, 10, 10)
        
        # Tab widget
        self.tabs = QTabWidget()
        
        # Dashboard tab
        dashboard_widget = self.create_dashboard()
        self.tabs.addTab(dashboard_widget, "📊 Dashboard")
        
        # Files tab
        files_widget = self.create_files_tab()
        self.tabs.addTab(files_widget, "📁 Files")
        
        # Notes tab
        notes_widget = self.create_notes_tab()
        self.tabs.addTab(notes_widget, "📝 Notes")
        
        # Calendar tab
        calendar_widget = self.create_calendar_tab()
        self.tabs.addTab(calendar_widget, "📅 Calendar")
        
        layout.addWidget(self.tabs)
        return frame
    
    def create_dashboard(self):
        """Create the main dashboard view"""
        widget = QWidget()
        layout = QVBoxLayout(widget)
        layout.setSpacing(15)
        layout.setContentsMargins(15, 15, 15, 15)
        
        # Title
        title = QLabel("📊 Dashboard")
        title.setStyleSheet("font-size: 18px; font-weight: bold;")
        layout.addWidget(title)
        
        # Stats grid
        stats_layout = QGridLayout()
        
        # Create stat cards
        self.file_stat_card = self.create_stat_card("📁 Files Scanned", "0")
        self.storage_stat_card = self.create_stat_card("💾 Storage Used", "0 B")
        self.notes_stat_card = self.create_stat_card("📝 Notes Created", "0")
        self.folder_stat_card = self.create_stat_card("📂 Current Folder", "None")
        
        stats_layout.addWidget(self.file_stat_card, 0, 0)
        stats_layout.addWidget(self.storage_stat_card, 0, 1)
        stats_layout.addWidget(self.notes_stat_card, 0, 2)
        stats_layout.addWidget(self.folder_stat_card, 0, 3)
        
        layout.addLayout(stats_layout)
        layout.addSpacing(20)
        
        # Recent files section
        recent_label = QLabel("📋 Recent Files:")
        recent_label.setStyleSheet("font-size: 14px; font-weight: bold;")
        layout.addWidget(recent_label)
        
        self.recent_files_list = QListWidget()
        self.recent_files_list.setMaximumHeight(150)
        layout.addWidget(self.recent_files_list)
        
        layout.addStretch()
        
        return widget
    
    def create_stat_card(self, title, value):
        """Create a statistic card"""
        card = QFrame()
        if self.dark_mode:
            card.setStyleSheet("""
                QFrame {
                    background-color: #2d2d2d;
                    border-radius: 10px;
                    border: 2px solid #444;
                }
            """)
        else:
            card.setStyleSheet("""
                QFrame {
                    background-color: white;
                    border-radius: 10px;
                    border: 2px solid #e0e7ff;
                }
            """)
        layout = QVBoxLayout(card)
        layout.setContentsMargins(15, 15, 15, 15)
        
        title_label = QLabel(title)
        title_label.setStyleSheet("font-size: 12px; font-weight: bold;")
        layout.addWidget(title_label)
        
        value_label = QLabel(value)
        value_label.setStyleSheet("font-size: 18px; font-weight: bold; color: #667eea;")
        layout.addWidget(value_label)
        
        card.value_label = value_label  # Store reference for updates
        return card
    
    def create_files_tab(self):
        """Create the files management tab"""
        widget = QWidget()
        layout = QVBoxLayout(widget)
        
        # Title
        title = QLabel("📁 File Manager")
        title.setStyleSheet("font-size: 18px; font-weight: bold;")
        layout.addWidget(title)
        
        # Search/Filter bar
        search_layout = QHBoxLayout()
        
        search_label = QLabel("Search:")
        search_layout.addWidget(search_label)
        
        search_input = QLineEdit()
        search_input.setPlaceholderText("🔍 Search files...")
        search_layout.addWidget(search_input)
        
        layout.addLayout(search_layout)
        
        # File list
        self.file_list_widget = QListWidget()
        layout.addWidget(self.file_list_widget)
        
        # Category filter
        category_layout = QHBoxLayout()
        category_layout.addWidget(QLabel("Filter by type:"))
        
        category_combo = QComboBox()
        category_combo.addItems(["All Files", "Documents", "Images", "Videos", "Audio", "Archives"])
        category_layout.addWidget(category_combo)
        category_layout.addStretch()
        
        layout.addLayout(category_layout)
        
        # Connect search
        search_input.textChanged.connect(lambda: self.filter_files(search_input.text()))
        category_combo.currentTextChanged.connect(lambda: self.filter_by_category(category_combo.currentText()))
        
        return widget
    
    def create_notes_tab(self):
        """Create the notes management tab"""
        widget = QWidget()
        layout = QVBoxLayout(widget)
        
        # Title
        title = QLabel("📝 Notes")
        title.setStyleSheet("font-size: 18px; font-weight: bold;")
        layout.addWidget(title)
        
        # Button layout
        button_layout = QHBoxLayout()
        
        new_note_btn = QPushButton("➕ New Note")
        new_note_btn.setStyleSheet("""
            QPushButton {
                background-color: #667eea;
                color: white;
                border: none;
                border-radius: 5px;
                padding: 8px 16px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #764ba2;
            }
        """)
        new_note_btn.clicked.connect(self.create_new_note)
        button_layout.addWidget(new_note_btn)
        
        save_note_btn = QPushButton("💾 Save Note")
        save_note_btn.setStyleSheet("""
            QPushButton {
                background-color: #22c55e;
                color: white;
                border: none;
                border-radius: 5px;
                padding: 8px 16px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #16a34a;
            }
        """)
        save_note_btn.clicked.connect(self.save_current_note)
        button_layout.addWidget(save_note_btn)
        
        clear_btn = QPushButton("🗑️ Clear")
        clear_btn.setStyleSheet("""
            QPushButton {
                background-color: #ef4444;
                color: white;
                border: none;
                border-radius: 5px;
                padding: 8px 16px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #dc2626;
            }
        """)
        clear_btn.clicked.connect(lambda: self.notes_display.clear())
        button_layout.addWidget(clear_btn)
        
        button_layout.addStretch()
        layout.addLayout(button_layout)
        
        # Notes display
        self.notes_display = QPlainTextEdit()
        self.notes_display.setPlaceholderText("✍️ Type your note here...\n\nNotes are auto-saved with timestamp!")
        layout.addWidget(self.notes_display)
        
        # Notes list
        notes_list_label = QLabel("📚 All Notes:")
        layout.addWidget(notes_list_label)
        
        self.notes_list_widget = QListWidget()
        self.notes_list_widget.setMaximumHeight(150)
        self.notes_list_widget.itemClicked.connect(self.load_note)
        layout.addWidget(self.notes_list_widget)
        
        self.refresh_notes_list()
        
        return widget
    
    def create_calendar_tab(self):
        """Create the calendar tab"""
        widget = QWidget()
        layout = QVBoxLayout(widget)
        
        # Title
        title = QLabel("📅 Calendar")
        title.setStyleSheet("font-size: 18px; font-weight: bold;")
        layout.addWidget(title)
        
        calendar = QCalendarWidget()
        layout.addWidget(calendar)
        
        return widget
    
    def apply_styles(self):
        """Apply global stylesheet"""
        self.setStyleSheet(get_stylesheet(self.dark_mode))
        
    def scan_folder(self):
        """Scan a folder for files"""
        folder = QFileDialog.getExistingDirectory(self, "Select Folder to Organize")
        if folder:
            self.current_folder = folder
            files = self.file_manager.scan_folder(folder)
            self.update_file_display(files)
            self.refresh_dashboard()
            QMessageBox.information(self, "Success", f"✅ Scanned {len(files)} files!")
    
    def update_file_display(self, files):
        """Update the file list display"""
        self.file_list_widget.clear()
        self.all_files = files
        
        for file_path in files[:100]:  # Show first 100 files
            item = QListWidgetItem(Path(file_path).name)
            item.setToolTip(str(file_path))
            self.file_list_widget.addItem(item)
    
    def filter_files(self, search_text):
        """Filter files by search text"""
        if not hasattr(self, 'all_files'):
            return
        
        self.file_list_widget.clear()
        
        for file_path in self.all_files:
            if search_text.lower() in Path(file_path).name.lower():
                item = QListWidgetItem(Path(file_path).name)
                item.setToolTip(str(file_path))
                self.file_list_widget.addItem(item)
    
    def filter_by_category(self, category):
        """Filter files by category"""
        if category == "All Files":
            self.update_file_display(self.all_files if hasattr(self, 'all_files') else [])
            return
        
        if not hasattr(self, 'all_files'):
            return
        
        # Map category names to extensions
        category_map = {
            "Documents": {'.pdf', '.doc', '.docx', '.txt', '.xlsx', '.xls', '.ppt', '.pptx'},
            "Images": {'.jpg', '.jpeg', '.png', '.gif', '.bmp', '.svg', '.ico'},
            "Videos": {'.mp4', '.avi', '.mkv', '.mov', '.wmv', '.flv'},
            "Audio": {'.mp3', '.wav', '.flac', '.aac', '.ogg', '.m4a'},
            "Archives": {'.zip', '.rar', '.7z', '.tar', '.gz', '.bz2'}
        }
        
        extensions = category_map.get(category, set())
        
        self.file_list_widget.clear()
        for file_path in self.all_files:
            if Path(file_path).suffix.lower() in extensions:
                item = QListWidgetItem(Path(file_path).name)
                item.setToolTip(str(file_path))
                self.file_list_widget.addItem(item)
    
    def refresh_dashboard(self):
        """Refresh the dashboard data"""
        # Update file stats
        if hasattr(self, 'all_files'):
            total_files = len(self.all_files)
            self.file_count_label.setText(f"📁 Files: {total_files}")
            self.file_stat_card.value_label.setText(str(total_files))
            
            # Update storage
            storage_size = self.file_manager.get_total_storage()
            self.storage_label.setText(f"💾 Storage: {storage_size}")
            self.storage_stat_card.value_label.setText(storage_size)
            
            # Update recent files
            recent = self.file_manager.get_recent_files(10)
            self.recent_files_list.clear()
            for f in recent:
                item = QListWidgetItem(Path(f).name)
                item.setToolTip(str(f))
                self.recent_files_list.addItem(item)
        
        # Update notes count
        all_notes = self.notes_manager.get_all_notes()
        self.notes_count_label.setText(f"📝 Notes: {len(all_notes)}")
        self.notes_stat_card.value_label.setText(str(len(all_notes)))
        
        # Update folder display
        if self.current_folder:
            folder_name = Path(self.current_folder).name
            self.folder_stat_card.value_label.setText(folder_name)
    
    def update_time(self):
        """Update the time display"""
        self.time_label.setText(datetime.now().strftime('%H:%M'))
    
    def create_new_note(self):
        """Create a new note"""
        self.notes_display.clear()
        self.notes_display.setFocus()
    
    def save_current_note(self):
        """Save the current note"""
        note_text = self.notes_display.toPlainText()
        if note_text.strip():
            self.notes_manager.save_note(note_text)
            self.notes_display.clear()
            self.refresh_notes_list()
            self.refresh_dashboard()
            QMessageBox.information(self, "Success", "✅ Note saved successfully!")
        else:
            QMessageBox.warning(self, "Empty Note", "⚠️ Please write something before saving!")
    
    def refresh_notes_list(self):
        """Refresh the notes list"""
        self.notes_list_widget.clear()
        all_notes = self.notes_manager.get_all_notes()
        
        for note in reversed(all_notes):  # Show newest first
            title = note.get('title', 'Untitled')
            item = QListWidgetItem(f"📝 {title}")
            item.setData(Qt.ItemDataRole.UserRole, note.get('id'))
            self.notes_list_widget.addItem(item)
    
    def load_note(self, item):
        """Load a note from the list"""
        note_id = item.data(Qt.ItemDataRole.UserRole)
        note = self.notes_manager.get_note_by_id(note_id)
        
        if note:
            self.notes_display.setPlainText(note['content'])
    
    def show_about(self):
        """Show about dialog"""
        QMessageBox.information(
            self,
            "About Workspace Organizer",
            "🎉 Workspace Organizer v2.0\n\n"
            "A beautiful productivity dashboard for organizing files and notes.\n\n"
            "Features:\n"
            "✅ File scanning and organization\n"
            "✅ Notes management with timestamps\n"
            "✅ Calendar view\n"
            "✅ Dark mode support\n"
            "✅ File statistics and storage info\n\n"
            "Made with ❤️ for productivity enthusiasts!"
        )


def main():
    app = QApplication(sys.argv)
    window = WorkspaceOrganizer()
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
