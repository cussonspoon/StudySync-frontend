import os
import sys
from PySide6.QtWidgets import QApplication, QWidget, QLabel, QPushButton, QVBoxLayout, QHBoxLayout, QScrollArea, QFrame
from PySide6.QtGui import QPixmap

class HorizontalImageScroller(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.image_paths = [
            "./static/images/pic1.jpg",
            "./static/images/pic2.jpg",
            "./static/images/pic3.jpg",
            "./static/images/pic3.jpg",
            "./static/images/pic3.jpg",
            "./static/images/pic1.jpg",
            "./static/images/pic2.jpg",
            "./static/images/pic3.jpg",
            "./static/images/pic3.jpg",
            "./static/images/pic3.jpg"
        ]

        # Create a scrollable area
        self.scroll_area = QScrollArea(self)
        self.scroll_area.setWidgetResizable(True)

        # Create a container widget for panels
        self.scroll_widget = QWidget()
        self.scroll_layout = QHBoxLayout(self.scroll_widget)

        # Create panels with 2 images each
        self.panels = []
        for i in range(0, len(self.image_paths), 2):
            panel = QWidget()
            panel_layout = QHBoxLayout(panel)

            # Add first image
            label1 = QLabel(self)
            pixmap1 = QPixmap(self.image_paths[i])
            if pixmap1.isNull():
                print(f"Error: Cannot load image {self.image_paths[i]}")
            label1.setPixmap(pixmap1.scaled(200, 150))  # Resize images
            panel_layout.addWidget(label1)

            # Add second image (if available)
            if i + 1 < len(self.image_paths):
                label2 = QLabel(self)
                pixmap2 = QPixmap(self.image_paths[i + 1])
                if pixmap2.isNull():
                    print(f"Error: Cannot load image {self.image_paths[i + 1]}")
                label2.setPixmap(pixmap2.scaled(200, 150))  # Resize images
                panel_layout.addWidget(label2)

            self.panels.append(panel)
            self.scroll_layout.addWidget(panel)

        self.scroll_area.setWidget(self.scroll_widget)

        # Navigation buttons
        # self.prev_button = QPushButton("←")
        # self.next_button = QPushButton("→")
        # self.prev_button.setFixedSize(20, 60)
        # self.next_button.setFixedSize(20, 60)
        
        # self.prev_button.clicked.connect(self.scroll_left)
        # self.next_button.clicked.connect(self.scroll_right)

        # # Layout setup
        # button_layout = QHBoxLayout()
        # self.scroll_layout.addWidget(self.prev_button)
        # self.scroll_layout.addWidget(self.next_button)

        main_layout = QVBoxLayout()
        main_layout.addWidget(self.scroll_area)
        # main_layout.addLayout(button_layout)

        self.setLayout(main_layout)

    def scroll_left(self):
        """Scroll left by one panel (2 images)."""
        self.scroll_area.horizontalScrollBar().setValue(self.scroll_area.horizontalScrollBar().value() - 400)

    def scroll_right(self):
        """Scroll right by one panel (2 images)."""
        self.scroll_area.horizontalScrollBar().setValue(self.scroll_area.horizontalScrollBar().value() + 400)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = HorizontalImageScroller()
    window.show()
    sys.exit(app.exec())

