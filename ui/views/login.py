from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QLabel,
    QPushButton,
    QLineEdit,
    QFormLayout,
    QMessageBox,
    QStackedWidget,
    QFrame,
    QCheckBox,
    QDialog,
)
from PySide6.QtCore import Qt, Signal, QDir
from PySide6.QtGui import QFont, QPixmap
from controllers.user_controller import UserController
from utils.global_vars import set_current_user
from utils.session_manager import SessionManager

class LoginPage(QWidget):
    login_successful = Signal()

    def __init__(self):
        super().__init__()
        self.user_controller = UserController()
        self.session_manager = SessionManager.get_instance()
        self.setupUi()

    def setupUi(self):
        """Set up the login page UI."""
        # Main layout
        self.main_layout = QVBoxLayout(self)
        self.main_layout.setContentsMargins(0, 0, 0, 0)
        self.main_layout.setSpacing(0)

        # Create a container for the login form
        self.container = QFrame(self)
        self.container.setObjectName("loginContainer")
        self.container.setStyleSheet("""
            QFrame#loginContainer {
                background-color: #FAFAFA;
                border-radius: 20px;
                padding: 40px;
            }
        """)

        # Container layout
        self.container_layout = QVBoxLayout(self.container)
        self.container_layout.setSpacing(30)
        self.container_layout.setAlignment(Qt.AlignCenter)

        # Logo
        self.logo = QLabel(self.container)
        self.logo.setFixedSize(200, 200)
        img_path = QDir.currentPath() + "/static/images/logo.png"
        self.logo.setPixmap(QPixmap(img_path))
        self.logo.setStyleSheet("""
            QLabel#logo {
                background-color: #FAFAFA;
            }
        """)
        self.logo.setScaledContents(True)
        self.logo.setAlignment(Qt.AlignCenter)
        self.container_layout.addWidget(self.logo)

        # Title
        self.title = QLabel("Welcome to StudySync", self.container)
        self.title.setObjectName("loginTitle")
        self.title.setStyleSheet("""
            QLabel#loginTitle {
                font-size: 32px;
                font-weight: bold;
                color: #333;
                text-align: center;
                background-color: #FAFAFA;
            }
        """)
        self.container_layout.addWidget(self.title)

        # Subtitle
        self.subtitle = QLabel("Sign in to continue", self.container)
        self.subtitle.setObjectName("loginSubtitle")
        self.subtitle.setStyleSheet("""
            QLabel#loginSubtitle {
                font-size: 16px;
                color: #666;
                text-align: center;
                background-color: #FAFAFA;
            }
        """)
        self.container_layout.addWidget(self.subtitle)

        # Form layout
        self.form_layout = QVBoxLayout()
        self.form_layout.setSpacing(20)

        # Username input
        self.username_input = QLineEdit(self.container)
        self.username_input.setObjectName("usernameInput")
        self.username_input.setPlaceholderText("Username")
        self.username_input.setStyleSheet("""
            QLineEdit#usernameInput {
                padding: 15px;
                border: 2px solid #E0E0E0;
                border-radius: 10px;
                font-size: 16px;
                color: black;
                background-color: #FAFAFA;
            }
            QLineEdit#usernameInput:focus {
                border-color: #4A90E2;
                background-color: white;
                color: black;
            }
        """)
        self.form_layout.addWidget(self.username_input)

        # Password input
        self.password_input = QLineEdit(self.container)
        self.password_input.setObjectName("passwordInput")
        self.password_input.setPlaceholderText("Password")
        self.password_input.setEchoMode(QLineEdit.Password)
        self.password_input.setStyleSheet("""
            QLineEdit#passwordInput {
                padding: 15px;
                border: 2px solid #E0E0E0;
                border-radius: 10px;
                font-size: 16px;
                background-color: #FAFAFA;
                color: black;
            }
            QLineEdit#passwordInput:focus {
                border-color: #4A90E2;
                background-color: white;
                color: black;
            }
        """)
        self.form_layout.addWidget(self.password_input)

        # Login button
        self.login_button = QPushButton("Sign In", self.container)
        self.login_button.setObjectName("loginButton")
        self.login_button.setStyleSheet("""
            QPushButton#loginButton {
                background-color: #4A90E2;
                color: white;
                border: none;
                border-radius: 10px;
                padding: 15px;
                font-size: 16px;
                font-weight: bold;
            }
            QPushButton#loginButton:hover {
                background-color: #357ABD;
            }
            QPushButton#loginButton:pressed {
                background-color: #2C6AA3;
            }
        """)
        self.login_button.clicked.connect(self.handle_login)
        self.form_layout.addWidget(self.login_button)

        # Register link
        self.register_link = QPushButton("Don't have an account? Sign up", self.container)
        self.register_link.setObjectName("registerLink")
        self.register_link.setStyleSheet("""
            QPushButton#registerLink {
                background-color: transparent;
                color: #4A90E2;
                border: none;
                font-size: 14px;
            }
            QPushButton#registerLink:hover {
                color: #357ABD;
                text-decoration: underline;
            }
        """)
        self.register_link.clicked.connect(self.show_register_dialog)
        self.form_layout.addWidget(self.register_link, alignment=Qt.AlignCenter)

        self.container_layout.addLayout(self.form_layout)
        self.main_layout.addWidget(self.container, alignment=Qt.AlignCenter)

        # Set background
        self.setStyleSheet("""
            QWidget {
                background-color: #F8F6F1;
            }
        """)

    def handle_login(self):
        """Handle login button click."""
        username = self.username_input.text()
        password = self.password_input.text()


        try:
            # Attempt login using UserController
            user = self.user_controller.login(username, password)

            if user:
                self.session_manager.set_current_user(user)
                # Login successful
                # Debug print to check user attributes
                print(
                    f"User ID: {user.id}, Username: {user.username}, Email: {getattr(user, 'email', 'N/A')}"
                )
                # Store user data in global, handle missing email
                set_current_user(
                    {
                        "id": user.id,
                        "username": user.username,
                        "email": getattr(
                            user, "email", "N/A"
                        ),  # Use 'N/A' if email is missing
                    }
                )
                self.login_successful.emit()
            else:
                # Show error message
                QMessageBox.warning(self, "Login Failed", "Invalid username or password")
        except Exception as e:
            # Show error message
            QMessageBox.warning(self, "Error", str(e))

    def show_register_dialog(self):
        """Show the register dialog."""
        dialog = RegisterDialog(self)
        if dialog.exec():
            # Registration successful, attempt login
            self.username_input.setText(dialog.username_input.text())
            self.password_input.setText(dialog.password_input.text())
            self.handle_login()

class RegisterDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.user_controller = UserController()
        self.setupUi()

    def setupUi(self):
        """Set up the register dialog UI."""
        self.setWindowTitle("Create Account")
        self.setFixedSize(400, 450)  # Reduced height since we removed the terms checkbox
        self.setStyleSheet("""
            QDialog {
                background-color: #FAFAFA;
            }
        """)

        # Main layout
        self.main_layout = QVBoxLayout(self)
        self.main_layout.setContentsMargins(40, 40, 40, 40)
        self.main_layout.setSpacing(30)

        # Title
        self.title = QLabel("Create Account", self)
        self.title.setObjectName("registerTitle")
        self.title.setStyleSheet("""
            QLabel#registerTitle {
                font-size: 24px;
                font-weight: bold;
                color: #333;
                text-align: center;
                background-color: #FAFAFA;
            }
        """)
        self.main_layout.addWidget(self.title)

        # Subtitle
        self.subtitle = QLabel("Join StudySync today", self)
        self.subtitle.setObjectName("registerSubtitle")
        self.subtitle.setStyleSheet("""
            QLabel#registerSubtitle {
                font-size: 16px;
                color: #666;
                text-align: center;
                background-color: #FAFAFA;
            }
        """)
        self.main_layout.addWidget(self.subtitle)

        # Form layout
        self.form_layout = QVBoxLayout()
        self.form_layout.setSpacing(5)
        self.form_layout.setAlignment(Qt.AlignCenter)
        self.form_layout.setContentsMargins(0, 0, 0, 0)

        # Username input
        self.username_input = QLineEdit(self)
        self.username_input.setObjectName("usernameInput")
        self.username_input.setPlaceholderText("Username")
        self.username_input.setStyleSheet("""
            QLineEdit#usernameInput {
                padding: 15px;
                border: 2px solid #E0E0E0;
                border-radius: 10px;
                font-size: 16px;
                background-color: #FAFAFA;
            }
            QLineEdit#usernameInput:focus {
                border-color: #4A90E2;
                background-color: white;
            }
        """)
        self.form_layout.addWidget(self.username_input)

        # Password input
        self.password_input = QLineEdit(self)
        self.password_input.setObjectName("passwordInput")
        self.password_input.setPlaceholderText("Password")
        self.password_input.setEchoMode(QLineEdit.Password)
        self.password_input.setStyleSheet("""
            QLineEdit#passwordInput {
                padding: 15px;
                border: 2px solid #E0E0E0;
                border-radius: 10px;
                font-size: 16px;
                background-color: #FAFAFA;
            }
            QLineEdit#passwordInput:focus {
                border-color: #4A90E2;
                background-color: white;
            }
        """)
        self.form_layout.addWidget(self.password_input)

        # Confirm password input
        self.confirm_password_input = QLineEdit(self)
        self.confirm_password_input.setObjectName("confirmPasswordInput")
        self.confirm_password_input.setPlaceholderText("Confirm Password")
        self.confirm_password_input.setEchoMode(QLineEdit.Password)
        self.confirm_password_input.setStyleSheet("""
            QLineEdit#confirmPasswordInput {
                padding: 15px;
                border: 2px solid #E0E0E0;
                border-radius: 10px;
                font-size: 16px;
                background-color: #FAFAFA;
            }
            QLineEdit#confirmPasswordInput:focus {
                border-color: #4A90E2;
                background-color: white;
            }
        """)
        self.form_layout.addWidget(self.confirm_password_input)

        self.main_layout.addLayout(self.form_layout)

        # Register button
        self.register_button = QPushButton("Create Account", self)
        self.register_button.setObjectName("registerButton")
        self.register_button.setStyleSheet("""
            QPushButton#registerButton {
                background-color: #4A90E2;
                color: white;
                border: none;
                border-radius: 10px;
                padding: 15px;
                font-size: 16px;
                font-weight: bold;
            }
            QPushButton#registerButton:hover {
                background-color: #357ABD;
            }
            QPushButton#registerButton:pressed {
                background-color: #2C6AA3;
            }
        """)
        self.register_button.clicked.connect(self.handle_register)
        self.main_layout.addWidget(self.register_button)

        # Login link
        self.login_link = QPushButton("Already have an account? Sign in", self)
        self.login_link.setObjectName("loginLink")
        self.login_link.setStyleSheet("""
            QPushButton#loginLink {
                background-color: transparent;
                color: #4A90E2;
                border: none;
                font-size: 14px;
            }
            QPushButton#loginLink:hover {
                color: #357ABD;
                text-decoration: underline;
            }
        """)
        self.login_link.clicked.connect(self.reject)
        self.main_layout.addWidget(self.login_link, alignment=Qt.AlignCenter)

    def handle_register(self):
        """Handle register button click."""
        username = self.username_input.text()
        password = self.password_input.text()
        confirm_password = self.confirm_password_input.text()

        # Validate inputs
        if not all([username, password, confirm_password]):
            QMessageBox.warning(self, "Error", "Please fill in all fields")
            return

        if password != confirm_password:
            QMessageBox.warning(self, "Error", "Passwords do not match")
            return

        try:
            # Attempt registration using UserController
            user = self.user_controller.register(username, password)

            if user:
                # Store user data in global
                set_current_user(
                    {"id": user.id, "username": user.username, "email": user.email}
                )
                self.login_successful.emit()
                # Registration successful
                self.accept()
            else:
                # Show error message
                QMessageBox.warning(self, "Registration Failed", "Failed to create account")
        except Exception as e:
            # Show error message
            QMessageBox.warning(self, "Error", str(e))
