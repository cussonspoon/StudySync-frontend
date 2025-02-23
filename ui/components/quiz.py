from PySide6.QtWidgets import (
    QApplication,
    QWidget,
    QVBoxLayout,
    QLabel,
    QRadioButton,
    QPushButton,
    QButtonGroup,
    QSpacerItem,
    QSizePolicy,
    QFrame,
)


class Quiz(QWidget):
    def __init__(self, parent=None, quiz_data=None):
        super().__init__()

        # Quiz data: questions, options, and correct answers
        self.questions = [
            {
                "question": "What is the capital of France?",
                "options": ["Paris", "London", "Rome", "Berlin"],
                "answer": "Paris",
            },
            {
                "question": "What is 5 + 3?",
                "options": ["5", "8", "10", "15"],
                "answer": "8",
            },
            {
                "question": "Which planet is known as the Red Planet?",
                "options": ["Earth", "Venus", "Mars", "Jupiter"],
                "answer": "Mars",
            },
        ]
        self.current_question_index = 0
        self.score = 0

        self.init_ui()

    def init_ui(self):
        """Initialize the quiz UI."""
        layout = QVBoxLayout()
        layout.setSpacing(20)

        spacer = QSpacerItem(30, 30, QSizePolicy.Minimum, QSizePolicy.Fixed)
        layout.addItem(spacer)
        # Question Label
        self.question_label = QLabel()
        self.question_label.setStyleSheet(
            """
            QLabel {
                font-size: 24px;
                font-weight: regular;
                padding: 10px;
                padding-left: 0;
                border: none;
                margin-bottom: 20px;
            }
            """
        )
        self.question_label.setWordWrap(True)

        self.frame = QFrame()
        self.frame.setLayout(QVBoxLayout())
        self.frame.setStyleSheet(
            """
            QFrame {
                background-color: #ecf0f1;
                border: 1px solid #bdc3c7;
                border-radius: 5px;
                padding: 15px;
            }
            """
        )
        self.frame.setMinimumHeight(200)
        self.frame.layout().setSpacing(10)

        self.frame.layout().addWidget(self.question_label)

        # Option Buttons
        self.options_group = QButtonGroup(self)
        self.option_buttons = []

        for i in range(4):  # Assuming 4 options per question
            button = QRadioButton()
            button.setStyleSheet(
                """
                QRadioButton {
                    background-color: rgb(252,254,252);
                    color: black;
                    font-size: 16px;
                    font-weight: normal;
                    padding: 10px;
                    border-radius: 10px;
                }
                QRadioButton::indicator {
                    width: 20px;
                    height: 20px;
                }
                QRadioButton::indicator::unchecked {
                    image: url(./static/icons/circle.svg);
                }
                QRadioButton::indicator::checked {
                    image: url(./static/icons/circle-check.svg);
                }
                QRadioButton::checked {
                    color: green;
                }
                """
            )
            button
            self.option_buttons.append(button)
            self.options_group.addButton(button)
            self.frame.layout().addWidget(button)

        layout.addWidget(self.frame)

        # Submit Button
        self.submit_button = QPushButton("Submit")
        self.submit_button.setStyleSheet(
            """
            QPushButton {
                background-color: #3498db;
                color: white;
                border: none;
                padding: 10px 20px;
                border-radius: 5px;
                font-size: 16px;
                font-weight: bold;
                font-family: Arial;
                
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

        # Reset Button (Initially Hidden)
        self.reset_button = QPushButton("Restart Quiz")
        self.reset_button.setStyleSheet(
            """
            QPushButton {
                background-color: #e74c3c;
                color: white;
                border: none;
                padding: 10px 20px;
                border-radius: 5px;
                font-size: 16px;
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
        self.reset_button.clicked.connect(self.reset_quiz)
        self.reset_button.hide()  # Hide initially

        layout.addWidget(self.submit_button)
        layout.addWidget(self.reset_button)
        self.setLayout(layout)
        self.setWindowTitle("Quiz App")
        self.setFixedWidth(550)

        self.load_question()

    def load_question(self):
        """Load the current question and update the UI."""
        if self.current_question_index < len(self.questions):
            self.reset_button.hide()  # Hide reset button while quiz is running
            question_data = self.questions[self.current_question_index]
            self.question_label.setText(question_data["question"])

            for i, option in enumerate(question_data["options"]):
                self.option_buttons[i].setText(option)
                self.option_buttons[i].setChecked(False)
                self.option_buttons[i].show()

            self.submit_button.show()  # Ensure submit button is visible

        else:
            self.display_result()

    def check_answer(self):
        """Check the selected answer and update the score."""
        selected_button = self.options_group.checkedButton()

        if selected_button:
            selected_answer = selected_button.text()
            correct_answer = self.questions[self.current_question_index]["answer"]

            if selected_answer == correct_answer:
                self.score += 1  # Increase score if answer is correct

            self.current_question_index += 1  # Move to next question
            self.load_question()

    def reset_quiz(self):
        """Reset the quiz to start from the first question."""
        self.current_question_index = 0
        self.score = 0
        self.load_question()

    def display_result(self):
        """Show final score and hide unnecessary UI elements."""
        self.question_label.setText(
            f"Quiz Finished! Your score: {self.score}/{len(self.questions)}"
        )

        # Hide all option buttons and submit button
        for button in self.option_buttons:
            button.hide()
        self.submit_button.hide()

        # Show reset button
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
