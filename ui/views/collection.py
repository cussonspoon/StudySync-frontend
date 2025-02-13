from PySide6.QtWidgets import QWidget, QLabel, QVBoxLayout

class CollectionPage(QWidget):
    
    def __init__(self):
        super().__init__()
        self.setupUi()

    def setupUi(self):
        layout = QVBoxLayout()
        self.label = QLabel("Welcome to Collection Page!")
        layout.addWidget(self.label)
        self.setLayout(layout)
