import sys
from PySide6.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QTextEdit
from controllers.user_controller import UserController

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

        self.user_controller = UserController()
        self.user_controller.api_response_received.connect(self.show_response)
        self.user_controller.api_error_occurred.connect(self.show_error)

    def initUI(self):
        self.layout = QVBoxLayout()
        
        self.text_edit = QTextEdit(self)
        self.layout.addWidget(self.text_edit)
        
        self.button = QPushButton("Fetch User Data", self)
        self.button.clicked.connect(self.fetch_user)
        self.layout.addWidget(self.button)

        self.setLayout(self.layout)
        self.setWindowTitle("BaseController Example")

    def fetch_user(self):
        data = self.user_controller.fetch_user_data("bfe17006-c937-425d-a85b-e06b23ff2dc0")
        print("from test.py", data)
        self.user_controller.post_user()
    def show_response(self, response):
        self.text_edit.setText(response)

    def show_error(self, error):
        self.text_edit.setText(f"Error: {error}")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
