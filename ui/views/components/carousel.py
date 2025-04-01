import os
import sys
from PySide6.QtCore import Qt, QDir
from PySide6.QtWidgets import (
    QApplication,
    QWidget,
    QLabel,
    QPushButton,
    QVBoxLayout,
    QHBoxLayout,
    QScrollArea,
    QFrame,
)
from PySide6.QtGui import QPixmap
from ui.views.components.folder import Folder


class HorizontalImageScroller(QWidget):
    def __init__(self, folders, parent=None):
        super().__init__(parent)

        # Sample folder data
        self.folders = folders
        self.folders = [
            {
                "name": "Folder 1",
                "count": "10",
                "date": "2024-01-01",
                "avatar": "static/images/profile.jpg",
                "image": "static/images/pic1.jpg",
            },
            {
                "name": "Folder 2",
                "count": "15",
                "date": "2024-01-02",
                "avatar": "static/images/profile.jpg",
                "image": "static/images/pic2.jpg",
            },
            {
                "name": "Folder 3",
                "count": "20",
                "date": "2024-01-03",
                "avatar": "static/images/profile.jpg",
                "image": "static/images/pic3.jpg",
            },
            {
                "name": "Folder 4",
                "count": "25",
                "date": "2024-01-04",
                "avatar": "static/images/profile.jpg",
                "image": "static/images/pic1.jpg",
            },
            {
                "name": "Folder 5",
                "count": "30",
                "date": "2024-01-05",
                "avatar": "static/images/profile.jpg",
                "image": "static/images/pic2.jpg",
            },
            {
                "name": "Folder 6",
                "count": "35",
                "date": "2024-01-06",
                "avatar": "static/images/profile.jpg",
                "image": "static/images/pic3.jpg",
            },
            {
                "name": "Folder 7",
                "count": "40",
                "date": "2024-01-07",
                "avatar": "static/images/profile.jpg",
                "image": "static/images/pic1.jpg",
            },
            {
                "name": "Folder 8",
                "count": "45",
                "date": "2024-01-08",
                "avatar": "static/images/profile.jpg",
                "image": "static/images/pic2.jpg",
            },
            {
                "name": "Folder 9",
                "count": "50",
                "date": "2024-01-09",
                "avatar": "static/images/profile.jpg",
                "image": "static/images/pic3.jpg",
            },
            {
                "name": "Folder 10",
                "count": "55",
                "date": "2024-01-10",
                "avatar": "static/images/profile.jpg",
                "image": "static/images/pic1.jpg",
            },
        ]

        # Create a scrollable area
        self.scroll_area = QScrollArea(self)
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.scroll_area.setMinimumHeight(300)  # Increased height to fit folders
        self.scroll_area.setStyleSheet(
            """
            QScrollArea {
                border: none;
                background-color: white;
                border-radius: 10px;
                outline: none;
            }
            QScrollBar:horizontal {
                border: none;
                background-color: transparent;
                height: 10px;
                margin: 0px;
            }

            QScrollBar::handle:horizontal {
                background-color: #BDBDBD;
                border-radius: 3px;
                min-width: 15px;
                margin: 2px 0;
            }

            QScrollBar::handle:horizontal:hover {
                background-color: #9E9E9E;
            }

            QScrollBar::add-line:horizontal, QScrollBar::sub-line:horizontal {
                width: 0px;
            }

            QScrollBar::add-page:horizontal, QScrollBar::sub-page:horizontal {
                background: none;
            }
        """
        )

        # Create a container widget for folders
        self.scroll_widget = QWidget()
        self.scroll_widget.setStyleSheet(
            "background-color: white; border-radius: 10px; border: none; outline: none;"
        )
        self.scroll_layout = QHBoxLayout(self.scroll_widget)
        self.scroll_layout.setSpacing(20)  # Add spacing between folders
        self.scroll_layout.setContentsMargins(
            20, 20, 20, 20
        )  # Add margins around the layout

        # Create and add folders
        for folder_data in self.folders:
            folder = Folder(
                folder_data["name"],
                folder_data["count"],
                folder_data["date"],
                folder_data["avatar"],
                folder_data["image"],
            )
            self.scroll_layout.addWidget(folder)

        # Add stretch to push folders to the left
        self.scroll_layout.addStretch()

        self.scroll_area.setWidget(self.scroll_widget)

        main_layout = QVBoxLayout()
        main_layout.addWidget(self.scroll_area)
        self.setLayout(main_layout)

    def scroll_left(self):
        """Scroll left by one folder."""
        self.scroll_area.horizontalScrollBar().setValue(
            self.scroll_area.horizontalScrollBar().value()
            - 220  # Width of folder + spacing
        )

    def scroll_right(self):
        """Scroll right by one folder."""
        self.scroll_area.horizontalScrollBar().setValue(
            self.scroll_area.horizontalScrollBar().value()
            + 220  # Width of folder + spacing
        )


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = HorizontalImageScroller()
    window.show()
    sys.exit(app.exec())
