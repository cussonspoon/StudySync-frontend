from PySide6.QtWidgets import (
    QApplication,
    QDialog,
    QVBoxLayout,
    QLabel,
    QRadioButton,
    QPushButton,
    QButtonGroup,
    QSpacerItem,
    QSizePolicy,
    QFrame,
    QHBoxLayout,
    QDialog,
)
from PySide6.QtCore import Qt, Signal
from PySide6.QtGui import QFont, QColor
from models.quiz import Question
from typing import List


class QuizStart(QDialog):
    quiz_completed = Signal()  # Signal to emit when quiz is completed/closed

    def __init__(self, parent=None, questions: List[Question] = None):
        super().__init__(parent)

        # Set window flags to make it a proper window
        self.setWindowFlags(
            Qt.Window | Qt.WindowSystemMenuHint | Qt.WindowCloseButtonHint
        )
        self.setModal(True)  # Make it modal

        # Quiz data: questions, options, and correct answers
        self.questions = questions or []
        self.current_question_index = 0
        self.score = 0

        self.init_ui()

    def closeEvent(self, event):
        """Override close event to emit signal when quiz window is closed"""
        self.quiz_completed.emit()
        super().closeEvent(event)

    def init_ui(self):
        """Initialize the quiz UI."""
        # Main layout
        main_layout = QVBoxLayout()
        main_layout.setSpacing(20)
        main_layout.setContentsMargins(30, 30, 30, 30)
        self.setLayout(main_layout)

        # Quiz title container
        title_container = QFrame()
        title_container.setStyleSheet(
            """
            QFrame {
                background-color: #2c3e50;
                border-radius: 15px;
                padding: 20px;
            }
        """
        )
        title_layout = QVBoxLayout(title_container)
        title_layout.setContentsMargins(0, 0, 0, 0)

        self.quiz_title = QLabel("Quiz Title")
        self.quiz_title.setStyleSheet(
            """
            QLabel {
                font-size: 28px;
                font-weight: bold;
                color: white;
                padding: 10px;
            }
        """
        )
        self.quiz_title.setAlignment(Qt.AlignCenter)
        title_layout.addWidget(self.quiz_title)
        main_layout.addWidget(title_container)

        # Progress indicator
        progress_container = QFrame()
        progress_container.setStyleSheet(
            """
            QFrame {
                background-color: #f8f9fa;
                border-radius: 10px;
                padding: 10px;
            }
        """
        )
        progress_layout = QHBoxLayout(progress_container)
        progress_layout.setContentsMargins(10, 10, 10, 10)

        self.progress_label = QLabel()
        self.progress_label.setStyleSheet(
            """
            QLabel {
                font-size: 16px;
                color: #2c3e50;
                font-weight: bold;
            }
        """
        )
        progress_layout.addWidget(self.progress_label)
        main_layout.addWidget(progress_container)

        # Question container
        self.frame = QFrame()
        self.frame.setStyleSheet(
            """
            QFrame {
                background-color: white;
                border: 2px solid #e9ecef;
                border-radius: 15px;
                padding: 25px;
            }
        """
        )
        frame_layout = QVBoxLayout(self.frame)
        frame_layout.setSpacing(20)

        # Question label
        self.question_label = QLabel()
        self.question_label.setStyleSheet(
            """
            QLabel {
                font-size: 20px;
                color: #2c3e50;
                font-weight: 500;
                padding: 10px;
            }
        """
        )
        self.question_label.setWordWrap(True)
        self.question_label.setAlignment(Qt.AlignCenter)
        frame_layout.addWidget(self.question_label)

        # Options container
        self.options_group = QButtonGroup(self)
        self.option_buttons = []

        for i in range(4):
            option_container = QFrame()
            option_container.setStyleSheet(
                """
                QFrame {
                    background-color: #f8f9fa;
                    border-radius: 10px;
                    padding: 5px;
                }
                QFrame:hover {
                    background-color: #e9ecef;
                }
            """
            )
            option_layout = QHBoxLayout(option_container)
            option_layout.setContentsMargins(10, 10, 10, 10)

            button = QRadioButton()
            button.setStyleSheet(
                """
                QRadioButton {
                    font-size: 16px;
                    color: #2c3e50;
                    padding: 10px;
                }
                QRadioButton::indicator {
                    width: 24px;
                    height: 24px;
                }
                QRadioButton::indicator::unchecked {
                    image: url(./static/images/circle.svg);
                }
                QRadioButton::indicator::checked {
                    image: url(./static/images/circle-check.svg);
                }
                QRadioButton:checked {
                    color: #27ae60;
                }
            """
            )
            self.option_buttons.append(button)
            self.options_group.addButton(button)
            option_layout.addWidget(button)
            frame_layout.addWidget(option_container)

        main_layout.addWidget(self.frame)

        # Buttons container
        buttons_container = QFrame()
        buttons_container.setStyleSheet(
            """
            QFrame {
                background-color: transparent;
            }
        """
        )
        buttons_layout = QHBoxLayout(buttons_container)
        buttons_layout.setSpacing(20)

        # Submit button
        self.submit_button = QPushButton("Submit Answer")
        self.submit_button.setStyleSheet(
            """
            QPushButton {
                background-color: #3498db;
                color: white;
                border: none;
                padding: 15px 30px;
                border-radius: 10px;
                font-size: 16px;
                font-weight: bold;
                min-width: 200px;
            }
            QPushButton:hover {
                background-color: #2980b9;
            }
            QPushButton:pressed {
                background-color: #1c669b;
            }
        """
        )
        self.submit_button.clicked.connect(self.check_answer)

        # Reset button
        self.reset_button = QPushButton("Restart Quiz")
        self.reset_button.setStyleSheet(
            """
            QPushButton {
                background-color: #e74c3c;
                color: white;
                border: none;
                padding: 15px 30px;
                border-radius: 10px;
                font-size: 16px;
                font-weight: bold;
                min-width: 200px;
            }
            QPushButton:hover {
                background-color: #c0392b;
            }
            QPushButton:pressed {
                background-color: #a93226;
            }
        """
        )
        self.reset_button.clicked.connect(self.reset_quiz)
        self.reset_button.hide()

        buttons_layout.addWidget(self.submit_button)
        buttons_layout.addWidget(self.reset_button)
        main_layout.addWidget(buttons_container)

        # Set window properties
        self.setWindowTitle("Quiz App")
        self.setFixedWidth(600)
        self.setStyleSheet(
            """
            QWidget {
                background-color: #f8f9fa;
            }
        """
        )

        self.load_question()

    def load_question(self):
        """Load the current question and update the UI."""
        if self.current_question_index < len(self.questions):
            self.reset_button.hide()
            question_data = self.questions[self.current_question_index]
            self.question_label.setText(question_data.question)
            self.quiz_title.setText(f"Quiz {self.current_question_index + 1}")
            self.progress_label.setText(
                f"Question {self.current_question_index + 1} of {len(self.questions)}"
            )

            for i, option in enumerate(question_data.choices):
                self.option_buttons[i].setText(option.choice)
                self.option_buttons[i].setChecked(False)
                self.option_buttons[i].show()

            self.submit_button.show()
        else:
            self.display_result()

    def check_answer(self):
        """Check the selected answer and update the score."""
        selected_button = self.options_group.checkedButton()

        if selected_button:
            selected_answer = selected_button.text()

            for answer in self.questions[self.current_question_index].choices:
                if answer.is_answer:
                    correct_answer = answer.choice
                    if selected_answer == correct_answer:
                        self.score += 1
                        break

            self.current_question_index += 1
            self.load_question()

    def reset_quiz(self):
        """Reset the quiz to start from the first question."""
        self.current_question_index = 0
        self.score = 0
        self.load_question()

    def display_result(self):
        """Show final score and hide unnecessary UI elements."""
        self.question_label.setText(
            f"Quiz Completed!\nYour score: {self.score}/{len(self.questions)}"
        )
        self.quiz_title.setText("Quiz Results")
        self.progress_label.setText("Final Score")

        for button in self.option_buttons:
            button.hide()
        self.submit_button.hide()
        self.reset_button.show()

    def next_question(self):
        """Move to the next question."""
        if self.current_question_index < len(self.questions):
            self.current_question_index += 1
            self.load_question()

    def previous_question(self):
        """Move to the previous question."""
        if self.current_question_index > 0:
            self.current_question_index -= 1
            self.load_question()
