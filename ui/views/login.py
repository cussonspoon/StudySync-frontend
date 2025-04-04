from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QLabel,
    QPushButton,
    QLineEdit,
    QFormLayout,
    QMessageBox,
    QStackedWidget,
)
from PySide6.QtCore import Qt, Signal
from PySide6.QtGui import QFont
from controllers.user_controller import UserController
from utils.global_vars import set_current_user


class LoginPage(QWidget):
    login_successful = Signal()  # Define the signal at the class level

    def __init__(self, parent=None):
        super().__init__(parent)
        self.user_controller = UserController()
        self.setup_ui()

    def setup_ui(self):
        """Sets up the login page UI."""
        self.layout = QVBoxLayout()
        self.layout.setAlignment(Qt.AlignCenter)
        self.layout.setSpacing(20)
        self.setLayout(self.layout)

        # Create stacked widget for login and register forms
        self.stacked_widget = QStackedWidget()
        self.layout.addWidget(self.stacked_widget)

        # Create login page
        self.login_page = QWidget()
        self.login_layout = QVBoxLayout()
        self.login_layout.setAlignment(Qt.AlignCenter)
        self.login_layout.setSpacing(20)
        self.login_page.setLayout(self.login_layout)

        # Title
        title = QLabel("StudySync")
        title.setFont(QFont("Arial", 24, QFont.Bold))
        title.setAlignment(Qt.AlignCenter)
        self.login_layout.addWidget(title)

        # Login form
        login_form = QFormLayout()
        login_form.setSpacing(10)
        login_form.setAlignment(Qt.AlignCenter)

        self.username_input = QLineEdit()
        self.username_input.setPlaceholderText("Username")
        self.username_input.setFixedWidth(300)
        login_form.addRow("Username:", self.username_input)

        self.password_input = QLineEdit()
        self.password_input.setPlaceholderText("Password")
        self.password_input.setEchoMode(QLineEdit.Password)
        self.password_input.setFixedWidth(300)
        login_form.addRow("Password:", self.password_input)

        self.login_layout.addLayout(login_form)

        # Login button container
        login_button_container = QWidget()
        login_button_layout = QVBoxLayout(login_button_container)
        login_button_layout.setAlignment(Qt.AlignCenter)

        self.login_button = QPushButton("Login")
        self.login_button.setFixedWidth(300)
        self.login_button.setStyleSheet(
            "padding: 10px; font-size: 16px; background-color: #4CAF50; color: white; border-radius: 5px;"
        )
        self.login_button.clicked.connect(self.handle_login)
        login_button_layout.addWidget(self.login_button)

        self.login_layout.addWidget(login_button_container)

        # Register link container
        register_link_container = QWidget()
        register_link_layout = QVBoxLayout(register_link_container)
        register_link_layout.setAlignment(Qt.AlignCenter)

        self.register_link = QPushButton("Don't have an account? Register")
        self.register_link.setStyleSheet("color: #4CAF50; border: none;")
        self.register_link.clicked.connect(self.show_register_form)
        register_link_layout.addWidget(self.register_link)

        self.login_layout.addWidget(register_link_container)

        # Create register page
        self.register_page = QWidget()
        self.register_layout = QVBoxLayout()
        self.register_layout.setAlignment(Qt.AlignCenter)
        self.register_layout.setSpacing(20)
        self.register_page.setLayout(self.register_layout)

        # Register title
        register_title = QLabel("Create Account")
        register_title.setFont(QFont("Arial", 24, QFont.Bold))
        register_title.setAlignment(Qt.AlignCenter)
        self.register_layout.addWidget(register_title)

        # Register form
        register_form = QFormLayout()
        register_form.setSpacing(10)
        register_form.setAlignment(Qt.AlignCenter)

        self.register_username_input = QLineEdit()
        self.register_username_input.setPlaceholderText("Username")
        self.register_username_input.setFixedWidth(300)
        register_form.addRow("Username:", self.register_username_input)

        self.register_password_input = QLineEdit()
        self.register_password_input.setPlaceholderText("Password")
        self.register_password_input.setEchoMode(QLineEdit.Password)
        self.register_password_input.setFixedWidth(300)
        register_form.addRow("Password:", self.register_password_input)

        self.register_layout.addLayout(register_form)

        # Register button container
        register_button_container = QWidget()
        register_button_layout = QVBoxLayout(register_button_container)
        register_button_layout.setAlignment(Qt.AlignCenter)

        self.register_button = QPushButton("Register")
        self.register_button.setFixedWidth(300)
        self.register_button.setStyleSheet(
            "padding: 10px; font-size: 16px; background-color: #4CAF50; color: white; border-radius: 5px;"
        )
        self.register_button.clicked.connect(self.handle_register)
        register_button_layout.addWidget(self.register_button)

        self.register_layout.addWidget(register_button_container)

        # Login link container
        login_link_container = QWidget()
        login_link_layout = QVBoxLayout(login_link_container)
        login_link_layout.setAlignment(Qt.AlignCenter)

        self.login_link = QPushButton("Already have an account? Login")
        self.login_link.setStyleSheet("color: #4CAF50; border: none;")
        self.login_link.clicked.connect(self.show_login_form)
        login_link_layout.addWidget(self.login_link)

        self.register_layout.addWidget(login_link_container)

        # Add pages to stacked widget
        self.stacked_widget.addWidget(self.login_page)
        self.stacked_widget.addWidget(self.register_page)

    def handle_login(self):
        """Handles the login process."""
        username = self.username_input.text()
        password = self.password_input.text()

        if not username or not password:
            QMessageBox.warning(
                self, "Error", "Please enter both username and password"
            )
            return

        try:
            user = self.user_controller.login(username, password)
            if user:
                # Store user data in global
                set_current_user(
                    {"id": user.id, "username": user.username, "email": user.email}
                )
                self.login_successful.emit()
            else:
                QMessageBox.warning(self, "Error", "Invalid username or password")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Login failed: {str(e)}")

    def handle_register(self):
        """Handles the registration process."""
        username = self.register_username_input.text()
        password = self.register_password_input.text()

        if not username or not password:
            QMessageBox.warning(
                self, "Error", "Please enter both username and password"
            )
            return

        try:
            user = self.user_controller.register(username, password)
            if user:
                # Store user data in global
                set_current_user(
                    {"id": user.id, "username": user.username, "email": user.email}
                )
                self.login_successful.emit()
            else:
                QMessageBox.warning(self, "Error", "Registration failed")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Registration failed: {str(e)}")

    def show_register_form(self):
        self.stacked_widget.setCurrentIndex(1)
        self.username_input.hide()
        self.password_input.hide()
        self.login_button.hide()
        self.register_link.hide()

    def show_login_form(self):
        self.stacked_widget.setCurrentIndex(0)
        self.username_input.show()
        self.password_input.show()
        self.login_button.show()
        self.register_link.show()
