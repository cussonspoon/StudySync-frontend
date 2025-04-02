from PySide6.QtWidgets import (
    QApplication,
    QMainWindow,
    QWidget,
    QLabel,
    QPushButton,
    QVBoxLayout,
    QHBoxLayout,
    QScrollArea,
    QFrame,
    QLineEdit,
    QMenu,
)
from PySide6.QtCore import Qt, QSize
from PySide6.QtGui import QPixmap, QAction, QIcon
import sys
from PySide6.QtWidgets import QDialog, QButtonGroup
from PySide6.QtGui import QFont


class Tag(QFrame):
    def __init__(self, name, color, removable=False):
        super().__init__()
        self.setFixedWidth(100)
        self.setStyleSheet(
            f"background-color: {color}; border-radius: 5px; padding: 3px;"
        )
        layout = QHBoxLayout(self)
        layout.setContentsMargins(5, 0, 5, 0)

        label = QLabel(name)
        label.setStyleSheet("font-size: 12px;")
        label.setAlignment(Qt.AlignCenter)
        layout.addWidget(label)

        if removable:
            remove_btn = QPushButton("x")
            remove_btn.setFixedSize(16, 16)
            remove_btn.setStyleSheet("border: none; color: black;")
            remove_btn.clicked.connect(self.deleteLater)
            layout.addWidget(remove_btn)


class FolderDetailPage(QWidget):
    def __init__(self):
        super().__init__()

        # === Scroll Area ===
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)

        content = QWidget()
        self.main_layout = QVBoxLayout(content)
        self.main_layout.setAlignment(Qt.AlignTop)
        scroll.setWidget(content)

        # === Banner ===
        banner = QFrame()
        banner.setStyleSheet("background-color: lightgray; border-radius: 10px;")
        banner.setFixedHeight(250)
        banner_layout = QVBoxLayout(banner)
        banner_layout.setSpacing(0)  # Reduce spacing between elements
        banner_layout.setContentsMargins(
            20, 60, 20, 20
        )  # Add top margin to center content

        self.folder_name = QLabel("📁 Folder Name")
        self.folder_name.setStyleSheet("font-size: 24px; font-weight: bold;")
        self.folder_name.setAlignment(Qt.AlignCenter)

        created_label = QLabel("Created Thursday, January 30, 2025")
        created_label.setAlignment(Qt.AlignCenter)

        upload_btn = QPushButton("📷 Upload image")
        upload_btn.setFixedSize(130, 30)
        upload_btn.setStyleSheet(
            "background-color: gray; color: white; border-radius: 5px;"
        )

        banner_layout.addWidget(self.folder_name)
        banner_layout.addWidget(created_label)
        banner_layout.addWidget(upload_btn, alignment=Qt.AlignRight)

        # Create a widget to hold all content cards
        self.content_area = QWidget()
        self.content_layout = QVBoxLayout(self.content_area)
        self.content_layout.setAlignment(Qt.AlignTop)
        self.content_layout.setSpacing(5)

        # === Owner & Collaborators ===
        owner_label = QLabel("Owner")
        owner_tag = Tag("Arhway", "#FBC490")

        self.main_layout.addSpacing(20)

        collaborator_label = QLabel("Collaborators")
        collaborator_layout = QHBoxLayout()
        collaborator_layout.setContentsMargins(0, 0, 0, 0)
        self.collaborators = []

        # Example collaborators
        for name, color in [("John", "#A9DFBF"), ("Jake", "#AED6F1")]:
            tag = Tag(name, color, removable=True)
            collaborator_layout.addWidget(tag)
            self.collaborators.append(tag)

        collaborator_layout.addStretch()

        # Visibility and Action Buttons Row
        visibility_row = QHBoxLayout()
        visibility = QLabel("Visibility: Private")
        visibility_row.addWidget(visibility)
        visibility_row.addStretch()  # Push buttons to the right

        # Action buttons
        self.action_btn = QPushButton("⋮")
        self.action_btn.setFixedSize(40, 40)
        self.action_btn.setStyleSheet(
            """
            QPushButton {
                background-color: #F0F0F0;
                border-radius: 5px;
                font-size: 20px;
            }
            QPushButton:hover {
                background-color: #E0E0E0;
            }
        """
        )
        self.action_menu = QMenu()
        self.action_menu.addAction("Add collaborator")
        self.action_menu.addAction("Change to public")
        self.action_btn.setMenu(self.action_menu)

        plus_btn = QPushButton("+")
        plus_btn.setFixedSize(40, 40)
        plus_btn.setStyleSheet(
            """
            QPushButton {
                background-color: #F0F0F0;
                border-radius: 5px;
                font-size: 24px;
            }
            QPushButton:hover {
                background-color: #E0E0E0;
            }
        """
        )

        visibility_row.addWidget(self.action_btn)
        visibility_row.addWidget(plus_btn)
        plus_btn.clicked.connect(self.show_create_dialog)

        # Add to main layout
        self.main_layout.addWidget(banner)
        self.main_layout.addSpacing(20)
        self.main_layout.addWidget(owner_label)
        self.main_layout.addWidget(owner_tag)
        self.main_layout.addWidget(collaborator_label)
        self.main_layout.addLayout(collaborator_layout)
        self.main_layout.addLayout(visibility_row)
        self.main_layout.addWidget(self.content_area)  # Add content area last

        # === Overall Layout ===
        layout = QVBoxLayout(self)
        layout.addWidget(scroll)

    def add_collaborator(self):
        # Simple example to add collaborator
        tag = Tag(f"User{len(self.collaborators)+1}", "#D5F5E3", removable=True)
        self.collaborators.append(tag)
        # Add to the collaborator layout
        collaborator_layout = self.findChild(QHBoxLayout)
        if collaborator_layout:
            collaborator_layout.insertWidget(len(self.collaborators) - 1, tag)

    def show_create_dialog(self):
        dialog = CreateModeDialog(self)
        dialog.exec()


class CreateModeDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Select Modes")
        self.setFixedSize(300, 300)
        self.setStyleSheet(
            """
            QDialog { background-color: #eaeaea; border-radius: 10px; }
            QPushButton {
                border: none;
                padding: 8px;
                font-size: 16px;
                border-radius: 6px;
            }
            QPushButton#modeBtn {
                background-color: white;
            }
            QPushButton#modeBtn:checked {
                background-color: #A9DFBF;
            }
            QPushButton#createBtn {
                background-color: #A9DFBF;
            }
        """
        )

        layout = QVBoxLayout(self)
        layout.setAlignment(Qt.AlignTop)

        title = QLabel("Select Modes")
        title.setFont(QFont("Arial", 14, QFont.Bold))
        title.setAlignment(Qt.AlignCenter)

        self.name_input = QLineEdit()
        self.name_input.setPlaceholderText("📝 Enter name...")
        self.name_input.setFixedHeight(30)
        self.name_input.setStyleSheet("border-radius: 5px; padding: 5px;")

        # Mode Buttons
        self.mode_group = QButtonGroup()
        modes_layout = QVBoxLayout()

        self.mode_buttons = {}
        for mode in ["📄 Note", "🗂️ Flashcard", "❓ Quiz"]:
            btn = QPushButton(mode)
            btn.setObjectName("modeBtn")
            btn.setCheckable(True)
            self.mode_group.addButton(btn)
            modes_layout.addWidget(btn)
            self.mode_buttons[mode] = btn

        create_btn = QPushButton("✅ Create")
        create_btn.setObjectName("createBtn")
        create_btn.setFixedWidth(100)
        create_btn.clicked.connect(self.create_content)

        layout.addWidget(title)
        layout.addWidget(self.name_input)
        layout.addLayout(modes_layout)
        layout.addWidget(create_btn, alignment=Qt.AlignCenter)

    def create_content(self):
        name = self.name_input.text()
        if not name:
            return

        selected_button = self.mode_group.checkedButton()
        if not selected_button:
            return

        mode = selected_button.text()
        parent = self.parent()

        # Create new content card
        content_card = QLabel()
        content_card.setFixedHeight(50)
        content_card.setStyleSheet(
            "background-color: #F2F2F2; border-radius: 5px; padding: 10px; margin: 5px 0px;"
        )

        # Set content based on mode
        if "Note" in mode:
            content_card.setText(f"{name}")
        elif "Flashcard" in mode:
            content_card.setText(f"{name} - 0 terms")
        elif "Quiz" in mode:
            content_card.setText(f"{name} - 0 Questions")

        # Insert at the top of the content area
        parent.content_layout.insertWidget(0, content_card)

        self.accept()


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Folder Detail")
        self.setMinimumSize(1000, 700)
        self.setCentralWidget(FolderDetailPage())


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
