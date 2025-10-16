# API Reference - Workspace Organizer

**Version**: v4.0  
**Last Updated**: October 16, 2025

---

## 📚 Table of Contents

1. [MainWindow Class](#mainwindow-class)
2. [FileManager Class](#filemanager-class)
3. [NotesManager Class](#notesmanager-class)
4. [Data Models](#data-models)
5. [Utility Functions](#utility-functions)
6. [Styling System](#styling-system)
7. [Signal/Slot System](#signalslot-system)

---

## 🪟 MainWindow Class

### Overview
Main application window inheriting from `QMainWindow`. Manages all UI components and orchestrates interactions between modules.

### Constructor

```python
MainWindow(parent=None)
```

**Parameters**:
- `parent` (QWidget, optional): Parent widget, typically None

**Attributes**:
```python
dark_mode: bool                    # Dark/Light mode flag
current_folder: str                # Currently selected folder path
all_files: List[Dict]              # List of file metadata
kanban_tasks: List[KanbanTask]     # Kanban board tasks
todo_items: List[TodoItem]         # Todo list items
notes: List[str]                   # Note contents
pomodoro_time: int                 # Pomodoro countdown (seconds)
pomodoro_running: bool             # Pomodoro active state
```

### Methods

#### Tab Creation Methods

```python
def create_dashboard_tab() -> QWidget
```
Creates the dashboard with quick stats and actions.

**Returns**: QWidget - Dashboard tab content

**Usage**:
```python
dashboard = self.create_dashboard_tab()
self.tabs.addTab(dashboard, "📊 Dashboard")
```

---

```python
def create_folders_tab() -> QWidget
```
Creates folder navigation interface.

**Returns**: QWidget - Folders tab content

---

```python
def create_files_tab() -> QWidget
```
Creates file list and search interface.

**Returns**: QWidget - Files tab content

---

```python
def create_todo_tab() -> QWidget
```
Creates todo list interface.

**Returns**: QWidget - Todo tab content

**Related Data**:
- `self.todo_items` - List of TodoItem objects
- `self.todo_input` - QLineEdit for input
- `self.todo_list` - QListWidget for display

---

```python
def create_kanban_tab() -> QWidget
```
Creates Kanban board with 3 columns.

**Returns**: QWidget - Kanban tab content

**Related Data**:
- `self.kanban_tasks` - List of KanbanTask objects
- `self.kanban_input` - QLineEdit for task input
- `self.kanban_todo_list` - QFrame (To Do column)
- `self.kanban_progress_list` - QFrame (In Progress column)
- `self.kanban_done_list` - QFrame (Done column)

---

```python
def create_pomodoro_tab() -> QWidget
```
Creates Pomodoro timer interface.

**Returns**: QWidget - Pomodoro tab content

**Related Data**:
- `self.pomodoro_time` - Current countdown (seconds)
- `self.pomodoro_running` - Timer state
- `self.pomodoro_timer` - QTimer instance
- `self.pomodoro_label` - Display label

---

```python
def create_calendar_tab() -> QWidget
```
Creates calendar interface.

**Returns**: QWidget - Calendar tab content

**Related Data**:
- `self.calendar` - QCalendarWidget instance

---

```python
def create_notes_tab() -> QWidget
```
Creates note-taking interface.

**Returns**: QWidget - Notes tab content

**Related Data**:
- `self.notes` - List of note strings
- `self.notes_input` - QTextEdit for input
- `self.notes_list` - QListWidget for display

---

#### Timer Management

```python
def setup_timers() -> None
```
Initialize QTimer instances for clock and Pomodoro.

**Details**:
- Creates `self.time_timer` (updates every 1000ms)
- Creates `self.pomodoro_timer` (updates every 1000ms)
- Connects timeout signals to callbacks

**Important**: Timers stored as instance variables to prevent garbage collection.

**Usage**:
```python
self.setup_timers()  # Called in __init__
```

---

```python
def update_time() -> None
```
Update clock display (called by time_timer).

**Frequency**: Every 1 second

**Updates**: 
- Current time label
- Date label
- Dashboard stats

---

```python
def update_pomodoro() -> None
```
Update Pomodoro countdown (called by pomodoro_timer).

**Frequency**: Every 1 second

**Behavior**:
- Decrements `self.pomodoro_time`
- Updates display
- Resets when time reaches 0

---

#### Kanban Methods

```python
def add_kanban_task() -> None
```
Add new task to Kanban board from input field.

**Gets input from**: `self.kanban_input` (QLineEdit)

**Adds to**: `self.kanban_tasks` (list)

**Creates**: KanbanTask with status "To Do"

**Usage**:
```python
# Connected to "Add" button click
add_btn.clicked.connect(self.add_kanban_task)
```

---

```python
def update_kanban_display() -> None
```
Refresh Kanban board display from task list.

**Gets child widgets**:
- `self.kanban_todo_list.list_widget` (To Do column)
- `self.kanban_progress_list.list_widget` (In Progress)
- `self.kanban_done_list.list_widget` (Done)

**Clears and repopulates** based on task status.

**Called after**: Adding/moving/deleting tasks

---

```python
def create_kanban_column(title: str, color: str) -> QFrame
```
Create a single Kanban column (helper method).

**Parameters**:
- `title` (str): Column header ("To Do", "In Progress", "Done")
- `color` (str): Hex color for border (#ef4444, #f59e0b, #10b981)

**Returns**: QFrame with:
- Column title label
- QListWidget for tasks
- Stored `list_widget` attribute

**Usage**:
```python
column = self.create_kanban_column("To Do", "#ef4444")
```

---

#### Todo Methods

```python
def add_todo_item() -> None
```
Add new item to Todo list.

**Gets input from**: `self.todo_input` (QLineEdit)

**Adds to**: `self.todo_items` (list)

**Creates**: TodoItem with completed=False

---

```python
def update_todo_display() -> None
```
Refresh Todo list display.

**Clears**: `self.todo_list` (QListWidget)

**Repopulates** with items from `self.todo_items`

**Updates checkboxes** based on completion state

---

```python
def toggle_todo_item(item: QListWidgetItem) -> None
```
Toggle completion state of Todo item.

**Parameters**:
- `item` (QListWidgetItem): Item to toggle

**Updates**:
- Todo item completion state
- Checkbox display
- Display refresh

---

#### File Management Methods

```python
def scan_folder_auto(folder_path: str) -> None
```
Auto-scan folder without dialog.

**Parameters**:
- `folder_path` (str): Absolute path to folder

**Updates**:
- `self.current_folder`
- `self.all_files` (list of file metadata)
- Files tab display

**Usage**:
```python
self.scan_folder_auto(os.path.expanduser("~/Desktop"))
```

---

```python
def on_scan_folder_clicked() -> None
```
Handle Scan Folder button click - shows folder dialog.

**Opens**: QFileDialog

**Calls**: `scan_folder_auto()` with selected path

---

```python
def open_vs_code() -> None
```
Open current folder in VS Code.

**Uses**: `subprocess.Popen()` to launch VS Code

**Target**: `self.current_folder`

---

```python
def open_in_explorer() -> None
```
Open current folder in File Explorer.

**Uses**: `os.startfile()` (Windows specific)

**Target**: `self.current_folder`

---

#### Theme Methods

```python
def toggle_dark_mode() -> None
```
Switch between dark and light themes.

**Updates**:
- `self.dark_mode` flag
- All widget stylesheets
- UI components

**Calls**: `self.setStyleSheet()` with new theme

---

#### Display Methods

```python
def update_dashboard_stats() -> None
```
Update statistics display on dashboard.

**Updates**:
- File count
- Storage usage
- Notes count
- Current folder
- Current time

---

```python
def show_message(title: str, message: str) -> None
```
Show information dialog message.

**Parameters**:
- `title` (str): Dialog title
- `message` (str): Message text

**Uses**: QMessageBox.information()

---

---

## 📂 FileManager Class

### Location
`core/file_manager.py`

### Constructor

```python
FileManager(root_folder: str)
```

**Parameters**:
- `root_folder` (str): Base folder for operations

---

### Methods

```python
def scan_folder(folder_path: str) -> List[str]
```
Recursively scan folder and return file paths.

**Parameters**:
- `folder_path` (str): Absolute path to scan

**Returns**: List of absolute file paths

**Behavior**:
- Recursive directory traversal
- Includes all files
- Returns empty list on error

**Example**:
```python
files = file_manager.scan_folder("C:/Users/username/Desktop")
# Returns: ['C:/...file1.txt', 'C:/...file2.pdf', ...]
```

---

```python
def get_file_metadata(file_path: str) -> Dict
```
Extract metadata from file.

**Parameters**:
- `file_path` (str): Absolute file path

**Returns**: Dictionary with keys:
```python
{
    'name': str,           # Filename
    'size': int,           # Size in bytes
    'size_formatted': str, # "1.5 MB"
    'type': str,           # File extension
    'modified': str,       # YYYY-MM-DD HH:MM
    'path': str            # Full path
}
```

**Example**:
```python
meta = file_manager.get_file_metadata("C:/file.txt")
print(meta['size_formatted'])  # "2.3 KB"
```

---

```python
def copy_to_folder(source: str, destination: str) -> bool
```
Copy file or folder to destination.

**Parameters**:
- `source` (str): Source file/folder path
- `destination` (str): Destination folder path

**Returns**: True on success, False on error

**Example**:
```python
success = file_manager.copy_to_folder(
    "C:/file.txt",
    "C:/backup/"
)
```

---

```python
def move_to_folder(source: str, destination: str) -> bool
```
Move file or folder to destination.

**Parameters**:
- `source` (str): Source file/folder path
- `destination` (str): Destination folder path

**Returns**: True on success, False on error

**Example**:
```python
success = file_manager.move_to_folder(
    "C:/unsorted/file.txt",
    "C:/documents/"
)
```

---

```python
def delete_file(file_path: str) -> bool
```
Delete file or folder (recursive).

**Parameters**:
- `file_path` (str): File/folder path to delete

**Returns**: True on success, False on error

**Example**:
```python
success = file_manager.delete_file("C:/temp/file.txt")
```

---

## 📝 NotesManager Class

### Location
`core/notes_manager.py`

### Constructor

```python
NotesManager()
```

---

### Methods

```python
def save_note(content: str) -> int
```
Save new note and return ID.

**Parameters**:
- `content` (str): Note text content

**Returns**: Note ID (integer)

**Example**:
```python
note_id = notes_manager.save_note("My important note")
```

---

```python
def update_note(note_id: int, content: str) -> bool
```
Update existing note by ID.

**Parameters**:
- `note_id` (int): Note ID
- `content` (str): New content

**Returns**: True on success, False if not found

**Example**:
```python
success = notes_manager.update_note(1, "Updated content")
```

---

```python
def delete_note(note_id: int) -> bool
```
Delete note by ID.

**Parameters**:
- `note_id` (int): Note ID to delete

**Returns**: True on success, False if not found

**Example**:
```python
success = notes_manager.delete_note(1)
```

---

```python
def get_all_notes() -> List[Dict]
```
Retrieve all notes.

**Returns**: List of note dictionaries:
```python
[
    {'id': 1, 'content': '...', 'created': '2025-10-16'},
    ...
]
```

**Example**:
```python
all_notes = notes_manager.get_all_notes()
for note in all_notes:
    print(note['content'])
```

---

```python
def search_notes(query: str) -> List[Dict]
```
Search notes by text content.

**Parameters**:
- `query` (str): Search term

**Returns**: Matching notes (case-insensitive)

**Example**:
```python
results = notes_manager.search_notes("important")
```

---

## 📊 Data Models

### KanbanTask

```python
class KanbanTask:
    def __init__(self, title: str, status: str):
        self.title = str              # Task title
        self.status = str             # "To Do", "In Progress", "Done"
        self.created_at = datetime    # Creation timestamp
```

**Example**:
```python
task = KanbanTask("Implement feature", "To Do")
task.status = "In Progress"
```

---

### TodoItem

```python
class TodoItem:
    def __init__(self, text: str, completed: bool = False):
        self.text = str              # Task text
        self.completed = bool        # Completion state
        self.created_at = datetime   # Creation timestamp
```

**Example**:
```python
todo = TodoItem("Buy groceries")
todo.completed = True
```

---

### PomodoroTimer

Data class representing Pomodoro session state:

```python
pomodoro_time: int                 # Remaining seconds (0-1500)
pomodoro_running: bool             # Timer active
pomodoro_sessions: int             # Sessions completed today
```

---

## 🔧 Utility Functions

### Styling

```python
def get_stylesheet(dark_mode: bool = False) -> str
```
Get complete stylesheet for current theme.

**Parameters**:
- `dark_mode` (bool): True for dark, False for light

**Returns**: Complete CSS stylesheet string

**Usage**:
```python
from ui.styles import get_stylesheet
stylesheet = get_stylesheet(dark_mode=True)
self.setStyleSheet(stylesheet)
```

---

```python
def get_dark_stylesheet() -> str
```
Get dark mode stylesheet (~280 lines CSS).

**Returns**: Dark theme CSS

**Colors Used**:
- Background: #1e1e1e
- Secondary: #2d2d2d
- Text: #e0e0e0
- Accent: #667eea

---

```python
def get_light_stylesheet() -> str
```
Get light mode stylesheet (~250 lines CSS).

**Returns**: Light theme CSS

**Colors Used**:
- Background: #f5f7fa
- Secondary: #f0f0f0
- Text: #333
- Accent: #667eea

---

## 🔌 Signal/Slot System

### Qt Signals (Read-Only)

These are Qt signals that can be connected to:

```python
QLineEdit.returnPressed       # Enter key in text field
QPushButton.clicked           # Button clicked
QListWidget.itemClicked       # List item clicked
QListWidget.itemDoubleClicked # List item double-clicked
QCheckBox.stateChanged        # Checkbox toggled
QTabWidget.currentChanged     # Tab switched
```

### Common Connections

```python
# Connect button to method
button.clicked.connect(self.on_button_click)

# Connect text input to handler
input_field.returnPressed.connect(self.on_return_pressed)

# Connect list selection
list_widget.itemClicked.connect(self.on_item_selected)

# Connect checkbox
checkbox.stateChanged.connect(self.on_checkbox_toggled)

# Connect tab change
tabs.currentChanged.connect(self.on_tab_changed)
```

---

## 📋 Usage Examples

### Adding a Kanban Task

```python
# From UI
text = self.kanban_input.text().strip()
if text:
    task = KanbanTask(text, "To Do")
    self.kanban_tasks.append(task)
    self.kanban_input.clear()
    self.update_kanban_display()
```

### Creating a New Tab

```python
def create_myfeature_tab(self):
    widget = QWidget()
    if self.dark_mode:
        widget.setStyleSheet("background-color: #1e1e1e;")
    
    layout = QVBoxLayout(widget)
    
    # Add components
    label = QLabel("My Feature")
    layout.addWidget(label)
    
    return widget

# Register tab
self.tabs.addTab(self.create_myfeature_tab(), "🎯 My Feature")
```

### File Operations

```python
# Scan folder
files = self.file_manager.scan_folder("C:/Desktop")

# Copy file
success = self.file_manager.copy_to_folder(
    "C:/source.txt",
    "C:/destination/"
)

# Get file info
meta = self.file_manager.get_file_metadata("C:/file.pdf")
print(f"{meta['name']}: {meta['size_formatted']}")
```

### Notes Operations

```python
# Create note
note_id = self.notes_manager.save_note("Meeting notes...")

# Search notes
results = self.notes_manager.search_notes("project")

# Update note
success = self.notes_manager.update_note(note_id, "Updated...")

# Delete note
success = self.notes_manager.delete_note(note_id)
```

---

**Last Updated**: October 16, 2025  
**API Version**: 1.0  
**Status**: Stable (v4.0)

