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

input_style = """
            QLineEdit {
                background-color: #ffffff;
                border: 1px solid #ccc;
                font-size: 16px;
                font-weight: normal;
                padding: 15px;
                border-radius: 10px;
            }
            """

header_style = """
            QLabel {
                font-size: 20px;
                font-weight: bold;
                margin-bottom: 10px;
            }
            """

cancel_btn_style = """
            QPushButton {
                background-color: #ffffff;
                color: black;
                border: none;
                padding: 10px 20px;
                border-radius: 10px;
                font-size: 16px;
            }
            QPushButton:hover {
                background-color: #f7f7f7;
            }
            QPushButton:pressed {
                background-color: #f7f7f7;
            }
            """

save_btn_style = """
            QPushButton {
                background-color: #ffffff;
                color: black;
                border: none;
                padding: 10px 20px;
                border-radius: 10px;
                font-size: 16px;
            }
            QPushButton:hover {
                background-color: #f7f7f7;
            }
            QPushButton:pressed {
                background-color: #f7f7f7;
            }
            """
            
radio_btn_style =  """
                QRadioButton {
                    background-color: none;
                    color: black;
                    font-size: 16px;
                    font-weight: normal;
                    padding: 10px;
                }
                QRadioButton::indicator {
                    width: 20px;
                    height: 20px;
                }
                QRadioButton::indicator::unchecked {
                    image: url(./static/images/circle.svg);
                }
                QRadioButton::indicator::checked {
                    image: url(./static/images/circle-check.svg);
                }
                QRadioButton::checked {
                    color: green;
                }
                """


class QuizDialog(QDialog):
    def __init__(self, quiz=None, parent=None, on_submit=None, dialog_type: str = "edit"):
        super().__init__(parent)
        self.setWindowTitle(dialog_type.capitalize() + " Quiz")
        self.setFixedSize(400, 500)
        self.setStyleSheet("background-color: #f7f7f7;")
        self.setModal(True)
        self.quiz = quiz
        self.on_submit = on_submit
        layout = QVBoxLayout(self)
        layout.setSpacing(5)
        # layout.setContentsMargins(10, 10, 10, 10)

        # Title Input
        question_header = QLabel("Question:")
        question_header.setStyleSheet(header_style)
        layout.addWidget(question_header)
        self.title_input = QLineEdit(self.quiz["question"] if self.quiz else "")
        self.title_input.setStyleSheet(input_style)
        layout.addWidget(self.title_input)

        # Questions List
        choice_header = QLabel("Choices:")
        choice_header.setStyleSheet(header_style)
        layout.addWidget(choice_header)

        # Create button group for radio buttons
        self.answer_group = QButtonGroup(self)

        # Choice 1 with radio button
        choice1_layout = QHBoxLayout()
        self.choice_1 = QLineEdit(self.quiz["choices"][0]["choice"] if self.quiz else "")
        self.choice_1.setStyleSheet(input_style)
        self.radio_1 = QRadioButton()
        self.radio_1.setStyleSheet(radio_btn_style)
        self.radio_1.setChecked(self.quiz["choices"][0]["is_answer"] if self.quiz else False)
        self.answer_group.addButton(self.radio_1)
        choice1_layout.addWidget(self.choice_1)
        choice1_layout.addWidget(self.radio_1)
        layout.addLayout(choice1_layout)

        # Choice 2 with radio button
        choice2_layout = QHBoxLayout()
        self.choice_2 = QLineEdit(self.quiz["choices"][1]["choice"] if self.quiz else "")
        self.choice_2.setStyleSheet(input_style)
        self.radio_2 = QRadioButton()
        self.radio_2.setStyleSheet(radio_btn_style)
        self.radio_2.setChecked(self.quiz["choices"][1]["is_answer"] if self.quiz else False)
        self.answer_group.addButton(self.radio_2)
        choice2_layout.addWidget(self.choice_2)
        choice2_layout.addWidget(self.radio_2)
        layout.addLayout(choice2_layout)

        # Choice 3 with radio button
        choice3_layout = QHBoxLayout()
        self.choice_3 = QLineEdit(self.quiz["choices"][2]["choice"] if self.quiz else "")
        self.choice_3.setStyleSheet(input_style)
        self.radio_3 = QRadioButton()
        self.radio_3.setStyleSheet(radio_btn_style)
        self.radio_3.setChecked(self.quiz["choices"][2]["is_answer"] if self.quiz else False)
        self.answer_group.addButton(self.radio_3)
        choice3_layout.addWidget(self.choice_3)
        choice3_layout.addWidget(self.radio_3)
        layout.addLayout(choice3_layout)

        # Choice 4 with radio button
        choice4_layout = QHBoxLayout()
        self.choice_4 = QLineEdit(self.quiz["choices"][3]["choice"] if self.quiz else "")
        self.choice_4.setStyleSheet(input_style)
        self.radio_4 = QRadioButton()
        self.radio_4.setStyleSheet(radio_btn_style)
        self.radio_4.setChecked(self.quiz["choices"][3]["is_answer"] if self.quiz else False)
        self.answer_group.addButton(self.radio_4)
        choice4_layout.addWidget(self.choice_4)
        choice4_layout.addWidget(self.radio_4)
        layout.addLayout(choice4_layout)

        # Save & Cancel Buttons
        btn_layout = QHBoxLayout()
        self.save_btn = QPushButton("Save")
        self.save_btn.setStyleSheet(save_btn_style)
        self.save_btn.clicked.connect(lambda: self.on_submit(self.get_quiz_data()))
        self.cancel_btn = QPushButton("Cancel")
        self.cancel_btn.setStyleSheet(cancel_btn_style)
        self.cancel_btn.clicked.connect(self.reject)
        btn_layout.addWidget(self.cancel_btn)
        btn_layout.addWidget(self.save_btn)
        layout.addLayout(btn_layout)

    def add_question(self):
        text = self.new_question_input.text().strip()
        if text:
            self.question_list.addItem(text)
            self.new_question_input.clear()
        else:
            QMessageBox.warning(self, "Warning", "Question cannot be empty.")

    def remove_question(self):
        selected_items = self.question_list.selectedItems()
        if selected_items:
            for item in selected_items:
                self.question_list.takeItem(self.question_list.row(item))
        else:
            QMessageBox.warning(self, "Warning", "Select a question to remove.")

    def get_quiz_data(self):
        return {
            "question": self.title_input.text(),
            "choices": [
                {
                    "choice": self.choice_1.text(),
                    "is_answer": self.radio_1.isChecked()
                },
                {
                    "choice": self.choice_2.text(),
                    "is_answer": self.radio_2.isChecked()
                },
                {
                    "choice": self.choice_3.text(),
                    "is_answer": self.radio_3.isChecked()
                },
                {
                    "choice": self.choice_4.text(),
                    "is_answer": self.radio_4.isChecked()
                }
            ]
        }
