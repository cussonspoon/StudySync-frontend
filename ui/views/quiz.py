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
)
from PySide6.QtCore import QRect, Qt
from utils.ui import QuizQuestionCard
from ..views.components.quiz_dialog import QuizDialog
from ..views.components.quiz import QuizStart
from models.quiz import Question, Quiz, Choice
from controllers.quiz_controller import QuizController
from typing import List

class QuizPage(QWidget):
    def __init__(self, parent=None, quiz: Quiz = None, quiz_controller: QuizController = None):
        super().__init__(parent)
        self.quiz = quiz
        self.quiz_controller = quiz_controller
        self.questions = []
        
        if self.quiz_controller:
            self.questions = self.quiz_controller.get_questions()
            self.quiz_controller.set_quiz(self.quiz)
        else:
            # Initialize with empty quiz if none provided
            if not self.quiz:
                self.quiz = Quiz(
                    id="",
                    title="New Quiz",
                    quiz_type="quiz",
                    mode="normal",
                    total_questions=0,
                    total_likes=0,
                    total_points=0,
                    points_to_pass=70,
                    time_limit=300,
                    folder_id="",
                    created_at=""
                )
        
        self.init_ui()

    def init_ui(self):
        self.setObjectName("Form")
        self.setStyleSheet("background-color: #FAFAFA;")
        self.setFixedWidth(1200)  # Set fixed width for the entire page
        self.setFixedHeight(800)
        
        # Set size policy to expand in both directions
        self.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Expanding)

        # 📌 Main Layout for the entire QuizPage
        self.main_layout = QVBoxLayout(self)
        self.main_layout.setContentsMargins(20, 20, 20, 20)  # Add some padding around the edges
        self.main_layout.setSpacing(20)  # Add spacing between elements
        self.main_layout.setAlignment(Qt.AlignTop)

        # 📌 Back Button Container (Full Width)
        back_button_container = QHBoxLayout()
        back_button_container.setContentsMargins(0, 0, 0, 0)
        back_button_container.setAlignment(Qt.AlignLeft)

        # 📌 Back Button
        self.back_button = QPushButton("← Back")
        self.back_button.setFixedSize(100, 50)
        self.back_button.setStyleSheet(
            "padding: 10px; font-size: 18px; background-color: #E0E0E0; color: black; border-radius: 10px;"
        )
        self.back_button.clicked.connect(self.go_back)
        back_button_container.addWidget(self.back_button)
        
        # Add back button container to main layout
        self.main_layout.addLayout(back_button_container)

        # 📌 Quiz Name
        self.quiz_name = QLabel(self.quiz.title)
        self.quiz_name.setObjectName("quiz_name")
        self.quiz_name.setStyleSheet(
            "background-color: rgb(217, 217, 217);\n"
            "color: rgb(0, 0, 0);\n"
            "padding: 20px;\n"
            "font-size: 40px;\n"
            "font-weight: bold;\n"
            "border-radius: 10px;"
            "border: 1px solid #DCDCDC;"
        )
        self.quiz_name.setWordWrap(True)
        self.quiz_name.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)
        self.main_layout.addWidget(self.quiz_name)

        # 📌 Scroll Area Setup
        self.scrollArea = QScrollArea()
        self.scrollArea.setWidgetResizable(True)
        self.scrollArea.setStyleSheet("""
            QScrollArea {
                background-color: #FAFAFA;
                border: none;
            }
            QScrollBar:vertical {
                border: none;
                background: #F0F0F0;
                width: 10px;
                margin: 0px;
            }
            QScrollBar::handle:vertical {
                background: #C0C0C0;
                min-height: 20px;
                border-radius: 5px;
            }
            QScrollBar::handle:vertical:hover {
                background: #A0A0A0;
            }
        """)

        # 📌 Content Widget for Scroll Area
        self.scrollAreaContent = QWidget()
        self.scrollArea.setWidget(self.scrollAreaContent)
        
        # 📌 Main Layout for the Scroll Area Content
        self.layout = QVBoxLayout(self.scrollAreaContent)
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.layout.setSpacing(20)
        self.layout.setAlignment(Qt.AlignTop)

        # 📌 Questions Layout
        self.questions_layout = QVBoxLayout()
        self.questions_layout.setSpacing(20)
        self.layout.addLayout(self.questions_layout)

        # 📌 Add Button Layout
        self.add_button_layout = QHBoxLayout()
        self.add_button_layout.setAlignment(Qt.AlignRight)
        self.add_button_layout.setSpacing(10)

        # 📌 Add Button
        self.add_button = QPushButton("Add Question")
        self.add_button.setStyleSheet(
            "padding: 10px; font-size: 18px; background-color: #4CAF50; color: white; border-radius: 10px;"
        )
        self.add_button.setFixedSize(200, 50)
        self.add_button.clicked.connect(lambda: self.show_question_dialog(dialog_type="add"))
        
        self.start_quiz_button = QPushButton("Start Quiz")
        self.start_quiz_button.setStyleSheet(
            "padding: 10px; font-size: 18px; background-color: #4CAF50; color: white; border-radius: 10px;"
        )
        self.start_quiz_button.setFixedSize(200, 50)
        self.start_quiz_button.clicked.connect(lambda: self.start_quiz())
        
        self.add_button_layout.addWidget(self.add_button)
        self.add_button_layout.addWidget(self.start_quiz_button)
        
        self.main_layout.addLayout(self.add_button_layout)
        
        # 📌 Add Scroll Area to Main Layout
        self.main_layout.addWidget(self.scrollArea)

        # 📌 Load Initial Questions
        if self.questions:
            self.load_questions(self.questions)

    def go_back(self):
        """Closes the quiz page widget."""
        self.close()

    def load_questions(self, questions: List[Question]):
        """Loads all questions into the list view."""
        for question in questions:
            # Convert Question object to display format
            question_data = {
                "question": question.question,
                "choices": [
                    {"choice": choice.choice, "is_answer": choice.is_answer}
                    for choice in question.choices
                ]
            }
            self.add_question_to_ui(question_data)

    def show_question_dialog(self, question: Question = None, dialog_type: str = "add"):
        """Shows a dialog to create or edit a question."""
        # Convert dictionary to Question object if needed
        if isinstance(question, dict):
            temp_question = Question(
                id="",  # Empty string for new questions
                question=question["question"],
                created_at="",
                quiz_id=self.quiz.id,
                choices=[Choice(id="", choice=choice["choice"], is_answer=choice["is_answer"], question_id="") for choice in question["choices"]]
            )
            question = temp_question
            
        if dialog_type == "add":
            self.dialog = QuizDialog(question=question, parent=self, on_submit=self.add_question, dialog_type=dialog_type)
        elif dialog_type == "edit":
            self.dialog = QuizDialog(question=question, parent=self, on_submit=self.save_question, dialog_type=dialog_type)

        self.dialog.exec_()

    def save_question(
        self, question_text, choices, question_data=None
    ):
        """Saves a new question or edits an existing one."""
        if (
            not question_text.strip()
            or any(not choice.strip() for choice in choices)
        ):
            return  # Prevent adding empty questions

        if question_data:
            # Editing an existing question
            question_data.question = question_text
            question_data.choices = choices
            self.refresh_questions()
        else:
            # Adding a new question
            new_question = Question(
                id="",  # Empty string for new questions
                question=question_text,
                created_at="",
                quiz_id=self.quiz.id,
                choices=[Choice(id="", choice=choice["choice"], is_answer=choice["is_answer"], question_id="") for choice in choices]
            )
            self.questions.append(new_question)
            self.add_question_to_ui({
                "question": question_text,
                "choices": choices
            })

        self.dialog.accept()
        
    def add_question(self, question_data):
        """Adds a new question to the quiz data and UI."""
        # Convert the question data to a Question object
        question = Question(
            id="",  # Empty string for new questions
            question=question_data["question"],
            created_at="",
            quiz_id=self.quiz.id,
            choices=[Choice(id="", choice=choice["choice"], is_answer=choice["is_answer"], question_id="") for choice in question_data["choices"]]
        )
        self.questions.append(question)
        self.add_question_to_ui(question_data)
        self.dialog.accept()

    def add_question_to_ui(self, question_data):
        """Creates a UI row for a question with answer choices, edit and remove buttons."""
        question_row = QVBoxLayout()

        # Question Label
        question_label = QuizQuestionCard(question_data["question"])
        question_label.setStyleSheet("font-size: 18px;")
        question_row.addWidget(question_label)

        # Edit & Remove Buttons
        buttons_layout = QHBoxLayout()
        buttons_layout.setAlignment(Qt.AlignRight)

        edit_button = QPushButton("Edit")
        edit_button.setStyleSheet(
            "padding: 8px; font-size: 14px; background-color: blue; color: white; border-radius: 5px;"
        )
        edit_button.clicked.connect(lambda: self.show_question_dialog(question=question_data, dialog_type="edit"))
        buttons_layout.addWidget(edit_button)

        remove_button = QPushButton("Remove")
        remove_button.setStyleSheet(
            "padding: 8px; font-size: 14px; background-color: red; color: white; border-radius: 5px;"
        )
        remove_button.clicked.connect(
            lambda: self.remove_question(question_label, question_row)
        )
        buttons_layout.addWidget(remove_button)

        question_row.addLayout(buttons_layout)
        self.questions_layout.addLayout(question_row)

    def _cleanup_layout(self, layout):
        """Helper method to clean up all widgets and nested layouts."""
        while layout.count():
            item = layout.takeAt(0)
            if item.widget():
                item.widget().deleteLater()
            elif item.layout():
                nested_layout = item.layout()
                self._cleanup_layout(nested_layout)
                nested_layout.deleteLater()

    def remove_question(self, question_label, question_row):
        """Removes a question from the UI and the data list."""
        # Remove from data
        question_text = question_label.question_text
        self.questions = [q for q in self.questions if q.question != question_text]

        # Clean up UI
        self._cleanup_layout(question_row)
        self.questions_layout.removeItem(question_row)
        question_row.deleteLater()

    def refresh_questions(self):
        """Clears and reloads all questions."""
        # Clean up existing questions
        self._cleanup_layout(self.questions_layout)
        self.questions_layout.deleteLater()
        # Reload questions
        self.load_questions()

    def start_quiz(self):
        """Starts the quiz."""
        # Convert dictionary questions to Question objects
        question_objects = []
        for question_dict in self.questions:
            question = Question(
                id="",  # Empty string for new questions
                question=question_dict["question"],
                created_at="",
                quiz_id=self.quiz.id,
                choices=[Choice(id="", choice=choice["choice"], is_answer=choice["is_answer"], question_id="") for choice in question_dict["choices"]]
            )
            question_objects.append(question)
            
        self.quiz_window = QuizStart(questions=question_objects)
        self.quiz_window.show()
