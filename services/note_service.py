from dotenv import load_dotenv
from models.folder import CreateFolder, Folder
from models.note import Note, UpdateNote
from models.user import User
import os


class NoteService:
    def __init__(self, note_data: Note):
        self._note = note_data
        self._items = []
        if note_data is not None:  # Only fetch items if we have a folder
            self._items = self.fetch_items()

    def get_note(self, id):
        pass

    def create_note(self, note_data: Note):
        pass

    def update_note(self, note_data: UpdateNote):
        pass

    def delete_note(self):
        pass


