from PySide6.QtWidgets import (
    QDialog,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QTextEdit,
    QPushButton,
    QListWidget,
    QListWidgetItem,
    QMessageBox,
    QRadioButton,
    QButtonGroup,
)
from PySide6.QtCore import Qt
from models.quiz import Question

# Define all styles in a dictionary for better organization
STYLES = {
    "dialog": """
        QDialog {
            background-color: #f8f9fa;
        }
    """,
    
    "input": """
        QLineEdit {
            background-color: #ffffff;
            border: 2px solid #e9ecef;
            border-radius: 10px;
            font-size: 16px;
            padding: 15px;
            color: #2c3e50;
        }
        QLineEdit:focus {
            border-color: #3498db;
        }
        QLineEdit::placeholder {
            color: #adb5bd;
        }
    """,
    
    "header": """
        QLabel {
            font-size: 20px;
            font-weight: bold;
            color: #2c3e50;
            margin-bottom: 10px;
        }
    """,
    
    "radio_button": """
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
    """,
    
    "button": """
        QPushButton {
            background-color: #ffffff;
            color: #2c3e50;
            border: 2px solid #e9ecef;
            border-radius: 10px;
            font-size: 16px;
            font-weight: bold;
            padding: 12px 25px;
            min-width: 120px;
        }
        QPushButton:hover {
            background-color: #f8f9fa;
            border-color: #dee2e6;
        }
        QPushButton:pressed {
            background-color: #e9ecef;
        }
    """,
    
    "save_button": """
        QPushButton {
            background-color: #2ecc71;
            color: white;
            border: none;
            border-radius: 10px;
            font-size: 16px;
            font-weight: bold;
            padding: 12px 25px;
            min-width: 120px;
        }
        QPushButton:hover {
            background-color: #27ae60;
        }
        QPushButton:pressed {
            background-color: #219653;
        }
    """,
    
    "cancel_button": """
        QPushButton {
            background-color: #e9ecef;
            color: #2c3e50;
            border: none;
            border-radius: 10px;
            font-size: 16px;
            font-weight: bold;
            padding: 12px 25px;
            min-width: 120px;
        }
        QPushButton:hover {
            background-color: #dee2e6;
        }
        QPushButton:pressed {
            background-color: #ced4da;
        }
    """
}

class QuizDialog(QDialog):
    def __init__(self, question: Question = None, parent=None, on_submit=None, dialog_type: str = "edit"):
        super().__init__(parent)
        self.setWindowTitle(dialog_type.capitalize() + " Question")
        self.setFixedSize(500, 600)
        self.setStyleSheet(STYLES["dialog"])
        self.setModal(True)
        self.question = question
        self.on_submit = on_submit

        # Main Layout
        layout = QVBoxLayout(self)
        layout.setSpacing(20)
        layout.setContentsMargins(30, 30, 30, 30)

        # Title Input
        question_header = QLabel("Question:")
        question_header.setStyleSheet(STYLES["header"])
        layout.addWidget(question_header)

        self.title_input = QLineEdit()
        self.title_input.setText(self.question.question if self.question else "")
        self.title_input.setStyleSheet(STYLES["input"])
        self.title_input.setPlaceholderText("Enter your question here...")
        layout.addWidget(self.title_input)

        # Choices Header
        choice_header = QLabel("Choices:")
        choice_header.setStyleSheet(STYLES["header"])
        layout.addWidget(choice_header)

        # Create button group for radio buttons
        self.answer_group = QButtonGroup(self)

        # Initialize choice inputs and radio buttons
        self.choice_inputs = []
        self.radio_buttons = []

        # Choice Inputs
        for i in range(4):
            choice_layout = QHBoxLayout()
            
            # Choice Input
            choice_input = QLineEdit()
            choice_input.setStyleSheet(STYLES["input"])
            choice_input.setPlaceholderText(f"Choice {i+1}...")
            
            # Set text if editing existing question
            if self.question and self.question.choices and len(self.question.choices) > i:
                choice_input.setText(self.question.choices[i].choice)
            
            self.choice_inputs.append(choice_input)
            choice_layout.addWidget(choice_input)

            # Radio Button
            radio = QRadioButton()
            radio.setStyleSheet(STYLES["radio_button"])
            
            # Set checked state if editing existing question
            if self.question and self.question.choices and len(self.question.choices) > i:
                radio.setChecked(self.question.choices[i].is_answer)
            
            self.radio_buttons.append(radio)
            self.answer_group.addButton(radio)
            choice_layout.addWidget(radio)

            layout.addLayout(choice_layout)

        # Buttons Layout
        btn_layout = QHBoxLayout()
        btn_layout.setSpacing(15)
        btn_layout.setAlignment(Qt.AlignRight)

        # Cancel Button
        self.cancel_btn = QPushButton("Cancel")
        self.cancel_btn.setStyleSheet(STYLES["cancel_button"])
        self.cancel_btn.clicked.connect(self.reject)
        btn_layout.addWidget(self.cancel_btn)

        # Save Button
        self.save_btn = QPushButton("Save")
        self.save_btn.setStyleSheet(STYLES["save_button"])
        self.save_btn.clicked.connect(self.save_question)
        btn_layout.addWidget(self.save_btn)

        layout.addLayout(btn_layout)

    def get_quiz_data(self):
        data = {
            "question": self.title_input.text(),
            "choices": [
                {
                    "choice": self.choice_inputs[i].text(),
                    "is_answer": self.radio_buttons[i].isChecked()
                }
                for i in range(4)
            ]
        }
        return data

    def save_question(self):
        """Handles saving the question and closing the dialog."""
        try:
            # Get the question data
            question_data = self.get_quiz_data()
            
            # Call the on_submit callback with the data
            if self.on_submit:
                self.on_submit(question_data)
            
            # Close the dialog
            self.accept()
            
        except Exception as e:
            print(f"Error saving question: {str(e)}")
            QMessageBox.warning(self, "Error", "Failed to save question. Please try again.")
