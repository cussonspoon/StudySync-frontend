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

from services.folder_service import FolderService
from services.quiz_service import QuizService
from .components.mode_card import ContentCard
from .components.note_window import popup_notewindow
from .components.quiz_window import popup_quizwindow
from models.quiz import Quiz
from services.note_service import NoteService


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
        self.items = []
        self.folder_id = None
        self.folder_total_items = None
        self.folder_created_at = None
        self.folder_img_url = None

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
        main_horizontal_layout.setSpacing(0)
        main_horizontal_layout.setContentsMargins(0, 0, 0, 0)  # Remove margins

        content_widget = QWidget()
        content_widget.setMinimumWidth(
            1209
        )  # Set to available space (MainWindow width - sidebar width)
        content_widget.setSizePolicy(
            QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding
        )  # Allow widget to expand

        # Move existing main_layout to content_widget
        self.main_layout = QVBoxLayout(content_widget)
        self.main_layout.setSpacing(2)
        self.main_layout.setContentsMargins(20, 10, 20, 10)  # Add some padding

        # === Scroll Area ===
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setWidget(content_widget)
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

        self.created_label = QLabel("")  # Store as instance variable
        self.created_label.setStyleSheet("color: black;")
        self.created_label.setAlignment(Qt.AlignCenter)

        upload_btn = QPushButton("📷 Upload image")
        upload_btn.setFixedSize(130, 30)
        upload_btn.setStyleSheet(
            "background-color: gray; color: white; border-radius: 5px;"
        )

        banner_layout.addWidget(self.folder_name)
        banner_layout.addWidget(self.created_label)
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

    def load_items(self):
        print(f"Loading items for folder ID: {self.folder_id}")  # Debug print
        # Clear existing items from the content layout
        while self.content_layout.count():
            item = self.content_layout.takeAt(0)
            if item.widget():
                item.widget().deleteLater()

        # Create a FolderService instance with None as initial folder data
        folder_service = FolderService(None)
        response = folder_service.fetch_items(self.folder_id)
        print(f"API Response: {response}")  # Debug print

        if not response:
            print("No response from API")  # Debug print
            return
        
        if not self.folder_id:
            print("Warning: No folder ID set!")
            return

        # Store all items for reference
        self.items = []

        # Load notes
        try:
            note_service = NoteService()
            print(f"Attempting to load notes for folder: {self.folder_id}")
            notes = note_service.get_notes_by_folder(self.folder_id)
            print(f"Found {len(notes)} notes: {[note['name'] for note in notes]}")  # Debug print

            for note in notes:
                print(f"Adding note to UI: {note['name']}")  # Debug print
                self.items.append(note)  # Store note data
                card = ContentCard(
                    name=note["name"], 
                    mode="📄 Note", 
                    item_data=note, 
                    parent=self
                )
                card.clicked.connect(self.handle_item_click)
                self.content_layout.addWidget(card)
        except Exception as e:
            print(f"Error loading notes: {e}")
            import traceback
            traceback.print_exc()

        # Load flashcards
        flashcards = response.get("flashcards", [])
        print(f"Found {len(flashcards)} flashcards")  # Debug print
        for flashcard in flashcards:
            self.items.append(flashcard)  # Store flashcard data
            card = ContentCard(
                name=flashcard["name"],
                mode="🗂️ Flashcard",
                item_data=flashcard,
                parent=self,
            )
            card.clicked.connect(self.handle_item_click)
            self.content_layout.addWidget(card)

        # Load quizzes
        quizzes = response.get("quizzes", [])
        print(f"Found {len(quizzes)} quizzes")  # Debug print
        for quiz in quizzes:
            self.items.append(quiz)  # Store quiz data
            card = ContentCard(
                name=quiz["title"],  # Note: quizzes use 'title' instead of 'name'
                mode="❓ Quiz",
                item_data=quiz,
                parent=self,
            )
            card.clicked.connect(self.handle_item_click)
            self.content_layout.addWidget(card)

        # Update the total items count
        self.folder_total_items = len(notes) + len(flashcards) + len(quizzes)
        print(f"Total items: {self.folder_total_items}")  # Debug print

    def handle_item_click(self, name, mode):
        """Handle clicks on content cards"""
        print(f"Opening {mode} item: {name}")

        # Find the item data
        item_data = next(
            (
                item
                for item in self.items
                if item.get("name", item.get("title")) == name
            ),
            None,
        )

        if not item_data:
            print(f"Could not find data for item: {name}")
            return

        if "Note" in mode:
            note_dialog = popup_notewindow(self)

            # Set window title to note name
            note_dialog.setWindowTitle(name)

            # Set note content
            note_dialog.title_input.setPlainText(name)
            note_dialog.content_input.setHtml(item_data.get("content", ""))

            # Store note ID and folder ID for updates
            note_dialog.note_id = item_data.get("id")
            note_dialog.folder_id = self.folder_id

            # Connect text change signals for auto-save
            note_dialog.title_input.textChanged.connect(
                lambda: self.handle_note_change(note_dialog)
            )
            note_dialog.content_input.textChanged.connect(
                lambda: self.handle_note_change(note_dialog)
            )

            # Show the dialog
            note_dialog.exec()

        elif "Quiz" in mode:
            # Create Quiz object from existing data
            quiz = Quiz(
                id=item_data.get("id", ""),
                title=item_data.get("title", ""),
                quiz_type=item_data.get("quiz_type", "multiple"),
                mode=item_data.get("mode", "normal"),
            )
            # Open quiz editor with existing quiz
            quiz_dialog = popup_quizwindow(self, quiz=quiz)
            if quiz_dialog.exec():
                quiz_data = quiz_dialog.getQuizData()
                print(f"Quiz Data: {quiz_data}")
                self.load_items()  # Refresh after edit

        elif "Flashcard" in mode:
            # TODO: Implement flashcard handling
            pass

    def handle_note_change(self, note_dialog):
        """Handle auto-save with delay when note content changes"""
        # Cancel any existing timer
        if hasattr(self, "_save_timer"):
            self._save_timer.stop()

        # Create new timer for delayed save
        from PySide6.QtCore import QTimer

        self._save_timer = QTimer()
        self._save_timer.setSingleShot(True)
        self._save_timer.timeout.connect(lambda: self.save_note_changes(note_dialog))
        self._save_timer.start(1000)  # 1 second delay

    def save_note_changes(self, note_dialog):
        """Save note changes to file"""
        try:
            note_data = note_dialog.getNoteData()
            note_service = NoteService()
            updated_note = note_service.update_note(
                folder_id=note_dialog.folder_id,
                note_id=note_dialog.note_id,
                update_data={
                    "name": note_data["title"],
                    "content": note_data["content"],
                },
            )
            if updated_note:
                print(f"Auto-saved note: {updated_note['name']}")
        except Exception as e:
            print(f"Error auto-saving note: {e}")
            import traceback

            traceback.print_exc()

    def update_created_label(self):
        if self.folder_created_at:
            # Convert the ISO string to a more readable format
            from datetime import datetime

            try:
                date = datetime.fromisoformat(
                    self.folder_created_at.replace("Z", "+00:00")
                )
                formatted_date = date.strftime("%B %d, %Y")
                self.created_label.setText(f"Created on {formatted_date}")
            except Exception as e:
                print(f"Error formatting date: {e}")
                self.created_label.setText(f"Created on {self.folder_created_at}")


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
        folder_id = parent.folder_id

        if "Note" in mode:
            self.accept()  # Close the create dialog first
            note_dialog = popup_notewindow(parent)
            note_dialog.title_input.setPlainText(name)

            # Create initial note
            try:
                note_service = NoteService()
                created_note = note_service.create_note(
                    folder_id=folder_id,
                    name=name,
                    content="",  # Empty content initially
                )

                if created_note:
                    # Store note ID and folder ID for updates
                    note_dialog.note_id = created_note["id"]
                    note_dialog.folder_id = folder_id

                    # Connect text change signals for auto-save
                    note_dialog.title_input.textChanged.connect(
                        lambda: parent.handle_note_change(note_dialog)
                    )
                    note_dialog.content_input.textChanged.connect(
                        lambda: parent.handle_note_change(note_dialog)
                    )

                    if note_dialog.exec():
                        # Final save on dialog accept
                        parent.save_note_changes(note_dialog)
                        # Refresh the folder contents
                        parent.load_items()

            except Exception as e:
                print(f"Error creating note: {e}")
                import traceback

                traceback.print_exc()

        elif "Flashcard" in mode:
            pass
            # try:
            #     folder_service = FolderService(None)
            #     created_flashcard = folder_service.create_flashcard(folder_id, name)
            #     if created_flashcard:
            #         # Only add to UI if backend creation was successful
            #         card = ContentCard(name=name, mode="🗂️ Flashcard", parent=parent)
            #         parent.content_layout.insertWidget(0, card)
            # except Exception as e:
            #     print(f"Error creating flashcard: {e}")

        elif "Quiz" in mode:
            try:
                # Create quiz using QuizService with folder_id
                quiz_service = QuizService(None)
                created_quiz = quiz_service.create_quiz(
                    title=name, folder_id=folder_id, quiz_type="multiple", mode="normal"
                )

                if created_quiz:
                    # Show quiz editor window
                    self.accept()  # Close create dialog first
                    quiz_dialog = popup_quizwindow(parent, quiz=created_quiz)
                    if quiz_dialog.exec():
                        quiz_data = quiz_dialog.getQuizData()
                        print(f"Quiz Data: {quiz_data}")
                        # Refresh the folder contents
                        parent.load_items()

            except Exception as e:
                print(f"Error creating quiz: {e}")

        self.accept()

    def handle_note_change(self, note_dialog):
        """Handle auto-save with delay when note content changes"""
        # Cancel any existing timer
        if hasattr(self, "_save_timer"):
            self._save_timer.stop()

        # Create new timer for delayed save
        from PySide6.QtCore import QTimer

        self._save_timer = QTimer()
        self._save_timer.setSingleShot(True)
        self._save_timer.timeout.connect(lambda: self.save_note_changes(note_dialog))
        self._save_timer.start(1000)  # 1 second delay

    def save_note_changes(self, note_dialog):
        """Save note changes to file"""
        try:
            note_data = note_dialog.getNoteData()
            note_service = NoteService()
            updated_note = note_service.update_note(
                folder_id=note_dialog.folder_id,
                note_id=note_dialog.note_id,
                update_data={
                    "name": note_data["title"],
                    "content": note_data["content"],
                },
            )
            if updated_note:
                print(f"Auto-saved note: {updated_note['name']}")
        except Exception as e:
            print(f"Error auto-saving note: {e}")
            import traceback

            traceback.print_exc()


# but first check if there's an existing note that match the folder_id , if so = load  note content in json file and put
