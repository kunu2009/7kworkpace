# Workspace Organizer - Architecture & Design Documentation

**Version**: v4.0  
**Date**: October 16, 2025

---

## 📐 System Architecture

### High-Level Overview

```
┌─────────────────────────────────────────────────────────────┐
│                        UI Layer (PyQt6)                      │
│  ┌────────────────────────────────────────────────────────┐  │
│  │ Dashboard │ Folders │ Files │ Todo │ Kanban │ Pomodoro│ │
│  │  Calendar │  Notes  │Analytics│ Organization         │  │
│  └────────────────────────────────────────────────────────┘  │
└──────────────────────┬───────────────────────────────────────┘
                       │
┌──────────────────────▼───────────────────────────────────────┐
│                   Business Logic Layer                        │
│  ┌────────────────────────────────────────────────────────┐  │
│  │  FileManager  │ NotesManager │ TaskManager │ Timers  │  │
│  └────────────────────────────────────────────────────────┘  │
└──────────────────────┬───────────────────────────────────────┘
                       │
┌──────────────────────▼───────────────────────────────────────┐
│                    Data Layer                                 │
│  ┌────────────────────────────────────────────────────────┐  │
│  │  JSON Files  │  SQLite (future)  │  Cloud Sync (v5)  │  │
│  └────────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────┘
```

---

## 🗂️ Directory Structure

```
Workspace-Organizer/
├── main.py                    # Entry point (1300+ lines)
├── requirements.txt           # Dependencies
├── ui/
│   ├── __init__.py
│   ├── styles.py             # CSS/Stylesheet definitions
│   └── widgets.py            # Custom widget components
├── core/
│   ├── __init__.py
│   ├── file_manager.py       # File operations
│   └── notes_manager.py      # Note storage/retrieval
├── documentation/
│   ├── ROADMAP_AND_FEATURES.md
│   ├── ARCHITECTURE.md
│   ├── SETUP_GUIDE.md
│   └── API_REFERENCE.md
├── assets/
│   ├── icons/
│   ├── images/
│   └── fonts/
└── tests/                     # Unit tests (planned)
```

---

## 🔄 Application Flow

### Startup Sequence

```
1. main.py loads
2. Import all dependencies (PyQt6, etc.)
3. Create MainWindow instance
4. Initialize data managers (FileManager, NotesManager)
5. Setup UI components (10 tabs)
6. Load user preferences (dark mode, default folder)
7. Start timers (clock, Pomodoro)
8. Show main window
9. Auto-scan default folder (Desktop)
```

### Tab Loading

Each tab is created lazily:
- Dashboard: Loads immediately
- Other tabs: Created on demand when clicked
- Data cached in class variables (self.kanban_tasks, self.todo_items, etc.)

---

## 🏗️ Core Classes & Modules

### main.py - MainWindow Class

**Responsibilities**:
- UI creation and management
- Tab coordination
- Timer management
- Theme switching
- File operations integration

**Key Methods**:
```python
class MainWindow(QMainWindow):
    # Initialization
    __init__()              # Setup window and UI
    setup_timers()          # Start clock/Pomodoro timers
    
    # Tab Creation
    create_dashboard_tab()  # Overview and stats
    create_folders_tab()    # Folder navigation
    create_files_tab()      # File list and search
    create_organization_tab()  # Auto-organization
    create_todo_tab()       # Task management
    create_kanban_tab()     # Kanban board
    create_pomodoro_tab()   # Timer
    create_calendar_tab()   # Calendar
    create_notes_tab()      # Note-taking
    create_analytics_tab()  # Statistics
    
    # Updates & Data
    update_time()           # Clock updates
    update_pomodoro()       # Timer tick
    update_kanban_display() # Refresh Kanban
    update_todo_display()   # Refresh Todo
    
    # Events
    on_theme_change()       # Dark/Light mode toggle
    scan_folder_auto()      # File scanning
```

### core/file_manager.py - FileManager Class

**Responsibilities**:
- Scanning directories
- File metadata extraction
- File operations (copy, move, delete)
- File categorization

**Key Methods**:
```python
class FileManager:
    scan_folder(path)           # Recursive folder scan
    get_file_metadata(path)     # Extract file info
    copy_to_folder(src, dest)   # Copy operations
    move_to_folder(src, dest)   # Move operations
    delete_file(path)           # Delete with safety
```

### core/notes_manager.py - NotesManager Class

**Responsibilities**:
- Note CRUD operations
- Note persistence
- Note categorization

**Key Methods**:
```python
class NotesManager:
    save_note(content)          # Save new note
    update_note(note_id, content)  # Edit note
    delete_note(note_id)        # Delete note
    get_all_notes()             # Retrieve notes
    search_notes(query)         # Search notes
```

### Data Models

#### KanbanTask
```python
class KanbanTask:
    title: str              # Task title
    status: str            # "To Do", "In Progress", "Done"
    created_at: datetime   # Creation timestamp
    # Future: due_date, priority, color, description
```

#### TodoItem
```python
class TodoItem:
    text: str              # Task text
    completed: bool        # Completion status
    created_at: datetime   # Creation timestamp
    # Future: due_date, priority, category, recurring
```

#### PomodoroTimer
```python
class PomodoroTimer:
    duration: int          # 25 minutes default
    elapsed: int           # Current elapsed time
    state: str             # "running", "paused", "break"
    sessions_today: int    # Count
    # Future: history, stats, preferences
```

---

## 💾 Data Persistence

### Current Approach (v4.0)
- **Kanban Tasks**: Stored in Python list (self.kanban_tasks)
- **Todo Items**: Stored in Python list (self.todo_items)
- **Notes**: Stored in Python list (self.notes)
- **User Preferences**: Application defaults

**Limitation**: Data is lost on app restart (in-memory only)

### Planned Improvement (v4.1)
- JSON file persistence in `~/.workspace-organizer/`
- Auto-save on changes
- Backup versioning

### Future (v5.0)
- SQLite database for scalability
- Cloud sync support
- Backup automation

---

## 🎨 UI/Styling Architecture

### Theme System

**File**: `ui/styles.py`

Two main functions:
1. `get_light_stylesheet()` - Light theme CSS
2. `get_dark_stylesheet()` - Dark theme CSS

**Application**:
```python
def get_stylesheet(dark_mode=False):
    if dark_mode:
        return get_dark_stylesheet()
    return get_light_stylesheet()

# Usage in MainWindow
self.setStyleSheet(get_stylesheet(self.dark_mode))
```

### Color Schemes

**Dark Mode**:
- Background: #1e1e1e
- Secondary: #2d2d2d
- Text: #e0e0e0
- Accent: #667eea

**Light Mode**:
- Background: #f5f7fa
- Secondary: #f0f0f0
- Text: #333
- Accent: #667eea

### Widget-Specific Styling

CSS rules for each widget type:
- QLineEdit/QTextEdit - Text input areas
- QPushButton - All buttons
- QListWidget - List displays
- QTableWidget - Table displays
- QCalendarWidget - Calendar view
- QTabBar - Tab headers
- QScrollBar - Scroll areas

---

## ⏱️ Timer Architecture

### QTimer Usage

Two separate QTimer instances:

1. **time_timer** (self.time_timer)
   - Interval: 1000ms (1 second)
   - Callback: update_time()
   - Purpose: Update clock display

2. **pomodoro_timer** (self.pomodoro_timer)
   - Interval: 1000ms (1 second)
   - Callback: update_pomodoro()
   - Purpose: Countdown timer

**Important**: Timers stored as instance variables to prevent garbage collection

### State Management

```python
self.pomodoro_time = 25 * 60  # Seconds (25 minutes)
self.pomodoro_running = False
self.pomodoro_sessions = 0

def update_pomodoro(self):
    if self.pomodoro_running:
        self.pomodoro_time -= 1
        self.pomodoro_label.setText(time_format(self.pomodoro_time))
        
        if self.pomodoro_time <= 0:
            # Session complete
            self.pomodoro_running = False
            self.show_notification()
```

---

## 🔌 Integration Points

### File Manager Integration
- **Folders Tab**: Uses FileManager.scan_folder()
- **Files Tab**: Uses FileManager metadata
- **Organization Tab**: Uses FileManager operations

### External Applications
- **VS Code**: subprocess call with folder path
- **File Explorer**: subprocess with file/folder path
- **Copy/Paste**: Clipboard integration (QClipboard)

---

## 🔐 Security Considerations

### Current Implementation
- File access via os.path module
- No encryption or authentication
- Local file operations only

### Future Improvements (v5.0)
- Encryption for cloud sync
- User authentication
- Permission-based access control
- Audit logging

---

## 📊 Performance Characteristics

### Startup
- Import time: ~500ms
- UI creation: ~800ms
- Initial file scan: ~200ms (Desktop folder)
- Total: ~1.5s

### Runtime
- UI response: ~50ms
- File operations: Async where possible
- Memory usage: ~80MB (baseline)

### Optimization Strategies
1. Lazy tab loading (create on demand)
2. Threading for file operations
3. Caching of file metadata
4. Efficient list updates (clear + repopulate)

---

## 🧪 Testing Strategy (Planned)

### Unit Tests
- FileManager operations
- Note persistence
- Timer logic
- Data models

### Integration Tests
- Tab interactions
- File operations
- Data synchronization
- UI updates

### UI Tests
- Theme switching
- Tab navigation
- Button clicks
- Keyboard shortcuts

---

## 🚀 Deployment

### Distribution Methods (Planned)
1. **EXE**: PyInstaller build
2. **Portable**: No installation required
3. **Installer**: NSIS installer
4. **Zip**: Source distribution

### Dependencies
```
PyQt6==6.6.1
PyQt6-sip==13.5.2
```

---

## 📚 Code Style Guidelines

### Naming Conventions
- **Classes**: PascalCase (MainWindow, FileManager)
- **Functions**: snake_case (create_folder_tab)
- **Constants**: UPPER_SNAKE_CASE (DEFAULT_TIMEOUT)
- **Private**: _leading_underscore (_internal_method)

### Documentation
- Docstrings for all classes and methods
- Type hints where applicable
- Comments for complex logic

### Best Practices
- DRY (Don't Repeat Yourself)
- Single responsibility principle
- Meaningful variable names
- Keep methods focused and small

---

## 🔄 Version Control & Releases

### Branching Model
- `main` - Stable releases
- `develop` - Development branch
- `feature/*` - Feature branches

### Release Process
1. Create release branch
2. Bump version in code
3. Update changelog
4. Merge to main and tag
5. Build distributions
6. Deploy to platforms

---

## 📖 Future Architecture Improvements

### Planned Changes
1. **Plugin System**: Dynamic extension loading
2. **Service Layer**: Abstracted business logic
3. **API Layer**: REST API for integrations
4. **Database**: Migration to SQLite/PostgreSQL
5. **Async/Await**: Async operations throughout
6. **Dependency Injection**: Better testability

### Technical Debt
- [ ] Split main.py into smaller modules
- [ ] Implement proper error handling
- [ ] Add logging throughout
- [ ] Create comprehensive tests
- [ ] Document all APIs
- [ ] Standardize UI components

---

**Last Updated**: October 16, 2025  
**Architecture Version**: 1.0  
**Next Review**: v5.0 planning

