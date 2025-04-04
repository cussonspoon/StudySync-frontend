from PySide6.QtWidgets import (
    QLabel,
    QPushButton,
    QVBoxLayout,
    QHBoxLayout,
    QFrame,
)
from PySide6.QtCore import Qt
from .note_window import popup_notewindow
from .quiz_window import popup_quizwindow
from models.quiz import Quiz


class ContentCard(QFrame):
    def __init__(self, name, mode, parent=None):
        super().__init__(parent)
        self.name = name
        self.mode = mode
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

        # Add subtitle based on mode
        if "Note" in mode:
            subtitle = QLabel("Note")
        elif "Flashcard" in mode:
            subtitle = QLabel("Flashcard set - 0 terms")
        elif "Quiz" in mode:
            subtitle = QLabel("Quiz - 0 Questions")
        subtitle.setStyleSheet("font-size: 14px; color: #666666;")
        text_layout.addWidget(subtitle)

        # Add "by User"
        by_user = QLabel("by User")
        by_user.setStyleSheet("font-size: 12px; color: #666666;")
        text_layout.addWidget(by_user)

        # Add text layout to card
        card_layout.addLayout(text_layout)
        card_layout.addStretch()

    def mousePressEvent(self, event):
        """Handle mouse press events to open appropriate window"""
        if event.button() == Qt.LeftButton:
            if "Note" in self.mode:
                note_dialog = popup_notewindow(self.parent())
                note_dialog.title_input.setPlainText(self.name)  # Set the title
                if note_dialog.exec():
                    note_data = note_dialog.getNoteData()
                    print("Note Data:", note_data)  # You can handle the note data here
            elif "Quiz" in self.mode:
                # Create a new quiz with empty ID
                quiz = Quiz(
                    id="",  # Empty ID for new quiz
                    title=self.name,
                    quiz_type="quiz",
                    mode="normal",
                )
                quiz_dialog = popup_quizwindow(self.parent(), quiz=quiz)
                if quiz_dialog.exec():
                    quiz_data = quiz_dialog.getQuizData()
                    print("Quiz Data:", quiz_data)  # You can handle the quiz data here
        super().mousePressEvent(event)
