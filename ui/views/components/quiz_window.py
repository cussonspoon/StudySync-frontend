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
from PySide6.QtGui import QIcon
from utils.ui import QuizQuestionCard
from .quiz_dialog import QuizDialog
from .quiz_start import QuizStart
from models.quiz import Question, Quiz, Choice
from controllers.quiz_controller import QuizController
from services.quiz_service import QuizService


class popup_quizwindow(QDialog):
    def __init__(self, parent=None, quiz: Quiz = None):
        super().__init__(
            parent,
            Qt.WindowSystemMenuHint | Qt.WindowTitleHint | Qt.WindowCloseButtonHint,
        )
        self.setModal(True)
        self.setWindowTitle("New Quiz")
        self.setFixedSize(1000, 800)

        # Initialize with empty quiz if none provided
        if quiz is None:
            self.quiz = Quiz(
                id="",  # Empty ID for new quiz
                title="New Quiz",
                quiz_type="quiz",
                mode="normal",
            )
        else:
            self.quiz = quiz

        self.quiz_controller = QuizController(self.quiz)
        self.questions = []
        self.quiz_created = False  # Track if quiz has been created on server

        self.setupUi()

    def setupUi(self):
        # Main Layout
        self.main_layout = QVBoxLayout(self)
        self.main_layout.setContentsMargins(0, 0, 0, 0)
        self.main_layout.setSpacing(0)

        # Content Widget
        content_widget = QWidget()
        content_widget.setStyleSheet("background-color: #F7F6F3;")
        content_layout = QVBoxLayout(content_widget)
        content_layout.setContentsMargins(20, 20, 20, 20)
        content_layout.setSpacing(20)

        # Quiz Name
        self.quiz_name = QLabel(self.quiz.title)
        self.quiz_name.setObjectName("quiz_name")
        self.quiz_name.setStyleSheet(
            """
            background-color: rgb(217, 217, 217);
            color: rgb(0, 0, 0);
            padding: 20px;
            font-size: 40px;
            font-weight: bold;
            border-radius: 10px;
            border: 1px solid #DCDCDC;
            """
        )
        self.quiz_name.setWordWrap(True)
        content_layout.addWidget(self.quiz_name)

        # Scroll Area Setup
        self.scrollArea = QScrollArea()
        self.scrollArea.setWidgetResizable(True)
        self.scrollArea.setStyleSheet(
            """
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
        """
        )

        # Content Widget for Scroll Area
        self.scrollAreaContent = QWidget()
        self.scrollArea.setWidget(self.scrollAreaContent)

        # Layout for Scroll Area Content
        self.layout = QVBoxLayout(self.scrollAreaContent)
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.layout.setSpacing(20)
        self.layout.setAlignment(Qt.AlignTop)

        # Questions Layout
        self.questions_layout = QVBoxLayout()
        self.questions_layout.setSpacing(20)
        self.layout.addLayout(self.questions_layout)

        # Add Button Layout
        self.add_button_layout = QHBoxLayout()
        self.add_button_layout.setAlignment(Qt.AlignRight)
        self.add_button_layout.setSpacing(10)

        # Add Button
        self.add_button = QPushButton()
        self.add_button.setIcon(QIcon("static/images/plus.svg"))
        self.add_button.setIconSize(QSize(24, 24))
        self.add_button.setStyleSheet(
            "padding: 10px; background-color: #4CAF50; color: white; border-radius: 10px;"
        )
        self.add_button.setFixedSize(50, 50)
        self.add_button.clicked.connect(
            lambda: self.show_question_dialog(dialog_type="add")
        )

        self.start_quiz_button = QPushButton("Start Quiz")
        self.start_quiz_button.setStyleSheet(
            "padding: 10px; font-size: 18px; background-color: #4CAF50; color: white; border-radius: 10px;"
        )
        self.start_quiz_button.setFixedSize(200, 50)
        self.start_quiz_button.clicked.connect(lambda: self.start_quiz())

        self.refresh_button = QPushButton()
        self.refresh_button.setIcon(QIcon("static/images/refresh.svg"))
        self.refresh_button.setIconSize(QSize(24, 24))
        self.refresh_button.setStyleSheet(
            "padding: 10px; background-color: #4CAF50; border-radius: 10px; color: white;"
        )
        self.refresh_button.setFixedSize(50, 50)
        self.refresh_button.clicked.connect(lambda: self.refresh_questions())

        self.add_button_layout.addWidget(self.add_button)
        self.add_button_layout.addWidget(self.refresh_button)
        self.add_button_layout.addWidget(self.start_quiz_button)

        content_layout.addLayout(self.add_button_layout)
        content_layout.addWidget(self.scrollArea)

        self.main_layout.addWidget(content_widget)

        # Only load questions if we have an existing quiz
        if self.quiz.id:
            try:
                self.load_questions()
            except Exception as e:
                print("Error loading questions:", str(e))

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

        if dialog_type == "add":
            self.dialog = QuizDialog(
                question=question,
                parent=self,
                on_submit=self.add_question,
                dialog_type=dialog_type,
            )
        elif dialog_type == "edit":
            self.dialog = QuizDialog(
                question=question,
                parent=self,
                on_submit=self.save_question,
                dialog_type=dialog_type,
            )

        self.dialog.exec_()

    def save_question(self, question_text, choices, question_data=None):
        """Saves a new question or edits an existing one."""
        if not question_text.strip() or any(not choice.strip() for choice in choices):
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
                choices=[
                    Choice(
                        id="",
                        choice=choice["choice"],
                        is_answer=choice["is_answer"],
                        question_id="",
                    )
                    for choice in choices
                ],
            )
            self.questions.append(new_question)
            self.add_question_to_ui({"question": question_text, "choices": choices})

        self.dialog.accept()

    def ensure_quiz_exists(self):
        """Ensures the quiz exists on the server before adding questions."""
        if not self.quiz_created and not self.quiz.id:
            try:
                # Create the quiz on the server using QuizService
                quiz_service = QuizService(self.quiz)
                new_quiz = quiz_service.create_quiz(self.quiz.title)

                # Update our quiz with the server-assigned data
                self.quiz.id = new_quiz.id
                self.quiz.quiz_type = new_quiz.quiz_type
                self.quiz.mode = new_quiz.mode

                self.quiz_created = True
                # Update the controller with the new quiz
                self.quiz_controller.set_quiz(self.quiz)
                return True
            except Exception as e:
                print("Error creating quiz:", str(e))
                QMessageBox.critical(
                    self, "Error", f"Failed to create quiz on server: {str(e)}"
                )
                return False
        return True

    def add_question(self, question_data):
        """Adds a new question to the quiz data and UI."""
        try:
            # Ensure quiz exists before adding question
            if not self.ensure_quiz_exists():
                QMessageBox.critical(self, "Error", "Failed to create quiz on server")
                return

            reply = self.quiz_controller.post_question(
                self.quiz.id, question_data["question"]
            )
            question_id = reply["id"]
            for choice in question_data["choices"]:
                self.quiz_controller.post_choice(
                    question_id, choice["choice"], choice["is_answer"]
                )
            self.dialog.accept()  # Close the dialog after successful save
            self.refresh_questions()
        except Exception as e:
            print("Error adding question:", str(e))
            QMessageBox.critical(self, "Error", f"Failed to add question: {str(e)}")

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
        edit_button.clicked.connect(
            lambda: self.show_question_dialog(
                question=question_data, dialog_type="edit"
            )
        )
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

        # Create a new questions layout
        self.questions_layout = QVBoxLayout()
        self.questions_layout.setSpacing(20)
        self.layout.addLayout(self.questions_layout)

        # Reload questions
        self.load_questions()

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

        self.quiz_window = QuizStart(questions=question_objects)
        self.quiz_window.show()

    def getQuizData(self):
        """Returns the quiz data when dialog is closed."""
        return {"title": self.quiz_name.text(), "questions": self.questions}
