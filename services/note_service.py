import json
import os
from datetime import datetime
import uuid
from models.note import CreateNote, UpdateNote


class NoteService:
    def __init__(self):
        # Create notes directory if it doesn't exist
        self.notes_dir = "notes"
        if not os.path.exists(self.notes_dir):
            os.makedirs(self.notes_dir)

    def _get_folder_notes_path(self, folder_id: str) -> str:
        """Get path to the folder's notes JSON file"""
        return os.path.join(self.notes_dir, f"folder_{folder_id}_notes.json")

    def _load_notes(self, folder_id: str) -> list:
        """Load notes from JSON file"""
        file_path = self._get_folder_notes_path(folder_id)
        if os.path.exists(file_path):
            try:
                with open(file_path, "r") as f:
                    return json.load(f)
            except json.JSONDecodeError:
                print(f"Error reading notes file: {file_path}")
                return []
        return []

    def _save_notes(self, folder_id: str, notes: list):
        """Save notes to JSON file"""
        file_path = self._get_folder_notes_path(folder_id)
        with open(file_path, "w") as f:
            json.dump(notes, f, indent=2)

    def create_note(self, folder_id: str, name: str, content: str) -> dict:
        """Create a new note in the specified folder"""
        notes = self._load_notes(folder_id)

        # Create new note
        new_note = {
            "id": str(uuid.uuid4()),
            "name": name,
            "content": content,
            "folder_id": folder_id,
            "created_at": datetime.now().isoformat(),
        }

        # Add to notes list
        notes.append(new_note)

        # Save to file
        self._save_notes(folder_id, notes)

        return new_note

    def get_note(self, folder_id: str, note_id: str) -> dict:
        """Get a specific note by ID"""
        notes = self._load_notes(folder_id)
        for note in notes:
            if note["id"] == note_id:
                return note
        return None

    def get_notes_by_folder(self, folder_id: str) -> list:
        """Get all notes in a folder"""
        return self._load_notes(folder_id)

    def update_note(self, folder_id: str, note_id: str, update_data: dict) -> dict:
        """Update an existing note"""
        notes = self._load_notes(folder_id)

        # Find and update the note
        for note in notes:
            if note["id"] == note_id:
                note.update(update_data)
                self._save_notes(folder_id, notes)
                return note

        return None

    def delete_note(self, folder_id: str, note_id: str) -> bool:
        """Delete a note"""
        notes = self._load_notes(folder_id)
        initial_count = len(notes)

        # Remove note with matching ID
        notes = [note for note in notes if note["id"] != note_id]

        if len(notes) < initial_count:
            self._save_notes(folder_id, notes)
            return True

        return False
