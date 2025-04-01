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
from ..views.components.quiz import Quiz



class QuizPage(QWidget):
    def __init__(self, parent=None, quiz_data=None):
        super().__init__(parent)
        self.quiz_data = quiz_data if quiz_data else []  # Store questions
        self.init_ui()
        
       

    def init_ui(self):
        self.setObjectName("Form")
        self.setStyleSheet("background-color: #FAFAFA;")
        self.setFixedWidth(1200)  # Set fixed width for the entire page
        
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
        self.quiz_name = QLabel("Quiz Name")
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
        self.load_questions()

    def go_back(self):
        """Handles the back button click event. Placeholder for navigation logic."""
        print("Back button clicked!")  # Replace with actual navigation logic

    def load_questions(self):
        """Loads all questions into the list view."""
        for question_data in self.quiz_data:
            print(question_data)
            self.add_question_to_ui(question_data)

    def show_question_dialog(self, quiz_data=None, dialog_type: str = "add"):
        """Shows a dialog to create or edit a question."""
        if dialog_type == "add":
            self.dialog = QuizDialog(quiz=quiz_data, parent=self, on_submit=self.add_question, dialog_type=dialog_type)
        elif dialog_type == "edit":
            self.dialog = QuizDialog(quiz=quiz_data, parent=self, on_submit=self.save_question, dialog_type=dialog_type)

        self.dialog.exec_()
        if self.dialog.result() == QDialog.Accepted:
            self.load_questions()

    def save_question(
        self, question_text, choices, correct_choice, question_data=None
    ):
        """Saves a new question or edits an existing one."""
        if (
            not question_text.strip()
            or any(not choice.strip() for choice in choices)
            or correct_choice == -1
        ):
            return  # Prevent adding empty questions

        if question_data:
            # Editing an existing question
            question_data["question"] = question_text
            question_data["choices"] = choices
            question_data["correct_choice"] = correct_choice
            self.refresh_questions()
        else:
            # Adding a new question
            new_question_data = {
                "question": question_text,
                "choices": choices,
                "correct_choice": correct_choice,
            }
            self.quiz_data.append(new_question_data)
            self.add_question_to_ui(new_question_data)

        self.dialog.accept()
        
    def add_question(self, question_data):
        """Adds a new question to the quiz data and UI."""
        self.quiz_data.append(question_data)
        # create all choices with quiz_id
        # create correct choice with question_id
        self.add_question_to_ui(question_data)
        self.dialog.accept()

    def add_question_to_ui(self, question_data):
        """Creates a UI row for a question with answer choices, edit and remove buttons."""
        question_row = QVBoxLayout()

        # Question Label
        print(question_data)
        question_label = QuizQuestionCard(question_data["question"])
        question_label.setStyleSheet("font-size: 18px;")
        question_row.addWidget(question_label)

        # Choices Labels
        # for i, choice in enumerate(question_data["choices"]):
        #     choice_label = QLabel(
        #         f"- {choice} {'✔' if i == question_data['correct_choice'] else ''}"
        #     )
        #     choice_label.setStyleSheet("font-size: 18px; padding-left: 10px;")
        #     question_row.addWidget(choice_label)

        # Edit & Remove Buttons
        buttons_layout = QHBoxLayout()
        buttons_layout.setAlignment(Qt.AlignRight)

        edit_button = QPushButton("Edit")
        edit_button.setStyleSheet(
            "padding: 8px; font-size: 14px; background-color: blue; color: white; border-radius: 5px;"
        )
        edit_button.clicked.connect(lambda: self.show_question_dialog(quiz_data=question_data, dialog_type="edit"))
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
        self.quiz_data = [q for q in self.quiz_data if q["question"] != question_text]

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
        self.quiz_window = Quiz(quiz_data=self.quiz_data)
        self.quiz_window.show()
