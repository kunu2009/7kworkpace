# Workspace Organizer - Python Desktop Application

A beautiful, modern productivity dashboard for organizing files, notes, and managing your workspace on Windows.

## Features

✨ **Beautiful Dashboard**
- Modern UI with gradient colors and smooth animations
- Calendar integration
- Real-time clock and date display
- Quick statistics on your files

📁 **File Management**
- Scan and organize folders automatically
- Categorize files by type (Documents, Images, Videos, etc.)
- Search functionality
- File browser with recent files

📝 **Notes Management**
- Create and manage notes
- Save notes with timestamps
- Search through notes
- Quick note access from dashboard

📊 **Productivity Stats**
- Total files count
- Storage usage
- File categorization
- Quick access to frequently used files

## Installation

### Prerequisites
- Python 3.8 or higher
- Windows OS

### Quick Setup

1. **Clone/Extract the project** to your desired location

2. **Install dependencies:**
```bash
python -m pip install -r requirements.txt
```

3. **Run the application:**
```bash
python main.py
```

Or use the quick start menu:
```bash
python quickstart.py
```

## Building Executable

To create a standalone `.exe` file:

```bash
python build_exe.py
```

The executable will be created in the `dist/` folder as `WorkspaceOrganizer.exe`

### Create Desktop Shortcut
1. Navigate to `dist/` folder
2. Right-click `WorkspaceOrganizer.exe`
3. Select "Send to > Desktop (create shortcut)"

## Project Structure

```
Workspace-Organizer/
├── main.py              # Main application entry point
├── build_exe.py         # Build script for creating executable
├── quickstart.py        # Quick start menu
├── requirements.txt     # Python dependencies
├── ui/
│   ├── __init__.py
│   ├── widgets.py      # Custom UI widgets
│   └── styles.py       # Stylesheet definitions
└── core/
    ├── __init__.py
    ├── file_manager.py # File scanning and management
    └── notes_manager.py # Notes storage and retrieval
```

## Usage

### Scanning a Folder
1. Click "Scan Folder" button in the left sidebar
2. Select a folder to organize
3. The app will display all files in that folder
4. Files are automatically categorized

### Creating Notes
1. Go to the "Notes" tab
2. Click "+ New Note"
3. Type your note
4. Your notes are automatically saved

### Viewing Calendar
1. Go to the "Calendar" tab
2. Select dates and view events
3. Check your productivity statistics

## Data Storage

All your data is stored locally in:
```
C:\Users\YourUsername\.workspace_organizer\
```

- `config.json` - Application settings
- `notes/` - Your saved notes

## Keyboard Shortcuts

| Shortcut | Action |
|----------|--------|
| `Ctrl+N` | New Note |
| `Ctrl+S` | Scan Folder |
| `Ctrl+Q` | Quit Application |

## Customization

### Change Theme Colors
Edit `ui/styles.py` and modify the color values:
- Primary color: `#667eea` (purple)
- Secondary color: `#764ba2` (darker purple)
- Background: `#f5f7fa` (light gray)

### Add More Categories
Edit `core/file_manager.py` and add file extensions to the categorization logic.

## Troubleshooting

### App won't start
- Make sure all dependencies are installed: `pip install -r requirements.txt`
- Check that Python 3.8+ is installed

### Executable won't run
- Try rebuilding: `python build_exe.py`
- Make sure you have admin privileges if running from restricted folders

### Notes not saving
- Check that `C:\Users\YourUsername\.workspace_organizer\` exists
- Verify you have write permissions to that folder

## Performance Tips

- Avoid scanning very large folders (with 100k+ files) at once
- Close the app before the folder changes externally
- Clear old notes periodically to keep the app responsive

## Future Enhancements

- [ ] Cloud sync for notes
- [ ] File tagging system
- [ ] Custom color themes
- [ ] Dark mode
- [ ] File preview
- [ ] Scheduled backups
- [ ] Integration with cloud storage
- [ ] Multi-folder scanning

## Support

For issues or feature requests, check the code comments or modify the files as needed.

## License

Free to use and modify for personal use.

---

Happy organizing! 🎉 Boost your productivity with Workspace Organizer!
