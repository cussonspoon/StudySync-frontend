# import os
# from PySide6.QtWidgets import QLabel, QWidget, QHBoxLayout, QLineEdit, QApplication
# from PySide6.QtGui import QFont, QPixmap
# from PySide6.QtCore import Qt, QDir
# import sys

# #add text here


# class Frame(QWidget):
#     def __init__(self, frame_name, pos_x, pos_y, width, height, color, border_radius, have_border = False, parent=None):
#         super().__init__(parent)
#         self.setObjectName(frame_name)
#         self.setGeometry(pos_x, pos_y, width, height)
#         self.setStyleSheet(f"background-color: {color}; border-radius: {border_radius};")
#         if have_border:
#             self.setStyleSheet(f"border: 1px solid {color};")


# class Text(QWidget):
#     def __init__(self, pos_x, pos_y, font_size, text, color="333333",  parent=None):
#         super().__init__(parent)

#         self.text_area = QLabel(parent)
#         self.text_area.setObjectName("recommendsText")
#         self.text_area.move(pos_x, pos_y)  # Adjusted Y position to follow carousel
#         font = QFont()
#         font.setPointSize(font_size)
#         self.text_area.setFont(font)
#         self.text_area.setText(text)
#         self.text_area.setStyleSheet(f"color: #{color};")

#         self.text_area.adjustSize()
#         self.text_area.show()

# class Image(QWidget): 
#     def __init__(self, pos_x, pos_y, width, length, img_src, parent=None): 
#         super().__init__(parent)

#         self.image = QLabel(parent)
#         self.image.setObjectName("image")
#         self.image.setGeometry(pos_x, pos_y, width, length)
#         img_path = os.path.join(QDir.currentPath(), f"static/images/{img_src}")
#         self.load_image(self.image, img_path,  width, length)

#     def load_image(self, label, path, width, height):
#         """Loads an image into a QLabel while maintaining aspect ratio."""
#         if not os.path.exists(path):
#             label.setText("⚠️ Image not found")
#             label.setStyleSheet("color: red; font-size: 14px;")
#             print(f"⚠️ Warning: Image not found at {path}")
#             return

#         pixmap = QPixmap(path)
#         if pixmap.isNull():
#             label.setText("⚠️ Error loading image")
#             label.setStyleSheet("color: red; font-size: 14px;")
#             print(f"⚠️ Error loading image at {path}")
#         else:
#             scaled_pixmap = pixmap.scaled(width, height, Qt.KeepAspectRatioByExpanding, Qt.SmoothTransformation)

#             label.setFixedSize(width, height)
#             label.setAlignment(Qt.AlignCenter)  # Center image in the QLabel
#             label.setStyleSheet("background-color: transparent;")  # Remove unwanted background color
#             label.setPixmap(scaled_pixmap)


# class SearchBar(QWidget):
#     def __init__(self, parent=None):
#         super().__init__(parent)

#         # Main Layout
#         layout = QHBoxLayout(self)
#         layout.setContentsMargins(10, 5, 10, 5)  

#         # self.search_icon = QLabel(self)
#         img_path = os.path.join(QDir.currentPath(), f"static/images/search.png")
#         # self.search_icon.setPixmap(QPixmap(img_path).scaled(18, 18, Qt.KeepAspectRatio))
#         # self.search_icon.setAlignment(Qt.AlignVCenter)

#         self.search_input = QLineEdit(self)
#         self.search_input.setPlaceholderText("Search by subject name")
#         self.search_input.setFont(QFont("Arial", 12))

#         self.search_input.setStyleSheet("""
#             QLineEdit {
#                 background-color: #E6E6E6;
#                 border: none;
#                 padding: 8px;
#                 border-radius: 5px;
#                 font-size: 14px;
#                 color: black; /* Text color when typing */
#             }
#             QLineEdit::placeholder {
#                 color: #8D8D8D; /* Placeholder text color */
#             }
#         """)

#         # layout.addWidget(self.search_icon)
#         layout.addWidget(self.search_input)

#         self.setStyleSheet("""
#             QWidget {
#                 background-color: #E6E6E6;
#                 border-radius: 15px;
#             }
#         """)

#         self.setFixedWidth(300)  
#         self.setFixedHeight(40)  


# # Run Application
# if __name__ == "__main__":
#     app = QApplication(sys.argv)
#     window = QWidget()
#     layout = QHBoxLayout(window)

#     search_bar = SearchBar(0, 0)
#     layout.addWidget(search_bar)

#     window.setLayout(layout)
#     window.show()
#     sys.exit(app.exec())


import os
import sys
from PySide6.QtWidgets import (
    QLabel, QWidget, QHBoxLayout, QVBoxLayout, QLineEdit, QApplication, QFrame, QSizePolicy
)
from PySide6.QtGui import QFont, QPixmap
from PySide6.QtCore import Qt, QDir


class Frame(QWidget):
    def __init__(self, frame_name, width, height, color, border_radius, have_border=False, parent=None):
        """Creates a styled frame with optional border."""
        super().__init__(parent)
        self.setObjectName(frame_name)
        self.setFixedSize(width, height)

        # Apply styles
        border_style = f"border: 1px solid {color};" if have_border else ""
        self.setStyleSheet(f"background-color: {color}; border-radius: {border_radius}px; {border_style}")


class Text(QLabel):
    def __init__(self, font_size, text, color="333333", parent=None):
        """Creates a styled text label."""
        super().__init__(text, parent)
        self.setObjectName("textLabel")
        font = QFont()
        font.setPointSize(font_size)
        self.setFont(font)
        self.setStyleSheet(f"color: #{color};")
        self.adjustSize()


class Image(QLabel):
    def __init__(self, width, height, img_src, parent=None):
        """Loads and displays an image."""
        super().__init__(parent)
        self.setObjectName("image")
        self.setFixedSize(width, height)
        img_path = os.path.join(QDir.currentPath(), f"static/images/{img_src}")
        self.load_image(img_path, width, height)
        
    def load_image(self, path, width, height):
        """Loads an image into QLabel while maintaining aspect ratio."""
        if not os.path.exists(path):
            self.setText("⚠️ Image not found")
            self.setStyleSheet("color: red; font-size: 14px;")
            print(f"⚠️ Warning: Image not found at {path}")
            return

        pixmap = QPixmap(path)
        if pixmap.isNull():
            self.setText("⚠️ Error loading image")
            self.setStyleSheet("color: red; font-size: 14px;")
            print(f"⚠️ Error loading image at {path}")
        else:
            scaled_pixmap = pixmap.scaled(width, height, Qt.KeepAspectRatioByExpanding, Qt.SmoothTransformation)
            self.setPixmap(scaled_pixmap)
            self.setAlignment(Qt.AlignCenter)  # Center image


class SearchBar(QWidget):
    def __init__(self, parent=None):
        """Creates a search bar widget."""
        super().__init__(parent)

        # Main Layout
        layout = QHBoxLayout(self)
        layout.setContentsMargins(10, 5, 10, 5)
        layout.setAlignment(Qt.AlignLeft)

        self.search_input = QLineEdit(self)
        self.search_input.setPlaceholderText("Search by subject name")
        self.search_input.setFont(QFont("Arial", 12))
        self.search_input.setStyleSheet("""
            QLineEdit {
                background-color: #E6E6E6;
                border: none;
                padding: 10px;
                border-radius: 5px;
                font-size: 14px;
                color: black;
            }
            QLineEdit::placeholder {
                color: #8D8D8D;
            }
        """)

        layout.addWidget(self.search_input)

        # Apply overall styling
        self.setStyleSheet("""
            QWidget {
                background-color: #E6E6E6;
                border-radius: 15px;
            }
        """)

        self.setFixedSize(500, 60)  # Set fixed size for search bar

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

# ✅ Run Application Test
if __name__ == "__main__":
    app = QApplication(sys.argv)
    
    # Main Window
    window = QWidget()
    layout = QVBoxLayout(window)
    layout.setAlignment(Qt.AlignCenter)

    # Test UI Components
    search_bar = SearchBar(window)
    text_label = Text(16, "Welcome to StudySync", "333333", window)
    image_test = Image(100, 100, "profile.jpg", window)

    # Add Components to Layout
    layout.addWidget(search_bar)
    layout.addWidget(text_label)
    layout.addWidget(image_test)

    window.setLayout(layout)
    window.show()
    sys.exit(app.exec())

