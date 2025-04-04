from PySide6.QtWidgets import (
    QWidget,
    QLabel,
    QVBoxLayout,
    QHBoxLayout,
    QPushButton,
    QFrame,
    QGridLayout,
    QApplication,
    QDialog,
    QLineEdit,
    QDialogButtonBox,
)
from PySide6.QtCore import Qt, QSize, Signal
from PySide6.QtGui import QFont, QPixmap
from ui.views.components.note_window import popup_notewindow
from ui.views.components.folder import Folder
from ui.views.components.flashcard_window import popup_flashcardwindow
from ui.views.components.flashcard_components.models import (
    Flashcard,
    TermWord,
    get_sample_flashcards,
)
from datetime import datetime


class JoinContestDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(
            parent,
            Qt.WindowSystemMenuHint | Qt.WindowTitleHint | Qt.WindowCloseButtonHint,
        )
        self.folders = []
        self.setModal(True)
        self.setWindowTitle("Join contest code")
        self.setupUi()
        self.setFixedSize(385, 133)
        self.setStyleSheet(
            """
            QDialog {
                background-color: #F8F6F1;
            }
            """
        )

    def setupUi(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(25, 25, 25, 25)
        layout.setSpacing(15)

        # Text input for the contest code
        self.lineEdit = QLineEdit(self)
        self.lineEdit.setPlaceholderText("Enter contest code here")
        self.lineEdit.setFont(QFont("Arial", 10))
        layout.addWidget(self.lineEdit)

        # Styling for QLineEdit
        self.lineEdit.setStyleSheet(
            """
            QLineEdit {
                border: 2px solid #E0E0E0;
                border-radius: 10px;
                padding: 10px;
            }
            QLineEdit:focus {
                border: 2px solid #0066CC;
            }
        """
        )

        # Custom OK button (smaller size)
        self.okButton = QPushButton("OK", self)
        self.okButton.setFont(QFont("Arial", 10))  # Slightly smaller font
        self.okButton.setFixedSize(70, 30)  # Reduced button size
        self.okButton.setStyleSheet(
            """
            QPushButton {
                background-color: #0066CC;
                color: white;
                border: none;
                border-radius: 15px; 
                padding: 5px 10px;
            }
            QPushButton:hover {
                background-color: #0052A3;
            }
            QPushButton:pressed {
                background-color: #004080;
            }
        """
        )
        self.okButton.clicked.connect(self.accept)

        layout.addWidget(self.okButton, alignment=Qt.AlignRight)

    def getContestCode(self):
        return self.lineEdit.text()


class CollectionPage(QWidget):
    folder_clicked = Signal(str, int, str)  # Modified to pass name, count, date

    def __init__(self):
        super().__init__()
        self.folders = []
        self.setupUi()
        self.setStyleSheet(
            """
            QWidget {
                background-color: #FAFAFA;
            }
        """
        )

    def set_controller(self, controller):
        self.collection_controller = controller

    def update_folders(self, folders):
        """Updates the grid with new folders"""
        # Clear existing folders from grid
        for i in reversed(range(self.grid_layout.count())):
            self.grid_layout.itemAt(i).widget().deleteLater()

        # Add new folders
        for i, folder in enumerate(folders):
            folder_widget = self.create_folder_widget(
                folder["name"],
                folder["count"],
                folder["date"],
                folder["avatar"],
                folder["image"],
            )
            self.grid_layout.addWidget(folder_widget, i // 4, i % 4)

    def setupUi(self):
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(25, 10, 10, 10)
        main_layout.setSpacing(5)

        # Header layout for "My Collection" and image
        header_layout = QHBoxLayout()
        main_layout.addLayout(header_layout)

        # Header
        header_label = QLabel("My Collection")
        header_label.setFont(QFont("Arial", 16, QFont.Bold))
        header_layout.addWidget(header_label, alignment=Qt.AlignLeft)
        header_label.setStyleSheet(
            """
            QLabel {
                color: black;
            }
            """
        )

        # Image next to the header
        image_label = QLabel()
        pixmap = QPixmap("static/images/collectiongirl.svg")
        image_label.setPixmap(
            pixmap.scaledToHeight(200)
        )  # Scale the image to a suitable height
        image_label.setScaledContents(True)
        header_layout.addWidget(image_label, alignment=Qt.AlignLeft)

        # Stretch to push everything left
        header_layout.addStretch(1)

        # From latest (aligned to left)
        from_latest_layout = QHBoxLayout()
        main_layout.addLayout(from_latest_layout)

        # Icon for "From latest"
        sort_icon_label = QLabel()
        sort_icon_pixmap = QPixmap("static/images/sortby.svg")
        sort_icon_label.setPixmap(
            sort_icon_pixmap.scaledToHeight(20)
        )  # Adjust size as needed
        sort_icon_label.setScaledContents(True)
        from_latest_layout.addWidget(sort_icon_label, alignment=Qt.AlignCenter)

        # "From latest" button
        sort_button = QPushButton("From latest")
        sort_button.setStyleSheet(
            """
            QPushButton {
                background-color: transparent;
                color: #888888;
                font-size: 20px;
                border: none;
            }
        """
        )
        from_latest_layout.addWidget(sort_button)
        from_latest_layout.addStretch(1)  # Ensure button and icon are left-aligned

        # Private/Public buttons centered
        toggle_layout = QHBoxLayout()
        main_layout.addLayout(toggle_layout)

        # Define button style
        button_style = """
            QPushButton {
                background-color: #F0F0F0;
                border-radius: 15px;
                padding: 5px 15px;
                font-size: 12px;
            }
            QPushButton:checked {
                background-color: #ffc99a;
            }
        """

        private_button = QPushButton("Private")
        public_button = QPushButton("Public")
        private_button.setStyleSheet(button_style)
        public_button.setStyleSheet(button_style)
        private_button.setCheckable(True)
        private_button.setChecked(True)
        public_button.setCheckable(True)
        toggle_layout.addWidget(private_button)
        toggle_layout.addWidget(public_button)
        toggle_layout.addStretch(1)

        # Create add folder button
        add_folder_button = QPushButton("+")
        add_folder_button.setStyleSheet(
            """
            QPushButton {
                background-color: #87db8a;
                border-radius: 15px;
                padding: 5px 15px;
                font-size: 12px;
                color: #333;
            }
            QPushButton:hover {
                background-color: #79AD47;
            }
            """
        )
        print("Connecting add folder button")  # Debug print
        add_folder_button.clicked.connect(self.on_add_folder_clicked)
        toggle_layout.addWidget(add_folder_button)

        # Create note and flashcard buttons
        note_button = QPushButton("Note")
        note_button.clicked.connect(self.showNoteWindow)
        toggle_layout.addWidget(note_button)

        flashcard_button = QPushButton("Flashcard")
        flashcard_button.clicked.connect(self.showFlashcardWindow)
        toggle_layout.addWidget(flashcard_button)

        # Grid layout for folders
        self.grid_layout = QGridLayout()
        self.grid_layout.setSpacing(10)
        self.grid_layout.setVerticalSpacing(30)
        main_layout.addLayout(self.grid_layout)

        main_layout.addStretch(1)

    def showNoteWindow(self):
        note_dialog = popup_notewindow(self)
        if note_dialog.exec():
            note_data = note_dialog.getNoteData()
            print("Note Data:", note_data)  # You can handle the note data here

    def showFlashcardWindow(self):
        # Get sample flashcards from the API
        flashcards = get_sample_flashcards()

        if flashcards:
            # Create and show the flashcard window with the first flashcard set
            flashcard_dialog = popup_flashcardwindow(flashcards[0], self)
            if flashcard_dialog.exec():
                # Get the results when the dialog is closed
                results = flashcard_dialog.getFlashcardData()
                print("Flashcard Results:", results)
        else:
            print("No flashcard sets available")

    def create_folder_widget(self, name, count, date, avatar_url, img_url):
        folder = Folder(name, count, date, avatar_url, img_url)
        folder.mousePressEvent = lambda e: self.on_folder_click(name, count, date)
        return folder

    def showJoinContestDialog(self):
        dialog = JoinContestDialog()
        if dialog.exec():
            contest_code = dialog.getContestCode()
            print("Contest Code Entered:", contest_code)  # or handle the code as needed

    def on_add_folder_clicked(self):
        print("Add folder button clicked")  # Debug print
        if hasattr(self, "collection_controller"):
            print("Calling controller's createFolder")  # Debug print
            self.collection_controller.createFolder()
            # self.collection_controller.navigate_to_folder("Untitled", 0, "Just now")
        else:
            print("No collection controller found")  # Debug print

    def on_folder_click(self, name, count, date):
        print(f"Folder clicked: {name}, count: {count}, date: {date}")  # Debug print
        if hasattr(self, "collection_controller"):
            self.collection_controller.navigate_to_folder(name, str(count), date)
        else:
            print("No collection controller found")  # Debug print
