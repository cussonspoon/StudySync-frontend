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
    QSizePolicy,
)
from PySide6.QtCore import Qt, QSize
from PySide6.QtGui import QPixmap, QAction, QIcon
import sys
from PySide6.QtWidgets import QDialog, QButtonGroup
from PySide6.QtGui import QFont
from .components.mode_card import ContentCard
from .components.note_window import popup_notewindow


class Tag(QFrame):
    def __init__(self, name, color, removable=False):
        super().__init__()
        self.setFixedWidth(100)
        self.setStyleSheet(
            f"background-color: {color}; border-radius: 5px; padding: 3px;"
        )
        self.setSizePolicy(QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Fixed)

        layout = QHBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)

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

        self.setStyleSheet(
            """
            QWidget {
                background-color: #FAFAFA;
                color: black;
            }
            QLabel {
                color: black;
            }
            QScrollArea {
                border: none;
            }
            """
        )

        # Create main horizontal layout to hold content
        main_horizontal_layout = QHBoxLayout(self)
        # main_horizontal_layout.setContentsMargins(10, 10, 10, 10)
        main_horizontal_layout.setSpacing(0)

        content_widget = QWidget()
        content_widget.setFixedWidth(1190)

        # Move existing main_layout to content_widget
        self.main_layout = QVBoxLayout(content_widget)
        # self.main_layout.setContentsMargins(10, 10, 10, 10)
        self.main_layout.setSpacing(2)

        # === Scroll Area ===
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setWidget(content_widget)  # Changed to use content_widget directly
        scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)

        # Add scroll area to main horizontal layout
        main_horizontal_layout.addWidget(scroll)

        # === Banner ===
        banner = QFrame()
        banner.setStyleSheet("background-color: lightgray; border-radius: 10px;")
        banner.setFixedHeight(250)
        banner_layout = QVBoxLayout(banner)
        banner_layout.setSpacing(0)
        banner_layout.setContentsMargins(10, 10, 10, 10)

        self.folder_name = QLabel("📁 Folder Name")
        self.folder_name.setStyleSheet(
            """
            QLabel {
                font-size: 24px;
                font-weight: bold;
                color: black;
                margin-top: 40px;
                margin-bottom: 0px;
                margin-left: 0px;
                margin-right: 0px;
            }
            """
        )
        self.folder_name.setAlignment(Qt.AlignCenter)

        created_label = QLabel("Created Thursday, January 30, 2025")
        created_label.setStyleSheet("color: black;")
        created_label.setAlignment(Qt.AlignCenter)

        upload_btn = QPushButton("📷 Upload image")
        upload_btn.setFixedSize(130, 30)
        upload_btn.setStyleSheet(
            "background-color: gray; color: white; border-radius: 5px;"
        )

        banner_layout.addWidget(self.folder_name)
        banner_layout.addWidget(created_label)
        banner_layout.addWidget(upload_btn, alignment=Qt.AlignRight)

        # Add banner to main layout
        self.main_layout.addWidget(banner)

        # Create a widget to hold all content cards
        self.content_area = QWidget()
        self.content_layout = QVBoxLayout(self.content_area)
        self.content_layout.setAlignment(Qt.AlignTop)
        # self.content_layout.setSpacing(5)

        # === Information Section ===
        info_section = QWidget()
        info_layout = QVBoxLayout(info_section)
        info_layout.setSpacing(10)
        info_layout.setContentsMargins(0, 0, 0, 0)

        # === Owner & Collaborators ===
        owner_label = QLabel("Owner")
        owner_label.setStyleSheet("color: black;")
        owner_tag = Tag("Arhway", "#FBC490")

        collaborator_label = QLabel("Collaborators")
        collaborator_label.setStyleSheet("color: black;")
        collaborator_layout = QHBoxLayout()
        collaborator_layout.setContentsMargins(0, 0, 0, 0)
        collaborator_layout.setSpacing(0)
        self.collaborators = []

        # Example collaborators
        for name, color in [("John", "#A9DFBF"), ("Jake", "#AED6F1")]:
            tag = Tag(name, color, removable=True)
            collaborator_layout.addWidget(tag)
            self.collaborators.append(tag)

        collaborator_layout.addStretch()

        # Visibility and Action Buttons Row
        visibility_row = QHBoxLayout()
        visibility_row.setContentsMargins(0, 5, 0, 5)
        visibility = QLabel("Visibility: Private")
        visibility.setStyleSheet("color: black;")
        visibility_row.addWidget(visibility)
        visibility_row.addStretch()

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

        # Add all components to info layout
        info_layout.addWidget(owner_label)
        info_layout.addWidget(owner_tag)
        info_layout.addSpacing(5)
        info_layout.addWidget(collaborator_label)
        info_layout.addLayout(collaborator_layout)
        info_layout.addSpacing(5)
        info_layout.addLayout(visibility_row)

        # Add info section to main layout
        self.main_layout.addWidget(info_section)
        self.main_layout.addWidget(self.content_area)

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

    def set_back_callback(self, callback):
        self.back_btn.clicked.connect(callback)


# class ContentCard(QFrame):
#     def __init__(self, name, mode, parent=None):
#         super().__init__(parent)
#         self.setFixedHeight(100)
#         self.setStyleSheet(
#             """
#             QFrame {
#                 background-color: white;
#                 border: 0px solid #E0E0E0;
#                 border-radius: 8px;
#             }
#             QLabel {
#                 color: black;
#                 background: transparent;
#             }
#             """
#         )

#         # Create horizontal layout for the card
#         card_layout = QHBoxLayout(self)
#         card_layout.setContentsMargins(10, 10, 10, 10)
#         card_layout.setSpacing(15)

#         # Add icon/image placeholder
#         icon = QLabel()
#         icon.setFixedSize(80, 80)
#         icon.setStyleSheet("background-color: #E0E0E0; border-radius: 4px;")
#         card_layout.addWidget(icon)

#         # Create vertical layout for text content
#         text_layout = QVBoxLayout()
#         text_layout.setSpacing(2)

#         # Add title
#         title = QLabel(name.upper())
#         title.setStyleSheet("font-size: 16px; font-weight: bold;")
#         text_layout.addWidget(title)

#         # Add subtitle based on mode
#         if "Note" in mode:
#             subtitle = QLabel("Note")
#         elif "Flashcard" in mode:
#             subtitle = QLabel("Flashcard set - 0 terms")
#         elif "Quiz" in mode:
#             subtitle = QLabel("Quiz - 0 Questions")
#         subtitle.setStyleSheet("font-size: 14px; color: #666666;")
#         text_layout.addWidget(subtitle)

#         # Add "by User"
#         by_user = QLabel("by User")
#         by_user.setStyleSheet("font-size: 12px; color: #666666;")
#         text_layout.addWidget(by_user)

#         # Add text layout to card
#         card_layout.addLayout(text_layout)
#         card_layout.addStretch()


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

        # Create new content card using ContentCard class
        content_card = ContentCard(name, mode, parent)

        # Insert at the top of the content area
        parent.content_layout.insertWidget(0, content_card)

        # Show appropriate window based on mode
        if "Note" in mode:
            self.accept()  # Close the create dialog first
            note_dialog = popup_notewindow(parent)
            note_dialog.title_input.setPlainText(name)  # Set the title
            if note_dialog.exec():
                note_data = note_dialog.getNoteData()
                print("Note Data:", note_data)  # You can handle the note data here
        elif "Flashcard" in mode:
            pass
        elif "Quiz" in mode:
            pass
        else:
            self.accept()
