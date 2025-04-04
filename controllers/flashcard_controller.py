from typing import Dict, List, Optional
from models.flashcard import Flashcard, TermWord
from controllers.base_controller import BaseController
from PySide6.QtCore import QJsonDocument

class FlashcardController(BaseController):
    def __init__(self, flashcard: Flashcard, parent=None):
        super().__init__(parent)
        self.flashcard = flashcard
        self.terms: List[TermWord] = []
        self.terms = self.get_terms(flashcard.id)
    
    def set_flashcard(self, flashcard: Flashcard):
        self.flashcard = flashcard
        self.terms = flashcard.terms  # Update words when flashcard set changes
    
    def get_flashcard(self):
        return self.flashcard
    
    def get_terms(self, flashcard_id: str):
        """Fetches all words for a flashcard set."""
        url = f"{self.SERVER_URL}/flashcard/{flashcard_id}/term"
        reply = self.perform_get_request_sync(url)
        
        # Parse the JSON response
        json_doc = QJsonDocument.fromJson(reply.readAll())
        if json_doc.isNull():
            raise ValueError("Invalid JSON response from server")
        
        # Convert QJsonArray to list of Word objects
        terms_array = json_doc.array()
        self.terms = []
        
        for i in range(terms_array.size()):
            term_obj = terms_array.at(i).toVariant()
            
            # Create Word object
            term = TermWord(
                id=term_obj.get('id', ''),
                term=term_obj.get('term', ''),
                definition=term_obj.get('definition', ''),
                created_at=term_obj.get('created_at', ''),
                updated_at=term_obj.get('updated_at', '')
            )
            self.terms.append(term)

        return self.terms
    
    def set_terms(self, terms: List[TermWord]):
        self.terms = terms

    def post_term(self, flashcard_id: str, term: str, definition: str):
        """Creates a new term in the flashcard."""
        url = f"{self.SERVER_URL}/flashcard/{flashcard_id}/term"
        data = {
            "term": term,
            "definition": definition
        }
        reply = self.perform_post_request_sync(url, data)
        json_doc = QJsonDocument.fromJson(reply.readAll())
        if json_doc.isNull():
            raise ValueError("Invalid JSON response from server")
        return json_doc.object()

    def update_term(self, term: TermWord):
        """Updates an existing term."""
        url = f"{self.SERVER_URL}/term/{term.id}"
        data = {
            "term": term.term,
            "definition": term.definition
        }
        reply = self.perform_put_request_sync(url, data)
        json_doc = QJsonDocument.fromJson(reply.readAll())
        if json_doc.isNull():
            raise ValueError("Invalid JSON response from server")
        return json_doc.object()

    def delete_term(self, term_id: str):
        """Deletes a term from the flashcard."""
        url = f"{self.SERVER_URL}/term/{term_id}"
        reply = self.perform_delete_request_sync(url)
        return reply.statusCode() == 200
