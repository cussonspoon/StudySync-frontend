# import sys
# import os
# from PySide6.QtCore import QCoreApplication, QMetaObject, QRect, Qt, QDir
# from PySide6.QtGui import QFont, QPixmap
# from PySide6.QtWidgets import QApplication, QMainWindow, QFrame, QLabel, QScrollArea, QWidget

# from ui.views.components.carousel import HorizontalImageScroller

# #task 
# # use painter to mask image to circle
# # add carousel to home page 
# class HomePage(QWidget):
#     def __init__(self):
#         super().__init__()
#         self.setupUi()

#     def setupUi(self):
#         self.setObjectName("Form")
#         self.resize(1200, 771)

#         self.setStyleSheet("background-color: #FAFAFA;")

#         # 📌 Scroll Area Setup
#         self.scrollArea = QScrollArea(self)
#         self.scrollArea.setObjectName("scrollArea")
#         self.scrollArea.setGeometry(QRect(0, 110, 1250, 800))
#         self.scrollArea.setWidgetResizable(True)

#         self.scrollAreaWidgetContents = QWidget()
#         self.scrollAreaWidgetContents.setObjectName("scrollAreaWidgetContents")
#         self.scrollAreaWidgetContents.setGeometry(QRect(0, 0, 1199, 659))

#         # 📌 Banner Image
#         self.bannerPic = QLabel(self.scrollAreaWidgetContents)
#         self.bannerPic.setObjectName("bannerPic")
#         self.bannerPic.setGeometry(QRect(10, 0, 1171, 291))
#         img_path = os.path.join(QDir.currentPath(), "static/images/banner.jpg")
#         self.load_image(self.bannerPic, img_path)

#         # 📌 Profile Picture
#         self.profilePic = QLabel(self.scrollAreaWidgetContents)
#         self.profilePic.setObjectName("profilePic")
#         self.profilePic.setGeometry(QRect(50, 240, 91, 91))
#         self.profilePic.setScaledContents(True)
#         img_path = os.path.join(QDir.currentPath(), "static/images/profile.jpg")
#         self.load_image(self.profilePic, img_path)

#         # 📌 Text Label
#         self.collectionText = QLabel(self.scrollAreaWidgetContents)
#         self.collectionText.setObjectName("collectionText")
#         self.collectionText.setGeometry(QRect(30, 370, 141, 21))
#         font = QFont()
#         font.setPointSize(21)
#         self.collectionText.setFont(font)
#         self.collectionText.setText("My Collections")
#         self.collectionText.setStyleSheet("color: #333333;")

#         # 📌 Collection Icon
#         self.collectionIcon = QLabel(self.scrollAreaWidgetContents)
#         self.collectionIcon.setObjectName("collectionIcon")
#         self.collectionIcon.setGeometry(QRect(200, 320, 141, 101))
#         self.collectionIcon.setScaledContents(True)
#         img_path = os.path.join(QDir.currentPath(), "static/images/collectionIcon.png")
#         self.load_image(self.collectionIcon, img_path)

#         # 📌 Content Frame
#         # self.folder_frame = QFrame(self.scrollAreaWidgetContents)
#         # self.folder_frame.setObjectName("folder_frame")
#         # self.folder_frame.setGeometry(QRect(10, 430, 1200, 200))
#         # self.folder_frame.setFrameShape(QFrame.Shape.StyledPanel)
#         # self.folder_frame.setFrameShadow(QFrame.Shadow.Raised)

#         # self.horizontalScroller = HorizontalImageScroller(self.folder_frame)
#         self.horizontalScroller = HorizontalImageScroller(self.scrollAreaWidgetContents)
#         self.horizontalScroller.setGeometry(QRect(10, 430, 1220, 450))


#         self.label4 = QLabel(self.scrollAreaWidgetContents)
#         self.label4.setObjectName("label4")
#         self.label4.setGeometry(QRect(30, 890, 141, 21))
#         font = QFont()
#         font.setPointSize(21)
#         self.label4.setFont(font)
#         self.label4.setText("Recommended")
        

#         # Add widget to Scroll Area
#         self.scrollArea.setWidget(self.scrollAreaWidgetContents)

#         # 📌 Header Frame
#         self.searchFrame = QFrame(self)
#         self.searchFrame.setObjectName("searchFrame")
#         self.searchFrame.setGeometry(QRect(-1, 0, 1250, 111))
#         self.searchFrame.setFrameShape(QFrame.Shape.StyledPanel)
#         self.searchFrame.setFrameShadow(QFrame.Shadow.Raised)

#         # 📌 Header Content Frame
#         self.searchBar = QFrame(self.searchFrame)
#         self.searchBar.setObjectName("searchBar")
#         self.searchBar.setGeometry(QRect(280, 30, 701, 51))
#         self.searchBar.setFrameShape(QFrame.Shape.StyledPanel)
#         self.searchBar.setFrameShadow(QFrame.Shadow.Raised)

#         QMetaObject.connectSlotsByName(self)

#     def load_image(self, label, path):
#         """Loads an image into a QLabel safely"""
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
#             label.setPixmap(pixmap)

# class MainWindow(QMainWindow):
#     def __init__(self):
#         super().__init__()
#         self.setWindowTitle("StudySync Dashboard")  # Set Window Title
#         self.setGeometry(100, 100, 1200, 771)  # Set Window Size
#         self.ui = HomePage()
#         self.setCentralWidget(self.ui)

# if __name__ == "__main__":
#     app = QApplication(sys.argv)
#     window = MainWindow()
#     window.show()
#     sys.exit(app.exec())

import sys
import os
from PySide6.QtCore import Qt, QDir
from PySide6.QtGui import QFont, QPixmap
from PySide6.QtWidgets import QApplication, QMainWindow, QFrame, QLabel, QScrollArea, QWidget

from ui.views.components.carousel import HorizontalImageScroller

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
        self.collectionText.setGeometry(30, 370, 141, 21)
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
        self.horizontalScroller = HorizontalImageScroller(self.scrollAreaWidgetContents)
        self.horizontalScroller.setGeometry(10, 430, 1220, 250)

        # 📌 Recommended Section
        self.label4 = QLabel(self.scrollAreaWidgetContents)
        self.label4.setObjectName("label4")
        self.label4.setGeometry(30, 710, 141, 21)  # Adjusted Y position to follow carousel
        font = QFont()
        font.setPointSize(21)
        self.label4.setFont(font)
        self.label4.setText("Recommended")
        self.label4.setStyleSheet("color: #333333;")

        # 📌 Ensure scrollable content height is correct
        self.scrollAreaWidgetContents.setMinimumHeight(900)
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
            pixmap = pixmap.scaled(width, height, Qt.KeepAspectRatio, Qt.SmoothTransformation)
            label.setPixmap(pixmap)

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
