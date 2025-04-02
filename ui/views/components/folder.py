from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QFrame,
    QLabel,
)
from PySide6.QtGui import QPixmap
from PySide6.QtCore import Qt, QSize


class Folder(QWidget):
    def __init__(self, name, count, date, avatar_url, img_url):
        super().__init__()
        self.setupUi(name, count, date, avatar_url, img_url)

    def setupUi(self, name, count, date, avatar_url, img_url):
        # Main layout for the folder widget
        layout = QVBoxLayout(self)
        layout.setSpacing(0)  # Set to 0 to remove spacing
        layout.setContentsMargins(0, 0, 0, 0)  # Remove margins for proper alignment

        # Frame for the preview
        frame = QFrame()
        frame.setFixedSize(200, 150)
        frame.setStyleSheet(
            """
            QFrame {
                background-color: #F0F0F0;
                border: 1px solid #ccc;
                border-radius: 10px;
            }
        """
        )

        # Image label
        image_label = QLabel(frame)
        image_label.setFixedSize(200, 150)
        image_label.setScaledContents(True)
        image_label.setStyleSheet("border-radius: 10px; overflow: hidden;")

        # Load and set the image
        pixmap = QPixmap(img_url)
        if not pixmap.isNull():
            pixmap = pixmap.scaled(
                QSize(200, 150), Qt.KeepAspectRatioByExpanding, Qt.SmoothTransformation
            )
            image_label.setPixmap(pixmap)

        layout.addWidget(frame)

        # Folder name with icon
        name_layout = QHBoxLayout()
        name_layout.setSpacing(3)
        name_layout.setContentsMargins(0, 0, 0, 0)

        profile_icon = QLabel()
        profile_icon.setFixedSize(16, 16)
        profile_icon.setPixmap(
            QPixmap(avatar_url).scaled(
                16, 16, Qt.KeepAspectRatio, Qt.SmoothTransformation
            )
        )
        name_layout.addWidget(profile_icon)

        label_name = QLabel(name)
        label_name.setStyleSheet(
            """
            QLabel {
                font-family: sans-serif;
                font-size: 14px;
                font-weight: bold;
                color: black;
            }
        """
        )
        name_layout.addWidget(label_name)
        name_layout.addStretch()
        layout.addLayout(name_layout)

        # Date
        date_label = QLabel(date)
        date_label.setStyleSheet(
            """
            QLabel {
                font-family: sans-serif;
                font-size: 10px; 
                font-weight: normal;
                color: black;
                margin-top: -4px;
                margin-bottom: -4px;
            }
        """
        )
        layout.addWidget(date_label)

        # Items count with icon
        count_layout = QHBoxLayout()
        count_layout.setSpacing(3)
        count_layout.setContentsMargins(0, -4, 0, 0)  # Increased negative top margin

        count_icon = QLabel()
        count_icon.setFixedSize(16, 16)
        count_icon.setPixmap(
            QPixmap("static/images/collectioncount.svg").scaled(
                14, 14, Qt.KeepAspectRatio, Qt.SmoothTransformation
            )
        )
        count_layout.addWidget(count_icon)

        label_count = QLabel("Items(" + count + ")")
        label_count.setStyleSheet(
            """
            QLabel {
                font-family: sans-serif;
                font-size: 12px;
                font-weight: normal;
                color: black;
            }
        """
        )
        count_layout.addWidget(label_count)
        count_layout.addStretch()
        layout.addLayout(count_layout)
