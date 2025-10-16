# Implementation Plan for Workspace Organizer v4.1+

**Status**: Phase 1 Implementation Started  
**Last Updated**: October 16, 2025  
**Version**: v4.0 → v4.1

---

## ✅ Completed in v4.0
- [x] Dashboard with quick stats
- [x] File management (folders, files, organization)
- [x] Todo list with checkboxes
- [x] Kanban board (3 columns: To Do, In Progress, Done)
- [x] Pomodoro timer (25 min work, 5 min break)
- [x] Notes tab
- [x] Calendar
- [x] Analytics tab
- [x] Dark/Light mode toggle
- [x] File organization (by type, by date)
- [x] Duplicate detection
- [x] Empty folder cleanup

---

## 🚀 Currently Implementing (Phase 1: v4.1)

### Quick Wins - High Priority (Easy, Fast, High Value)

#### ✅ 1. Keyboard Shortcuts (COMPLETE)
**Shortcuts Implemented**:
- `Ctrl+N` → Focus on Todo input (switch to Todo tab)
- `Ctrl+K` → Focus on Kanban input (switch to Kanban tab)
- `Ctrl+S` → Save note (or quick save action)
- `Ctrl+Q` → Quit application
- `Alt+O` → Organize files dialog
- `Alt+S` → Scan folder
- `Alt+T` → Toggle dark/light mode

**Files Modified**: `main.py`
**Methods Added**:
- `setup_keyboard_shortcuts()` - Register all shortcuts
- `focus_todo_input()` - Ctrl+N handler
- `focus_kanban_input()` - Ctrl+K handler
- `quick_save()` - Ctrl+S handler

**Status**: ✅ IMPLEMENTED & TESTED

---

#### 🔄 2. Global Search Bar (IN PROGRESS)
**Features to Add**:
- [ ] Search across files, todos, kanban tasks, notes
- [ ] Search with filters (file type, date range, priority)
- [ ] Search history (last 10 searches)
- [ ] Recent search suggestions
- [ ] Real-time search results
- [ ] Search in: Files | Todos | Kanban | Notes | All

**Implementation Plan**:
1. Create new "Search" tab with search UI
2. Add search_history list to track recent searches
3. Implement search functions for each data type:
   - `search_files(query)` - Search all_files by name, type, path
   - `search_todos(query)` - Search todos by title
   - `search_kanban(query)` - Search kanban_tasks by title
   - `search_notes(query)` - Search notes_manager by content
4. Add search result display with clickable results
5. Add Ctrl+F shortcut to focus search bar
6. Add search history display

**Estimated Time**: 2-3 days

---

#### 3. App Statistics (Quick)
**Features to Add**:
- [ ] Files organized today (count)
- [ ] Tasks completed today (count)
- [ ] Time focused (Pomodoro sessions completed)
- [ ] Current streak (days)
- [ ] Display in dashboard or sidebar

**Implementation Plan**:
1. Add statistics tracking to data models
2. Create stats dashboard card
3. Update stats on file organization and task completion
4. Add streak counter to Pomodoro timer

**Estimated Time**: 1 day

---

#### 4. Favorites & Pinning (Quick)
**Features to Add**:
- [ ] Pin important tasks to top
- [ ] Favorite folders for quick access
- [ ] Star important notes
- [ ] Quick access bar showing pinned items
- [ ] Ctrl+P to pin current item

**Implementation Plan**:
1. Add `is_pinned` boolean to task/note models
2. Create quick access bar at top of relevant tabs
3. Add pin/unpin button to items
4. Sort pinned items to top

**Estimated Time**: 1 day

---

#### 5. Export Features
**Features to Add**:
- [ ] Export todos to CSV
- [ ] Export kanban tasks to CSV
- [ ] Export calendar to iCal format
- [ ] Export notes to PDF/HTML
- [ ] Export with customizable fields

**Estimated Time**: 2-3 days

---

#### 6. Settings Panel
**Features to Add**:
- [ ] Sound preferences (enable/disable, volume)
- [ ] Notification settings
- [ ] Theme customization
- [ ] Default folder settings
- [ ] Auto-save interval
- [ ] Export settings/Import settings

**Estimated Time**: 2-3 days

---

#### 7. System Tray Integration
**Features to Add**:
- [ ] Minimize to tray (show/hide from tray)
- [ ] Quick access menu from tray
- [ ] Tray notifications for:
  - Pomodoro timer end
  - Task reminders
  - Low storage warnings
- [ ] Ctrl+M to minimize to tray

**Estimated Time**: 1-2 days

---

### Phase 1A: Kanban Board Enhancements

#### Features to Add:
- [ ] Task prioritization (High, Medium, Low) with color coding
- [ ] Task due dates (QDateEdit)
- [ ] Task descriptions/notes (expandable)
- [ ] Task categories/tags
- [ ] Drag-and-drop between columns
- [ ] Inline task editing
- [ ] Delete task with confirmation
- [ ] Export tasks to CSV
- [ ] Task search/filter
- [ ] Recycle bin for deleted tasks
- [ ] Task creation keyboard shortcut (Ctrl+K) ✅

**Technical Details**:
- Extend `KanbanTask` class with: due_date, description, category, priority, color
- Implement Qt drag-and-drop (QDrag, QDropEvent)
- Add task detail dialog for editing
- Persistent storage in JSON file (json module)
- Add `deleted_tasks` list with recovery option

**Estimated Time**: 4-5 days

---

### Phase 1B: Todo List Enhancements

#### Features to Add:
- [ ] Task due dates (QDateEdit)
- [ ] Recurring tasks (Daily, Weekly, Monthly) using `dateutil.rrule`
- [ ] Task priority levels (High, Medium, Low)
- [ ] Categories/Projects
- [ ] Subtasks (tree view)
- [ ] Time tracking per task
- [ ] Task completion history
- [ ] Smart sorting (by priority, date, status)
- [ ] Bulk edit/delete
- [ ] Task templates
- [ ] Undo/Redo functionality

**Technical Details**:
- Extend `TodoItem` class with new properties
- Use SQLite for better querying (add core/database.py)
- Use `dateutil.rrule` for recurrence
- Create QTreeWidget for subtasks
- Implement undo stack using Qt's QUndoStack

**Estimated Time**: 5-6 days

---

### Phase 1C: Pomodoro Enhancements

#### Features to Add:
- [ ] Configurable timer duration (default 25 mins, configurable 1-60 mins)
- [ ] Configurable break timer (default 5 mins, configurable 1-30 mins)
- [ ] Session history tracking (daily, weekly, monthly stats)
- [ ] Audio/visual notifications (alarm sound + desktop popup)
- [ ] Focus mode (disable all notifications)
- [ ] Daily pomodoro statistics
- [ ] Streak counter (consecutive days with sessions)
- [ ] Pause/Resume functionality ✅ (already has pause button)
- [ ] Skip to break button
- [ ] Sound preferences (enable/disable, select sound)
- [ ] Desktop notifications (using plyer)
- [ ] Tray icon integration

**Technical Details**:
- Add plyer library for desktop notifications
- Store session history in database or JSON
- Add settings dialog for timer configuration
- Implement notification system

**Estimated Time**: 4 days

---

### Phase 1D: Calendar Improvements

#### Features to Add:
- [ ] Event creation on double-click
- [ ] Event editing and deletion (dialog)
- [ ] Event color coding
- [ ] Multi-day events
- [ ] All-day events
- [ ] Event reminders (e.g., 1 day before, 1 hour before)
- [ ] Month/Week/Day views
- [ ] Today highlight (current date styling)
- [ ] Navigation keyboard shortcuts (arrow keys)
- [ ] Calendar import (iCal/Google Calendar)
- [ ] Event search

**Technical Details**:
- Create custom event model
- Extend QCalendarWidget with event overlay
- Add event detail dialog
- Event storage in JSON/SQLite
- Calendar sync module for imports

**Estimated Time**: 5-6 days

---

### Phase 1E: Notes Tab Enhancement

#### Features to Add:
- [ ] Rich text formatting (Bold, Italic, Underline, Colors)
- [ ] Code syntax highlighting (Pygments)
- [ ] Note categories/folders
- [ ] Note tags with color coding
- [ ] Search notes (global search integration)
- [ ] Pin/Star important notes
- [ ] Note templates
- [ ] Quick note capture (floating window)
- [ ] Note history/versions
- [ ] Markdown support
- [ ] Export to PDF/HTML (reportlab)

**Technical Details**:
- Use QTextEdit with HTML support (already supports rich text)
- Integrate Markdown library for parsing
- Add Pygments for code highlighting
- Use reportlab for PDF export
- Version control for notes (store timestamps)

**Estimated Time**: 5-6 days

---

## 📊 Phase 1 Summary

**Total Quick Wins**: 7 features (5-10 days)  
**Total Phase 1 Enhancements**: 60+ features (20-30 days)  
**Total Phase 1 Time**: ~30-40 days

---

## 📦 Dependencies to Add

```
python-dateutil==2.8.2  ✅ (already installed)
plyer==2.1.0  (desktop notifications)
Markdown==3.5  (markdown parsing)
Pygments==2.14.0  (syntax highlighting)
reportlab==4.0.0  (PDF generation)
SQLAlchemy==2.0.0  (ORM for database)
sqlalchemy-utils==0.39.0  (utils)
```

---

## 🎯 Development Workflow

### For Each Feature:
1. **Plan**: Understand requirements and dependencies
2. **Design**: Sketch UI changes and data model changes
3. **Implement**: Write code in main.py or supporting modules
4. **Test**: Run the app and test the feature manually
5. **Document**: Update README and API_REFERENCE.md
6. **Commit**: Push to GitHub with descriptive commit message

### Directory Structure (Final):
```
Workspace-Organizer/
├── main.py (1500+ lines) ← Main application
├── core/
│   ├── __init__.py
│   ├── file_manager.py
│   ├── notes_manager.py
│   └── database.py (new) ← SQLite models
├── ui/
│   ├── __init__.py
│   └── styles.py
├── data/ (new)
│   ├── tasks.json
│   ├── todos.json
│   ├── calendar.json
│   └── workspace.db
├── requirements.txt
└── documentation/
```

---

## 🔍 Quality Checklist

Before committing each feature:
- [ ] Code follows existing style (4-space indents, clear naming)
- [ ] No hardcoded values (use constants or config)
- [ ] Error handling (try-except blocks)
- [ ] User-friendly error messages (QMessageBox)
- [ ] Dark mode compatible (test both themes)
- [ ] Keyboard shortcuts working
- [ ] No memory leaks (test repeated actions)
- [ ] Performance acceptable (< 100ms UI response)
- [ ] Data persists correctly
- [ ] Related documentation updated

---

## 📈 Success Metrics

**Phase 1 (v4.1) Success = All of:**
- ✅ All 7 quick wins implemented
- ✅ All keyboard shortcuts working
- ✅ Kanban board with drag-drop and colors
- ✅ Todo list with recurring tasks
- ✅ Pomodoro timer enhancements (configurable, notifications)
- ✅ Calendar with events
- ✅ Notes with rich text and export
- ✅ App runs without crashes
- ✅ All 3 themes working (dark, light, custom)
- ✅ 50+ tests passing

---

## 📅 Timeline

**Week 1**: Quick Wins (keyboard shortcuts, search, stats)  
**Week 2**: Kanban & Favorites  
**Week 3**: Todo enhancements  
**Week 4**: Pomodoro & Calendar  
**Week 5**: Notes & Export  
**Week 6**: Testing & Polish  

**Target Release**: v4.1 (30-40 days from start)

---

## 🚀 Next Steps

1. ✅ Implement keyboard shortcuts (DONE)
2. 🔄 Implement global search bar (CURRENT)
3. Implement app statistics
4. Implement favorites & pinning
5. Implement export features
6. Create settings panel
7. Add system tray integration
8. Then: Phase 1A, 1B, 1C, 1D, 1E
9. Test and release v4.1
10. Move to Phase 2 (v4.5)

---

## 💾 Data Persistence

**Current Storage Methods**:
- Todos: in memory (self.todos list)
- Kanban tasks: in memory (self.kanban_tasks list)
- Notes: json file (notes_manager.py)
- Files: scanned from disk

**Phase 1 Plan**:
- Todos & Kanban: Move to JSON files for persistence
- Calendar events: Store in JSON or SQLite
- Search history: Store in JSON
- Statistics: Store in SQLite for querying
- Preferences: Store in JSON (config.json)

---

## 🔐 Security Considerations

- [ ] Validate all user inputs before saving
- [ ] Sanitize file paths (prevent directory traversal)
- [ ] Validate JSON before loading
- [ ] Handle missing or corrupted data files gracefully
- [ ] No sensitive data in logs

---

**Prepared by**: Development Team  
**Version**: v1.0  
**Status**: APPROVED FOR IMPLEMENTATION
