from PySide6.QtWidgets import QWidget, QLabel, QVBoxLayout

from ..components.quiz import Quiz


class CollectionPage(QWidget):

    def __init__(self):
        super().__init__()
        self.setupUi()

    def setupUi(self):
        layout = QVBoxLayout()
        self.label = QLabel("Welcome to Collection Page!")
        layout.addWidget(self.label)

        self.quiz = Quiz()

        layout.addWidget(self.quiz)

        self.setLayout(layout)
