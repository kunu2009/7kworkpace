"""
Notes Manager - Handle notes operations
"""

import json
import os
from pathlib import Path
from datetime import datetime
from typing import List


class NotesManager:
    def __init__(self):
        self.notes_dir = Path.home() / ".workspace_organizer" / "notes"
        self.notes_dir.mkdir(parents=True, exist_ok=True)
    
    def save_note(self, content: str, title: str = "") -> str:
        """Save a note and return its ID"""
        timestamp = datetime.now().isoformat()
        note_id = datetime.now().strftime("%Y%m%d%H%M%S")
        
        if not title:
            # Use first 30 chars as title
            title = content[:30] + ("..." if len(content) > 30 else "")
        
        note_data = {
            "id": note_id,
            "title": title,
            "content": content,
            "created": timestamp,
            "modified": timestamp
        }
        
        note_file = self.notes_dir / f"{note_id}.json"
        with open(note_file, 'w', encoding='utf-8') as f:
            json.dump(note_data, f, indent=2)
        
        return note_id
    
    def get_all_notes(self) -> List[dict]:
        """Get all notes"""
        notes = []
        for note_file in self.notes_dir.glob("*.json"):
            try:
                with open(note_file, 'r', encoding='utf-8') as f:
                    note = json.load(f)
                    notes.append(note)
            except:
                pass
        
        # Sort by created date (newest first)
        notes.sort(key=lambda x: x.get('created', ''), reverse=True)
        return notes
    
    def get_note(self, note_id: str) -> dict:
        """Get a specific note"""
        note_file = self.notes_dir / f"{note_id}.json"
        if note_file.exists():
            with open(note_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        return {}
    
    def get_note_by_id(self, note_id: str) -> dict:
        """Get a specific note by ID (alias for get_note)"""
        return self.get_note(note_id)
    
    def update_note(self, note_id: str, content: str, title: str = "") -> bool:
        """Update a note"""
        note_file = self.notes_dir / f"{note_id}.json"
        if not note_file.exists():
            return False
        
        with open(note_file, 'r', encoding='utf-8') as f:
            note = json.load(f)
        
        note['content'] = content
        if title:
            note['title'] = title
        note['modified'] = datetime.now().isoformat()
        
        with open(note_file, 'w', encoding='utf-8') as f:
            json.dump(note, f, indent=2)
        
        return True
    
    def delete_note(self, note_id: str) -> bool:
        """Delete a note"""
        note_file = self.notes_dir / f"{note_id}.json"
        if note_file.exists():
            note_file.unlink()
            return True
        return False
    
    def search_notes(self, query: str) -> List[dict]:
        """Search notes by content"""
        query = query.lower()
        results = []
        
        for note in self.get_all_notes():
            if (query in note.get('title', '').lower() or
                query in note.get('content', '').lower()):
                results.append(note)
        
        return results
