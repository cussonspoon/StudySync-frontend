
import sys
import os
from PySide6.QtCore import Qt, QDir
from PySide6.QtGui import QFont, QPixmap
from PySide6.QtWidgets import QApplication, QMainWindow, QFrame, QLabel, QScrollArea, QWidget

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

        # 📌 Banner Image
        self.bannerPic = QLabel(self.scrollAreaWidgetContents)
        self.bannerPic.setObjectName("bannerPic")
        self.bannerPic.setGeometry(10, 0, 1171, 291)
        img_path = os.path.join(QDir.currentPath(), "static/images/banner.jpg")
        self.load_image(self.bannerPic, img_path, 1171, 291)

        # 📌 Profile Picture
        self.profilePic = QLabel(self.scrollAreaWidgetContents)
        self.profilePic.setObjectName("profilePic")
        self.profilePic.setGeometry(50, 240, 91, 91)
        img_path = os.path.join(QDir.currentPath(), "static/images/profile.jpg")
        self.load_image(self.profilePic, img_path, 91, 91)

        # 📌 Collection Text
        self.collectionText = QLabel(self.scrollAreaWidgetContents)
        self.collectionText.setObjectName("collectionText")
        self.collectionText.setGeometry(30, 360, 170, 30)
        font = QFont()
        font.setPointSize(21)
        self.collectionText.setFont(font)
        self.collectionText.setText("My Collections")
        self.collectionText.setStyleSheet("color: #333333;")

        # 📌 Collection Icon
        self.collectionIcon = QLabel(self.scrollAreaWidgetContents)
        self.collectionIcon.setObjectName("collectionIcon")
        self.collectionIcon.setGeometry(200, 320, 141, 101)
        img_path = os.path.join(QDir.currentPath(), "static/images/collectionIcon.png")
        self.load_image(self.collectionIcon, img_path, 141, 101)

        # 📌 Horizontal Image Scroller (Carousel)
        self.collections = HorizontalImageScroller(self.scrollAreaWidgetContents)
        self.collections.setGeometry(10, 430, 1180, 250)

        # 📌 Recommended Section
        self.recommendsText = QLabel(self.scrollAreaWidgetContents)
        self.recommendsText.setObjectName("recommendsText")
        self.recommendsText.setGeometry(30, 710, 350, 30)  # Adjusted Y position to follow carousel
        font = QFont()
        font.setPointSize(21)
        self.recommendsText.setFont(font)
        self.recommendsText.setText("Recommended folder for you")
        self.recommendsText.setStyleSheet("color: #333333;")

        self.recommendFolders = HorizontalImageScroller(self.scrollAreaWidgetContents)
        self.recommendFolders.setGeometry(10, 780, 1180, 250)

        self.taskText = Text(30, 1090, 21, "Task", "333333", self.scrollAreaWidgetContents)
        self.taskImg = Image(90, 1050, 141, 101, "task.png", self.scrollAreaWidgetContents)

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

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
