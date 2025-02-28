from PySide6.QtWidgets import (
    QWidget, QLabel, QVBoxLayout, QHBoxLayout,
    QPushButton, QFrame, QGridLayout, QApplication
)
from PySide6.QtCore import Qt
from PySide6.QtGui import QFont

class CollectionPage(QWidget):
    def __init__(self):
        super().__init__()
        self.setupUi()

    def setupUi(self):
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(25, 100, 10, 10)
        main_layout.setSpacing(5)

        # Header
        header_label = QLabel("My Collection")
        main_layout.addWidget(header_label, alignment=Qt.AlignLeft)

        # From latest (aligned to left)
        from_latest_layout = QHBoxLayout()
        main_layout.addLayout(from_latest_layout)
        sort_button = QPushButton("From latest")
        sort_button.setStyleSheet("""
            QPushButton {
                background-color: transparent;
                color: #888888;
                font-size: 12px;
                border: none;
            }
        """)
        from_latest_layout.addWidget(sort_button)
        from_latest_layout.addStretch(1)

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
                background-color: #FFD7BA;
            }
        """)
        public_button.setStyleSheet(private_button.styleSheet())  # Use the same style as private_button
        private_button.setCheckable(True)
        private_button.setChecked(True)
        public_button.setCheckable(True)
        toggle_layout.addWidget(private_button)
        toggle_layout.addWidget(public_button)
        toggle_layout.addStretch(1)

        # Join Contest Button aligned to the right
        join_contest_button = QPushButton("Join contest")
        join_contest_button.setStyleSheet("""
            QPushButton {
                background-color: #FFD7BA; /* Peach color */
                border-radius: 15px; /* Rounded corners */
                padding: 5px 15px; /* Padding around the text */
                font-size: 12px; /* Text size */
                color: #333; /* Text color */
            }
            QPushButton:hover {
                background-color: #E6C3AC; /* Slightly darker shade on hover */
            }
        """)


        # Add Folder Button, styled to look like a small square button
        add_folder_button = QPushButton("+")
        add_folder_button.setStyleSheet("""
            QPushButton {
                background-color: #8CC152; 
                border-radius: 15px; /* Rounded corners */
                padding: 5px 15px; /* Padding around the text */
                font-size: 12px; /* Text size */
                color: #333; /* Text color */
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
        main_layout.addLayout(grid_layout)
        for i in range(8):
            folder_widget = self.create_folder_widget("Folder name", "9 items")
            grid_layout.addWidget(folder_widget, i // 4, i % 4)

        main_layout.addStretch(1)

    def create_folder_widget(self, name, count):
        folder_widget = QWidget()
        layout = QVBoxLayout(folder_widget)
        layout.setSpacing(5)
        frame = QFrame()
        frame.setFixedSize(200, 150)
        frame.setStyleSheet("border: 1px solid #ccc; border-radius: 10px;")
        layout.addWidget(frame, alignment=Qt.AlignCenter)
        label_name = QLabel(name)
        label_name.setObjectName("folderNameLabel")
        label_name.setAlignment(Qt.AlignCenter)
        layout.addWidget(label_name)
        label_count = QLabel(count)
        label_count.setObjectName("folderNameLabel")
        label_count.setAlignment(Qt.AlignCenter)
        layout.addWidget(label_count)
        return folder_widget

if __name__ == "__main__":
    app = QApplication([])
    window = CollectionPage()
    window.show()
    app.exec()
