import os
from PySide6.QtWidgets import (
    QLabel,
    QWidget,
    QFrame,
    QVBoxLayout,
    QHBoxLayout,
    QGraphicsDropShadowEffect,
    QSizePolicy,
)
from PySide6.QtGui import QFont, QPixmap, QColor
from PySide6.QtCore import Qt, QDir

# add text here


class Text(QWidget):
    def __init__(self, pos_x, pos_y, font_size, text, color="333333", parent=None):
        super().__init__(parent)

        self.text_area = QLabel(parent)
        self.text_area.setObjectName("recommendsText")
        self.text_area.move(pos_x, pos_y)  # Adjusted Y position to follow carousel
        font = QFont()
        font.setPointSize(font_size)
        self.text_area.setFont(font)
        self.text_area.setText(text)
        self.text_area.setStyleSheet(f"color: #{color};")

        self.text_area.adjustSize()
        self.text_area.show()


class Image(QWidget):
    def __init__(self, pos_x, pos_y, width, length, img_src, parent=None):
        super().__init__(parent)

        self.image = QLabel(parent)
        self.image.setObjectName("image")
        self.image.setGeometry(pos_x, pos_y, width, length)
        img_path = os.path.join(QDir.currentPath(), f"static/images/{img_src}")
        self.load_image(self.image, img_path, width, length)

    def load_image(self, label, path, width, height):
        """Loads an image into a QLabel while maintaining aspect ratio."""
        if not os.path.exists(path):
            label.setText("⚠️ Image not found")
            label.setStyleSheet("color: red; font-size: 14px;")
            print(f"⚠️ Warning: Image not found at {path}")
            return

        pixmap = QPixmap(path)
        if pixmap.isNull():
            label.setText("⚠️ Error loading image")
            label.setStyleSheet("color: red; font-size: 14px;")
            print(f"⚠️ Error loading image at {path}")
        else:
            scaled_pixmap = pixmap.scaled(
                width, height, Qt.KeepAspectRatioByExpanding, Qt.SmoothTransformation
            )

            label.setFixedSize(width, height)
            label.setAlignment(Qt.AlignCenter)  # Center image in the QLabel
            label.setStyleSheet(
                "background-color: transparent;"
            )  # Remove unwanted background color
            label.setPixmap(scaled_pixmap)


class QuizQuestionCard(QWidget):
    def __init__(self, question_text="Sample Question?"):
        super().__init__()

        self.question_text = question_text

        # Set size policy to expand horizontally
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)

        # 📌 Card Container (QFrame)
        self.card = QFrame(self)
        self.card.setStyleSheet(
            """
            QFrame {
                background-color: white;
                border-radius: 10px;
                border: 1px solid #E0E0E0;
            }
            """
        )
        self.card.setFixedHeight(120)  # Adjust based on layout
        self.card.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)  # Make card expand horizontally

        # 📌 Layout for Card
        layout = QVBoxLayout(self.card)
        layout.setContentsMargins(20, 20, 20, 20)  # Increased padding

        # 📌 Question Label
        self.question_label = QLabel(self.question_text)
        self.question_label.setWordWrap(True)
        self.question_label.setStyleSheet(
            "font-weight: bold; font-size: 16px; border: none; color: #333333;"
        )
        self.question_label.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)  # Make label expand horizontally

        # Add question label to layout
        layout.addWidget(self.question_label)

        # 📌 Main Layout
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)  # Remove margins to allow full width
        main_layout.addWidget(self.card)

        self.setLayout(main_layout)
