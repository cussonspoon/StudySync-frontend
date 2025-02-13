# Entry point - initializes app, loads UI
import sys
from PySide6.QtWidgets import QApplication, QMainWindow
from ui.views.main_window import Ui_MainWindow  # Import the generated UI class


def apply_stylesheet(app, stylesheet_path="./static/styles/style.qss"):
    """Load and apply the QSS file."""
    with open(stylesheet_path, "r") as file:
        qss = file.read()
        app.setStyleSheet(qss)

class MainApp(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)  # Load the UI

if __name__ == "__main__":
    app = QApplication(sys.argv)
    apply_stylesheet(app)  # Apply QSS
    window = MainApp()
    window.show()
    sys.exit(app.exec())