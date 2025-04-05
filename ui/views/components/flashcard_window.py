from PySide6.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QPushButton,
    QLabel, QWidget, QFrame, QGraphicsDropShadowEffect, QMessageBox
)
from PySide6.QtCore import Qt, QPropertyAnimation, QEasingCurve, QSequentialAnimationGroup, Signal, QSize

from PySide6.QtGui import QFont, QColor
from .flashcard_components.models import Flashcard, TermWord, get_flashcard_by_id, get_sample_flashcards

class FlashcardProgressBar(QWidget):
    def __init__(self, total, learning, known, parent=None):
        super().__init__(parent)
        self.setFixedHeight(30)
        
        layout = QHBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(10)
        
        # Learning count
        self.learning_label = QLabel(f"🤔 Still learning ({learning})")
        self.learning_label.setStyleSheet("color: #FFA500;")  # Orange color
        layout.addWidget(self.learning_label)
        
        layout.addStretch()
        
        # Known count
        self.known_label = QLabel(f"✓ Know ({known})")
        self.known_label.setStyleSheet("color: #32CD32;")  # Green color
        layout.addWidget(self.known_label)

    def updateCounts(self, learning, known):
        self.learning_label.setText(f"🤔 Still learning ({learning})")
        self.known_label.setText(f"✓ Know ({known})")

class FlashcardDisplay(QFrame):
    def __init__(self, parent=None):
        super().__init__(parent)
        # Add shadow effect
        self.setGraphicsEffect(None)  # Clear any existing effect
        shadow = QGraphicsDropShadowEffect(self)
        shadow.setBlurRadius(20)
        shadow.setXOffset(0)
        shadow.setYOffset(4)
        shadow.setColor(QColor(0, 0, 0, 50))  # Semi-transparent black
        self.setGraphicsEffect(shadow)
        
        self.setStyleSheet("""
            QFrame {
                background-color: #b8d9ff;
                border-radius: 10px;
                min-height: 300px;
                border: none;
            }
        """)
        
        self.layout = QVBoxLayout(self)
        self.layout.setAlignment(Qt.AlignCenter)
        self.layout.setSpacing(20)
        
        self.word_label = QLabel("Word")
        self.word_label.setFont(QFont("Arial", 24))
        self.word_label.setWordWrap(True)
        self.word_label.setFixedWidth(400)
        self.word_label.setFixedHeight(200)
        self.word_label.setAlignment(Qt.AlignCenter)
        self.layout.addWidget(self.word_label)

        # Click to flip instruction
        self.flip_instruction = QLabel("Click to flip")
        self.flip_instruction.setStyleSheet("color: #666666; font-size: 12px;")
        self.flip_instruction.setAlignment(Qt.AlignCenter)
        self.layout.addWidget(self.flip_instruction)

        self.is_showing_word = True
        self.current_term = None

    def mousePressEvent(self, event):
        if self.current_term:
            self.flipCard()

    def setTerm(self, term: TermWord):
        self.current_term = term
        self.is_showing_word = True
        self.word_label.setText(term.term)

    def flipCard(self):
        if not self.current_term:
            return

        # Create shrink animation (simulate rotating to side)
        shrink = QPropertyAnimation(self, b"maximumWidth")
        shrink.setDuration(150)
        shrink.setStartValue(self.width())
        shrink.setEndValue(0)
        shrink.setEasingCurve(QEasingCurve.InOutQuad)

        # Create expand animation (simulate rotating back)
        expand = QPropertyAnimation(self, b"maximumWidth")
        expand.setDuration(150)
        expand.setStartValue(0)
        expand.setEndValue(self.width())
        expand.setEasingCurve(QEasingCurve.InOutQuad)

        # When halfway through (after shrink), swap content
        def toggle_text():
            if self.is_showing_word:
                self.word_label.setText(self.current_term.definition)
            else:
                self.word_label.setText(self.current_term.term)
            self.is_showing_word = not self.is_showing_word

        shrink.finished.connect(toggle_text)

        # Chain animations
        animation_group = QSequentialAnimationGroup(self)
        animation_group.addAnimation(shrink)
        animation_group.addAnimation(expand)
        animation_group.start()



class popup_flashcardwindow(QDialog):
    def __init__(self, flashcard_data: Flashcard, parent=None):
        super().__init__(parent, Qt.WindowSystemMenuHint | Qt.WindowTitleHint | Qt.WindowCloseButtonHint)
        self.setModal(True)
        
        # Store the flashcard data
        self.flashcard_data = flashcard_data
        print("flashcard_data", flashcard_data)
        
        # Set window title
        if self.flashcard_data:
            self.setWindowTitle(f"Flashcard Set: {self.flashcard_data.name}")
        else:
            self.setWindowTitle("Flashcard Set")
            
        # Initialize state
        self.current_index = 0
        self.known_terms = set()
        self.setFixedSize(800, 600)
        self.setupUi()
        
        # Load first term if available
        if self.flashcard_data and self.flashcard_data.terms:
            self.loadTerm(0)

    def setupUi(self):
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(20, 20, 20, 20)
        main_layout.setSpacing(20)

        # Top section with progress and title
        top_section = QWidget()
        top_layout = QVBoxLayout(top_section)
        top_layout.setContentsMargins(0, 0, 0, 0)
        top_layout.setSpacing(5)  # Small spacing between elements

        # Progress indicator
        total_terms = len(self.flashcard_data.terms) if self.flashcard_data else 0
        self.progress_text = QLabel(f"{self.current_index + 1}/{total_terms}")
        self.progress_text.setAlignment(Qt.AlignCenter)
        self.progress_text.setFont(QFont("Arial", 16))
        top_layout.addWidget(self.progress_text)

        # Flashcard set name
        set_name = self.flashcard_data.name if self.flashcard_data else "Flashcard Set"
        self.set_name_label = QLabel(set_name)
        self.set_name_label.setAlignment(Qt.AlignCenter)
        self.set_name_label.setFont(QFont("Arial", 14))
        self.set_name_label.setStyleSheet("color: #666666;")
        top_layout.addWidget(self.set_name_label)

        # Separator line
        separator = QFrame()
        separator.setFrameShape(QFrame.HLine)
        separator.setFrameShadow(QFrame.Sunken)
        separator.setStyleSheet("""
            QFrame {
                border: none;
                background-color: #E0E0E0;
                height: 1px;
                margin-top: 10px;
                margin-bottom: 10px;
            }
        """)
        top_layout.addWidget(separator)

        main_layout.addWidget(top_section)

        # Progress bar with counts
        self.progress_bar = FlashcardProgressBar(
            total_terms,
            total_terms - len(self.known_terms),
            len(self.known_terms)
        )
        main_layout.addWidget(self.progress_bar)

        # Flashcard display
        self.flashcard = FlashcardDisplay()
        main_layout.addWidget(self.flashcard)

        # Navigation buttons
        nav_layout = QHBoxLayout()
        
        self.prev_button = QPushButton("←")
        self.prev_button.setFixedSize(40, 40)
        self.prev_button.setStyleSheet("""
            QPushButton {
                background-color: white;
                border: 1px solid #E0E0E0;
                border-radius: 20px;
                font-size: 20px;
            }
            QPushButton:hover {
                background-color: #F0F0F0;
            }
            QPushButton:disabled {
                background-color: #F5F5F5;
                color: #CCCCCC;
            }
        """)
        self.prev_button.clicked.connect(self.previousTerm)
        
        self.next_button = QPushButton("→")
        self.next_button.setFixedSize(40, 40)
        self.next_button.setStyleSheet(self.prev_button.styleSheet())
        self.next_button.clicked.connect(self.nextTerm)
        
        # Know/Don't Know buttons
        self.dont_know_button = QPushButton("Still Learning")
        self.dont_know_button.setStyleSheet("""
            QPushButton {
                background-color: #FFF3E0;
                border: none;
                border-radius: 20px;
                padding: 10px 20px;
                color: #FF9800;
            }
            QPushButton:hover {
                background-color: #FFE0B2;
            }
        """)
        self.dont_know_button.clicked.connect(lambda: self.markTerm(False))

        self.know_button = QPushButton("Know")
        self.know_button.setStyleSheet("""
            QPushButton {
                background-color: #E8F5E9;
                border: none;
                border-radius: 20px;
                padding: 10px 20px;
                color: #4CAF50;
            }
            QPushButton:hover {
                background-color: #C8E6C9;
            }
        """)
        self.know_button.clicked.connect(lambda: self.markTerm(True))
        
        nav_layout.addWidget(self.prev_button)
        nav_layout.addStretch()
        nav_layout.addWidget(self.dont_know_button)
        nav_layout.addWidget(self.know_button)
        nav_layout.addStretch()
        nav_layout.addWidget(self.next_button)
        
        main_layout.addLayout(nav_layout)

        # Update button states
        self.updateNavigationButtons()

    def loadTerm(self, index):
        if not self.flashcard_data or not self.flashcard_data.terms:
            return

        self.current_index = index
        current_term = self.flashcard_data.terms[index]
        self.flashcard.setTerm(current_term)
        
        # Update progress
        total_terms = len(self.flashcard_data.terms)
        self.progress_text.setText(f"{index + 1}/{total_terms}")
        self.progress_bar.updateCounts(
            total_terms - len(self.known_terms),
            len(self.known_terms)
        )
        self.updateNavigationButtons()

    def previousTerm(self):
        if self.current_index > 0:
            self.loadTerm(self.current_index - 1)

    def nextTerm(self):
        if self.current_index < len(self.flashcard_data.terms) - 1:
            self.loadTerm(self.current_index + 1)

    def markTerm(self, known: bool):
        if self.flashcard_data and self.flashcard_data.terms:
            current_term = self.flashcard_data.terms[self.current_index]
            if known:
                self.known_terms.add(current_term.id)
            else:
                self.known_terms.discard(current_term.id)
            
            self.progress_bar.updateCounts(
                len(self.flashcard_data.terms) - len(self.known_terms),
                len(self.known_terms)
            )
            
            # Automatically move to next term if available
            if self.current_index < len(self.flashcard_data.terms) - 1:
                self.nextTerm()

    def updateNavigationButtons(self):
        self.prev_button.setEnabled(self.current_index > 0)
        self.next_button.setEnabled(
            self.current_index < len(self.flashcard_data.terms) - 1 if self.flashcard_data else False
        )

    def getFlashcardData(self):
        return {
            'flashcard_id': self.flashcard_data.id if self.flashcard_data else None,
            'total_terms': len(self.flashcard_data.terms) if self.flashcard_data else 0,
            'known_terms': list(self.known_terms),
            'current_index': self.current_index
        } 