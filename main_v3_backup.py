"""
Workspace Organizer - Enhanced Version 3.0
Complete Dark Mode Support & Advanced File Management
"""

import sys
import os
from datetime import datetime
from pathlib import Path
import json
import traceback
import shutil

try:
    from PyQt6.QtWidgets import (
        QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
        QGridLayout, QLabel, QLineEdit, QPushButton, QFileDialog, QScrollArea,
        QFrame, QListWidget, QListWidgetItem, QTextEdit, QCalendarWidget,
        QTabWidget, QPlainTextEdit, QMessageBox, QComboBox, QMenuBar, QMenu,
        QProgressBar, QSpinBox, QCheckBox, QDialog, QTableWidget, QTableWidgetItem,
        QHeaderView, QDoubleSpinBox
    )
    from PyQt6.QtCore import Qt, QDate, QSize, QTimer, pyqtSignal, QThread, pyqtSignal as Signal
    from PyQt6.QtGui import QIcon, QFont, QColor, QPixmap, QImage, QLinearGradient, QStandardItemModel
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
    traceback.print_exc()
    sys.exit(1)


class WorkspaceOrganizer(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Workspace Organizer - Advanced File Management")
        self.setGeometry(100, 100, 1600, 950)
        self.setMinimumSize(900, 700)
        
        # Initialize managers
        self.file_manager = FileManager()
        self.notes_manager = NotesManager()
        
        # Theme state
        self.dark_mode = True  # Default to dark mode
        self.current_folder = None
        self.all_files = []
        self.filtered_files = []
        
        # Setup UI
        self.setup_menu_bar()
        self.setup_ui()
        self.apply_styles()
        
        # Load initial data
        self.refresh_dashboard()
        self.setup_timers()
        
    def setup_menu_bar(self):
        """Setup the menu bar with File and View options"""
        menubar = self.menuBar()
        
        # File menu
        file_menu = menubar.addMenu("📁 File")
        
        scan_action = file_menu.addAction("🔍 Scan Folder")
        scan_action.triggered.connect(self.scan_folder)
        scan_action.setShortcut("Ctrl+O")
        
        file_menu.addSeparator()
        
        open_folder_action = file_menu.addAction("📂 Open in Explorer")
        open_folder_action.triggered.connect(self.open_folder_explorer)
        
        file_menu.addSeparator()
        
        exit_action = file_menu.addAction("❌ Exit")
        exit_action.triggered.connect(self.close)
        exit_action.setShortcut("Ctrl+Q")
        
        # View menu
        view_menu = menubar.addMenu("👁️ View")
        
        theme_action = view_menu.addAction("🌙 Toggle Theme")
        theme_action.triggered.connect(self.toggle_dark_mode)
        theme_action.setShortcut("Ctrl+D")
        
        view_menu.addSeparator()
        
        refresh_action = view_menu.addAction("🔄 Refresh")
        refresh_action.triggered.connect(self.refresh_dashboard)
        refresh_action.setShortcut("F5")
        
        # Tools menu
        tools_menu = menubar.addMenu("🛠️ Tools")
        
        organize_action = tools_menu.addAction("📋 Organize Files")
        organize_action.triggered.connect(self.organize_files_dialog)
        
        duplicate_action = tools_menu.addAction("🔍 Find Duplicates")
        duplicate_action.triggered.connect(self.find_duplicates)
        
        cleanup_action = tools_menu.addAction("🧹 Cleanup")
        cleanup_action.triggered.connect(self.cleanup_dialog)
        
        # Help menu
        help_menu = menubar.addMenu("❓ Help")
        about_action = help_menu.addAction("ℹ️ About")
        about_action.triggered.connect(self.show_about)
        
    def setup_timers(self):
        """Setup timers for periodic updates"""
        timer = QTimer()
        timer.timeout.connect(self.update_time)
        timer.start(1000)
        
    def toggle_dark_mode(self):
        """Toggle between light and dark mode"""
        self.dark_mode = not self.dark_mode
        self.apply_styles()
        # Recreate UI with new theme
        self.recreate_all_ui()
        
    def apply_styles(self):
        """Apply global stylesheet"""
        self.setStyleSheet(get_stylesheet(self.dark_mode))
        
    def recreate_all_ui(self):
        """Recreate UI to apply theme changes everywhere"""
        # Clear central widget
        central = self.centralWidget()
        if central:
            central.deleteLater()
        
        # Recreate UI
        self.setup_ui()
        self.apply_styles()
        
    def setup_ui(self):
        """Setup the main UI layout"""
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # Set background color
        bg_color = "#1e1e1e" if self.dark_mode else "#f5f7fa"
        central_widget.setStyleSheet(f"QWidget {{ background-color: {bg_color}; }}")
        
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
                border-right: 2px solid rgba(0,0,0,0.2);
            }
        """)
        layout = QVBoxLayout(frame)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(20)
        
        # App title
        title = QLabel("📊 Workspace\nOrganizer")
        title.setStyleSheet("color: white; font-size: 22px; font-weight: bold;")
        layout.addWidget(title)
        
        # Date and time display
        date_label = QLabel(f"{datetime.now().strftime('%B %d, %Y')}")
        date_label.setStyleSheet("color: white; font-size: 13px; font-weight: bold;")
        layout.addWidget(date_label)
        
        # Current time
        self.time_label = QLabel(datetime.now().strftime('%H:%M'))
        self.time_label.setStyleSheet("color: rgba(255,255,255,0.9); font-size: 20px; font-weight: bold;")
        layout.addWidget(self.time_label)
        
        # Quick stats section
        layout.addSpacing(30)
        
        stats_label = QLabel("📊 QUICK STATS")
        stats_label.setStyleSheet("color: white; font-size: 12px; font-weight: bold; letter-spacing: 1px;")
        layout.addWidget(stats_label)
        
        # File count
        self.file_count_label = QLabel("📁 Files: 0")
        self.file_count_label.setStyleSheet("color: rgba(255,255,255,0.95); font-size: 12px;")
        layout.addWidget(self.file_count_label)
        
        # Storage info
        self.storage_label = QLabel("💾 Storage: 0 B")
        self.storage_label.setStyleSheet("color: rgba(255,255,255,0.95); font-size: 12px;")
        layout.addWidget(self.storage_label)
        
        # Notes count
        self.notes_count_label = QLabel("📝 Notes: 0")
        self.notes_count_label.setStyleSheet("color: rgba(255,255,255,0.95); font-size: 12px;")
        layout.addWidget(self.notes_count_label)
        
        # Folder info
        self.folder_info_label = QLabel("📂 Folder: None")
        self.folder_info_label.setStyleSheet("color: rgba(255,255,255,0.95); font-size: 11px;")
        self.folder_info_label.setWordWrap(True)
        layout.addWidget(self.folder_info_label)
        
        layout.addStretch()
        
        # Action buttons
        scan_btn = QPushButton("🔍 SCAN FOLDER")
        scan_btn.setStyleSheet("""
            QPushButton {
                background-color: rgba(255,255,255,0.15);
                color: white;
                border: 2px solid white;
                border-radius: 25px;
                padding: 12px;
                font-weight: bold;
                font-size: 11px;
            }
            QPushButton:hover {
                background-color: rgba(255,255,255,0.25);
            }
            QPushButton:pressed {
                background-color: rgba(255,255,255,0.35);
            }
        """)
        scan_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        scan_btn.clicked.connect(self.scan_folder)
        layout.addWidget(scan_btn)
        
        organize_btn = QPushButton("📋 ORGANIZE")
        organize_btn.setStyleSheet("""
            QPushButton {
                background-color: rgba(34, 197, 94, 0.8);
                color: white;
                border: 2px solid rgba(34, 197, 94, 1);
                border-radius: 25px;
                padding: 12px;
                font-weight: bold;
                font-size: 11px;
            }
            QPushButton:hover {
                background-color: rgba(34, 197, 94, 1);
            }
            QPushButton:pressed {
                background-color: rgba(22, 163, 74, 0.9);
            }
        """)
        organize_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        organize_btn.clicked.connect(self.organize_files_dialog)
        layout.addWidget(organize_btn)
        
        return frame
    
    def create_right_content(self):
        """Create the right content area with tabs"""
        frame = QFrame()
        bg_color = "#1e1e1e" if self.dark_mode else "#f5f7fa"
        frame.setStyleSheet(f"QFrame {{ background-color: {bg_color}; }}")
        layout = QVBoxLayout(frame)
        layout.setContentsMargins(5, 5, 5, 5)
        
        # Tab widget
        self.tabs = QTabWidget()
        self.update_tab_styles()
        
        # Dashboard tab
        dashboard_widget = self.create_dashboard()
        self.tabs.addTab(dashboard_widget, "📊 Dashboard")
        
        # Files tab with advanced features
        files_widget = self.create_advanced_files_tab()
        self.tabs.addTab(files_widget, "📁 Files")
        
        # Organization tab
        org_widget = self.create_organization_tab()
        self.tabs.addTab(org_widget, "📋 Organization")
        
        # Notes tab
        notes_widget = self.create_notes_tab()
        self.tabs.addTab(notes_widget, "📝 Notes")
        
        # Analytics tab
        analytics_widget = self.create_analytics_tab()
        self.tabs.addTab(analytics_widget, "📈 Analytics")
        
        # Calendar tab
        calendar_widget = self.create_calendar_tab()
        self.tabs.addTab(calendar_widget, "📅 Calendar")
        
        layout.addWidget(self.tabs)
        return frame
    
    def update_tab_styles(self):
        """Update tab widget styles based on theme"""
        if self.dark_mode:
            tab_style = """
                QTabWidget::pane { border: none; background-color: #1e1e1e; }
                QTabBar::tab { 
                    background-color: #333; 
                    color: #e0e0e0; 
                    padding: 10px 20px; 
                    margin-right: 2px; 
                    border-radius: 4px 4px 0 0;
                    font-weight: bold;
                }
                QTabBar::tab:selected { 
                    background-color: #667eea; 
                    color: white; 
                }
                QTabBar::tab:hover:!selected {
                    background-color: #444;
                }
            """
        else:
            tab_style = """
                QTabWidget::pane { border: none; background-color: #f5f7fa; }
                QTabBar::tab { 
                    background-color: #e0e7ff; 
                    color: #333; 
                    padding: 10px 20px; 
                    margin-right: 2px; 
                    border-radius: 4px 4px 0 0;
                    font-weight: bold;
                }
                QTabBar::tab:selected { 
                    background-color: #667eea; 
                    color: white; 
                }
                QTabBar::tab:hover:!selected {
                    background-color: #d0d7ff;
                }
            """
        self.tabs.setStyleSheet(tab_style)
    
    def create_dashboard(self):
        """Create the main dashboard view"""
        widget = QWidget()
        if self.dark_mode:
            widget.setStyleSheet("background-color: #1e1e1e; color: #e0e0e0;")
        layout = QVBoxLayout(widget)
        layout.setSpacing(15)
        layout.setContentsMargins(15, 15, 15, 15)
        
        # Title
        title = QLabel("📊 Dashboard")
        title_style = "font-size: 20px; font-weight: bold; color: %s;" % ("#e0e0e0" if self.dark_mode else "#333")
        title.setStyleSheet(title_style)
        layout.addWidget(title)
        
        # Stats grid
        stats_layout = QGridLayout()
        
        self.file_stat_card = self.create_stat_card("📁 Files Scanned", "0")
        self.storage_stat_card = self.create_stat_card("💾 Storage Used", "0 B")
        self.notes_stat_card = self.create_stat_card("📝 Notes Created", "0")
        self.types_stat_card = self.create_stat_card("📂 File Types", "0")
        
        stats_layout.addWidget(self.file_stat_card, 0, 0)
        stats_layout.addWidget(self.storage_stat_card, 0, 1)
        stats_layout.addWidget(self.notes_stat_card, 0, 2)
        stats_layout.addWidget(self.types_stat_card, 0, 3)
        
        layout.addLayout(stats_layout)
        layout.addSpacing(20)
        
        # Recent files section
        recent_label = QLabel("📋 Recent Files:")
        recent_label.setStyleSheet("font-size: 14px; font-weight: bold; color: %s;" % ("#e0e0e0" if self.dark_mode else "#333"))
        layout.addWidget(recent_label)
        
        self.recent_files_list = QListWidget()
        self.recent_files_list.setMaximumHeight(180)
        layout.addWidget(self.recent_files_list)
        
        # File type breakdown
        type_label = QLabel("📊 File Type Distribution:")
        type_label.setStyleSheet("font-size: 14px; font-weight: bold; color: %s;" % ("#e0e0e0" if self.dark_mode else "#333"))
        layout.addWidget(type_label)
        
        self.file_types_list = QListWidget()
        self.file_types_list.setMaximumHeight(150)
        layout.addWidget(self.file_types_list)
        
        layout.addStretch()
        
        return widget
    
    def create_stat_card(self, title, value):
        """Create a statistic card"""
        card = QFrame()
        bg = "#2d2d2d" if self.dark_mode else "white"
        border_color = "#444" if self.dark_mode else "#e0e7ff"
        text_color = "#e0e0e0" if self.dark_mode else "#333"
        
        card.setStyleSheet(f"""
            QFrame {{
                background-color: {bg};
                border-radius: 10px;
                border: 2px solid {border_color};
            }}
        """)
        layout = QVBoxLayout(card)
        layout.setContentsMargins(15, 15, 15, 15)
        
        title_label = QLabel(title)
        title_label.setStyleSheet(f"font-size: 12px; font-weight: bold; color: {text_color};")
        layout.addWidget(title_label)
        
        value_label = QLabel(value)
        value_label.setStyleSheet(f"font-size: 20px; font-weight: bold; color: #667eea;")
        layout.addWidget(value_label)
        
        card.value_label = value_label
        return card
    
    def create_advanced_files_tab(self):
        """Create advanced file management tab"""
        widget = QWidget()
        if self.dark_mode:
            widget.setStyleSheet("background-color: #1e1e1e; color: #e0e0e0;")
        layout = QVBoxLayout(widget)
        
        # Title
        title = QLabel("📁 File Manager - Advanced")
        title.setStyleSheet("font-size: 16px; font-weight: bold; color: %s;" % ("#e0e0e0" if self.dark_mode else "#333"))
        layout.addWidget(title)
        
        # Filter and search bar
        filter_layout = QHBoxLayout()
        
        search_label = QLabel("Search:")
        search_label.setStyleSheet("color: %s;" % ("#e0e0e0" if self.dark_mode else "#333"))
        filter_layout.addWidget(search_label)
        
        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("🔍 Search files by name...")
        self.search_input.textChanged.connect(self.filter_files)
        filter_layout.addWidget(self.search_input)
        
        filter_layout.addSpacing(20)
        
        category_label = QLabel("Filter:")
        category_label.setStyleSheet("color: %s;" % ("#e0e0e0" if self.dark_mode else "#333"))
        filter_layout.addWidget(category_label)
        
        self.category_combo = QComboBox()
        self.category_combo.addItems([
            "All Files", "Documents", "Images", "Videos", "Audio", 
            "Archives", "Code", "Large Files", "Duplicates"
        ])
        self.category_combo.currentTextChanged.connect(self.apply_category_filter)
        filter_layout.addWidget(self.category_combo)
        
        filter_layout.addSpacing(20)
        
        size_label = QLabel("Min Size (MB):")
        size_label.setStyleSheet("color: %s;" % ("#e0e0e0" if self.dark_mode else "#333"))
        filter_layout.addWidget(size_label)
        
        self.size_filter = QDoubleSpinBox()
        self.size_filter.setMinimum(0)
        self.size_filter.setMaximum(10000)
        self.size_filter.setSingleStep(1)
        self.size_filter.valueChanged.connect(self.apply_category_filter)
        filter_layout.addWidget(self.size_filter)
        
        filter_layout.addStretch()
        
        layout.addLayout(filter_layout)
        
        # File table
        table_label = QLabel("📋 Files:")
        table_label.setStyleSheet("font-size: 12px; font-weight: bold; color: %s;" % ("#e0e0e0" if self.dark_mode else "#333"))
        layout.addWidget(table_label)
        
        self.file_table = QTableWidget()
        self.file_table.setColumnCount(5)
        self.file_table.setHorizontalHeaderLabels(["Name", "Size", "Type", "Modified", "Path"])
        self.file_table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        layout.addWidget(self.file_table)
        
        # Action buttons
        button_layout = QHBoxLayout()
        
        open_btn = QPushButton("📂 Open File")
        open_btn.clicked.connect(self.open_selected_file)
        button_layout.addWidget(open_btn)
        
        delete_btn = QPushButton("🗑️ Delete")
        delete_btn.setStyleSheet("QPushButton { background-color: #ef4444; }")
        delete_btn.clicked.connect(self.delete_selected_file)
        button_layout.addWidget(delete_btn)
        
        copy_btn = QPushButton("📋 Copy Path")
        copy_btn.clicked.connect(self.copy_file_path)
        button_layout.addWidget(copy_btn)
        
        button_layout.addStretch()
        layout.addLayout(button_layout)
        
        return widget
    
    def create_organization_tab(self):
        """Create file organization tab"""
        widget = QWidget()
        if self.dark_mode:
            widget.setStyleSheet("background-color: #1e1e1e; color: #e0e0e0;")
        layout = QVBoxLayout(widget)
        
        title = QLabel("📋 File Organization Tools")
        title.setStyleSheet("font-size: 16px; font-weight: bold; color: %s;" % ("#e0e0e0" if self.dark_mode else "#333"))
        layout.addWidget(title)
        
        info_label = QLabel(
            "💡 Use these tools to organize your files:\n\n"
            "• Auto-Organize: Automatically sort files into folders by type\n"
            "• Find Duplicates: Locate and manage duplicate files\n"
            "• Cleanup: Remove empty folders and temporary files\n"
            "• Archive: Compress old files\n"
            "• Move By Date: Organize by creation/modification date"
        )
        info_label.setStyleSheet("color: %s; padding: 10px;" % ("#e0e0e0" if self.dark_mode else "#333"))
        info_label.setWordWrap(True)
        layout.addWidget(info_label)
        
        layout.addSpacing(20)
        
        button_layout = QGridLayout()
        
        buttons_config = [
            ("🔄 Auto-Organize", self.organize_by_type),
            ("🔍 Find Duplicates", self.find_duplicates),
            ("🧹 Cleanup Empty", self.cleanup_empty_folders),
            ("📦 Archive Old Files", self.archive_old_files),
            ("📅 Organize by Date", self.organize_by_date),
            ("⚙️ Settings", self.show_org_settings),
        ]
        
        for idx, (label, callback) in enumerate(buttons_config):
            btn = QPushButton(label)
            btn.setMinimumHeight(60)
            btn.setStyleSheet("""
                QPushButton {
                    background-color: #667eea;
                    color: white;
                    border: none;
                    border-radius: 5px;
                    font-weight: bold;
                    font-size: 12px;
                }
                QPushButton:hover {
                    background-color: #764ba2;
                }
            """)
            btn.clicked.connect(callback)
            button_layout.addWidget(btn, idx // 2, idx % 2)
        
        layout.addLayout(button_layout)
        layout.addStretch()
        
        return widget
    
    def create_notes_tab(self):
        """Create the notes management tab"""
        widget = QWidget()
        if self.dark_mode:
            widget.setStyleSheet("background-color: #1e1e1e; color: #e0e0e0;")
        layout = QVBoxLayout(widget)
        
        title = QLabel("📝 Notes")
        title.setStyleSheet("font-size: 16px; font-weight: bold; color: %s;" % ("#e0e0e0" if self.dark_mode else "#333"))
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
        notes_list_label.setStyleSheet("font-size: 12px; font-weight: bold; color: %s;" % ("#e0e0e0" if self.dark_mode else "#333"))
        layout.addWidget(notes_list_label)
        
        self.notes_list_widget = QListWidget()
        self.notes_list_widget.setMaximumHeight(150)
        self.notes_list_widget.itemClicked.connect(self.load_note)
        layout.addWidget(self.notes_list_widget)
        
        self.refresh_notes_list()
        
        return widget
    
    def create_analytics_tab(self):
        """Create analytics and statistics tab"""
        widget = QWidget()
        if self.dark_mode:
            widget.setStyleSheet("background-color: #1e1e1e; color: #e0e0e0;")
        layout = QVBoxLayout(widget)
        
        title = QLabel("📈 Analytics & Statistics")
        title.setStyleSheet("font-size: 16px; font-weight: bold; color: %s;" % ("#e0e0e0" if self.dark_mode else "#333"))
        layout.addWidget(title)
        
        # Create analytics table
        self.analytics_table = QTableWidget()
        self.analytics_table.setColumnCount(3)
        self.analytics_table.setHorizontalHeaderLabels(["Statistic", "Value", "Details"])
        self.analytics_table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        layout.addWidget(self.analytics_table)
        
        # Refresh button
        refresh_btn = QPushButton("🔄 Refresh Analytics")
        refresh_btn.clicked.connect(self.update_analytics)
        layout.addWidget(refresh_btn)
        
        # Update analytics
        self.update_analytics()
        
        return widget
    
    def create_calendar_tab(self):
        """Create the calendar tab"""
        widget = QWidget()
        if self.dark_mode:
            widget.setStyleSheet("background-color: #1e1e1e; color: #e0e0e0;")
        layout = QVBoxLayout(widget)
        
        title = QLabel("📅 Calendar")
        title.setStyleSheet("font-size: 16px; font-weight: bold; color: %s;" % ("#e0e0e0" if self.dark_mode else "#333"))
        layout.addWidget(title)
        
        calendar = QCalendarWidget()
        layout.addWidget(calendar)
        
        return widget
    
    def scan_folder(self):
        """Scan a folder for files"""
        folder = QFileDialog.getExistingDirectory(self, "Select Folder to Organize")
        if folder:
            self.current_folder = folder
            files = self.file_manager.scan_folder(folder)
            self.all_files = files
            self.filtered_files = files
            self.update_file_display(files)
            self.refresh_dashboard()
            QMessageBox.information(self, "✅ Success", f"Scanned {len(files)} files!\n\nFolder: {Path(folder).name}")
    
    def update_file_display(self, files):
        """Update the file list display"""
        self.file_table.setRowCount(0)
        
        for idx, file_path in enumerate(files[:500]):  # Show first 500
            try:
                file_stat = os.stat(file_path)
                size_mb = file_stat.st_size / (1024 * 1024)
                mod_time = datetime.fromtimestamp(file_stat.st_mtime).strftime('%Y-%m-%d %H:%M')
                
                self.file_table.insertRow(idx)
                
                name = Path(file_path).name
                file_type = Path(file_path).suffix or "No ext"
                
                name_item = QListWidgetItem(name)
                size_item = QListWidgetItem(f"{size_mb:.2f} MB")
                type_item = QListWidgetItem(file_type)
                time_item = QListWidgetItem(mod_time)
                path_item = QListWidgetItem(file_path)
                
                self.file_table.setItem(idx, 0, QTableWidgetItem(name))
                self.file_table.setItem(idx, 1, QTableWidgetItem(f"{size_mb:.2f} MB"))
                self.file_table.setItem(idx, 2, QTableWidgetItem(file_type))
                self.file_table.setItem(idx, 3, QTableWidgetItem(mod_time))
                self.file_table.setItem(idx, 4, QTableWidgetItem(file_path))
            except:
                pass
    
    def filter_files(self, search_text):
        """Filter files by search text"""
        if not self.all_files:
            return
        
        search_text = search_text.lower()
        filtered = [f for f in self.all_files if search_text in Path(f).name.lower()]
        
        self.filtered_files = filtered
        self.apply_category_filter()
    
    def apply_category_filter(self):
        """Apply category and size filters"""
        if not self.filtered_files:
            return
        
        category = self.category_combo.currentText()
        min_size = self.size_filter.value() * 1024 * 1024  # Convert MB to bytes
        
        files_to_show = self.filtered_files
        
        # Apply category filter
        if category != "All Files":
            category_map = {
                "Documents": {'.pdf', '.doc', '.docx', '.txt', '.xlsx', '.xls', '.ppt', '.pptx', '.odt'},
                "Images": {'.jpg', '.jpeg', '.png', '.gif', '.bmp', '.svg', '.ico', '.webp'},
                "Videos": {'.mp4', '.avi', '.mkv', '.mov', '.wmv', '.flv', '.m4v'},
                "Audio": {'.mp3', '.wav', '.flac', '.aac', '.ogg', '.m4a', '.wma'},
                "Archives": {'.zip', '.rar', '.7z', '.tar', '.gz', '.bz2', '.iso'},
                "Code": {'.py', '.js', '.java', '.cpp', '.c', '.html', '.css', '.sql', '.json'},
                "Large Files": None,  # Special case
                "Duplicates": None,  # Special case
            }
            
            extensions = category_map.get(category)
            if extensions:
                files_to_show = [f for f in files_to_show if Path(f).suffix.lower() in extensions]
            elif category == "Large Files":
                files_to_show = [f for f in files_to_show if os.path.getsize(f) > min_size]
        
        # Apply size filter
        if min_size > 0:
            files_to_show = [f for f in files_to_show if os.path.getsize(f) > min_size]
        
        self.update_file_display(files_to_show)
    
    def open_selected_file(self):
        """Open selected file"""
        current_row = self.file_table.currentRow()
        if current_row >= 0:
            file_path = self.file_table.item(current_row, 4).text()
            try:
                os.startfile(file_path)
            except:
                QMessageBox.warning(self, "Error", "Could not open file")
    
    def delete_selected_file(self):
        """Delete selected file"""
        current_row = self.file_table.currentRow()
        if current_row >= 0:
            file_path = self.file_table.item(current_row, 4).text()
            
            reply = QMessageBox.question(
                self, "Confirm Delete",
                f"Are you sure you want to delete:\n{Path(file_path).name}?",
                QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
            )
            
            if reply == QMessageBox.StandardButton.Yes:
                try:
                    os.remove(file_path)
                    self.all_files.remove(file_path)
                    self.apply_category_filter()
                    QMessageBox.information(self, "✅ Success", "File deleted successfully!")
                except Exception as e:
                    QMessageBox.warning(self, "Error", f"Could not delete file:\n{str(e)}")
    
    def copy_file_path(self):
        """Copy file path to clipboard"""
        current_row = self.file_table.currentRow()
        if current_row >= 0:
            file_path = self.file_table.item(current_row, 4).text()
            from PyQt6.QtGui import QClipboard
            clipboard = QApplication.clipboard()
            clipboard.setText(file_path)
            QMessageBox.information(self, "✅ Copied", "File path copied to clipboard!")
    
    def organize_by_type(self):
        """Organize files by type into folders"""
        if not self.current_folder:
            QMessageBox.warning(self, "No Folder", "Please scan a folder first!")
            return
        
        if QMessageBox.question(
            self, "Confirm",
            "This will organize files into folders by type.\nContinue?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        ) == QMessageBox.StandardButton.Yes:
            self.file_manager.organize_by_type(self.current_folder)
            self.scan_folder()
            QMessageBox.information(self, "✅ Done", "Files organized by type!")
    
    def organize_by_date(self):
        """Organize files by date"""
        if not self.current_folder:
            QMessageBox.warning(self, "No Folder", "Please scan a folder first!")
            return
        
        if QMessageBox.question(
            self, "Confirm",
            "This will organize files into folders by date.\nContinue?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        ) == QMessageBox.StandardButton.Yes:
            self.file_manager.organize_by_date(self.current_folder)
            self.scan_folder()
            QMessageBox.information(self, "✅ Done", "Files organized by date!")
    
    def find_duplicates(self):
        """Find duplicate files"""
        if not self.all_files:
            QMessageBox.warning(self, "No Files", "Please scan a folder first!")
            return
        
        QMessageBox.information(self, "🔍 Finding", "Scanning for duplicates...\n\nThis may take a moment for large folders.")
        duplicates = self.file_manager.find_duplicates(self.all_files)
        
        if duplicates:
            msg = "Found duplicate files:\n\n"
            for group in list(duplicates.values())[:5]:  # Show first 5 groups
                msg += f"• {len(group)} copies of: {Path(group[0]).name}\n"
            QMessageBox.information(self, "✅ Results", msg)
        else:
            QMessageBox.information(self, "✅ Results", "No duplicates found!")
    
    def cleanup_empty_folders(self):
        """Remove empty folders"""
        if not self.current_folder:
            QMessageBox.warning(self, "No Folder", "Please scan a folder first!")
            return
        
        if QMessageBox.question(
            self, "Confirm",
            "This will remove empty folders.\nContinue?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        ) == QMessageBox.StandardButton.Yes:
            count = self.file_manager.cleanup_empty_folders(self.current_folder)
            QMessageBox.information(self, "✅ Done", f"Removed {count} empty folders!")
    
    def archive_old_files(self):
        """Archive old files"""
        QMessageBox.information(self, "📦 Archive", "Archive feature coming soon!")
    
    def cleanup_dialog(self):
        """Show cleanup dialog"""
        QMessageBox.information(self, "🧹 Cleanup", "Cleanup tools available in Organization tab!")
    
    def organize_files_dialog(self):
        """Show organize dialog"""
        self.tabs.setCurrentIndex(2)  # Switch to Organization tab
    
    def open_folder_explorer(self):
        """Open current folder in explorer"""
        if self.current_folder:
            try:
                os.startfile(self.current_folder)
            except:
                QMessageBox.warning(self, "Error", "Could not open folder")
        else:
            QMessageBox.warning(self, "No Folder", "Please scan a folder first!")
    
    def show_org_settings(self):
        """Show organization settings"""
        QMessageBox.information(self, "⚙️ Settings", "Settings dialog coming soon!")
    
    def refresh_dashboard(self):
        """Refresh the dashboard data"""
        if self.all_files:
            total_files = len(self.all_files)
            self.file_count_label.setText(f"📁 Files: {total_files}")
            self.file_stat_card.value_label.setText(str(total_files))
            
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
            
            # File type breakdown
            self.file_types_list.clear()
            categorized = self.file_manager.categorize_files()
            for category, files in categorized.items():
                if files:
                    self.file_types_list.addItem(QListWidgetItem(f"📂 {category}: {len(files)} files"))
            
            # Update types count
            unique_types = len(set(Path(f).suffix.lower() for f in self.all_files))
            self.types_stat_card.value_label.setText(str(unique_types))
        
        # Update notes count
        all_notes = self.notes_manager.get_all_notes()
        self.notes_count_label.setText(f"📝 Notes: {len(all_notes)}")
        self.notes_stat_card.value_label.setText(str(len(all_notes)))
        
        # Update folder display
        if self.current_folder:
            folder_name = Path(self.current_folder).name
            self.folder_info_label.setText(f"📂 {folder_name}")
    
    def update_analytics(self):
        """Update analytics table"""
        self.analytics_table.setRowCount(0)
        
        if not self.all_files:
            return
        
        stats = [
            ("Total Files", str(len(self.all_files)), "All files in folder"),
            ("Total Size", self.file_manager.get_total_storage(), "Combined size"),
            ("File Types", str(len(set(Path(f).suffix for f in self.all_files))), "Unique extensions"),
            ("Largest File", self.get_largest_file_info(), "Biggest file"),
            ("Average Size", f"{sum(os.path.getsize(f) for f in self.all_files) / len(self.all_files) / 1024 / 1024:.2f} MB", "Per file"),
        ]
        
        for idx, (stat, value, detail) in enumerate(stats):
            self.analytics_table.insertRow(idx)
            self.analytics_table.setItem(idx, 0, QTableWidgetItem(stat))
            self.analytics_table.setItem(idx, 1, QTableWidgetItem(value))
            self.analytics_table.setItem(idx, 2, QTableWidgetItem(detail))
    
    def get_largest_file_info(self):
        """Get info about largest file"""
        if not self.all_files:
            return "N/A"
        
        largest = max(self.all_files, key=lambda f: os.path.getsize(f))
        size = os.path.getsize(largest) / (1024 * 1024)
        return f"{Path(largest).name} ({size:.2f} MB)"
    
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
            QMessageBox.information(self, "✅ Success", "Note saved successfully!")
        else:
            QMessageBox.warning(self, "Empty Note", "Please write something before saving!")
    
    def refresh_notes_list(self):
        """Refresh the notes list"""
        self.notes_list_widget.clear()
        all_notes = self.notes_manager.get_all_notes()
        
        for note in reversed(all_notes):
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
            "About Workspace Organizer v3.0",
            "🎉 Advanced File Management & Productivity Dashboard\n\n"
            "Professional-grade features:\n"
            "✅ Advanced file management with filtering\n"
            "✅ Auto-organization by type & date\n"
            "✅ Duplicate file detection\n"
            "✅ File analytics & statistics\n"
            "✅ Complete dark mode support\n"
            "✅ Notes with timestamps\n"
            "✅ Calendar planning\n"
            "✅ Folder cleanup tools\n\n"
            "Made with ❤️ for productivity enthusiasts!"
        )


def main():
    app = QApplication(sys.argv)
    window = WorkspaceOrganizer()
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
