from PySide6.QtWidgets import (
    QLabel,
    QPushButton,
    QVBoxLayout,
    QHBoxLayout,
    QFrame,
)
from PySide6.QtCore import Qt, Signal
from .note_window import popup_notewindow
from .quiz_window import popup_quizwindow
from .flashcard_window import popup_flashcardwindow
from models.quiz import Quiz
from models.flashcard import Flashcard
from controllers.flashcard_controller import FlashcardController
from datetime import datetime


class ContentCard(QFrame):
    # Add a signal that will be emitted when card is clicked
    clicked = Signal(str, str, dict)  # Will emit (name, mode, item_data)

    def __init__(self, name, mode, item_data=None, parent=None):
        super().__init__(parent)
        self.name = name
        self.mode = mode
        self.item_data = item_data or {}  # Store the full item data
        self.setFixedHeight(100)
        self.setStyleSheet(
            """
            QFrame {
                background-color: white;
                border: 0px solid #E0E0E0;
                border-radius: 8px;
            }
            QLabel {
                color: black;
                background: transparent;
            }
            """
        )
        self.setCursor(Qt.PointingHandCursor)  # Add cursor change on hover

        # Create horizontal layout for the card
        card_layout = QHBoxLayout(self)
        card_layout.setContentsMargins(10, 10, 10, 10)
        card_layout.setSpacing(15)

        # Add icon/image placeholder
        icon = QLabel()
        icon.setFixedSize(80, 80)
        icon.setStyleSheet("background-color: #E0E0E0; border-radius: 4px;")
        card_layout.addWidget(icon)

        # Create vertical layout for text content
        text_layout = QVBoxLayout()
        text_layout.setSpacing(2)

        # Add title
        title = QLabel(name.upper())
        title.setStyleSheet("font-size: 16px; font-weight: bold;")
        text_layout.addWidget(title)

        # Add subtitle based on mode and item data
        if "Note" in mode:
            subtitle = QLabel("Note")
            if self.item_data.get('content'):
                subtitle.setText(f"Note - {len(self.item_data['content'])} characters")
        elif "Flashcard" in mode:
            subtitle = QLabel("Flashcard set - 0 terms")
            self.subtitle = subtitle  # Store reference to update term count later
            if self.item_data.get('terms'):
                term_count = len(self.item_data['terms'])
                subtitle.setText(f"Flashcard set - {term_count} terms")
        elif "Quiz" in mode:
            subtitle = QLabel("Quiz - 0 Questions")
            if self.item_data.get('questions'):
                question_count = len(self.item_data['questions'])
                subtitle.setText(f"Quiz - {question_count} Questions")
        subtitle.setStyleSheet("font-size: 14px; color: #666666;")
        text_layout.addWidget(subtitle)

        # Add creation date if available
        created_at = self.item_data.get('created_at')
        if created_at:
            try:
                # Try to parse the date string
                date = datetime.fromisoformat(created_at.replace('Z', '+00:00'))
                formatted_date = date.strftime("%B %d, %Y")
                date_label = QLabel(f"Created on {formatted_date}")
            except:
                date_label = QLabel(f"Created on {created_at}")
            date_label.setStyleSheet("font-size: 12px; color: #666666;")
            text_layout.addWidget(date_label)

        # Add text layout to card
        card_layout.addLayout(text_layout)
        card_layout.addStretch()

    def mousePressEvent(self, event):
        """Handle mouse press events to emit clicked signal"""
        if event.button() == Qt.LeftButton:
            self.clicked.emit(self.name, self.mode, self.item_data)
        super().mousePressEvent(event)