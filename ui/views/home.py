import sys
import os
from PySide6.QtCore import Qt, QDir
from PySide6.QtGui import QFont, QPixmap
from PySide6.QtWidgets import (
    QApplication,
    QMainWindow,
    QFrame,
    QLabel,
    QScrollArea,
    QWidget,
    QPushButton,
    QVBoxLayout,
    QHBoxLayout,
    QLineEdit,
    QLabel,
    QFrame,
    QScrollArea,
    QSizePolicy,
    QSpacerItem,
)

from ui.views.components.carousel import HorizontalImageScroller
from utils.ui import Text, Image, SearchBar


class HomePage(QWidget):
    def __init__(self):
        super().__init__()
        self.setupUi()

    def setupUi(self):
        self.setObjectName("Form")
        self.setStyleSheet("background-color: #FAFAFA;")

        self.searchFrame = QFrame(self)
        self.searchFrame.setFixedHeight(111)
        self.searchFrame.setStyleSheet(
            "background-color:  #F8F6F1; margin: 0px; padding: 0px;"
        )

        search_layout = QVBoxLayout(self.searchFrame)
        search_layout.setAlignment(Qt.AlignCenter)
        self.searchBar = SearchBar(self.searchFrame)
        search_layout.addWidget(self.searchBar)
        self.searchFrame.setLayout(search_layout)

        self.scrollArea = QScrollArea(self)
        self.scrollArea.setWidgetResizable(True)
        self.scrollArea.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        self.scrollArea.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.scrollArea.setStyleSheet("background-color: #F8F6F1;")

        self.scrollAreaWidgetContents = QWidget()
        self.scroll_layout = QVBoxLayout(self.scrollAreaWidgetContents)
        self.scroll_layout.setAlignment(Qt.AlignTop)
        self.scroll_layout.setSpacing(10)

        self.bannerFrame = QFrame(self.scrollAreaWidgetContents)
        self.bannerFrame.setFixedSize(1171, 360)
        self.bannerLayout = QVBoxLayout(self.bannerFrame)
        self.bannerLayout.setContentsMargins(0, 0, 0, 0)
        self.bannerFrame.setStyleSheet("margin: 0px;")
        self.bannerLayout.setAlignment(Qt.AlignTop)

        self.bannerPic = Image(1171, 291, "banner.jpg", self.bannerFrame)
        self.bannerLayout.addWidget(self.bannerPic)

        self.profilePic = Image(91, 91, "profile.jpg", self.bannerFrame)
        self.profilePic.move(30, 250)  # Adjust overlap

        self.bannerPic.setStyleSheet("margin: 0px; padding: 0px;")
        self.profilePic.setStyleSheet("margin: 0px; padding: 0px;")

        self.bannerFrame.setLayout(self.bannerLayout)
        self.scroll_layout.addWidget(self.bannerFrame)
        self.bannerFrame.setStyleSheet("background-color: transparent;")

        # spacing_banner = QFrame(self.scrollAreaWidgetContents)
        # spacing_banner.setFixedHeight(20)  # 20px spacing
        # self.scroll_layout.addWidget(spacing_banner)

        collection_layout = QHBoxLayout()
        self.collectionIcon = Image(
            155, 101, "collectionIcon.png", self.scrollAreaWidgetContents
        )
        self.collectionText = Text(
            21, "My Collections", "333333", self.scrollAreaWidgetContents
        )

        collection_layout.addWidget(self.collectionText)
        collection_layout.addWidget(self.collectionIcon)
        collection_layout.addStretch()  # Pushes content to the left

        collection_container = QFrame(self.scrollAreaWidgetContents)
        collection_container.setLayout(collection_layout)
        self.scroll_layout.addWidget(collection_container)

        self.collections = HorizontalImageScroller(self.scrollAreaWidgetContents)
        self.scroll_layout.addWidget(self.collections)

        spacing_collections = QFrame(self.scrollAreaWidgetContents)
        spacing_collections.setFixedHeight(20)  # 20px spacing
        self.scroll_layout.addWidget(spacing_collections)

        self.recommendsText = Text(
            21, "Recommended folders for you", "333333", self.scrollAreaWidgetContents
        )
        self.scroll_layout.addWidget(self.recommendsText)

        self.recommendFolders = HorizontalImageScroller(self.scrollAreaWidgetContents)
        self.scroll_layout.addWidget(self.recommendFolders)

        spacing_recommended = QFrame(self.scrollAreaWidgetContents)
        spacing_recommended.setFixedHeight(20)  # 20px spacing
        self.scroll_layout.addWidget(spacing_recommended)

        task_layout = QHBoxLayout()
        self.taskText = Text(21, "Task", "333333", self.scrollAreaWidgetContents)
        self.taskImg = Image(141, 130, "task.png", self.scrollAreaWidgetContents)

        task_layout.addWidget(self.taskText)
        task_layout.addWidget(self.taskImg)
        task_layout.addStretch()

        task_container = QFrame(self.scrollAreaWidgetContents)
        task_container.setLayout(task_layout)
        self.scroll_layout.addWidget(task_container)

        self.taskManagement = TaskManagement(
            50, 1180, 800, 700, self.scrollAreaWidgetContents
        )
        self.taskManagement.setMinimumHeight(400)
        self.scroll_layout.addWidget(self.taskManagement)

        self.scrollAreaWidgetContents.setLayout(self.scroll_layout)
        self.scrollArea.setWidget(self.scrollAreaWidgetContents)

        main_layout = QVBoxLayout(self)
        main_layout.addWidget(self.searchFrame)
        main_layout.addWidget(self.scrollArea)
        self.setLayout(main_layout)

    def update_scroll_height(self):
        """Adjusts the scroll area height when tasks are added."""
        total_height = self.scroll_layout.sizeHint().height() + 20  # Add extra padding
        self.scrollAreaWidgetContents.setMinimumHeight(total_height)


class TaskManagement(QWidget):
    def __init__(self, pos_x, pos_y, width, length, parent=None):
        super().__init__(parent)
        self.setWindowTitle("To-Do List")
        self.setGeometry(pos_x, pos_y, width, length)
        self.setFixedSize(width, length)

        self.layout = QVBoxLayout(self)

        # Scrollable
        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)
        # self.scroll_area.setFixedSize(width - 50, length - 100)

        self.scroll_widget = QWidget()
        self.task_container = QVBoxLayout(self.scroll_widget)

        self.scroll_area.setWidget(self.scroll_widget)

        # Add Task Button
        self.add_task_btn = QPushButton("+ Add Task")
        self.add_task_btn.clicked.connect(self.add_task)

        self.add_task_btn.setStyleSheet(
            """
            QPushButton {
                background: transparent;  
                border: none;             
                font-size: 16px;         
                color: grey;          
                padding: 5px;           
                text-align: left;
            }
            QPushButton:hover {
                color: green;           
            }
        """
        )

        self.task_container.setSpacing(2)
        self.task_container.setAlignment(Qt.AlignTop)
        self.layout.setSpacing(0)

        self.layout.addWidget(self.add_task_btn)
        self.layout.addWidget(self.scroll_area)

    def add_task(self):

        task_frame = QFrame()
        task_frame.setObjectName("taskFrame")
        task_frame.setFixedHeight(50)
        task_frame.setStyleSheet("background-color: #F1F0E9; padding: 2px;")

        task_layout = QHBoxLayout(task_frame)

        circle_btn = QPushButton("●")
        circle_btn.setFixedSize(20, 20)
        circle_btn.setStyleSheet("color: gray; border: none; font-size: 18px;")
        circle_btn.clicked.connect(lambda: self.toggle_status(status_label))

        task_input = QLineEdit()
        task_input.setPlaceholderText("Enter your task here...")
        task_input.setFont(QFont("Arial", 12))

        task_input.setStyleSheet(
            """
            QLineEdit {
                border: none; 
                padding: 5px;
                font-size: 12px;
                color: black;
                outline: none; 
            }
            QLineEdit:focus {
                border: 1px solid #BDB395; 
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
        separator.setStyleSheet("background-color: #BDB395; height: 1px; border: none;")

        task_layout.addWidget(circle_btn)
        task_layout.addWidget(task_input)
        task_layout.addWidget(status_label)
        task_layout.addWidget(cancel_btn)
        task_layout.addWidget(separator)

        self.task_container.insertWidget(self.task_container.count(), task_frame)

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


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("StudySync Dashboard")  # Set Window Title
        self.setGeometry(100, 100, 1200, 771)  # Set Window Size
        self.ui = HomePage()
        self.setCentralWidget(self.ui)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
