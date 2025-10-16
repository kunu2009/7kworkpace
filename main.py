"""
Workspace Organizer - Version 4.0
Complete Dark Mode + Advanced Folder Operations + Productivity Tools
"""

import sys
import os
from datetime import datetime
from pathlib import Path
import json
import traceback
import shutil
import subprocess
import platform

try:
    from PyQt6.QtWidgets import (
        QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
        QGridLayout, QLabel, QLineEdit, QPushButton, QFileDialog, QScrollArea,
        QFrame, QListWidget, QListWidgetItem, QTextEdit, QCalendarWidget,
        QTabWidget, QPlainTextEdit, QMessageBox, QComboBox, QMenuBar, QMenu,
        QProgressBar, QSpinBox, QCheckBox, QDialog, QTableWidget, QTableWidgetItem,
        QHeaderView, QDoubleSpinBox, QTreeWidget, QTreeWidgetItem, QProgressBar
    )
    from PyQt6.QtCore import Qt, QDate, QSize, QTimer, pyqtSignal, QThread, QDateTime, QTime
    from PyQt6.QtGui import QIcon, QFont, QColor, QPixmap, QImage, QLinearGradient, QKeySequence, QShortcut
except ImportError as e:
    print(f"❌ Error: PyQt6 import failed!")
    print(f"   Error details: {e}")
    print(f"   Python: {sys.executable}")
    print(f"   Version: {sys.version}")
    sys.exit(1)

try:
    from ui.styles import get_stylesheet
    from core.file_manager import FileManager
    from core.notes_manager import NotesManager
except ImportError as e:
    print(f"❌ Error importing modules: {e}")
    traceback.print_exc()
    sys.exit(1)


class PomodoroTimer:
    """Simple Pomodoro timer management"""
    def __init__(self):
        self.work_duration = 25 * 60  # 25 minutes
        self.break_duration = 5 * 60  # 5 minutes
        self.remaining = self.work_duration
        self.is_work = True
        self.is_running = False


class TodoItem:
    """Todo item with title, completion status, and pinning"""
    def __init__(self, title, priority="Normal"):
        self.title = title
        self.priority = priority
        self.completed = False
        self.created_date = datetime.now()
        self.is_pinned = False  # NEW: Pin/star functionality


class KanbanTask:
    """Kanban task with status, priority, and pinning"""
    def __init__(self, title, status="To Do", priority="Normal"):
        self.title = title
        self.status = status  # To Do, In Progress, Done
        self.priority = priority
        self.is_pinned = False  # NEW: Pin/star functionality


class WorkspaceOrganizer(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Workspace Organizer v4.0 - Advanced File Management")
        self.setGeometry(100, 100, 1700, 1000)
        self.setMinimumSize(1000, 700)
        
        # Initialize managers
        self.file_manager = FileManager()
        self.notes_manager = NotesManager()
        
        # Theme state
        self.dark_mode = True  # Default to dark mode
        self.current_folder = None
        self.all_files = []
        self.filtered_files = []
        
        # Productivity features
        self.todos = []
        self.kanban_tasks = []
        self.pomodoro = PomodoroTimer()
        
        # Search features
        self.search_history = []  # Store last 10 searches
        self.search_results = []  # Current search results
        self.max_history = 10
        
        # Statistics tracking
        self.stats = {
            'files_organized_today': 0,
            'tasks_completed': 0,
            'pomodoro_sessions': 0,
            'pomodoro_hours': 0,
            'current_streak': 0,
            'total_files_organized': 0,
            'total_tasks_completed': 0
        }
        self.today_date = datetime.now().date()
        
        # Setup UI
        self.setup_menu_bar()
        self.setup_ui()
        self.apply_styles()
        self.setup_keyboard_shortcuts()
        
        # Load initial data - default to Desktop
        desktop_path = str(Path.home() / "Desktop")
        self.current_folder = desktop_path
        self.scan_folder_auto(desktop_path)
        self.refresh_dashboard()
        self.setup_timers()
        
    def setup_menu_bar(self):
        """Setup the menu bar with File and View options"""
        menubar = self.menuBar()
        menubar.setStyleSheet("background-color: #2d2d2d; color: #e0e0e0;" if self.dark_mode else "background-color: white; color: #333;")
        
        # File menu
        file_menu = menubar.addMenu("📁 File")
        
        scan_action = file_menu.addAction("🔍 Scan Folder")
        scan_action.triggered.connect(self.scan_folder)
        scan_action.setShortcut("Ctrl+O")
        
        file_menu.addSeparator()
        
        open_vscode_action = file_menu.addAction("💻 Open Folder in VS Code")
        open_vscode_action.triggered.connect(self.open_in_vscode)
        
        open_explorer_action = file_menu.addAction("📂 Open in Explorer")
        open_explorer_action.triggered.connect(self.open_folder_explorer)
        
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
        # Store as instance variables so they don't get garbage collected
        self.time_timer = QTimer()
        self.time_timer.timeout.connect(self.update_time)
        self.time_timer.start(1000)
        
        self.pomodoro_timer = QTimer()
        self.pomodoro_timer.timeout.connect(self.update_pomodoro)
        self.pomodoro_timer.start(1000)
    
    def setup_keyboard_shortcuts(self):
        """Setup keyboard shortcuts for common actions"""
        # Ctrl+N: New Todo
        shortcut_new_todo = QShortcut(QKeySequence("Ctrl+N"), self)
        shortcut_new_todo.activated.connect(self.focus_todo_input)
        
        # Ctrl+K: New Kanban Task
        shortcut_new_kanban = QShortcut(QKeySequence("Ctrl+K"), self)
        shortcut_new_kanban.activated.connect(self.focus_kanban_input)
        
        # Ctrl+S: Save (save note or organize)
        shortcut_save = QShortcut(QKeySequence("Ctrl+S"), self)
        shortcut_save.activated.connect(self.quick_save)
        
        # Ctrl+Q: Quit (already in menu, but adding shortcut ensures it works)
        shortcut_quit = QShortcut(QKeySequence("Ctrl+Q"), self)
        shortcut_quit.activated.connect(self.close)
        
        # Alt+O: Organize Files
        shortcut_organize = QShortcut(QKeySequence("Alt+O"), self)
        shortcut_organize.activated.connect(self.organize_files_dialog)
        
        # Alt+S: Scan Folder
        shortcut_scan = QShortcut(QKeySequence("Alt+S"), self)
        shortcut_scan.activated.connect(self.scan_folder)
        
        # Alt+T: Toggle dark mode
        shortcut_theme = QShortcut(QKeySequence("Alt+T"), self)
        shortcut_theme.activated.connect(self.toggle_dark_mode)
        
        # Ctrl+F: Focus search (NEW)
        shortcut_search = QShortcut(QKeySequence("Ctrl+F"), self)
        shortcut_search.activated.connect(self.focus_search_input)
        
        # Ctrl+P: Pin/Unpin selected item
        shortcut_pin = QShortcut(QKeySequence("Ctrl+P"), self)
        shortcut_pin.activated.connect(self.pin_current_item)
    
    def focus_todo_input(self):
        """Focus on todo input field (Ctrl+N)"""
        try:
            # Switch to Todo tab
            for i in range(self.tabs.count()):
                if "Todo" in self.tabs.tabText(i):
                    self.tabs.setCurrentIndex(i)
                    break
            # Focus on input
            if hasattr(self, 'todo_input'):
                self.todo_input.setFocus()
                self.todo_input.selectAll()
        except:
            pass
    
    def focus_kanban_input(self):
        """Focus on kanban input field (Ctrl+K)"""
        try:
            # Switch to Kanban tab
            for i in range(self.tabs.count()):
                if "Kanban" in self.tabs.tabText(i):
                    self.tabs.setCurrentIndex(i)
                    break
            # Focus on input
            if hasattr(self, 'kanban_input'):
                self.kanban_input.setFocus()
                self.kanban_input.selectAll()
        except:
            pass
    
    def focus_search_input(self):
        """Focus on search input field (Ctrl+F)"""
        try:
            # Switch to Search tab
            for i in range(self.tabs.count()):
                if "Search" in self.tabs.tabText(i):
                    self.tabs.setCurrentIndex(i)
                    break
            # Focus on search input
            if hasattr(self, 'search_input'):
                self.search_input.setFocus()
                self.search_input.selectAll()
        except:
            pass
    
    def pin_current_item(self):
        """Pin/unpin the currently selected item based on active tab (Ctrl+P)"""
        try:
            current_tab_index = self.tabs.currentIndex()
            current_tab_text = self.tabs.tabText(current_tab_index)
            
            if "Todo" in current_tab_text and hasattr(self, 'todo_list'):
                self.pin_todo()
            elif "Kanban" in current_tab_text:
                # Pin the currently selected item in the active kanban column
                for column in [self.kanban_todo_list, self.kanban_progress_list, self.kanban_done_list]:
                    list_widget = getattr(column, 'list_widget', None)
                    if list_widget and list_widget.hasFocus():
                        self.pin_kanban_task(list_widget)
                        return
        except:
            pass
    
    def quick_save(self):
        """Quick save action (Ctrl+S)"""
        try:
            # If notes tab is active, save note
            current_tab = self.tabs.currentWidget()
            if hasattr(self, 'notes_text') and self.notes_text.hasFocus():
                self.save_note()
            else:
                # General save message
                QMessageBox.information(self, "Saved", "Changes saved! 💾")
        except Exception as e:
            QMessageBox.warning(self, "Save Error", f"Save failed: {e}")
        
    def toggle_dark_mode(self):
        """Toggle between light and dark mode"""
        self.dark_mode = not self.dark_mode
        self.apply_styles()
        self.recreate_all_ui()
        
    def apply_styles(self):
        """Apply global stylesheet"""
        self.setStyleSheet(get_stylesheet(self.dark_mode))
        
    def recreate_all_ui(self):
        """Recreate UI to apply theme changes everywhere"""
        central = self.centralWidget()
        if central:
            central.deleteLater()
        self.setup_ui()
        self.apply_styles()
        
    def setup_ui(self):
        """Setup the main UI layout"""
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        bg_color = "#1e1e1e" if self.dark_mode else "#f5f7fa"
        central_widget.setStyleSheet(f"QWidget {{ background-color: {bg_color}; }}")
        
        main_layout = QHBoxLayout(central_widget)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)
        
        left_sidebar = self.create_left_sidebar()
        main_layout.addWidget(left_sidebar, 2)
        
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
        layout.setSpacing(15)
        
        # App title
        title = QLabel("📊 Workspace\nOrganizer v4")
        title.setStyleSheet("color: white; font-size: 20px; font-weight: bold;")
        layout.addWidget(title)
        
        # Date and time display
        date_label = QLabel(f"{datetime.now().strftime('%B %d, %Y')}")
        date_label.setStyleSheet("color: white; font-size: 12px; font-weight: bold;")
        layout.addWidget(date_label)
        
        self.time_label = QLabel(datetime.now().strftime('%H:%M'))
        self.time_label.setStyleSheet("color: rgba(255,255,255,0.9); font-size: 18px; font-weight: bold;")
        layout.addWidget(self.time_label)
        
        # Quick stats section
        layout.addSpacing(20)
        
        stats_label = QLabel("📊 QUICK STATS")
        stats_label.setStyleSheet("color: white; font-size: 11px; font-weight: bold; letter-spacing: 1px;")
        layout.addWidget(stats_label)
        
        self.file_count_label = QLabel("📁 Files: 0")
        self.file_count_label.setStyleSheet("color: rgba(255,255,255,0.95); font-size: 11px;")
        layout.addWidget(self.file_count_label)
        
        self.storage_label = QLabel("💾 Storage: 0 B")
        self.storage_label.setStyleSheet("color: rgba(255,255,255,0.95); font-size: 11px;")
        layout.addWidget(self.storage_label)
        
        self.notes_count_label = QLabel("📝 Notes: 0")
        self.notes_count_label.setStyleSheet("color: rgba(255,255,255,0.95); font-size: 11px;")
        layout.addWidget(self.notes_count_label)
        
        self.folder_info_label = QLabel("📂 Folder: Desktop")
        self.folder_info_label.setStyleSheet("color: rgba(255,255,255,0.95); font-size: 10px;")
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
                padding: 10px;
                font-weight: bold;
                font-size: 10px;
            }
            QPushButton:hover {
                background-color: rgba(255,255,255,0.25);
            }
        """)
        scan_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        scan_btn.clicked.connect(self.scan_folder)
        layout.addWidget(scan_btn)
        
        vscode_btn = QPushButton("💻 VS CODE")
        vscode_btn.setStyleSheet("""
            QPushButton {
                background-color: rgba(255,255,255,0.15);
                color: white;
                border: 2px solid white;
                border-radius: 25px;
                padding: 10px;
                font-weight: bold;
                font-size: 10px;
            }
            QPushButton:hover {
                background-color: rgba(255,255,255,0.25);
            }
        """)
        vscode_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        vscode_btn.clicked.connect(self.open_in_vscode)
        layout.addWidget(vscode_btn)
        
        organize_btn = QPushButton("📋 ORGANIZE")
        organize_btn.setStyleSheet("""
            QPushButton {
                background-color: rgba(34, 197, 94, 0.8);
                color: white;
                border: 2px solid rgba(34, 197, 94, 1);
                border-radius: 25px;
                padding: 10px;
                font-weight: bold;
                font-size: 10px;
            }
            QPushButton:hover {
                background-color: rgba(34, 197, 94, 1);
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
        
        self.tabs = QTabWidget()
        self.update_tab_styles()
        
        # Dashboard tab
        self.tabs.addTab(self.create_dashboard(), "📊 Dashboard")
        
        # Search tab (NEW)
        self.tabs.addTab(self.create_search_tab(), "🔍 Search")
        
        # Folder Tree tab
        self.tabs.addTab(self.create_folder_tree_tab(), "📂 Folders")
        
        # Files tab
        self.tabs.addTab(self.create_advanced_files_tab(), "📁 Files")
        
        # Organization tab
        self.tabs.addTab(self.create_organization_tab(), "📋 Organization")
        
        # Todo List tab
        self.tabs.addTab(self.create_todo_tab(), "✓ Todo List")
        
        # Kanban Board tab
        self.tabs.addTab(self.create_kanban_tab(), "📌 Kanban")
        
        # Pomodoro Timer tab
        self.tabs.addTab(self.create_pomodoro_tab(), "⏱️ Pomodoro")
        
        # Notes tab
        self.tabs.addTab(self.create_notes_tab(), "📝 Notes")
        
        # Analytics tab
        self.tabs.addTab(self.create_analytics_tab(), "📈 Analytics")
        
        # Calendar tab
        self.tabs.addTab(self.create_calendar_tab(), "📅 Calendar")
        
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
                    padding: 8px 16px; 
                    margin-right: 2px; 
                    border-radius: 4px 4px 0 0;
                    font-weight: bold;
                    font-size: 11px;
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
                    padding: 8px 16px; 
                    margin-right: 2px; 
                    border-radius: 4px 4px 0 0;
                    font-weight: bold;
                    font-size: 11px;
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
    
    def create_stat_card(self, title, value):
        """Create a stat card widget"""
        frame = QFrame()
        if self.dark_mode:
            frame.setStyleSheet("""
                QFrame {
                    background-color: #2d2d2d;
                    border: 2px solid #667eea;
                    border-radius: 10px;
                    padding: 15px;
                }
            """)
        else:
            frame.setStyleSheet("""
                QFrame {
                    background-color: white;
                    border: 2px solid #667eea;
                    border-radius: 10px;
                    padding: 15px;
                }
            """)
        
        layout = QVBoxLayout(frame)
        
        title_label = QLabel(title)
        title_label.setStyleSheet(f"font-size: 12px; font-weight: bold; color: {'#e0e0e0' if self.dark_mode else '#333'};")
        layout.addWidget(title_label)
        
        value_label = QLabel(value)
        value_label.setStyleSheet(f"font-size: 20px; font-weight: bold; color: #667eea;")
        layout.addWidget(value_label)
        
        return frame
    
    def create_dashboard(self):
        """Create the main dashboard view"""
        widget = QWidget()
        if self.dark_mode:
            widget.setStyleSheet("background-color: #1e1e1e; color: #e0e0e0;")
        layout = QVBoxLayout(widget)
        layout.setSpacing(15)
        layout.setContentsMargins(15, 15, 15, 15)
        
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
        
        # Recent files
        recent_label = QLabel("📋 Recent Files:")
        recent_label.setStyleSheet("font-size: 14px; font-weight: bold; color: %s;" % ("#e0e0e0" if self.dark_mode else "#333"))
        layout.addWidget(recent_label)
        
        self.recent_files_list = QListWidget()
        self.recent_files_list.setMaximumHeight(150)
        layout.addWidget(self.recent_files_list)
        
        layout.addStretch()
        return widget
    
    def create_search_tab(self):
        """Create global search tab"""
        widget = QWidget()
        if self.dark_mode:
            widget.setStyleSheet("background-color: #1e1e1e; color: #e0e0e0;")
        layout = QVBoxLayout(widget)
        layout.setContentsMargins(15, 15, 15, 15)
        layout.setSpacing(10)
        
        title = QLabel("🔍 Global Search")
        title_style = "font-size: 18px; font-weight: bold; color: %s;" % ("#e0e0e0" if self.dark_mode else "#333")
        title.setStyleSheet(title_style)
        layout.addWidget(title)
        
        # Search input
        search_layout = QHBoxLayout()
        
        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("Search in Files, Todos, Kanban, Notes... (Ctrl+F)")
        self.search_input.setStyleSheet(f"background-color: {'#2d2d2d' if self.dark_mode else 'white'}; color: {'#e0e0e0' if self.dark_mode else '#333'}; border: 2px solid #667eea; border-radius: 5px; padding: 8px; font-size: 12px;")
        self.search_input.textChanged.connect(self.perform_global_search)
        self.search_input.setMinimumHeight(40)
        search_layout.addWidget(self.search_input)
        
        search_btn = QPushButton("🔎 Search")
        search_btn.clicked.connect(self.perform_global_search)
        search_btn.setStyleSheet("background-color: #667eea; color: white; border: none; border-radius: 5px; padding: 8px 16px; font-weight: bold;")
        search_layout.addWidget(search_btn)
        
        clear_btn = QPushButton("✕ Clear")
        clear_btn.clicked.connect(self.clear_search)
        clear_btn.setStyleSheet("background-color: #ef4444; color: white; border: none; border-radius: 5px; padding: 8px 16px; font-weight: bold;")
        search_layout.addWidget(clear_btn)
        
        layout.addLayout(search_layout)
        
        # Filter buttons
        filter_layout = QHBoxLayout()
        
        filter_label = QLabel("Filter by:")
        filter_label.setStyleSheet(f"color: {'#e0e0e0' if self.dark_mode else '#333'}; font-weight: bold;")
        filter_layout.addWidget(filter_label)
        
        self.search_filter = QComboBox()
        self.search_filter.addItems(["All", "Files", "Todos", "Kanban", "Notes"])
        self.search_filter.setStyleSheet(f"background-color: {'#2d2d2d' if self.dark_mode else 'white'}; color: {'#e0e0e0' if self.dark_mode else '#333'}; border: 2px solid #667eea; border-radius: 5px; padding: 5px;")
        self.search_filter.currentTextChanged.connect(self.perform_global_search)
        filter_layout.addWidget(self.search_filter)
        
        filter_layout.addStretch()
        layout.addLayout(filter_layout)
        
        # Search results
        results_label = QLabel("Search Results:")
        results_label.setStyleSheet(f"font-size: 12px; font-weight: bold; color: {'#e0e0e0' if self.dark_mode else '#333'};")
        layout.addWidget(results_label)
        
        self.search_results_list = QListWidget()
        self.search_results_list.itemDoubleClicked.connect(self.navigate_to_search_result)
        layout.addWidget(self.search_results_list)
        
        # Search history
        history_label = QLabel("Recent Searches:")
        history_label.setStyleSheet(f"font-size: 12px; font-weight: bold; color: {'#e0e0e0' if self.dark_mode else '#333'};")
        layout.addWidget(history_label)
        
        self.search_history_list = QListWidget()
        self.search_history_list.setMaximumHeight(80)
        self.search_history_list.itemClicked.connect(self.search_from_history)
        layout.addWidget(self.search_history_list)
        
        return widget
    
    def perform_global_search(self):
        """Perform search across all data types"""
        query = self.search_input.text().strip().lower()
        if not query:
            self.search_results_list.clear()
            return
        
        filter_type = self.search_filter.currentText()
        results = []
        
        # Search files
        if filter_type in ["All", "Files"]:
            for file_info in self.all_files:
                if query in file_info['name'].lower() or query in file_info['type'].lower() or query in file_info['path'].lower():
                    results.append(("📄 File", file_info['name'], file_info))
        
        # Search todos
        if filter_type in ["All", "Todos"]:
            for i, todo in enumerate(self.todos):
                if query in todo.title.lower():
                    results.append(("✓ Todo", todo.title, todo))
        
        # Search kanban tasks
        if filter_type in ["All", "Kanban"]:
            for i, task in enumerate(self.kanban_tasks):
                if query in task.title.lower():
                    results.append(("📌 Kanban", task.title, task))
        
        # Search notes
        if filter_type in ["All", "Notes"]:
            notes_text = self.notes_text.toPlainText().lower() if hasattr(self, 'notes_text') else ""
            if query in notes_text:
                results.append(("📝 Notes", f"Found in notes content", None))
        
        # Display results
        self.search_results_list.clear()
        self.search_results = results
        
        for result_type, result_name, result_data in results:
            item = QListWidgetItem(f"{result_type} | {result_name}")
            item.setData(Qt.ItemDataRole.UserRole, result_data)
            self.search_results_list.addItem(item)
        
        # Update status
        if results:
            status_text = f"Found {len(results)} result{'s' if len(results) != 1 else ''}"
        else:
            status_text = "No results found"
        
        # Add to search history
        if query not in [h.lower() for h in self.search_history]:
            self.search_history.insert(0, query)
            if len(self.search_history) > self.max_history:
                self.search_history.pop()
            self.update_search_history_display()
    
    def update_search_history_display(self):
        """Update the search history list display"""
        self.search_history_list.clear()
        for search_query in self.search_history[:10]:
            item = QListWidgetItem(f"🔎 {search_query}")
            self.search_history_list.addItem(item)
    
    def search_from_history(self, item):
        """Search using a history item"""
        search_query = item.text().replace("🔎 ", "").strip()
        self.search_input.setText(search_query)
    
    def navigate_to_search_result(self, item):
        """Navigate to search result"""
        result_data = item.data(Qt.ItemDataRole.UserRole)
        item_text = item.text()
        
        if "File" in item_text:
            # Navigate to Files tab
            for i in range(self.tabs.count()):
                if "Files" in self.tabs.tabText(i):
                    self.tabs.setCurrentIndex(i)
                    break
        elif "Todo" in item_text:
            # Navigate to Todo tab
            for i in range(self.tabs.count()):
                if "Todo" in self.tabs.tabText(i):
                    self.tabs.setCurrentIndex(i)
                    break
        elif "Kanban" in item_text:
            # Navigate to Kanban tab
            for i in range(self.tabs.count()):
                if "Kanban" in self.tabs.tabText(i):
                    self.tabs.setCurrentIndex(i)
                    break
        elif "Notes" in item_text:
            # Navigate to Notes tab
            for i in range(self.tabs.count()):
                if "Notes" in self.tabs.tabText(i):
                    self.tabs.setCurrentIndex(i)
                    break
        
        QMessageBox.information(self, "Navigate", f"Navigated to result: {item_text}")
    
    def clear_search(self):
        """Clear search results and input"""
        self.search_input.clear()
        self.search_results_list.clear()
        self.search_results = []
    
    def create_folder_tree_tab(self):
        """Create folder tree navigation tab"""
        widget = QWidget()
        if self.dark_mode:
            widget.setStyleSheet("background-color: #1e1e1e; color: #e0e0e0;")
        layout = QVBoxLayout(widget)
        layout.setContentsMargins(15, 15, 15, 15)
        layout.setSpacing(10)
        
        title = QLabel("📂 Folder Navigation")
        title_style = "font-size: 18px; font-weight: bold; color: %s;" % ("#e0e0e0" if self.dark_mode else "#333")
        title.setStyleSheet(title_style)
        layout.addWidget(title)
        
        # Current folder display
        current_label = QLabel(f"📍 Current: {self.current_folder or 'Desktop'}")
        current_label.setStyleSheet(f"font-size: 12px; color: #667eea; font-weight: bold;")
        layout.addWidget(current_label)
        
        # Folder tree
        self.folder_tree = QTreeWidget()
        self.folder_tree.setHeaderLabel("Folders & Subfolders")
        self.populate_folder_tree()
        layout.addWidget(self.folder_tree)
        
        # Quick access buttons
        button_layout = QHBoxLayout()
        
        open_selected_btn = QPushButton("📂 Open Selected Folder")
        open_selected_btn.clicked.connect(self.open_selected_folder)
        button_layout.addWidget(open_selected_btn)
        
        copy_path_btn = QPushButton("📋 Copy Path")
        copy_path_btn.clicked.connect(self.copy_folder_path)
        button_layout.addWidget(copy_path_btn)
        
        layout.addLayout(button_layout)
        
        return widget
    
    def populate_folder_tree(self):
        """Populate folder tree with current folder and subfolders"""
        self.folder_tree.clear()
        
        if not self.current_folder or not os.path.isdir(self.current_folder):
            return
        
        try:
            root_item = QTreeWidgetItem(self.folder_tree)
            root_item.setText(0, os.path.basename(self.current_folder))
            root_item.setData(0, Qt.ItemDataRole.UserRole, self.current_folder)
            
            self.add_subfolders(root_item, self.current_folder)
            self.folder_tree.expandItem(root_item)
        except Exception as e:
            print(f"Error populating folder tree: {e}")
    
    def add_subfolders(self, parent_item, folder_path, max_depth=3, current_depth=0):
        """Recursively add subfolders to tree"""
        if current_depth >= max_depth:
            return
        
        try:
            for item in sorted(os.listdir(folder_path)):
                full_path = os.path.join(folder_path, item)
                if os.path.isdir(full_path) and not item.startswith('.'):
                    child_item = QTreeWidgetItem(parent_item)
                    child_item.setText(0, f"📁 {item}")
                    child_item.setData(0, Qt.ItemDataRole.UserRole, full_path)
                    
                    self.add_subfolders(child_item, full_path, max_depth, current_depth + 1)
        except PermissionError:
            pass
    
    def open_selected_folder(self):
        """Open selected folder from tree"""
        current_item = self.folder_tree.currentItem()
        if current_item:
            folder_path = current_item.data(0, Qt.ItemDataRole.UserRole)
            if folder_path:
                self.current_folder = folder_path
                self.scan_folder_auto(folder_path)
                self.refresh_dashboard()
                QMessageBox.information(self, "Folder Changed", f"Now scanning: {folder_path}")
    
    def copy_folder_path(self):
        """Copy selected folder path to clipboard"""
        current_item = self.folder_tree.currentItem()
        if current_item:
            folder_path = current_item.data(0, Qt.ItemDataRole.UserRole)
            if folder_path:
                clipboard = QApplication.clipboard()
                clipboard.setText(folder_path)
                QMessageBox.information(self, "Copied", f"Path copied: {folder_path}")
    
    def create_todo_tab(self):
        """Create todo list tab"""
        widget = QWidget()
        if self.dark_mode:
            widget.setStyleSheet("background-color: #1e1e1e; color: #e0e0e0;")
        layout = QVBoxLayout(widget)
        layout.setContentsMargins(15, 15, 15, 15)
        layout.setSpacing(10)
        
        title = QLabel("✓ Todo List")
        title_style = "font-size: 18px; font-weight: bold; color: %s;" % ("#e0e0e0" if self.dark_mode else "#333")
        title.setStyleSheet(title_style)
        layout.addWidget(title)
        
        # Input area
        input_layout = QHBoxLayout()
        self.todo_input = QLineEdit()
        self.todo_input.setPlaceholderText("Add new todo...")
        self.todo_input.setStyleSheet(f"background-color: {'#2d2d2d' if self.dark_mode else 'white'}; color: {'#e0e0e0' if self.dark_mode else '#333'}; border: 2px solid #667eea; border-radius: 5px; padding: 8px;")
        input_layout.addWidget(self.todo_input)
        
        add_btn = QPushButton("➕ Add")
        add_btn.clicked.connect(self.add_todo)
        add_btn.setStyleSheet("background-color: #667eea; color: white; border: none; border-radius: 5px; padding: 8px 16px; font-weight: bold;")
        input_layout.addWidget(add_btn)
        
        layout.addLayout(input_layout)
        
        # Todo list display
        self.todo_list = QListWidget()
        self.todo_list.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)
        self.todo_list.customContextMenuRequested.connect(self.show_todo_context_menu)
        self.update_todo_list_display()
        layout.addWidget(self.todo_list)
        
        # Control buttons layout
        btn_layout = QHBoxLayout()
        
        pin_btn = QPushButton("📌 Pin Selected")
        pin_btn.clicked.connect(self.pin_todo)
        pin_btn.setStyleSheet("background-color: #f59e0b; color: white; border: none; border-radius: 5px; padding: 8px 16px; font-weight: bold;")
        btn_layout.addWidget(pin_btn)
        
        delete_btn = QPushButton("🗑️ Delete Selected")
        delete_btn.clicked.connect(self.delete_todo)
        delete_btn.setStyleSheet("background-color: #ef4444; color: white; border: none; border-radius: 5px; padding: 8px 16px; font-weight: bold;")
        btn_layout.addWidget(delete_btn)
        
        layout.addLayout(btn_layout)
        
        return widget
    
    def add_todo(self):
        """Add new todo item"""
        text = self.todo_input.text().strip()
        if text:
            self.todos.append(TodoItem(text))
            self.todo_input.clear()
            self.update_todo_list_display()
    
    def delete_todo(self):
        """Delete selected todo"""
        current = self.todo_list.currentRow()
        if current >= 0:
            self.todos.pop(current)
            self.update_todo_list_display()
    
    def delete_kanban_task(self, column_list):
        """Delete selected kanban task"""
        current = column_list.currentRow()
        if current >= 0 and column_list.item(current):
            original_index = column_list.item(current).data(Qt.ItemDataRole.UserRole)
            if original_index is not None and original_index < len(self.kanban_tasks):
                self.kanban_tasks.pop(original_index)
                self.update_kanban_display()
    
    def toggle_todo_complete(self, item):
        """Toggle todo completion when clicked (double-click)"""
        current = self.todo_list.row(item)
        if current >= 0 and current < len(self.todos):
            self.todos[current].completed = not self.todos[current].completed
            if self.todos[current].completed:
                self.increment_tasks_completed()
            self.update_todo_list_display()
    
    def update_todo_list_display(self):
        """Update todo list display with pinned items at top"""
        self.todo_list.clear()
        self.todo_list.itemDoubleClicked.disconnect() if self.todo_list.receivers(self.todo_list.itemDoubleClicked) > 0 else None
        
        # Sort: pinned items first, then regular items
        pinned_todos = [t for t in self.todos if t.is_pinned]
        regular_todos = [t for t in self.todos if not t.is_pinned]
        sorted_todos = pinned_todos + regular_todos
        
        for i, todo in enumerate(sorted_todos):
            pin_icon = "📌" if todo.is_pinned else "  "
            complete_icon = "✓" if todo.completed else "○"
            item_text = f"{pin_icon} {complete_icon} {todo.title}"
            item = QListWidgetItem(item_text)
            item.setData(Qt.ItemDataRole.UserRole, self.todos.index(todo))  # Store original index
            self.todo_list.addItem(item)
        
        self.todo_list.itemDoubleClicked.connect(self.toggle_todo_complete)
    
    def pin_todo(self):
        """Pin/unpin selected todo"""
        current = self.todo_list.currentRow()
        if current >= 0 and self.todo_list.item(current):
            original_index = self.todo_list.item(current).data(Qt.ItemDataRole.UserRole)
            if original_index is not None and original_index < len(self.todos):
                self.todos[original_index].is_pinned = not self.todos[original_index].is_pinned
                self.update_todo_list_display()
    
    def show_todo_context_menu(self, pos):
        """Show right-click context menu for todos"""
        item = self.todo_list.itemAt(pos)
        if not item:
            return
        
        menu = QMenu()
        
        # Pin/Unpin action
        current = self.todo_list.row(item)
        if current >= 0:
            original_index = item.data(Qt.ItemDataRole.UserRole)
            if original_index is not None and original_index < len(self.todos):
                is_pinned = self.todos[original_index].is_pinned
                pin_action = menu.addAction("📌 Unpin" if is_pinned else "📌 Pin")
                pin_action.triggered.connect(self.pin_todo)
        
        menu.addSeparator()
        
        # Delete action
        delete_action = menu.addAction("🗑️ Delete")
        delete_action.triggered.connect(self.delete_todo)
        
        menu.exec(self.todo_list.mapToGlobal(pos))
    
    
    def create_kanban_tab(self):
        """Create Kanban board tab"""
        widget = QWidget()
        if self.dark_mode:
            widget.setStyleSheet("background-color: #1e1e1e; color: #e0e0e0;")
        layout = QVBoxLayout(widget)
        layout.setContentsMargins(15, 15, 15, 15)
        layout.setSpacing(10)
        
        title = QLabel("📌 Kanban Board")
        title_style = "font-size: 18px; font-weight: bold; color: %s;" % ("#e0e0e0" if self.dark_mode else "#333")
        title.setStyleSheet(title_style)
        layout.addWidget(title)
        
        # Input area
        input_layout = QHBoxLayout()
        self.kanban_input = QLineEdit()
        self.kanban_input.setPlaceholderText("Add new task...")
        self.kanban_input.setStyleSheet(f"background-color: {'#2d2d2d' if self.dark_mode else 'white'}; color: {'#e0e0e0' if self.dark_mode else '#333'}; border: 2px solid #667eea; border-radius: 5px; padding: 8px;")
        input_layout.addWidget(self.kanban_input)
        
        add_btn = QPushButton("➕ Add")
        add_btn.clicked.connect(self.add_kanban_task)
        add_btn.setStyleSheet("background-color: #667eea; color: white; border: none; border-radius: 5px; padding: 8px 16px; font-weight: bold;")
        input_layout.addWidget(add_btn)
        
        layout.addLayout(input_layout)
        
        # Three columns: To Do, In Progress, Done
        columns_layout = QHBoxLayout()
        
        self.kanban_todo_list = self.create_kanban_column("To Do", "#ef4444")
        self.kanban_progress_list = self.create_kanban_column("In Progress", "#f59e0b")
        self.kanban_done_list = self.create_kanban_column("Done", "#10b981")
        
        columns_layout.addWidget(self.kanban_todo_list)
        columns_layout.addWidget(self.kanban_progress_list)
        columns_layout.addWidget(self.kanban_done_list)
        
        layout.addLayout(columns_layout)
        
        return widget
    
    def create_kanban_column(self, title, color):
        """Create a Kanban column"""
        frame = QFrame()
        frame.setStyleSheet(f"""
            QFrame {{
                background-color: {'#2d2d2d' if self.dark_mode else '#f0f0f0'};
                border: 2px solid {color};
                border-radius: 8px;
                padding: 10px;
            }}
        """)
        
        layout = QVBoxLayout(frame)
        
        col_title = QLabel(title)
        col_title.setStyleSheet(f"font-size: 14px; font-weight: bold; color: {color};")
        layout.addWidget(col_title)
        
        list_widget = QListWidget()
        list_widget.setStyleSheet(f"""
            QListWidget {{
                background-color: {'#1e1e1e' if self.dark_mode else 'white'};
                color: {'#e0e0e0' if self.dark_mode else '#333'};
                border: 1px solid {color};
                border-radius: 5px;
            }}
            QListWidget::item {{
                background-color: {'#333' if self.dark_mode else '#f9f9f9'};
                color: {'#e0e0e0' if self.dark_mode else '#333'};
                padding: 8px;
                border-radius: 3px;
                margin: 2px;
            }}
            QListWidget::item:selected {{
                background-color: {color};
                color: white;
            }}
        """)
        layout.addWidget(list_widget)
        
        # Store the list widget in the frame for easy access
        frame.list_widget = list_widget
        
        # Enable context menu for right-click
        list_widget.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)
        list_widget.customContextMenuRequested.connect(lambda pos: self.show_kanban_context_menu(pos, list_widget))
        
        return frame
    
    def add_kanban_task(self):
        """Add new Kanban task"""
        text = self.kanban_input.text().strip()
        if text:
            task = KanbanTask(text, "To Do")
            self.kanban_tasks.append(task)
            self.kanban_input.clear()
            self.update_kanban_display()
    
    def update_kanban_display(self):
        """Update Kanban board display with pinned items at top"""
        # Get the list widgets from the stored references
        todo_list = getattr(self.kanban_todo_list, 'list_widget', None)
        progress_list = getattr(self.kanban_progress_list, 'list_widget', None)
        done_list = getattr(self.kanban_done_list, 'list_widget', None)
        
        # Clear all lists
        if todo_list:
            todo_list.clear()
        if progress_list:
            progress_list.clear()
        if done_list:
            done_list.clear()
        
        # Add tasks to appropriate columns (pinned first)
        for task in self.kanban_tasks:
            pin_icon = "📌" if task.is_pinned else "  "
            task_item = QListWidgetItem(f"{pin_icon} 📋 {task.title}")
            task_item.setData(Qt.ItemDataRole.UserRole, self.kanban_tasks.index(task))
            
            if task.status == "To Do" and todo_list:
                todo_list.addItem(task_item)
            elif task.status == "In Progress" and progress_list:
                progress_list.addItem(task_item)
            elif task.status == "Done" and done_list:
                done_list.addItem(task_item)
        
        # Re-sort each column to put pinned items first
        for list_widget in [todo_list, progress_list, done_list]:
            if list_widget:
                self._sort_kanban_column(list_widget)
    
    def _sort_kanban_column(self, column_list):
        """Sort a kanban column to put pinned items first"""
        items = []
        for i in range(column_list.count()):
            item = column_list.takeItem(0)
            items.append(item)
        
        # Sort: pinned items first
        pinned = [item for item in items if item.text().startswith("📌")]
        unpinned = [item for item in items if not item.text().startswith("📌")]
        
        for item in pinned + unpinned:
            column_list.addItem(item)
    
    def pin_kanban_task(self, column_list):
        """Pin/unpin selected kanban task"""
        current = column_list.currentRow()
        if current >= 0 and column_list.item(current):
            original_index = column_list.item(current).data(Qt.ItemDataRole.UserRole)
            if original_index is not None and original_index < len(self.kanban_tasks):
                self.kanban_tasks[original_index].is_pinned = not self.kanban_tasks[original_index].is_pinned
                self.update_kanban_display()
    
    def show_kanban_context_menu(self, pos, column_list):
        """Show right-click context menu for kanban tasks"""
        item = column_list.itemAt(pos)
        if not item:
            return
        
        menu = QMenu()
        
        # Pin/Unpin action
        current = column_list.row(item)
        if current >= 0:
            original_index = item.data(Qt.ItemDataRole.UserRole)
            if original_index is not None and original_index < len(self.kanban_tasks):
                is_pinned = self.kanban_tasks[original_index].is_pinned
                pin_action = menu.addAction("📌 Unpin" if is_pinned else "📌 Pin")
                pin_action.triggered.connect(lambda: self.pin_kanban_task(column_list))
        
        menu.addSeparator()
        
        # Delete action
        delete_action = menu.addAction("🗑️ Delete")
        delete_action.triggered.connect(lambda: self.delete_kanban_task(column_list))
        
        menu.exec(column_list.mapToGlobal(pos))
    
    def create_pomodoro_tab(self):
        """Create Pomodoro timer tab"""
        widget = QWidget()
        if self.dark_mode:
            widget.setStyleSheet("background-color: #1e1e1e; color: #e0e0e0;")
        layout = QVBoxLayout(widget)
        layout.setContentsMargins(15, 15, 15, 15)
        layout.setSpacing(20)
        
        title = QLabel("⏱️ Pomodoro Timer")
        title_style = "font-size: 18px; font-weight: bold; color: %s;" % ("#e0e0e0" if self.dark_mode else "#333")
        title.setStyleSheet(title_style)
        layout.addWidget(title)
        
        layout.addSpacing(30)
        
        # Timer display
        self.pomodoro_display = QLabel("25:00")
        self.pomodoro_display.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.pomodoro_display.setStyleSheet("font-size: 80px; font-weight: bold; color: #667eea;")
        layout.addWidget(self.pomodoro_display)
        
        # Status display
        self.pomodoro_status = QLabel("Work Session")
        self.pomodoro_status.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.pomodoro_status.setStyleSheet(f"font-size: 16px; color: {'#e0e0e0' if self.dark_mode else '#333'};")
        layout.addWidget(self.pomodoro_status)
        
        layout.addSpacing(20)
        
        # Control buttons
        button_layout = QHBoxLayout()
        
        start_btn = QPushButton("▶️ Start")
        start_btn.clicked.connect(self.start_pomodoro)
        start_btn.setStyleSheet("background-color: #10b981; color: white; border: none; border-radius: 5px; padding: 12px 24px; font-size: 14px; font-weight: bold;")
        button_layout.addWidget(start_btn)
        
        pause_btn = QPushButton("⏸️ Pause")
        pause_btn.clicked.connect(self.pause_pomodoro)
        pause_btn.setStyleSheet("background-color: #f59e0b; color: white; border: none; border-radius: 5px; padding: 12px 24px; font-size: 14px; font-weight: bold;")
        button_layout.addWidget(pause_btn)
        
        reset_btn = QPushButton("🔄 Reset")
        reset_btn.clicked.connect(self.reset_pomodoro)
        reset_btn.setStyleSheet("background-color: #ef4444; color: white; border: none; border-radius: 5px; padding: 12px 24px; font-size: 14px; font-weight: bold;")
        button_layout.addWidget(reset_btn)
        
        layout.addLayout(button_layout)
        
        layout.addSpacing(20)
        
        # Progress bar
        self.pomodoro_progress = QProgressBar()
        self.pomodoro_progress.setStyleSheet("""
            QProgressBar {
                border: 2px solid #667eea;
                border-radius: 5px;
                text-align: center;
                color: white;
            }
            QProgressBar::chunk {
                background-color: #667eea;
            }
        """)
        layout.addWidget(self.pomodoro_progress)
        
        layout.addStretch()
        
        return widget
    
    def start_pomodoro(self):
        """Start Pomodoro timer"""
        self.pomodoro.is_running = True
    
    def pause_pomodoro(self):
        """Pause Pomodoro timer"""
        self.pomodoro.is_running = False
    
    def reset_pomodoro(self):
        """Reset Pomodoro timer"""
        self.pomodoro.is_running = False
        self.pomodoro.remaining = self.pomodoro.work_duration
        self.pomodoro.is_work = True
        self.update_pomodoro_display()
    
    def update_pomodoro(self):
        """Update Pomodoro timer"""
        if self.pomodoro.is_running and self.pomodoro.remaining > 0:
            self.pomodoro.remaining -= 1
            self.update_pomodoro_display()
        elif self.pomodoro.is_running and self.pomodoro.remaining == 0:
            # Switch between work and break
            if self.pomodoro.is_work:
                # Work session completed - track it
                self.increment_pomodoro_sessions()
                
                self.pomodoro.is_work = False
                self.pomodoro.remaining = self.pomodoro.break_duration
                QMessageBox.information(self, "Session Complete! 🎉", 
                    f"Great work! Take a 5-minute break.\n\nToday's Sessions: {self.stats['pomodoro_sessions']}")
            else:
                self.pomodoro.is_work = True
                self.pomodoro.remaining = self.pomodoro.work_duration
                QMessageBox.information(self, "Break Over! 💪", "Time for another 25-minute session!")
            self.update_pomodoro_display()
    
    def update_pomodoro_display(self):
        """Update Pomodoro display"""
        minutes = self.pomodoro.remaining // 60
        seconds = self.pomodoro.remaining % 60
        self.pomodoro_display.setText(f"{minutes:02d}:{seconds:02d}")
        
        status = "Work Session 💪" if self.pomodoro.is_work else "Break Time ☕"
        self.pomodoro_status.setText(status)
        
        # Update progress bar
        max_duration = self.pomodoro.work_duration if self.pomodoro.is_work else self.pomodoro.break_duration
        progress = 100 - (self.pomodoro.remaining / max_duration * 100)
        self.pomodoro_progress.setValue(int(progress))
    
    def create_advanced_files_tab(self):
        """Create advanced files tab with table and filters"""
        widget = QWidget()
        if self.dark_mode:
            widget.setStyleSheet("background-color: #1e1e1e; color: #e0e0e0;")
        layout = QVBoxLayout(widget)
        layout.setContentsMargins(10, 10, 10, 10)
        layout.setSpacing(10)
        
        # Title
        title = QLabel("📁 Files")
        title_style = "font-size: 18px; font-weight: bold; color: %s;" % ("#e0e0e0" if self.dark_mode else "#333")
        title.setStyleSheet(title_style)
        layout.addWidget(title)
        
        # Filters
        filter_layout = QHBoxLayout()
        
        search_label = QLabel("🔍 Search:")
        filter_layout.addWidget(search_label)
        
        self.file_search_input = QLineEdit()
        self.file_search_input.setPlaceholderText("Search files...")
        self.file_search_input.setStyleSheet(f"background-color: {'#2d2d2d' if self.dark_mode else 'white'}; color: {'#e0e0e0' if self.dark_mode else '#333'}; border: 2px solid #667eea; border-radius: 5px; padding: 8px;")
        self.file_search_input.textChanged.connect(self.filter_files)
        filter_layout.addWidget(self.file_search_input)
        
        layout.addLayout(filter_layout)
        
        # File table
        self.files_table = QTableWidget()
        self.files_table.setColumnCount(5)
        self.files_table.setHorizontalHeaderLabels(["Name", "Size", "Type", "Modified", "Path"])
        self.populate_files_table()
        layout.addWidget(self.files_table)
        
        return widget
    
    def populate_files_table(self):
        """Populate files table"""
        self.files_table.setRowCount(len(self.all_files))
        for row, file_info in enumerate(self.all_files):
            self.files_table.setItem(row, 0, QTableWidgetItem(file_info['name']))
            self.files_table.setItem(row, 1, QTableWidgetItem(file_info['size']))
            self.files_table.setItem(row, 2, QTableWidgetItem(file_info['type']))
            self.files_table.setItem(row, 3, QTableWidgetItem(file_info['modified']))
            self.files_table.setItem(row, 4, QTableWidgetItem(file_info['path']))
    
    def filter_files(self):
        """Filter files based on search"""
        search_text = self.file_search_input.text().lower()
        self.filtered_files = [f for f in self.all_files if search_text in f['name'].lower()]
        self.files_table.setRowCount(len(self.filtered_files))
        for row, file_info in enumerate(self.filtered_files):
            self.files_table.setItem(row, 0, QTableWidgetItem(file_info['name']))
            self.files_table.setItem(row, 1, QTableWidgetItem(file_info['size']))
            self.files_table.setItem(row, 2, QTableWidgetItem(file_info['type']))
            self.files_table.setItem(row, 3, QTableWidgetItem(file_info['modified']))
            self.files_table.setItem(row, 4, QTableWidgetItem(file_info['path']))
    
    def create_organization_tab(self):
        """Create organization tab"""
        widget = QWidget()
        if self.dark_mode:
            widget.setStyleSheet("background-color: #1e1e1e; color: #e0e0e0;")
        layout = QVBoxLayout(widget)
        layout.setContentsMargins(15, 15, 15, 15)
        layout.setSpacing(10)
        
        title = QLabel("📋 Organization Tools")
        title_style = "font-size: 18px; font-weight: bold; color: %s;" % ("#e0e0e0" if self.dark_mode else "#333")
        title.setStyleSheet(title_style)
        layout.addWidget(title)
        
        layout.addSpacing(10)
        
        # Buttons
        org_by_type_btn = QPushButton("📂 Organize by Type")
        org_by_type_btn.clicked.connect(self.organize_by_type)
        org_by_type_btn.setStyleSheet("background-color: #667eea; color: white; border: none; border-radius: 5px; padding: 12px; font-weight: bold;")
        layout.addWidget(org_by_type_btn)
        
        org_by_date_btn = QPushButton("📅 Organize by Date")
        org_by_date_btn.clicked.connect(self.organize_by_date)
        org_by_date_btn.setStyleSheet("background-color: #667eea; color: white; border: none; border-radius: 5px; padding: 12px; font-weight: bold;")
        layout.addWidget(org_by_date_btn)
        
        dup_btn = QPushButton("🔍 Find Duplicates")
        dup_btn.clicked.connect(self.find_duplicates)
        dup_btn.setStyleSheet("background-color: #f59e0b; color: white; border: none; border-radius: 5px; padding: 12px; font-weight: bold;")
        layout.addWidget(dup_btn)
        
        cleanup_btn = QPushButton("🧹 Cleanup Empty Folders")
        cleanup_btn.clicked.connect(self.cleanup_dialog)
        cleanup_btn.setStyleSheet("background-color: #ef4444; color: white; border: none; border-radius: 5px; padding: 12px; font-weight: bold;")
        layout.addWidget(cleanup_btn)
        
        layout.addStretch()
        
        return widget
    
    def create_notes_tab(self):
        """Create notes tab"""
        widget = QWidget()
        if self.dark_mode:
            widget.setStyleSheet("background-color: #1e1e1e; color: #e0e0e0;")
        layout = QVBoxLayout(widget)
        layout.setContentsMargins(15, 15, 15, 15)
        
        title = QLabel("📝 Notes")
        title_style = "font-size: 18px; font-weight: bold; color: %s;" % ("#e0e0e0" if self.dark_mode else "#333")
        title.setStyleSheet(title_style)
        layout.addWidget(title)
        
        self.notes_text = QTextEdit()
        self.notes_text.setStyleSheet(f"background-color: {'#2d2d2d' if self.dark_mode else 'white'}; color: {'#e0e0e0' if self.dark_mode else '#333'}; border: 2px solid #667eea; border-radius: 5px; padding: 8px;")
        layout.addWidget(self.notes_text)
        
        save_btn = QPushButton("💾 Save Note")
        save_btn.clicked.connect(self.save_note)
        layout.addWidget(save_btn)
        
        return widget
    
    def create_analytics_tab(self):
        """Create analytics tab"""
        widget = QWidget()
        if self.dark_mode:
            widget.setStyleSheet("background-color: #1e1e1e; color: #e0e0e0;")
        layout = QVBoxLayout(widget)
        layout.setContentsMargins(15, 15, 15, 15)
        
        title = QLabel("📈 Analytics")
        title_style = "font-size: 18px; font-weight: bold; color: %s;" % ("#e0e0e0" if self.dark_mode else "#333")
        title.setStyleSheet(title_style)
        layout.addWidget(title)
        
        self.analytics_text = QTextEdit()
        self.analytics_text.setReadOnly(True)
        self.analytics_text.setStyleSheet(f"background-color: {'#2d2d2d' if self.dark_mode else 'white'}; color: {'#e0e0e0' if self.dark_mode else '#333'}; border: 2px solid #667eea; border-radius: 5px; padding: 8px;")
        layout.addWidget(self.analytics_text)
        
        return widget
    
    def create_calendar_tab(self):
        """Create calendar tab"""
        widget = QWidget()
        if self.dark_mode:
            widget.setStyleSheet("background-color: #1e1e1e; color: #e0e0e0;")
        layout = QVBoxLayout(widget)
        layout.setContentsMargins(15, 15, 15, 15)
        
        title = QLabel("📅 Calendar")
        title_style = "font-size: 18px; font-weight: bold; color: %s;" % ("#e0e0e0" if self.dark_mode else "#333")
        title.setStyleSheet(title_style)
        layout.addWidget(title)
        
        # Calendar widget with dark mode styling
        self.calendar = QCalendarWidget()
        
        if self.dark_mode:
            calendar_style = """
                QCalendarWidget {
                    background-color: #2d2d2d;
                    color: #e0e0e0;
                    border: 2px solid #667eea;
                    border-radius: 5px;
                }
                QCalendarWidget QWidget {
                    background-color: #2d2d2d;
                    color: #e0e0e0;
                    alternate-background-color: #2d2d2d;
                }
                QCalendarWidget QAbstractItemView {
                    background-color: #1e1e1e;
                    color: #e0e0e0;
                    selection-background-color: #667eea;
                    selection-color: white;
                    border: none;
                    alternate-background-color: #1e1e1e;
                }
                QCalendarWidget QAbstractItemView:enabled {
                    color: #e0e0e0;
                    background-color: #1e1e1e;
                }
                QCalendarWidget QAbstractItemView:disabled {
                    color: #666;
                }
                QCalendarWidget QTableView {
                    background-color: #1e1e1e;
                    color: #e0e0e0;
                    gridline-color: #333;
                    selection-background-color: #667eea;
                }
                QCalendarWidget QHeaderView {
                    background-color: #333;
                }
                QCalendarWidget QHeaderView::section {
                    background-color: #333;
                    color: #e0e0e0;
                    padding: 5px;
                    border: 1px solid #444;
                    font-weight: bold;
                }
                QCalendarWidget QSpinBox {
                    background-color: #333;
                    color: #e0e0e0;
                    border: 1px solid #667eea;
                    border-radius: 3px;
                    padding: 3px;
                    selection-background-color: #667eea;
                    selection-color: white;
                }
                QCalendarWidget QSpinBox::up-button,
                QCalendarWidget QSpinBox::down-button {
                    background-color: #667eea;
                    color: white;
                    border-radius: 3px;
                }
                QCalendarWidget QToolButton {
                    background-color: #667eea;
                    color: white;
                    border: none;
                    border-radius: 3px;
                    padding: 4px 8px;
                    font-weight: bold;
                }
                QCalendarWidget QToolButton:hover {
                    background-color: #764ba2;
                }
                QCalendarWidget QToolButton:pressed {
                    background-color: #5568d3;
                }
                QCalendarWidget QMenu {
                    background-color: #2d2d2d;
                    color: #e0e0e0;
                    border: 1px solid #667eea;
                }
                QCalendarWidget QMenu::item:selected {
                    background-color: #667eea;
                    color: white;
                }
            """
        else:
            calendar_style = """
                QCalendarWidget {
                    background-color: white;
                    color: #333;
                    border: 2px solid #667eea;
                    border-radius: 5px;
                }
                QCalendarWidget QWidget {
                    background-color: white;
                    color: #333;
                }
                QCalendarWidget QAbstractItemView {
                    background-color: white;
                    color: #333;
                    selection-background-color: #667eea;
                    selection-color: white;
                    border: none;
                }
                QCalendarWidget QHeaderView::section {
                    background-color: #e0e7ff;
                    color: #333;
                    padding: 5px;
                    border: 1px solid #ccc;
                    font-weight: bold;
                }
                QCalendarWidget QSpinBox {
                    background-color: white;
                    color: #333;
                    border: 1px solid #667eea;
                    border-radius: 3px;
                    padding: 3px;
                }
                QCalendarWidget QSpinBox::up-button,
                QCalendarWidget QSpinBox::down-button {
                    background-color: #667eea;
                    color: white;
                    border-radius: 3px;
                }
                QCalendarWidget QToolButton {
                    background-color: #667eea;
                    color: white;
                    border: none;
                    border-radius: 3px;
                    padding: 4px 8px;
                    font-weight: bold;
                }
                QCalendarWidget QToolButton:hover {
                    background-color: #764ba2;
                }
                QCalendarWidget QToolButton:pressed {
                    background-color: #5568d3;
                }
            """
        
        self.calendar.setStyleSheet(calendar_style)
        layout.addWidget(self.calendar)
        
        return widget
    
    def scan_folder_auto(self, folder_path):
        """Auto scan folder without dialog"""
        if os.path.isdir(folder_path):
            self.current_folder = folder_path
            file_paths = self.file_manager.scan_folder(folder_path)
            
            # Convert file paths to dictionaries
            self.all_files = []
            for file_path in file_paths:
                try:
                    file_stat = os.stat(file_path)
                    file_size = file_stat.st_size
                    file_name = os.path.basename(file_path)
                    file_ext = os.path.splitext(file_name)[1]
                    mod_time = datetime.fromtimestamp(file_stat.st_mtime).strftime('%Y-%m-%d %H:%M')
                    
                    # Format size
                    if file_size < 1024:
                        size_str = f"{file_size} B"
                    elif file_size < 1024 ** 2:
                        size_str = f"{file_size / 1024:.1f} KB"
                    elif file_size < 1024 ** 3:
                        size_str = f"{file_size / (1024**2):.1f} MB"
                    else:
                        size_str = f"{file_size / (1024**3):.1f} GB"
                    
                    self.all_files.append({
                        'name': file_name,
                        'size': size_str,
                        'type': file_ext or 'File',
                        'modified': mod_time,
                        'path': file_path
                    })
                except:
                    pass
            
            self.folder_info_label.setText(f"📂 Folder: {os.path.basename(folder_path)}")
            self.populate_files_table()
    
    def scan_folder(self):
        """Scan folder for files"""
        folder_path = QFileDialog.getExistingDirectory(self, "Select Folder to Scan")
        if folder_path:
            self.scan_folder_auto(folder_path)
            self.refresh_dashboard()
            QMessageBox.information(self, "Scan Complete", f"Scanned {len(self.all_files)} files")
    
    def open_in_vscode(self):
        """Open current folder in VS Code"""
        if not self.current_folder:
            QMessageBox.warning(self, "No Folder", "Please scan a folder first")
            return
        
        try:
            if platform.system() == "Windows":
                subprocess.Popen(f'code "{self.current_folder}"')
            elif platform.system() == "Darwin":
                subprocess.Popen(["code", self.current_folder])
            else:
                subprocess.Popen(["code", self.current_folder])
            QMessageBox.information(self, "Success", "VS Code opened!")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Could not open VS Code: {e}")
    
    def open_folder_explorer(self):
        """Open current folder in file explorer"""
        if not self.current_folder:
            QMessageBox.warning(self, "No Folder", "Please scan a folder first")
            return
        
        try:
            if platform.system() == "Windows":
                subprocess.Popen(f'explorer "{self.current_folder}"')
            elif platform.system() == "Darwin":
                subprocess.Popen(["open", self.current_folder])
            else:
                subprocess.Popen(["xdg-open", self.current_folder])
            QMessageBox.information(self, "Success", "Folder opened!")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Could not open folder: {e}")
    
    def organize_by_type(self):
        """Organize files by type"""
        if not self.current_folder:
            QMessageBox.warning(self, "No Folder", "Please scan a folder first")
            return
        
        try:
            # Count files before organization
            files_count = len(self.all_files)
            
            self.file_manager.organize_by_type(self.current_folder)
            
            # Track organization
            self.stats['files_organized_today'] += files_count
            self.stats['total_files_organized'] += files_count
            
            QMessageBox.information(self, "Success", f"Files organized by type! ({files_count} files)")
            self.scan_folder_auto(self.current_folder)
            self.update_statistics_display()
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Organization failed: {e}")
    
    def organize_by_date(self):
        """Organize files by date"""
        if not self.current_folder:
            QMessageBox.warning(self, "No Folder", "Please scan a folder first")
            return
        
        try:
            # Count files before organization
            files_count = len(self.all_files)
            
            self.file_manager.organize_by_date(self.current_folder)
            
            # Track organization
            self.stats['files_organized_today'] += files_count
            self.stats['total_files_organized'] += files_count
            
            QMessageBox.information(self, "Success", f"Files organized by date! ({files_count} files)")
            self.scan_folder_auto(self.current_folder)
            self.update_statistics_display()
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Organization failed: {e}")
    
    def find_duplicates(self):
        """Find duplicate files"""
        if not self.current_folder:
            QMessageBox.warning(self, "No Folder", "Please scan a folder first")
            return
        
        try:
            duplicates = self.file_manager.find_duplicates(self.current_folder)
            if duplicates:
                dup_text = "\n\n".join([f"{i+1}. {dup}" for i, dup in enumerate(duplicates)])
                QMessageBox.information(self, "Duplicates Found", f"Found {len(duplicates)} duplicate groups:\n\n{dup_text}")
            else:
                QMessageBox.information(self, "No Duplicates", "No duplicate files found!")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Duplicate detection failed: {e}")
    
    def cleanup_dialog(self):
        """Show cleanup dialog"""
        if not self.current_folder:
            QMessageBox.warning(self, "No Folder", "Please scan a folder first")
            return
        
        reply = QMessageBox.question(self, "Cleanup Empty Folders", 
                                     "Remove all empty folders recursively?",
                                     QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
        
        if reply == QMessageBox.StandardButton.Yes:
            try:
                self.file_manager.cleanup_empty_folders(self.current_folder)
                QMessageBox.information(self, "Success", "Empty folders removed!")
                self.scan_folder_auto(self.current_folder)
            except Exception as e:
                QMessageBox.critical(self, "Error", f"Cleanup failed: {e}")
    
    def organize_files_dialog(self):
        """Show organization dialog"""
        if not self.current_folder:
            QMessageBox.warning(self, "No Folder", "Please scan a folder first")
            return
        
        reply = QMessageBox.question(self, "Organize Files",
                                     "Choose organization method:\n\nYes = By Type\nNo = By Date",
                                     QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
        
        if reply == QMessageBox.StandardButton.Yes:
            self.organize_by_type()
        else:
            self.organize_by_date()
    
    def save_note(self):
        """Save note"""
        text = self.notes_text.toPlainText()
        if text.strip():
            self.notes_manager.save_note(text)
            self.notes_text.clear()
            QMessageBox.information(self, "Saved", "Note saved successfully!")
    
    def refresh_dashboard(self):
        """Refresh dashboard with current data"""
        if not self.current_folder:
            return
        
        # Update stats
        file_count = len(self.all_files)
        storage_bytes = 0
        for f in self.all_files:
            try:
                size_str = f.get('size', '0 B').split()[0]
                if size_str.replace('.', '', 1).isdigit():
                    storage_bytes += float(size_str)
            except:
                pass
        
        # Format storage
        if storage_bytes < 1024:
            storage_display = f"{storage_bytes:.1f} B"
        elif storage_bytes < 1024 ** 2:
            storage_display = f"{storage_bytes / 1024:.1f} KB"
        elif storage_bytes < 1024 ** 3:
            storage_display = f"{storage_bytes / (1024**2):.1f} MB"
        else:
            storage_display = f"{storage_bytes / (1024**3):.1f} GB"
        
        self.file_count_label.setText(f"📁 Files: {file_count}")
        self.storage_label.setText(f"💾 Storage: {storage_display}")
        
        # Update statistics cards with current data
        self.file_stat_card = self.create_stat_card("📁 Files Scanned", str(file_count))
        self.storage_stat_card = self.create_stat_card("💾 Storage Used", storage_display)
        self.notes_stat_card = self.create_stat_card("📝 Tasks Completed", f"{self.stats['tasks_completed']}")
        self.types_stat_card = self.create_stat_card("🔥 Current Streak", f"{self.stats['current_streak']} days")
        
        # Update recent files
        self.recent_files_list.clear()
        for file_info in self.all_files[:10]:
            self.recent_files_list.addItem(f"📄 {file_info['name']}")
    
    def update_statistics_display(self):
        """Update the statistics display on dashboard"""
        try:
            # Calculate today's stats
            tasks_completed = len([t for t in self.todos if t.completed])
            
            # Update stat cards if they exist
            if hasattr(self, 'file_stat_card'):
                self.file_stat_card = self.create_stat_card("📁 Today's Files", f"{self.stats['files_organized_today']}")
            if hasattr(self, 'storage_stat_card'):
                self.storage_stat_card = self.create_stat_card("✓ Tasks Done", f"{tasks_completed}")
            if hasattr(self, 'notes_stat_card'):
                self.notes_stat_card = self.create_stat_card("🍅 Pomodoro", f"{self.stats['pomodoro_sessions']}")
            if hasattr(self, 'types_stat_card'):
                self.types_stat_card = self.create_stat_card("🔥 Streak", f"{self.stats['current_streak']}")
        except:
            pass
    
    def increment_tasks_completed(self):
        """Increment task completion counter"""
        self.stats['tasks_completed'] += 1
        self.stats['total_tasks_completed'] += 1
        self.update_statistics_display()
    
    def increment_pomodoro_sessions(self):
        """Increment pomodoro counter when session completes"""
        self.stats['pomodoro_sessions'] += 1
        self.stats['pomodoro_hours'] += 0.42  # 25 mins ≈ 0.42 hours
        self.update_statistics_display()
    
    def increment_files_organized(self):
        """Increment files organized counter"""
        self.stats['files_organized_today'] += 1
        self.stats['total_files_organized'] += 1
        self.update_statistics_display()
    
    def update_streak(self):
        """Update current streak (called daily)"""
        current_date = datetime.now().date()
        if current_date > self.today_date:
            # New day - check if streak should continue
            if self.stats['tasks_completed'] > 0 or self.stats['pomodoro_sessions'] > 0:
                self.stats['current_streak'] += 1
            else:
                self.stats['current_streak'] = 0
            
            # Reset daily counters
            self.today_date = current_date
            self.stats['files_organized_today'] = 0
            self.stats['tasks_completed'] = 0
            self.stats['pomodoro_sessions'] = 0
        
        self.update_statistics_display()
    
    def update_time(self):
        """Update current time display"""
        self.time_label.setText(datetime.now().strftime('%H:%M'))
    
    def show_about(self):
        """Show about dialog"""
        QMessageBox.information(self, "About",
                               "Workspace Organizer v4.0\n\n"
                               "Advanced File Management\n"
                               "Productivity Tools\n"
                               "Dark Mode Support\n\n"
                               "© 2025")


def main():
    app = QApplication(sys.argv)
    organizer = WorkspaceOrganizer()
    organizer.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
