# main.py
from PySide6.QtWidgets import QApplication, QMainWindow
from ui.views.main_window import Ui_MainWindow
from controllers.window_controller import WindowController
import sys

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        # Controller
        self.controller = WindowController(self.ui)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
