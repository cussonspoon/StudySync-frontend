from PySide6.QtWidgets import (
    QWidget, QLabel, QVBoxLayout, QHBoxLayout,
    QPushButton, QFrame, QGridLayout, QApplication,
    QDialog, QLineEdit, QDialogButtonBox
)
from PySide6.QtCore import Qt, QSize
from PySide6.QtGui import QFont, QPixmap

class JoinContestDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent, Qt.WindowSystemMenuHint | Qt.WindowTitleHint | Qt.WindowCloseButtonHint)
        self.setModal(True)
        self.setWindowTitle("Join contest code")
        self.setupUi()
        self.setFixedSize(385, 133)

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
        self.lineEdit.setStyleSheet("""
            QLineEdit {
                border: 2px solid #E0E0E0;
                border-radius: 10px;
                padding: 10px;
            }
            QLineEdit:focus {
                border: 2px solid #0066CC;
            }
        """)

        # Custom OK button (smaller size)
        self.okButton = QPushButton("OK", self)
        self.okButton.setFont(QFont("Arial", 10))  # Slightly smaller font
        self.okButton.setFixedSize(70, 30)  # Reduced button size
        self.okButton.setStyleSheet("""
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
        """)
        self.okButton.clicked.connect(self.accept)

        layout.addWidget(self.okButton, alignment=Qt.AlignRight)

    def getContestCode(self):
        return self.lineEdit.text()

class CollectionPage(QWidget):
    def __init__(self):
        super().__init__()
        self.setupUi()

    def setupUi(self):
        main_layout = QVBoxLayout(self)
        # Reduce the top margin here
        main_layout.setContentsMargins(25, 10, 10, 10)  # Reduced from 100 to 10
        main_layout.setSpacing(5)

        # Header layout for "My Collection" and image
        header_layout = QHBoxLayout()
        main_layout.addLayout(header_layout)

        # Header
        header_label = QLabel("My Collection")
        header_label.setFont(QFont("Arial", 16, QFont.Bold))
        header_layout.addWidget(header_label, alignment=Qt.AlignLeft)

        # Image next to the header
        image_label = QLabel()
        pixmap = QPixmap("static/images/collectiongirl.svg")
        image_label.setPixmap(pixmap.scaledToHeight(200))  # Scale the image to a suitable height
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
        sort_icon_label.setPixmap(sort_icon_pixmap.scaledToHeight(20))  # Adjust size as needed
        sort_icon_label.setScaledContents(True)
        from_latest_layout.addWidget(sort_icon_label, alignment=Qt.AlignCenter)

        # "From latest" button
        sort_button = QPushButton("From latest")
        sort_button.setStyleSheet("""
            QPushButton {
                background-color: transparent;
                color: #888888;
                font-size: 20px;
                border: none;
            }
        """)
        from_latest_layout.addWidget(sort_button)
        from_latest_layout.addStretch(1)  # Ensure button and icon are left-aligned

        # Private/Public buttons centered
        toggle_layout = QHBoxLayout()
        main_layout.addLayout(toggle_layout)
        private_button = QPushButton("Private")
        public_button = QPushButton("Public")
        private_button.setStyleSheet("""
            QPushButton {
                background-color: #F0F0F0;
                border-radius: 15px;
                padding: 5px 15px;
                font-size: 12px;
            }
            QPushButton:checked {
                background-color: #ffc99a;
            }
        """)
        public_button.setStyleSheet(private_button.styleSheet())
        private_button.setCheckable(True)
        private_button.setChecked(True)
        public_button.setCheckable(True)
        toggle_layout.addWidget(private_button)
        toggle_layout.addWidget(public_button)
        toggle_layout.addStretch(1)

        # Join Contest Button aligned to the right
        join_contest_button = QPushButton("Join contest")
        join_contest_button.clicked.connect(self.showJoinContestDialog)
        main_layout.addWidget(join_contest_button, alignment=Qt.AlignRight)
        join_contest_button.setStyleSheet("""
            QPushButton {
                background-color: #ffc99a;
                border-radius: 15px;
                padding: 5px 15px;
                font-size: 12px;
                color: #333;
            }
            QPushButton:hover {
                background-color: #E6C3AC;
            }
        """)
        add_folder_button = QPushButton("+")
        add_folder_button.setStyleSheet("""
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
        """)
        toggle_layout.addStretch(1)
        toggle_layout.addWidget(join_contest_button)
        toggle_layout.addWidget(add_folder_button)

        # Grid Layout for folders
        grid_layout = QGridLayout()
        grid_layout.setSpacing(10)
        main_layout.addStretch(1)
        main_layout.addLayout(grid_layout)
        for i in range(8):
            folder_widget = self.create_folder_widget("Folder name", "9 items", "Thursday, January 30, 2025","static/images/logo.png", "static/images/folderimgplaceholder.jpg" )
            grid_layout.addWidget(folder_widget, i // 4, i % 4)

        main_layout.addStretch(1)

    def create_folder_widget(self, name, count, date, avatar_url, img_url):
        folder_widget = QWidget()
        layout = QVBoxLayout(folder_widget)
        layout.setSpacing(5)
        layout.setContentsMargins(0, 0, 0, 0)  # Remove margins for proper alignment

        # Frame for the preview
        frame = QFrame()
        frame.setFixedSize(200, 150)
        frame.setStyleSheet("""
            QFrame {
                background-color: #F0F0F0;
                border: 1px solid #ccc;
                border-radius: 10px;
            }
        """)

        # Image label
        image_label = QLabel(frame)
        image_label.setFixedSize(200, 150)
        image_label.setScaledContents(True)
        image_label.setStyleSheet("border-radius: 10px; overflow: hidden;")

        # Load and set the image
        pixmap = QPixmap(img_url)
        if not pixmap.isNull():
            pixmap = pixmap.scaled(QSize(200, 150), Qt.KeepAspectRatioByExpanding, Qt.SmoothTransformation)
            image_label.setPixmap(pixmap)

        layout.addWidget(frame)

        # Folder name with icon
        name_layout = QHBoxLayout()
        name_layout.setSpacing(5)
        
        profile_icon = QLabel()
        profile_icon.setFixedSize(16, 16)
        profile_icon.setPixmap(QPixmap(avatar_url).scaled(16, 16, Qt.KeepAspectRatio, Qt.SmoothTransformation))
        name_layout.addWidget(profile_icon)
        
        label_name = QLabel(name)
        label_name.setObjectName("folderNameLabel")
        name_layout.addWidget(label_name)
        name_layout.addStretch()
        layout.addLayout(name_layout)

        # Date
        date_label = QLabel(date)
        date_label.setStyleSheet("""
            QLabel {
                font-family: sans-serif;
                font-size: 10px; 
                font-weight: normal;
                color: #666666;
            }
        """)
        layout.addWidget(date_label)

        # Items count with icon
        count_layout = QHBoxLayout()
        count_layout.setSpacing(5)
        
        count_icon = QLabel()
        count_icon.setFixedSize(16, 16)
        count_icon.setPixmap(QPixmap("static/images/collectioncount.svg").scaled(14, 14, Qt.KeepAspectRatio, Qt.SmoothTransformation))
        count_layout.addWidget(count_icon)
        
        label_count = QLabel(count)
        label_count.setObjectName("folderNameLabel")
        count_layout.addWidget(label_count)
        count_layout.addStretch()
        layout.addLayout(count_layout)

        return folder_widget
    
    def showJoinContestDialog(self):
        dialog = JoinContestDialog()
        if dialog.exec():
            contest_code = dialog.getContestCode()
            print("Contest Code Entered:", contest_code)  # or handle the code as needed
