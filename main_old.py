"""
Workspace Organizer - Productivity Dashboard
A beautiful desktop application for organizing files, notes, and tracking productivity
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
        QTabWidget, QPlainTextEdit, QMessageBox
    )
    from PyQt6.QtCore import Qt, QDate, QSize, QTimer, pyqtSignal
    from PyQt6.QtGui import QIcon, QFont, QColor, QPixmap, QImage, QLinearGradient
    from PyQt6.QtCore import QTimer
except ImportError as e:
    print("❌ Error: PyQt6 is not installed!")
    print("   Please run: python -m pip install -r requirements.txt")
    sys.exit(1)

try:
    from ui.styles import get_stylesheet
    from ui.widgets import (
        StatsCard, FileCard, NoteCard, CustomCalendar,
        RoundedButton, GradientFrame
    )
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
        
        # Initialize managers
        self.file_manager = FileManager()
        self.notes_manager = NotesManager()
        
        # Setup UI
        self.setup_ui()
        self.apply_styles()
        
        # Load initial data
        self.refresh_dashboard()
        
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
        frame.setStyleSheet("""
            QFrame {
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                border-right: 2px solid rgba(0,0,0,0.1);
            }
        """)
        layout = QVBoxLayout(frame)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(20)
        
        # Date and time display
        date_label = QLabel(f"{datetime.now().strftime('%B %d, %Y')}")
        date_label.setStyleSheet("color: white; font-size: 18px; font-weight: bold;")
        layout.addWidget(date_label)
        
        # Current time
        self.time_label = QLabel(datetime.now().strftime('%H:%M'))
        self.time_label.setStyleSheet("color: rgba(255,255,255,0.8); font-size: 14px;")
        layout.addWidget(self.time_label)
        
        # Update time every second
        timer = QTimer()
        timer.timeout.connect(self.update_time)
        timer.start(1000)
        
        layout.addSpacing(30)
        
        # Quick stats
        stats_label = QLabel("Quick Stats")
        stats_label.setStyleSheet("color: white; font-size: 14px; font-weight: bold;")
        layout.addWidget(stats_label)
        
        # File count
        self.file_count_label = QLabel()
        self.file_count_label.setStyleSheet("color: rgba(255,255,255,0.9); font-size: 12px;")
        layout.addWidget(self.file_count_label)
        
        # Storage info
        self.storage_label = QLabel()
        self.storage_label.setStyleSheet("color: rgba(255,255,255,0.9); font-size: 12px;")
        layout.addWidget(self.storage_label)
        
        layout.addStretch()
        
        # Action buttons
        scan_btn = RoundedButton("Scan Folder")
        scan_btn.setStyleSheet("""
            QPushButton {
                background-color: rgba(255,255,255,0.2);
                color: white;
                border: 2px solid white;
                border-radius: 20px;
                padding: 10px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: rgba(255,255,255,0.3);
            }
        """)
        scan_btn.clicked.connect(self.scan_folder)
        layout.addWidget(scan_btn)
        
        settings_btn = RoundedButton("Settings")
        settings_btn.setStyleSheet("""
            QPushButton {
                background-color: rgba(255,255,255,0.2);
                color: white;
                border: 2px solid white;
                border-radius: 20px;
                padding: 10px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: rgba(255,255,255,0.3);
            }
        """)
        layout.addWidget(settings_btn)
        
        return frame
    
    def create_right_content(self):
        """Create the right content area with tabs"""
        frame = QFrame()
        frame.setStyleSheet("QFrame { background-color: #f5f7fa; }")
        layout = QVBoxLayout(frame)
        layout.setContentsMargins(10, 10, 10, 10)
        
        # Tab widget
        tabs = QTabWidget()
        tabs.setStyleSheet("""
            QTabWidget::pane {
                border: none;
                background-color: #f5f7fa;
            }
            QTabBar::tab {
                background-color: #e0e7ff;
                color: #333;
                padding: 8px 20px;
                margin-right: 2px;
                border-radius: 4px;
                font-weight: bold;
            }
            QTabBar::tab:selected {
                background-color: #667eea;
                color: white;
            }
        """)
        
        # Dashboard tab
        dashboard_widget = self.create_dashboard()
        tabs.addTab(dashboard_widget, "📊 Dashboard")
        
        # Files tab
        files_widget = self.create_files_tab()
        tabs.addTab(files_widget, "📁 Files")
        
        # Notes tab
        notes_widget = self.create_notes_tab()
        tabs.addTab(notes_widget, "📝 Notes")
        
        # Calendar tab
        calendar_widget = self.create_calendar_tab()
        tabs.addTab(calendar_widget, "📅 Calendar")
        
        layout.addWidget(tabs)
        return frame
    
    def create_dashboard(self):
        """Create the main dashboard view"""
        widget = QWidget()
        layout = QGridLayout(widget)
        layout.setSpacing(15)
        layout.setContentsMargins(15, 15, 15, 15)
        
        # Top row: Date/Time widgets
        date_card = GradientFrame("#667eea", "#764ba2")
        date_layout = QVBoxLayout(date_card)
        date_label = QLabel(f"JULY\n'24")
        date_label.setStyleSheet("color: white; font-size: 28px; font-weight: bold; text-align: center;")
        date_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        date_layout.addWidget(date_label)
        layout.addWidget(date_card, 0, 0, 1, 1)
        
        # Image placeholder
        image_card = QFrame()
        image_card.setStyleSheet("""
            QFrame {
                background-color: white;
                border-radius: 10px;
                border: 2px solid #e0e7ff;
            }
        """)
        image_layout = QVBoxLayout(image_card)
        image_label = QLabel("🖼️ Inspiration")
        image_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        image_label.setStyleSheet("color: #666; font-size: 14px;")
        image_layout.addWidget(image_label)
        layout.addWidget(image_card, 0, 1, 1, 1)
        
        # Music player card
        music_card = QFrame()
        music_card.setStyleSheet("""
            QFrame {
                background-color: #1a1a1a;
                border-radius: 10px;
            }
        """)
        music_layout = QVBoxLayout(music_card)
        music_label = QLabel("🎵 Now Playing\nJULIANA SILVA - HAPPY")
        music_label.setStyleSheet("color: white; font-size: 12px; text-align: center; font-weight: bold;")
        music_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        music_layout.addWidget(music_label)
        layout.addWidget(music_card, 1, 0, 1, 2)
        
        # Right column: Notes and Files
        # Notes section
        notes_card = QFrame()
        notes_card.setStyleSheet("""
            QFrame {
                background-color: white;
                border-radius: 10px;
                border: 2px solid #e0e7ff;
            }
        """)
        notes_layout = QVBoxLayout(notes_card)
        notes_title = QLabel("📋 NOTES")
        notes_title.setStyleSheet("color: #333; font-weight: bold; font-size: 12px;")
        notes_layout.addWidget(notes_title)
        
        self.notes_list = QListWidget()
        self.notes_list.setStyleSheet("""
            QListWidget {
                border: none;
                background-color: transparent;
            }
            QListWidget::item {
                border: none;
                padding: 5px;
                height: 25px;
            }
        """)
        notes_layout.addWidget(self.notes_list)
        layout.addWidget(notes_card, 0, 2, 2, 1)
        
        # Files section
        files_card = QFrame()
        files_card.setStyleSheet("""
            QFrame {
                background-color: #1a1a1a;
                border-radius: 10px;
                border: 2px solid #333;
            }
        """)
        files_layout = QVBoxLayout(files_card)
        files_title = QLabel("📂 FILES")
        files_title.setStyleSheet("color: white; font-weight: bold; font-size: 12px;")
        files_layout.addWidget(files_title)
        
        # File grid
        grid = QGridLayout()
        self.file_thumbnails = []
        for i in range(6):
            file_item = QFrame()
            file_item.setStyleSheet("""
                QFrame {
                    background-color: #333;
                    border-radius: 5px;
                    border: 1px solid #555;
                }
            """)
            file_item.setMinimumSize(50, 50)
            self.file_thumbnails.append(file_item)
            grid.addWidget(file_item, i // 3, i % 3)
        
        files_layout.addLayout(grid)
        layout.addWidget(files_card, 0, 3, 2, 1)
        
        # Bottom: System stats
        stats_frame = QFrame()
        stats_layout = QHBoxLayout(stats_frame)
        
        # Wifi, notifications, battery
        status_labels = ["📶 WiFi", "🔔 Alerts", "🔋 95%"]
        for label_text in status_labels:
            label = QLabel(label_text)
            label.setStyleSheet("color: #666; font-size: 11px;")
            stats_layout.addWidget(label)
        
        stats_layout.addStretch()
        
        layout.addWidget(stats_frame, 3, 0, 1, 4)
        
        return widget
    
    def create_files_tab(self):
        """Create the files management tab"""
        widget = QWidget()
        layout = QVBoxLayout(widget)
        
        # Search/Filter bar
        search_layout = QHBoxLayout()
        search_input = QLineEdit()
        search_input.setPlaceholderText("🔍 Search files...")
        search_input.setStyleSheet("""
            QLineEdit {
                padding: 10px;
                border: 2px solid #e0e7ff;
                border-radius: 5px;
                font-size: 12px;
            }
        """)
        search_layout.addWidget(search_input)
        layout.addLayout(search_layout)
        
        # File list
        self.file_list_widget = QListWidget()
        self.file_list_widget.setStyleSheet("""
            QListWidget {
                border: 2px solid #e0e7ff;
                border-radius: 5px;
                background-color: white;
            }
        """)
        layout.addWidget(self.file_list_widget)
        
        return widget
    
    def create_notes_tab(self):
        """Create the notes management tab"""
        widget = QWidget()
        layout = QVBoxLayout(widget)
        
        # New note button
        new_note_btn = QPushButton("+ New Note")
        new_note_btn.setStyleSheet("""
            QPushButton {
                background-color: #667eea;
                color: white;
                border: none;
                border-radius: 5px;
                padding: 10px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #764ba2;
            }
        """)
        new_note_btn.clicked.connect(self.create_new_note)
        layout.addWidget(new_note_btn)
        
        # Notes display
        self.notes_display = QPlainTextEdit()
        self.notes_display.setStyleSheet("""
            QPlainTextEdit {
                border: 2px solid #e0e7ff;
                border-radius: 5px;
                padding: 10px;
                font-size: 12px;
            }
        """)
        layout.addWidget(self.notes_display)
        
        return widget
    
    def create_calendar_tab(self):
        """Create the calendar tab"""
        widget = QWidget()
        layout = QVBoxLayout(widget)
        
        calendar = QCalendarWidget()
        calendar.setStyleSheet("""
            QCalendarWidget {
                background-color: white;
                border: 2px solid #e0e7ff;
                border-radius: 5px;
            }
            QCalendarWidget QAbstractItemView {
                selection-background-color: #667eea;
                color: #333;
            }
        """)
        layout.addWidget(calendar)
        
        return widget
    
    def apply_styles(self):
        """Apply global stylesheet"""
        self.setStyleSheet("""
            QMainWindow {
                background-color: #f5f7fa;
            }
            QLabel {
                color: #333;
            }
            QLineEdit, QTextEdit, QPlainTextEdit {
                background-color: white;
                border: 2px solid #e0e7ff;
                border-radius: 5px;
                padding: 5px;
                color: #333;
            }
        """)
    
    def scan_folder(self):
        """Scan a folder for files"""
        folder = QFileDialog.getExistingDirectory(self, "Select Folder to Organize")
        if folder:
            files = self.file_manager.scan_folder(folder)
            self.update_file_display(files)
    
    def update_file_display(self, files):
        """Update the file list display"""
        self.file_list_widget.clear()
        for file_path in files[:20]:  # Show first 20 files
            item = QListWidgetItem(Path(file_path).name)
            item.setToolTip(str(file_path))
            self.file_list_widget.addItem(item)
    
    def refresh_dashboard(self):
        """Refresh the dashboard data"""
        # Update file stats
        total_files = len(self.file_manager.get_recent_files())
        self.file_count_label.setText(f"📁 Files: {total_files}")
        
        # Update storage
        storage_size = self.file_manager.get_total_storage()
        self.storage_label.setText(f"💾 Storage: {storage_size}")
    
    def update_time(self):
        """Update the time display"""
        self.time_label.setText(datetime.now().strftime('%H:%M'))
    
    def create_new_note(self):
        """Create a new note"""
        note_text = self.notes_display.toPlainText()
        if note_text.strip():
            self.notes_manager.save_note(note_text)
            self.notes_display.clear()


def main():
    app = QApplication(sys.argv)
    window = WorkspaceOrganizer()
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
