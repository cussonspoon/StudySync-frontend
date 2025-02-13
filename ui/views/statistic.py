from PySide6.QtWidgets import QWidget, QLabel, QVBoxLayout

class StatPage(QWidget):

    def __init__(self):
        super().__init__()
        self.setupUi()

    def setupUi(self):
        layout = QVBoxLayout()
        self.label = QLabel("Welcome to Stat Page!")
        layout.addWidget(self.label)
        self.setLayout(layout)