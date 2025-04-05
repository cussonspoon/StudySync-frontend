from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, 
    QPushButton, QFrame, QScrollArea, QLineEdit,
    QSizePolicy, QDialog
)
from PySide6.QtCore import Qt, QSize
from PySide6.QtGui import QFont, QIcon
from typing import List, Dict, Union
from .models import get_sample_flashcards, Flashcard, TermWord
from ..flashcard_window import popup_flashcardwindow
from controllers.flashcard_controller import FlashcardController

class WordCard(QFrame):
    def __init__(self, word: str = "Word", parent=None):
        super().__init__(parent)
        self.word = word

        self.setupUi()

    def setupUi(self):
        self.setFixedSize(250, 150)
        self.setStyleSheet("""
            WordCard {
                background-color: #FFFFFF;
                border-radius: 8px;
                box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
            }
        """)

        layout = QVBoxLayout(self)
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        word_label = QLabel(self.word)
        word_label.setFont(QFont("Inter", 18))
        word_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        word_label.setStyleSheet("color: #1A1A1A;")
        layout.addWidget(word_label)

class TermInput(QFrame):
    def __init__(self, word: str = "", definition: str = "", parent=None):
        super().__init__(parent)
        self.setupUi()
        if word:
            self.word_input.setText(word)
        if definition:
            self.definition_input.setText(definition)

    def setupUi(self):
        self.setStyleSheet("""
            QFrame {
                background-color: white;
                border-radius: 8px;
            }
            QLineEdit {
                border: none;
                background: transparent;
                font-size: 14px;
                padding: 8px;
            }
        """)

        layout = QHBoxLayout(self)
        layout.setContentsMargins(10, 5, 10, 5)
        layout.setSpacing(10)

        # Word input
        self.word_input = QLineEdit()
        self.word_input.setPlaceholderText("Word")
        self.word_input.setFixedWidth(200)
        layout.addWidget(self.word_input)

        # Vertical separator
        separator = QFrame()
        separator.setFrameShape(QFrame.VLine)
        separator.setStyleSheet("background-color: #E0E0E0;")
        layout.addWidget(separator)

        # Definition input
        self.definition_input = QLineEdit()
        self.definition_input.setPlaceholderText("Definition")
        layout.addWidget(self.definition_input)

        # Delete button
        delete_button = QPushButton("×")
        delete_button.setStyleSheet("""
            QPushButton {
                color: #666666;
                background: transparent;
                border: none;
                font-size: 18px;
                padding: 5px;
            }
            QPushButton:hover {
                color: #FF4444;
            }
        """)
        delete_button.clicked.connect(self.deleteLater)
        layout.addWidget(delete_button)

class AddTermDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Add New Term")
        self.setModal(True)
        self.setFixedSize(500, 300)
        self.setStyleSheet("""
            QDialog {
                background-color: #f8f9fa;
                border-radius: 10px;
            }
            QLabel {
                font-size: 14px;
                color: #333;
                font-weight: bold;
                margin-bottom: 5px;
            }
            QLineEdit {
                padding: 10px;
                border: 2px solid #e0e0e0;
                border-radius: 6px;
                background-color: white;
                font-size: 14px;
                margin-bottom: 10px;
            }
            QLineEdit:focus {
                border: 2px solid #4CAF50;
            }
            QLineEdit:hover {
                border: 2px solid #ccc;
            }
            QPushButton {
                padding: 10px 20px;
                border-radius: 6px;
                font-size: 14px;
                font-weight: bold;
            }
            QPushButton#cancelBtn {
                background-color: #f8f9fa;
                border: 2px solid #dc3545;
                color: #dc3545;
            }
            QPushButton#cancelBtn:hover {
                background-color: #dc3545;
                color: white;
            }
            QPushButton#addBtn {
                background-color: #4CAF50;
                border: none;
                color: white;
            }
            QPushButton#addBtn:hover {
                background-color: #45a049;
            }
        """)
        
        layout = QVBoxLayout(self)
        layout.setContentsMargins(10, 20, 20, 10)
        layout.setSpacing(10)
        
        # Title
        title_label = QLabel("Add New Term")
        title_label.setStyleSheet("""
            font-size: 18px;
            color: #333;
            font-weight: bold;
            margin-bottom: 15px;
        """)
        layout.addWidget(title_label)
        
        # Word input
        word_label = QLabel("Word:")
        self.word_input = QLineEdit()
        self.word_input.setPlaceholderText("Enter the term or word")
        
        layout.addWidget(word_label)
        layout.addWidget(self.word_input)
        
        # Definition input
        definition_label = QLabel("Definition:")
        self.definition_input = QLineEdit()
        self.definition_input.setPlaceholderText("Enter the definition or explanation")
        
        layout.addWidget(definition_label)
        layout.addWidget(self.definition_input)
        
        # Buttons
        button_layout = QHBoxLayout()
        button_layout.setSpacing(15)
        
        cancel_button = QPushButton("Cancel")
        cancel_button.setObjectName("cancelBtn")
        cancel_button.clicked.connect(self.reject)
        
        add_button = QPushButton("Add Term")
        add_button.setObjectName("addBtn")
        add_button.clicked.connect(self.accept)
        
        button_layout.addStretch()
        button_layout.addWidget(cancel_button)
        button_layout.addWidget(add_button)
        
        layout.addStretch()
        layout.addLayout(button_layout)

    def get_term_data(self):
        """Get the term data as a dictionary"""
        return {
            "word": self.word_input.text().strip(),
            "definition": self.definition_input.text().strip()
        }

class FlashcardEditPage(QWidget):
    def __init__(self):
        super().__init__()
        self.terms: List[Dict[str, str]] = []
        # Get sample data
        sample_flashcards = get_sample_flashcards()
        self.current_flashcard = sample_flashcards[0] if sample_flashcards else None
        self.setupUi()
        # if self.current_flashcard:
        #     self.loadFlashcardData(self.current_flashcard)

    def setupUi(self):
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(20, 20, 20, 20)
        main_layout.setSpacing(20)

        # Header with back button and title
        header_layout = QHBoxLayout()
        
        self.back_button = QPushButton("←")
        self.back_button.setStyleSheet("""
            QPushButton {
                font-size: 24px;
                border: none;
                background: transparent;
                color: #1A1A1A;
            }
            QPushButton:hover {
                color: #666666;
            }
        """)
        header_layout.addWidget(self.back_button)

        # Title input
        self.title_input = QLineEdit()
        self.title_input.setPlaceholderText("(FLASHCARD NAME)")
        self.title_input.setStyleSheet("""
            QLineEdit {
                font-size: 18px;
                font-weight: bold;
                padding: 10px;
                background-color: #F0F0F0;
                border: none;
                border-radius: 8px;
            }
        """)
        header_layout.addWidget(self.title_input)

        # Upload Note button
        upload_button = QPushButton("Upload Note")
        upload_button.setStyleSheet("""
            QPushButton {
                background-color: transparent;
                border: 1px solid #CCCCCC;
                border-radius: 4px;
                padding: 8px 16px;
                color: #666666;
            }
            QPushButton:hover {
                background-color: #F0F0F0;
            }
        """)
        header_layout.addWidget(upload_button)

        # Start Flashcard button
        self.start_button = QPushButton("Start Flashcard")
        self.start_button.setStyleSheet("""
            QPushButton {
                background-color: #4CAF50;
                border: none;
                border-radius: 4px;
                padding: 8px 16px;
                color: white;
            }
            QPushButton:hover {
                background-color: #45a049;
            }
        """)
        self.start_button.clicked.connect(self.start_flashcard)
        header_layout.addWidget(self.start_button)

        main_layout.addLayout(header_layout)

        # Words scroll area
        words_scroll = QScrollArea()
        words_scroll.setWidgetResizable(True)
        words_scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOn)
        words_scroll.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        words_scroll.setStyleSheet("""
            QScrollArea {
                border: none;
                background-color: transparent;
            }
            QScrollBar:horizontal {
                height: 8px;
                background: #F5F5F5;
                border-radius: 4px;
            }
            QScrollBar::handle:horizontal {
                background: #CCCCCC;
                border-radius: 4px;
            }
            QScrollBar::handle:horizontal:hover {
                background: #999999;
            }
        """)

        words_container = QWidget()
        self.words_layout = QHBoxLayout(words_container)
        self.words_layout.setContentsMargins(0, 0, 0, 0)
        self.words_layout.setSpacing(15)
        self.words_layout.addStretch()

        words_scroll.setWidget(words_container)
        words_scroll.setFixedHeight(170)
        main_layout.addWidget(words_scroll)

        # Terms section
        terms_container = QWidget()
        terms_container.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)  # Allow vertical expansion
        terms_layout = QVBoxLayout(terms_container)
        terms_layout.setSpacing(10)
        terms_layout.setContentsMargins(0, 0, 0, 0)

        # Terms header
        terms_header = QHBoxLayout()
        self.terms_label = QLabel("Terms(0)")
        self.terms_label.setFont(QFont("Inter", 14))
        terms_header.addWidget(self.terms_label)

        add_term_button = QPushButton("+")
        add_term_button.setFixedSize(30, 30)
        add_term_button.setStyleSheet("""
            QPushButton {
                background-color: #F0F0F0;
                border: none;
                border-radius: 15px;
                font-size: 18px;
                color: #666666;
            }
            QPushButton:hover {
                background-color: #E0E0E0;
            }
        """)
        add_term_button.clicked.connect(self.add_term)
        terms_header.addWidget(add_term_button)
        terms_layout.addLayout(terms_header)

        # Terms scroll area
        terms_scroll = QScrollArea()
        terms_scroll.setWidgetResizable(True)
        terms_scroll.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)  # Allow scroll area to expand
        terms_scroll.setStyleSheet("""
            QScrollArea {
                border: none;
                background-color: transparent;
            }
            QScrollBar:vertical {
                width: 8px;
                background: #F5F5F5;
                border-radius: 4px;
            }
            QScrollBar::handle:vertical {
                background: #CCCCCC;
                border-radius: 4px;
            }
            QScrollBar::handle:vertical:hover {
                background: #999999;
            }
        """)

        self.terms_widget = QWidget()
        self.terms_list_layout = QVBoxLayout(self.terms_widget)
        self.terms_list_layout.setSpacing(10)
        self.terms_list_layout.addStretch()

        terms_scroll.setWidget(self.terms_widget)
        terms_layout.addWidget(terms_scroll)

        main_layout.addWidget(terms_container, 1)  # Give it a stretch factor of 1

    def loadFlashcardData(self, flashcard: Flashcard):
        """Load data from a Flashcard object into the UI"""
        # Set title
        print("flashcard", flashcard)
        print("loadFlashcardData", flashcard.id)
        self.title_input.setText(flashcard.name)
        self.current_flashcard = flashcard
        flashcard_controller = FlashcardController(flashcard)

        # Clear existing terms
        while self.terms_list_layout.count() > 1:  # Keep the stretch
            item = self.terms_list_layout.takeAt(0)
            if item.widget():
                item.widget().deleteLater()

        # Clear existing word cards
        while self.words_layout.count() > 1:  # Keep the stretch
            item = self.words_layout.takeAt(0)
            if item.widget():
                item.widget().deleteLater()
        
        terms = flashcard_controller.get_terms(flashcard.id)
        self.current_flashcard.terms = terms
        # self.set_terms(terms)
        # Add terms from flashcard
        for term in terms:
            # Add term input
            term_input = TermInput(term.term, term.definition)
            self.terms_list_layout.insertWidget(self.terms_list_layout.count() - 1, term_input)
            
            # Add word card
            word_card = WordCard(term.term)
            self.words_layout.insertWidget(self.words_layout.count() - 1, word_card)

        # Update terms count
        self.updateTermsCount()

    def add_term(self):
        """Add a new term through dialog and API"""
        dialog = AddTermDialog(self)
        if dialog.exec():
            term_data = dialog.get_term_data()
            
            if term_data["word"] and term_data["definition"]:
                try:
                    # Add term through API
                    flashcard_controller = FlashcardController(self.current_flashcard)
                    flashcard_controller.post_term(
                        self.current_flashcard.id,
                        term_data["word"],
                        term_data["definition"]
                    )
                    
                    # Reload flashcard data to show new term
                    self.loadFlashcardData(self.current_flashcard)
                except Exception as e:
                    print(f"Error adding term: {e}")

    def updateTermsCount(self):
        """Update the terms count label"""
        count = self.terms_list_layout.count() - 1  # Subtract 1 for the stretch
        self.terms_label.setText(f"Terms({count})")

    def get_terms(self) -> List[Dict[str, str]]:
        """Get all terms from the UI"""
        terms = []
        for i in range(self.terms_list_layout.count() - 1):  # -1 to exclude the stretch
            term_widget = self.terms_list_layout.itemAt(i).widget()
            if isinstance(term_widget, TermInput):
                word = term_widget.word_input.text()
                definition = term_widget.definition_input.text()
                if word or definition:  # Only add if either field has content
                    terms.append({
                        "word": word,
                        "definition": definition
                    })
        return terms

    def set_terms(self, terms: List[Union[Dict[str, str], TermWord]]):
        """Set terms in the UI"""
        # Clear existing terms
        while self.terms_list_layout.count() > 1:  # Keep the stretch
            item = self.terms_list_layout.takeAt(0)
            if item.widget():
                item.widget().deleteLater()

        # Clear existing word cards
        while self.words_layout.count() > 1:  # Keep the stretch
            item = self.words_layout.takeAt(0)
            if item.widget():
                item.widget().deleteLater()

        # Add new terms
        for term in terms:
            if isinstance(term, dict):
                word = term.get("term", "")
                definition = term.get("definition", "")
            else:  # TermWord object
                word = term.term
                definition = term.definition
                
            term_input = TermInput(word, definition)
            self.terms_list_layout.insertWidget(self.terms_list_layout.count() - 1, term_input)
            
            # Add word card
            word_card = WordCard(word)
            self.words_layout.insertWidget(self.words_layout.count() - 1, word_card)

        # Update terms count
        self.updateTermsCount()

    def start_flashcard(self):
        """Start the flashcard review session"""
        if self.current_flashcard:
            flashcard_window = popup_flashcardwindow(self.current_flashcard, self)
            flashcard_window.exec() 