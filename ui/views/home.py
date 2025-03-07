
import sys
import os
from PySide6.QtCore import Qt, QDir
from PySide6.QtGui import QFont, QPixmap
from PySide6.QtWidgets import QApplication, QMainWindow, QFrame, QLabel, QScrollArea, QWidget, QPushButton, QVBoxLayout, QHBoxLayout, QLineEdit, QLabel, QFrame, QScrollArea, QSizePolicy, QSpacerItem

from ui.views.components.carousel import HorizontalImageScroller
from utils.ui import Text, Image


class HomePage(QWidget):
    def __init__(self):
        super().__init__()
        self.setupUi()

    def setupUi(self):
        self.setObjectName("Form")
        self.resize(1200, 771)
        self.setStyleSheet("background-color: #FAFAFA;")

        # 📌 Scroll Area Setup
        self.scrollArea = QScrollArea(self)
        self.scrollArea.setObjectName("scrollArea")
        self.scrollArea.setGeometry(0, 110, 1250, 800)
        self.scrollArea.setWidgetResizable(True)
        self.scrollArea.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        self.scrollArea.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)

        self.scrollAreaWidgetContents = QWidget()
        self.scrollAreaWidgetContents.setObjectName("scrollAreaWidgetContents")
        self.scrollAreaWidgetContents.setGeometry(0, 0, 1250, 1000)  # Extended height for scrolling

        self.bannerPic = Image(10, 0, 1171, 291, "banner.jpg", self.scrollAreaWidgetContents)
        self.profilePic = Image(50, 240, 91, 91, "profile.jpg", self.scrollAreaWidgetContents)
        self.collectionText = Text(30, 360, 21, "My Collections", "333333", self.scrollAreaWidgetContents)
        self.collectionIcon = Image(200, 320, 141, 101, "collectionIcon.png", self.scrollAreaWidgetContents)

        self.collections = HorizontalImageScroller(self.scrollAreaWidgetContents)
        self.collections.setGeometry(10, 430, 1180, 250)
        self.recommendsText = Text(30, 710, 21, "Recommended folder for you", "333333", self.scrollAreaWidgetContents)

        self.recommendFolders = HorizontalImageScroller(self.scrollAreaWidgetContents)
        self.recommendFolders.setGeometry(10, 780, 1180, 250)

        self.taskText = Text(30, 1090, 21, "Task", "333333", self.scrollAreaWidgetContents)
        self.taskImg = Image(90, 1050, 141, 101, "task.png", self.scrollAreaWidgetContents)

        self.taskManagement = TaskManagement(27, 1170, 800, 400, self.scrollAreaWidgetContents)

        # 📌 Ensure scrollable content height is correct
        self.scrollAreaWidgetContents.setMinimumHeight(1500)
        self.scrollArea.setWidget(self.scrollAreaWidgetContents)

        # 📌 Header Frame
        self.searchFrame = QFrame(self)
        self.searchFrame.setObjectName("searchFrame")
        self.searchFrame.setGeometry(0, 0, 1250, 111)
        self.searchFrame.setFrameShape(QFrame.Shape.StyledPanel)
        self.searchFrame.setFrameShadow(QFrame.Shadow.Raised)
        
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
            scaled_pixmap = pixmap.scaled(width, height, Qt.KeepAspectRatioByExpanding, Qt.SmoothTransformation)

            label.setFixedSize(width, height)
            label.setAlignment(Qt.AlignCenter)  # Center image in the QLabel
            label.setStyleSheet("background-color: transparent;")  # Remove unwanted background color
            label.setPixmap(scaled_pixmap)

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("StudySync Dashboard")  # Set Window Title
        self.setGeometry(100, 100, 1200, 771)  # Set Window Size
        self.ui = HomePage()
        self.setCentralWidget(self.ui)


class TaskManagement(QWidget):
    def __init__(self, pos_x, pos_y, width, length, parent=None):
        super().__init__(parent)
        self.setWindowTitle("To-Do List")
        # self.setFixedSize(400, 500)
        self.setGeometry(pos_x, pos_y, width, length)

        self.layout = QVBoxLayout(self)

        #Scrollable 
        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area.setFixedSize(width, length) 
        
        self.scroll_widget = QWidget()
        self.task_container = QVBoxLayout(self.scroll_widget)
        
        self.scroll_area.setWidget(self.scroll_widget)

        # Add Task Button
        self.add_task_btn = QPushButton("Add Task")
        self.add_task_btn.clicked.connect(self.add_task)

        self.task_container.setSpacing(0)
        self.task_container.setAlignment(Qt.AlignTop)  
        self.layout.setSpacing(0)

        self.layout.addWidget(self.add_task_btn)
        self.layout.addWidget(self.scroll_area)

    def add_task(self):
        """Adds a new task with a circle button, text box, and status label."""

        task_frame = QFrame()
        # task_frame.setFrameShape(QFrame.Box)
        task_frame.setFixedHeight(70)
        task_frame.setStyleSheet("background-color: #F7F7F7; padding: 5px;")

        task_layout = QHBoxLayout(task_frame)

        # Circle Button (Leftmost)
        circle_btn = QPushButton("●")
        circle_btn.setFixedSize(20, 20)
        circle_btn.setStyleSheet("color: gray; border: none; font-size: 18px;")
        circle_btn.clicked.connect(lambda: self.toggle_status(status_label))

        # Task Input Field
        task_input = QLineEdit()
        task_input.setPlaceholderText("Enter your task here...")
        task_input.setFont(QFont("Arial", 12))

        task_input.setStyleSheet(
            """
            QLineEdit {
                border: 1px solid white;
                border-radius: 4px;
                padding: 5px;
                font-size: 12px;
                color: black;
                outline: none; /* Prevents the blue border */
            }
            QLineEdit:focus {
                border: 1px solid gray; /* Keeps the same border when clicked */
                outline: none;
            }
        """
        )

        # Status Label (Rightmost)
        status_label = QLabel("In Progress")
        status_label.setFont(QFont("Arial", 12))
        status_label.setStyleSheet("color: green;")

        cancel_btn = QPushButton("x")
        cancel_btn.setFixedSize(30, 30)
        cancel_btn.setStyleSheet("color: gray; border: none; font-size: 18px;")
        cancel_btn.clicked.connect(lambda: self.delete_task(task_frame))

        separator = QFrame()
        separator.setFrameShape(QFrame.HLine)

        task_layout.addWidget(circle_btn)
        task_layout.addWidget(task_input)
        task_layout.addWidget(status_label)
        task_layout.addWidget(cancel_btn)
        task_layout.addWidget(separator)

        self.task_container.insertWidget(self.task_container.count(), task_frame)
        # spacer = QSpacerItem(0, 0, QSizePolicy.Minimum, QSizePolicy.Fixed)
        # self.task_container.addItem(spacer)

    def toggle_status(self, label):
        """Toggles the status between 'In Progress' (green) and 'Done' (red)."""
        if label.text() == "In Progress":
            label.setText("Done")
            label.setStyleSheet("color: red;")
        else:
            label.setText("In Progress")
            label.setStyleSheet("color: green;")

    def delete_task(self, task_frame):
        for i in reversed(range(self.task_container.count())): 
            item = self.task_container.itemAt(i)
            if item.widget() == task_frame: 
                item.widget().deleteLater()
                break

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
