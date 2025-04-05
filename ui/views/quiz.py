from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QLabel,
    QPushButton,
    QScrollArea,
    QHBoxLayout,
    QFormLayout,
    QLineEdit,
    QDialog,
    QButtonGroup,
    QRadioButton,
    QFrame,
    QSizePolicy,
    QMessageBox,
)
from PySide6.QtCore import QRect, Qt, QSize
from PySide6.QtGui import QIcon, QFont
from utils.ui import QuizQuestionCard
from ..views.components.quiz_dialog import QuizDialog
from .components.quiz_start import QuizStart
from models.quiz import Question, Quiz, Choice
from controllers.quiz_controller import QuizController
from typing import List


class QuestionCard(QFrame):
    def __init__(self, question_data, parent=None):
        super().__init__(parent)
        self.question_data = question_data
        self.quiz_page = parent  # Store reference to QuizPage
        self.setup_ui()

    def setup_ui(self):
        self.setStyleSheet(
            """
            QFrame {
                background-color: #f8f9fa;
                border-radius: 10px;
                padding: 20px;
            }
        """
        )
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(15)

        # Question Label
        question_label = QuizQuestionCard(self.question_data["question"])
        question_label.setStyleSheet(
            """
            QLabel {
                font-size: 18px;
                color: #2c3e50;
                font-weight: 500;
                padding: 10px;
            }
        """
        )
        layout.addWidget(question_label)

        # Action Buttons
        buttons_layout = QHBoxLayout()
        buttons_layout.setContentsMargins(0, 0, 0, 0)
        buttons_layout.setSpacing(10)
        buttons_layout.setAlignment(Qt.AlignRight)

        # Edit Button
        edit_button = QPushButton("Edit")
        edit_button.setStyleSheet(
            """
            QPushButton {
                background-color: #3498db;
                color: white;
                border: none;
                border-radius: 5px;
                padding: 8px 15px;
                font-size: 14px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #2980b9;
            }
            QPushButton:pressed {
                background-color: #1c669b;
            }
        """
        )
        edit_button.clicked.connect(self.handle_edit)
        buttons_layout.addWidget(edit_button)

        # Remove Button
        remove_button = QPushButton("Remove")
        remove_button.setStyleSheet(
            """
            QPushButton {
                background-color: #e74c3c;
                color: white;
                border: none;
                border-radius: 5px;
                padding: 8px 15px;
                font-size: 14px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #c0392b;
            }
            QPushButton:pressed {
                background-color: #a93226;
            }
        """
        )
        remove_button.clicked.connect(self.handle_remove)
        buttons_layout.addWidget(remove_button)

        layout.addLayout(buttons_layout)

    def handle_edit(self):
        if self.quiz_page:
            self.quiz_page.show_question_dialog(
                question=self.question_data, dialog_type="edit"
            )

    def handle_remove(self):
        if self.quiz_page:
            self.quiz_page.remove_question(self)


class QuizPage(QWidget):
    def __init__(self, parent=None, quiz: Quiz = None):
        super().__init__(parent)
        self.quiz = Quiz(
            id="d592e4a8-6aea-4fa8-92dd-c562db757a0b",
            title="Quiz 1",
            quiz_type="quiz",
            mode="normal",
        )
        self.quiz_controller = QuizController(self.quiz)
        self.questions = []

        self.init_ui()

    def init_ui(self):
        self.setObjectName("Form")
        self.setStyleSheet(
            """
            QWidget {
                background-color: #f8f9fa;
            }
        """
        )
        self.setFixedWidth(1200)
        self.setFixedHeight(800)
        self.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Expanding)

        # Main Layout
        self.main_layout = QVBoxLayout(self)
        self.main_layout.setContentsMargins(30, 30, 30, 30)
        self.main_layout.setSpacing(25)
        self.main_layout.setAlignment(Qt.AlignTop)

        # Header Container
        header_container = QFrame()
        header_container.setStyleSheet(
            """
            QFrame {
                background-color: white;
                border-radius: 15px;
                padding: 20px;
            }
        """
        )
        header_layout = QVBoxLayout(header_container)
        header_layout.setContentsMargins(0, 0, 0, 0)
        header_layout.setSpacing(15)

        # Back Button and Title Container
        top_container = QHBoxLayout()
        top_container.setContentsMargins(0, 0, 0, 0)
        top_container.setSpacing(20)

        # Back Button
        self.back_button = QPushButton("← Back")
        self.back_button.setFixedSize(100, 40)
        self.back_button.setStyleSheet(
            """
            QPushButton {
                background-color: #e9ecef;
                color: #2c3e50;
                border: none;
                border-radius: 10px;
                font-size: 16px;
                font-weight: bold;
                padding: 8px;
            }
            QPushButton:hover {
                background-color: #dee2e6;
            }
            QPushButton:pressed {
                background-color: #ced4da;
            }
        """
        )
        self.back_button.clicked.connect(self.go_back)
        top_container.addWidget(self.back_button)

        # Quiz Title
        self.quiz_name = QLabel(self.quiz.title)
        self.quiz_name.setStyleSheet(
            """
            QLabel {
                color: #2c3e50;
                font-size: 32px;
                font-weight: bold;
                padding: 10px;
            }
        """
        )
        self.quiz_name.setWordWrap(True)
        self.quiz_name.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)
        top_container.addWidget(self.quiz_name)

        header_layout.addLayout(top_container)

        # Action Buttons Container
        action_container = QHBoxLayout()
        action_container.setContentsMargins(0, 0, 0, 0)
        action_container.setSpacing(15)
        action_container.setAlignment(Qt.AlignRight)

        # Add Button
        self.add_button = QPushButton()
        self.add_button.setIcon(QIcon("static/images/plus.svg"))
        self.add_button.setIconSize(QSize(24, 24))
        self.add_button.setStyleSheet(
            """
            QPushButton {
                background-color: #4CAF50;
                border: none;
                border-radius: 10px;
                padding: 10px;
            }
            QPushButton:hover {
                background-color: #45a049;
            }
            QPushButton:pressed {
                background-color: #3d8b40;
            }
        """
        )
        self.add_button.setFixedSize(50, 50)
        self.add_button.clicked.connect(
            lambda: self.show_question_dialog(dialog_type="add")
        )
        action_container.addWidget(self.add_button)

        # Refresh Button
        self.refresh_button = QPushButton()
        self.refresh_button.setIcon(QIcon("static/images/refresh.svg"))
        self.refresh_button.setIconSize(QSize(24, 24))
        self.refresh_button.setStyleSheet(
            """
            QPushButton {
                background-color: #3498db;
                border: none;
                border-radius: 10px;
                padding: 10px;
            }
            QPushButton:hover {
                background-color: #2980b9;
            }
            QPushButton:pressed {
                background-color: #1c669b;
            }
        """
        )
        self.refresh_button.setFixedSize(50, 50)
        self.refresh_button.clicked.connect(lambda: self.refresh_questions())
        action_container.addWidget(self.refresh_button)

        # Start Quiz Button
        self.start_quiz_button = QPushButton("Start Quiz")
        self.start_quiz_button.setStyleSheet(
            """
            QPushButton {
                background-color: #2ecc71;
                color: white;
                border: none;
                border-radius: 10px;
                font-size: 16px;
                font-weight: bold;
                padding: 10px 20px;
            }
            QPushButton:hover {
                background-color: #27ae60;
            }
            QPushButton:pressed {
                background-color: #219653;
            }
        """
        )
        self.start_quiz_button.setFixedSize(150, 50)
        self.start_quiz_button.clicked.connect(lambda: self.start_quiz())
        action_container.addWidget(self.start_quiz_button)

        header_layout.addLayout(action_container)
        self.main_layout.addWidget(header_container)

        # Questions Container
        questions_container = QFrame()
        questions_container.setStyleSheet(
            """
            QFrame {
                background-color: white;
                border-radius: 15px;
                padding: 20px;
            }
        """
        )
        questions_layout = QVBoxLayout(questions_container)
        questions_layout.setContentsMargins(0, 0, 0, 0)
        questions_layout.setSpacing(20)

        # Scroll Area
        self.scrollArea = QScrollArea()
        self.scrollArea.setWidgetResizable(True)
        self.scrollArea.setStyleSheet(
            """
            QScrollArea {
                background-color: transparent;
                border: none;
            }
            QScrollBar:vertical {
                border: none;
                background: #f8f9fa;
                width: 10px;
                margin: 0px;
            }
            QScrollBar::handle:vertical {
                background: #dee2e6;
                min-height: 20px;
                border-radius: 5px;
            }
            QScrollBar::handle:vertical:hover {
                background: #ced4da;
            }
        """
        )

        # Scroll Area Content
        self.scrollAreaContent = QWidget()
        self.scrollArea.setWidget(self.scrollAreaContent)

        # Questions Layout
        self.questions_layout = QVBoxLayout(self.scrollAreaContent)
        self.questions_layout.setContentsMargins(0, 0, 0, 0)
        self.questions_layout.setSpacing(20)
        self.questions_layout.setAlignment(Qt.AlignTop)

        questions_layout.addWidget(self.scrollArea)
        self.main_layout.addWidget(questions_container)

        # Load Initial Questions
        self.load_questions()

    def go_back(self):
        """Closes the quiz page widget."""
        self.close()

    def load_questions(self):
        """Loads all questions into the list view."""

        self.questions = self.quiz_controller.get_questions(self.quiz.id)

        for question in self.questions:
            # Convert Question object to display format
            question_data = {
                "question": question.question,
                "choices": [
                    {"choice": choice.choice, "is_answer": choice.is_answer}
                    for choice in question.choices
                ],
            }
            self.add_question_to_ui(question_data)

    def show_question_dialog(self, question: Question = None, dialog_type: str = "add"):
        """Shows a dialog to create or edit a question."""
        try:
            # Convert dictionary to Question object if needed
            if isinstance(question, dict):
                temp_question = Question(
                    id="",  # Empty string for new questions
                    question=question["question"],
                    created_at="",
                    quiz_id=self.quiz.id,
                    choices=[
                        Choice(
                            id="",
                            choice=choice["choice"],
                            is_answer=choice["is_answer"],
                            question_id="",
                        )
                        for choice in question["choices"]
                    ],
                )
                question = temp_question

            # Create and show dialog
            dialog = QuizDialog(
                question=question,
                parent=self,
                on_submit=(
                    self.add_question if dialog_type == "add" else self.save_question
                ),
                dialog_type=dialog_type,
            )
            dialog.exec_()

        except Exception as e:
            print(f"Error showing dialog: {str(e)}")
            QMessageBox.warning(
                self, "Error", "Failed to open dialog. Please try again."
            )

    def add_question(self, question_data):
        """Adds a new question to the quiz data and UI."""
        try:
            # Post question first
            reply = self.quiz_controller.post_question(
                self.quiz.id, question_data["question"]
            )
            question_id = reply["id"]

            # Post choices
            for choice in question_data["choices"]:
                self.quiz_controller.post_choice(
                    question_id, choice["choice"], choice["is_answer"]
                )

            # Refresh questions
            self.refresh_questions()

        except Exception as e:
            print("Error adding question:", str(e))
            QMessageBox.warning(
                self, "Error", "Failed to add question. Please try again."
            )

    def clear_layout(self):
        for i in reversed(range(self.questions_layout.count())):
            item = self.questions_layout.itemAt(i)
            item.widget().deleteLater()

    def save_question(self, question_data):
        """Saves an edited question."""
        try:
            # Update question
            self.quiz_controller.update_question(question_data)

            # Refresh questions
            self.refresh_questions()

        except Exception as e:
            print("Error saving question:", str(e))
            QMessageBox.warning(
                self, "Error", "Failed to save question. Please try again."
            )

    def add_question_to_ui(self, question_data):
        """Creates a UI row for a question with answer choices, edit and remove buttons."""
        question_card = QuestionCard(question_data, self)
        self.questions_layout.addWidget(question_card)

    def remove_question(self, question_card):
        try:
            # Remove from data
            question_text = question_card.question_data["question"]
            self.questions = [q for q in self.questions if q.question != question_text]

            # Remove from UI
            self.questions_layout.removeWidget(question_card)
            question_card.deleteLater()

            # Update the UI
            self.scrollAreaContent.update()
            self.scrollArea.update()

        except Exception as e:
            print(f"Error removing question: {e}")
            QMessageBox.warning(self, "Error", "Failed to remove question.")

    def refresh_questions(self):
        """Clears and reloads all questions from the API."""
        try:
            # Clear existing questions from UI
            self.clear_layout()

            # Clear existing questions list
            self.questions.clear()

            # Fetch fresh questions from API
            self.questions = self.quiz_controller.get_questions(self.quiz.id)

            # Update UI with new questions
            for question in self.questions:
                question_data = {
                    "question": question.question,
                    "choices": [
                        {"choice": choice.choice, "is_answer": choice.is_answer}
                        for choice in question.choices
                    ],
                }
                self.add_question_to_ui(question_data)

        except Exception as e:
            print(f"Error refreshing questions: {str(e)}")
            QMessageBox.warning(
                self, "Error", "Failed to refresh questions. Please try again."
            )

    def start_quiz(self):
        """Starts the quiz."""
        # Convert dictionary questions to Question objects
        question_objects = []
        for question in self.questions:
            # If question is already a Question object, use it directly
            if isinstance(question, Question):
                question_objects.append(question)
            # If it's a dictionary, convert it to a Question object
            elif isinstance(question, dict):
                question_obj = Question(
                    id="",  # Empty string for new questions
                    question=question["question"],
                    created_at="",
                    quiz_id=self.quiz.id,
                    choices=[
                        Choice(
                            id="",
                            choice=choice["choice"],
                            is_answer=choice["is_answer"],
                            question_id="",
                        )
                        for choice in question["choices"]
                    ],
                )
                question_objects.append(question_obj)

        self.quiz_window = QuizStart(parent=self, questions=question_objects)
        # Connect the quiz_completed signal to refresh the folder contents
        if isinstance(self.parent(), QWidget):
            self.quiz_window.quiz_completed.connect(self.parent().load_items)
        self.quiz_window.exec()  # Use exec() instead of show() for modal dialogs
