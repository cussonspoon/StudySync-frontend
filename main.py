# main.py
import sys
from PySide6.QtWidgets import QApplication, QMainWindow, QStackedWidget, QWidget
from PySide6.QtCore import Qt

from ui.views.login import LoginPage
from ui.views.main_window import Ui_MainWindow
from controllers.window_controller import WindowController
from utils.session_manager import SessionManager

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Study Sync")
        self.setMinimumSize(1300, 831)
        self.setMaximumSize(1300, 831)

        # Create stacked widget for login and main UI
        self.stacked_widget = QStackedWidget()
        self.setCentralWidget(self.stacked_widget)

        # Create login page
        self.login_page = LoginPage()
        self.stacked_widget.addWidget(self.login_page)

        # Create main UI
        self.main_ui = QWidget()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self.main_ui)
        self.stacked_widget.addWidget(self.main_ui)

        # Connect signals
        self.login_page.login_successful.connect(self.handle_login_successful)
        self.ui.logout.clicked.connect(self.handle_logout)

        # Show login page first
        self.stacked_widget.setCurrentWidget(self.login_page)

        # Controller
        self.controller = WindowController(self.ui)

    def handle_login_successful(self):
        """Handles successful login by switching to the main UI."""
        self.stacked_widget.setCurrentWidget(self.main_ui)

    def handle_logout(self):
        """Handles logout by clearing the session and switching back to login page."""
        session_manager = SessionManager.get_instance()
        session_manager.clear_session()
        self.stacked_widget.setCurrentWidget(self.login_page)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
