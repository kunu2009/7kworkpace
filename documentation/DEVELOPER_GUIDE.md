# Developer Guide - Workspace Organizer

**Version**: v4.0  
**Last Updated**: October 16, 2025

---

## 📖 Table of Contents

1. [Getting Started](#getting-started)
2. [Development Environment Setup](#development-environment-setup)
3. [Project Structure](#project-structure)
4. [Contributing Guide](#contributing-guide)
5. [Common Tasks](#common-tasks)
6. [Debugging Tips](#debugging-tips)
7. [Testing](#testing)
8. [Performance Profiling](#performance-profiling)
9. [Git Workflow](#git-workflow)
10. [FAQ](#faq)

---

## 🚀 Getting Started

### Prerequisites
- Python 3.8+
- pip (Python package manager)
- Git
- VS Code (recommended)

### Quick Start

```bash
# Clone the repository
git clone https://github.com/yourusername/workspace-organizer.git
cd Workspace-Organizer

# Create virtual environment
python -m venv venv
.\venv\Scripts\activate  # Windows
source venv/bin/activate  # macOS/Linux

# Install dependencies
pip install -r requirements.txt

# Run the application
python main.py
```

---

## 🔧 Development Environment Setup

### VS Code Extensions (Recommended)

1. **Python**
   - ms-python.python
   - For debugging and IntelliSense

2. **Pylance**
   - ms-python.vscode-pylance
   - Type checking and code analysis

3. **Black Formatter**
   - ms-python.black-formatter
   - Code formatting

4. **Pylint**
   - ms-python.pylint
   - Linting

5. **Git Graph**
   - mhutchie.git-graph
   - Git visualization

### PyCharm Configuration (Alternative)

```
Settings → Project → Python Interpreter
  ↓
Add Interpreter → Add Local Interpreter
  ↓
Select Python 3.8+ from venv
```

### IDE Debug Configuration

**VS Code** (`.vscode/launch.json`):
```json
{
    "version": "0.2.0",
    "configurations": [
        {
            "name": "Python: Workspace Organizer",
            "type": "python",
            "request": "launch",
            "program": "${workspaceFolder}/main.py",
            "console": "integratedTerminal",
            "justMyCode": true
        }
    ]
}
```

**PyCharm**: 
- Right-click main.py → Run 'main'
- Use debug mode (F9) from toolbar

---

## 📁 Project Structure Walkthrough

### Core Entry Point: main.py

```python
# Structure
├── Imports (PyQt6, os, sys, etc.)
├── Data Classes
│   ├── KanbanTask
│   ├── TodoItem
│   └── PomodoroTimer
├── MainWindow Class (1300+ lines)
│   ├── __init__()
│   ├── UI Creation Methods
│   ├── Event Handlers
│   └── Update Methods
└── main()
    └── app = QApplication()
        └── window = MainWindow()
        └── app.exec()
```

### Module: ui/styles.py

```python
# Functions
├── get_stylesheet(dark_mode=False)
├── get_light_stylesheet()
└── get_dark_stylesheet()

# CSS Organization
├── QMainWindow
├── QWidget
├── QPushButton (with :hover, :pressed states)
├── QLineEdit/QTextEdit
├── QListWidget
├── QTableWidget
├── QCalendarWidget
├── QTabBar
└── ... (25+ widget types)
```

### Module: core/file_manager.py

```python
class FileManager:
    def __init__(self, root_folder)
    def scan_folder(self, folder_path)
    def get_file_metadata(self, file_path)
    def copy_to_folder(self, source, destination)
    def move_to_folder(self, source, destination)
    def delete_file(self, file_path)
```

### Module: core/notes_manager.py

```python
class NotesManager:
    def __init__(self)
    def save_note(self, content)
    def update_note(self, note_id, content)
    def delete_note(self, note_id)
    def get_all_notes(self)
    def search_notes(self, query)
```

---

## 🤝 Contributing Guide

### Before You Start

1. **Fork the repository**
   ```bash
   gh repo fork yourusername/workspace-organizer
   ```

2. **Create a feature branch**
   ```bash
   git checkout -b feature/your-feature-name
   ```

3. **Keep your branch up-to-date**
   ```bash
   git fetch origin
   git rebase origin/develop
   ```

### Making Changes

#### Step 1: Understand the Feature
- Read the ROADMAP_AND_FEATURES.md
- Understand the current architecture
- Plan your implementation

#### Step 2: Implement the Feature
- Write clean, documented code
- Follow naming conventions
- Add type hints
- Keep methods small and focused

#### Step 3: Test Your Changes
- Run existing tests
- Write new tests for your feature
- Test manually in the app
- Check performance impact

#### Step 4: Commit Your Changes
```bash
git add .
git commit -m "feat: add feature description

- Added new X functionality
- Updated Y component
- Fixed Z bug"
```

#### Step 5: Push and Create PR
```bash
git push origin feature/your-feature-name
```
Then create a Pull Request on GitHub with:
- Clear description of changes
- Link to related issues
- Screenshots (if UI changes)
- Testing checklist

### Code Review Process

1. **Automated Checks**
   - Linting passes
   - Tests pass
   - No conflicts

2. **Manual Review**
   - Code quality
   - Design patterns
   - Documentation
   - Performance impact

3. **Approval & Merge**
   - Minimum 1 approval required
   - Squash and merge to develop

---

## 🛠️ Common Tasks

### Adding a New Tab

#### 1. Create the Tab Creation Method

```python
def create_my_tab(self):
    """Create My New Tab"""
    widget = QWidget()
    
    # Apply dark mode if needed
    if self.dark_mode:
        widget.setStyleSheet("background-color: #1e1e1e; color: #e0e0e0;")
    
    layout = QVBoxLayout(widget)
    layout.setContentsMargins(15, 15, 15, 15)
    
    # Add title
    title = QLabel("📌 My Tab Title")
    title_style = "font-size: 18px; font-weight: bold; color: %s;" % (
        "#e0e0e0" if self.dark_mode else "#333"
    )
    title.setStyleSheet(title_style)
    layout.addWidget(title)
    
    # Add your content here
    # layout.addWidget(your_widget)
    
    return widget
```

#### 2. Register the Tab in MainWindow.__init__()

```python
# In self.tabs setup
self.tabs.addTab(self.create_my_tab(), "📌 My Tab")
```

### Adding a New Styling Rule

#### Edit ui/styles.py:

```python
def get_dark_stylesheet():
    return """
    # ... existing styles ...
    
    QMyCustomWidget {
        background-color: #2d2d2d;
        color: #e0e0e0;
        border: 2px solid #667eea;
        border-radius: 5px;
        padding: 10px;
    }
    
    QMyCustomWidget:hover {
        border: 2px solid #764ba2;
    }
    """
```

### Adding a New Data Model

#### Create a class in main.py:

```python
class MyDataModel:
    """Description of your data model"""
    
    def __init__(self, title, description):
        self.title = title
        self.description = description
        self.created_at = datetime.now()
        
    def __repr__(self):
        return f"MyDataModel(title={self.title})"
```

#### Use in MainWindow:

```python
class MainWindow:
    def __init__(self):
        # Initialize your data list
        self.my_data_items = []
    
    def add_item(self, title, description):
        item = MyDataModel(title, description)
        self.my_data_items.append(item)
        self.update_display()
```

### Adding a File Operation

#### In core/file_manager.py:

```python
def your_operation(self, input_path):
    """Description of operation"""
    try:
        # Perform operation
        result = your_logic(input_path)
        return result
    except Exception as e:
        print(f"Error in your_operation: {e}")
        return None
```

#### Use in MainWindow:

```python
def on_button_click(self):
    result = self.file_manager.your_operation(self.current_folder)
    if result:
        self.show_message("Success", "Operation completed!")
```

---

## 🐛 Debugging Tips

### Print Debugging

```python
# Simple console output
print(f"Debug: {variable_name} = {variable_value}")

# In Qt context
print(f"Widget geometry: {widget.geometry()}")
```

### Qt Debugging

```python
# Check if widget is visible
print(f"Is visible: {widget.isVisible()}")

# Check stylesheet
print(f"Stylesheet: {widget.styleSheet()}")

# Check widget hierarchy
def print_hierarchy(widget, indent=0):
    print("  " * indent + widget.__class__.__name__)
    for child in widget.children():
        print_hierarchy(child, indent + 1)

print_hierarchy(self)
```

### Common Issues & Solutions

**Issue**: "White elements in dark mode"
- Check if stylesheet is applied
- Verify color values are correct
- Ensure transparency is set properly

```python
# Debug stylesheet
print(self.styleSheet())

# Apply debug style temporarily
widget.setStyleSheet("background-color: red;")  # Should show red if applied
```

**Issue**: "Timer not running"
- Verify timer is stored as instance variable (self.timer)
- Check if start() is called
- Verify timeout signal is connected

```python
print(f"Timer active: {self.pomodoro_timer.isActive()}")
print(f"Timer connections: {self.pomodoro_timer.receivers()}")
```

**Issue**: "Data not persisting"
- Add debug prints in save/load functions
- Check file paths
- Verify file permissions

```python
print(f"Saving to: {file_path}")
print(f"Data: {data}")
# Check if file exists after save
print(f"File exists: {os.path.exists(file_path)}")
```

### VS Code Debugging

1. **Set Breakpoint**: Click line number
2. **Run Debug**: F5 or Debug menu
3. **Step Through**: F10 (next line), F11 (into function)
4. **Watch Variables**: Add to watch panel
5. **Evaluate**: Click variables to see values

---

## 🧪 Testing

### Running Tests

```bash
# Run all tests
pytest

# Run specific test file
pytest tests/test_file_manager.py

# Run with coverage
pytest --cov=core --cov-report=html
```

### Writing Tests

#### Example Test:

```python
# tests/test_file_manager.py
import pytest
from core.file_manager import FileManager

class TestFileManager:
    def setup_method(self):
        self.fm = FileManager("test_folder")
    
    def test_scan_folder(self):
        result = self.fm.scan_folder("test_folder")
        assert result is not None
        assert isinstance(result, list)
    
    def test_invalid_path(self):
        result = self.fm.scan_folder("/invalid/path")
        assert result == []
```

### Test Coverage

```bash
# Generate coverage report
pytest --cov=core --cov-report=html

# View report
open htmlcov/index.html
```

---

## ⚡ Performance Profiling

### CPU Profiling

```python
import cProfile
import pstats

# Profile the app startup
profiler = cProfile.Profile()
profiler.enable()

# ... run your code ...

profiler.disable()
stats = pstats.Stats(profiler)
stats.sort_stats('cumulative')
stats.print_stats(20)  # Top 20 functions
```

### Memory Profiling

```python
from memory_profiler import profile

@profile
def expensive_function():
    # Your code here
    pass
```

### Identify Bottlenecks

```bash
# Run with profiling
python -m cProfile -s cumtime main.py

# Sort by time
python -m cProfile -s time main.py
```

---

## 🔄 Git Workflow

### Branch Naming Convention

```
feature/kanban-drag-drop       # New feature
bugfix/timer-not-running       # Bug fix
docs/setup-guide               # Documentation
chore/update-dependencies      # Maintenance
```

### Commit Message Format

```
<type>: <subject>

<body>

<footer>

# Types: feat, fix, docs, style, refactor, perf, test, chore
# Subject: 50 chars max, imperative mood
# Body: Explain what and why
# Footer: Reference issues (Fixes #123)
```

### Example Commits

```bash
git commit -m "feat: add drag-and-drop to Kanban board

- Implement QDrag and QDropEvent
- Update task order on drop
- Add visual feedback during drag

Closes #42"
```

---

## ❓ FAQ

### Q: How do I add a new dependency?

```bash
# Install the package
pip install package-name

# Update requirements.txt
pip freeze > requirements.txt

# Commit changes
git add requirements.txt
git commit -m "chore: add package-name dependency"
```

### Q: How do I debug the UI rendering?

```python
# Enable Qt debugging
import os
os.environ['QT_DEBUG_PLUGINS'] = '1'

# Show widget hierarchy
from PyQt6.QtWidgets import QApplication
app = QApplication.instance()

def print_all_widgets(widget, level=0):
    print("  " * level + widget.__class__.__name__)
    for child in widget.children():
        if hasattr(child, 'children'):
            print_all_widgets(child, level + 1)

print_all_widgets(window)
```

### Q: How do I profile performance?

```bash
# Install py-spy
pip install py-spy

# Profile the app
py-spy record -o profile.svg python main.py

# View profile
# Open profile.svg in browser (shows flame graph)
```

### Q: How do I run the app in development mode with hot reload?

```bash
# Install watchdog
pip install watchdog

# Create watch script
watchmedo shell-command \
    --patterns="*.py" \
    --recursive \
    --command='python main.py' \
    .
```

### Q: Where do I report bugs?

1. Check existing issues on GitHub
2. Create new issue with:
   - Detailed description
   - Steps to reproduce
   - Expected vs actual behavior
   - Screenshots
   - Python version
   - OS

### Q: How do I request a new feature?

1. Open an issue titled "Feature: Your Feature Name"
2. Describe the feature
3. Explain use case and benefit
4. Suggest implementation approach (optional)
5. Link to related issues

### Q: How do I contribute documentation?

1. Fork and create documentation branch
2. Write in Markdown format
3. Follow existing documentation style
4. Include code examples
5. Test links and formatting
6. Create PR with documentation changes

---

## 📞 Getting Help

- **GitHub Issues**: Report bugs and feature requests
- **Discussions**: General questions and ideas
- **Code Review**: Questions about implementation
- **Email**: developers@workspaceorganizer.local

---

**Last Updated**: October 16, 2025  
**Version**: 1.0

