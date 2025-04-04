import os
import sys
from PySide6.QtCore import Qt, QDir, Signal
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
    folder_clicked = Signal(object)  # Changed to pass a Folder object

    def __init__(self, folders, parent=None):
        super().__init__(parent)
        self.folders = folders
        self.home_controller = None
        self.setupUI()

    def setupUI(self):
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
            "background-color: white; border-radius: 10px;"
        )
        self.scroll_layout = QHBoxLayout(self.scroll_widget)
        self.scroll_layout.setSpacing(40)
        self.scroll_layout.setContentsMargins(40, 20, 40, 20)

        # Add stretch to push folders to the left
        self.scroll_layout.addStretch()

        self.scroll_area.setWidget(self.scroll_widget)

        main_layout = QVBoxLayout()
        main_layout.addWidget(self.scroll_area)
        self.setLayout(main_layout)

        # Create and add folders
        self.update_folders(self.folders)

    def update_folders(self, folders):
        """Update the folders displayed in the scroller."""
        # Clear existing folders
        while self.scroll_layout.count():
            item = self.scroll_layout.takeAt(0)
            if item.widget():
                item.widget().deleteLater()

        # Remove the stretch
        self.scroll_layout.takeAt(self.scroll_layout.count() - 1)

        # Add new folders
        for folder_data in folders:
            folder = Folder(
                folder_data.id,
                folder_data.name,
                folder_data.total_items,
                folder_data.created_at,
                folder_data.img_url,  # should be avatar
                folder_data.img_url,
            )
            # Connect folder click to the folder_clicked signal
            folder.clicked.connect(
                lambda checked=False, f=folder_data: self.folder_clicked.emit(f)
            )
            self.scroll_layout.addWidget(folder)

        # Add stretch back
        self.scroll_layout.addStretch()

    def scroll_left(self):
        """Scroll left by one folder."""
        self.scroll_area.horizontalScrollBar().setValue(
            self.scroll_area.horizontalScrollBar().value()
            - 240  # Increased from 220 to account for new spacing
        )

    def scroll_right(self):
        """Scroll right by one folder."""
        self.scroll_area.horizontalScrollBar().setValue(
            self.scroll_area.horizontalScrollBar().value()
            + 240  # Increased from 220 to account for new spacing
        )

    def set_controller(self, controller):
        """Set the home controller and connect signals."""
        self.home_controller = controller
        # Connect the folder_clicked signal to the controller's navigate_to_folder method
        self.folder_clicked.connect(self.home_controller.navigate_to_folder)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = HorizontalImageScroller()
    window.show()
    sys.exit(app.exec())
