# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'Dashboardp.ui'
##
## Created by: Qt User Interface Compiler version 6.8.0
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (
    QCoreApplication,
    QDate,
    QDateTime,
    QLocale,
    QMetaObject,
    QObject,
    QPoint,
    QRect,
    QSize,
    QTime,
    QUrl,
    Qt,
    QDir,
)
from PySide6.QtGui import (
    QBrush,
    QColor,
    QConicalGradient,
    QCursor,
    QFont,
    QFontDatabase,
    QGradient,
    QIcon,
    QImage,
    QKeySequence,
    QLinearGradient,
    QPainter,
    QPalette,
    QPixmap,
    QRadialGradient,
    QTransform,
    QPainterPath,
)
from PySide6.QtWidgets import (
    QApplication,
    QFrame,
    QLabel,
    QLineEdit,
    QScrollArea,
    QSizePolicy,
    QWidget,
)


class HomePage(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUi()

    def setCircularImage(self, img_path, size):
        """Load an image and apply a circular mask"""
        pixmap = QPixmap(img_path).scaled(
            size.width(),
            size.height(),
            Qt.KeepAspectRatioByExpanding,
            Qt.SmoothTransformation,
        )
        circular_pixmap = QPixmap(size.width(), size.height())
        circular_pixmap.fill(Qt.transparent)

        # Create circular mask
        painter = QPainter(circular_pixmap)
        painter.setRenderHint(QPainter.Antialiasing)
        path = QPainterPath()
        path.addEllipse(0, 0, size.width(), size.height())
        painter.setClipPath(path)
        painter.drawPixmap(0, 0, pixmap)
        painter.end()

        # Set the processed circular image to QLabel
        self.Profilepic.setPixmap(circular_pixmap)

    def setupUi(self):
        self.setObjectName("HomePage")
        self.setEnabled(False)
        self.resize(1300, 831)
        self.setMinimumSize(QSize(0, 0))

        # scrollArea
        self.scrollArea = QScrollArea(self)
        self.scrollArea.setObjectName("scrollArea")
        self.scrollArea.setGeometry(QRect(10, 90, 1281, 771))
        self.scrollArea.setWidgetResizable(True)
        self.scrollAreaWidgetContents = QWidget()
        self.scrollAreaWidgetContents.setObjectName("scrollAreaWidgetContents")
        self.scrollAreaWidgetContents.setGeometry(QRect(0, 0, 1279, 769))

        self.Banner = QLabel(self.scrollAreaWidgetContents)
        self.Banner.setObjectName("Banner")
        self.Banner.setGeometry(QRect(0, 0, 1281, 331))
        img_path = QDir.currentPath() + "/static/images/banner.jpg"
        self.Banner.setPixmap(QPixmap(img_path))

        self.Profilepic = QLabel(self.scrollAreaWidgetContents)
        self.Profilepic.setObjectName("Profilepic")
        self.Profilepic.setGeometry(QRect(60, 280, 111, 111))
        img_path = QDir.currentPath() + "/static/images/profile.jpg"
        self.setCircularImage(img_path, QSize(111, 111))
        # self.Profilepic.setPixmap(QPixmap(img_path))
        # self.Profilepic.setScaledContents(True)

        self.collectionFrame = QFrame(self.scrollAreaWidgetContents)
        self.collectionFrame.setObjectName("collectionFrame")
        self.collectionFrame.setGeometry(QRect(0, 400, 1281, 341))
        self.collectionFrame.setFrameShape(QFrame.Shape.StyledPanel)
        self.collectionFrame.setFrameShadow(QFrame.Shadow.Raised)

        self.collectionTopic = QFrame(self.collectionFrame)
        self.collectionTopic.setObjectName("collectionTopic")
        self.collectionTopic.setGeometry(QRect(40, 9, 301, 101))
        self.collectionTopic.setFrameShape(QFrame.Shape.StyledPanel)
        self.collectionTopic.setFrameShadow(QFrame.Shadow.Raised)

        self.collectionText = QLabel(self.collectionTopic)
        self.collectionText.setObjectName("collectionText")
        self.collectionText.setGeometry(QRect(10, 20, 131, 61))

        self.collectionIcon = QLabel(self.collectionTopic)
        self.collectionIcon.setObjectName("collectionIcon")
        self.collectionIcon.setGeometry(QRect(150, 0, 141, 91))
        self.collectionIcon.setPixmap(QPixmap("collection.png"))
        self.collectionIcon.setScaledContents(True)

        self.foldersFrame = QFrame(self.collectionFrame)
        self.foldersFrame.setObjectName("foldersFrame")
        self.foldersFrame.setGeometry(QRect(40, 110, 1241, 80))
        self.foldersFrame.setFrameShape(QFrame.Shape.StyledPanel)
        self.foldersFrame.setFrameShadow(QFrame.Shadow.Raised)

        self.recommendedFrame = QFrame(self.collectionFrame)
        self.recommendedFrame.setObjectName("recommendedFrame")
        self.recommendedFrame.setGeometry(QRect(40, 200, 1241, 131))
        self.recommendedFrame.setFrameShape(QFrame.Shape.StyledPanel)
        self.recommendedFrame.setFrameShadow(QFrame.Shadow.Raised)

        self.recommendText = QLabel(self.recommendedFrame)
        self.recommendText.setObjectName("recommendText")
        self.recommendText.setGeometry(QRect(10, 20, 251, 16))

        self.rFolders = QFrame(self.recommendedFrame)
        self.rFolders.setObjectName("rFolders")
        self.rFolders.setGeometry(QRect(10, 40, 1231, 81))
        self.rFolders.setFrameShape(QFrame.Shape.StyledPanel)
        self.rFolders.setFrameShadow(QFrame.Shadow.Raised)

        self.scrollArea.setWidget(self.scrollAreaWidgetContents)

        self.topbar = QFrame(self)
        self.topbar.setObjectName("topbar")
        self.topbar.setGeometry(QRect(10, 10, 1281, 80))
        self.topbar.setFrameShape(QFrame.Shape.StyledPanel)
        self.topbar.setFrameShadow(QFrame.Shadow.Raised)

        # self.searchBarFrame = QFrame(self.topbar)
        # self.searchBarFrame.setObjectName(u"searchBarFrame")
        # self.searchBarFrame.setGeometry(QRect(460, 20, 451, 41))
        # self.searchBarFrame.setFrameShape(QFrame.Shape.StyledPanel)
        # self.searchBarFrame.setFrameShadow(QFrame.Shadow.Raised)
        # self.searchBarFrame.setFocusPolicy(Qt.NoFocus)

        self.searchBarFrame = QFrame(self.topbar)
        self.searchBarFrame.setObjectName("searchBarFrame")
        self.searchBarFrame.setGeometry(QRect(460, 20, 451, 41))
        self.searchBarFrame.setFocusPolicy(Qt.ClickFocus)  # Fix blocking issue
        self.searchBarFrame.setAttribute(Qt.WA_TransparentForMouseEvents, False)

        self.searchIcon = QLabel(self.searchBarFrame)
        self.searchIcon.setObjectName("searchIcon")
        self.searchIcon.setGeometry(QRect(0, 0, 51, 41))
        img_path = QDir.currentPath() + "/static/images/search.png"
        self.searchIcon.setPixmap(QPixmap(img_path))
        self.searchIcon.setScaledContents(True)

        # self.lineEdit = QLineEdit(self.searchBarFrame)
        # self.lineEdit.setObjectName(u"searchInput")
        # self.lineEdit.setGeometry(QRect(50, 0, 381, 41))
        # self.lineEdit.setFrame(False)
        # self.lineEdit.setClearButtonEnabled(True)
        # self.lineEdit.setFocusPolicy(Qt.StrongFocus)
        # self.lineEdit.setAttribute(Qt.WA_InputMethodEnabled)
        # self.lineEdit.setClearButtonEnabled(True)

        self.lineEdit = QLineEdit(self.searchBarFrame)
        self.lineEdit.setObjectName("searchInput")
        self.lineEdit.setGeometry(QRect(50, 0, 381, 41))
        self.lineEdit.setFocusPolicy(Qt.ClickFocus)  # Ensures it can receive input
        self.lineEdit.setAttribute(Qt.WA_InputMethodEnabled, True)  # Enables text input
        self.lineEdit.setClearButtonEnabled(True)  # Optional: Adds a clear button

        self.setStyleSheet(
            """
                           
            QFrame {
                border: 1px solid #aaa;
                background-color: #F8F6F1;
            }
                    
            QWidget {
                background-color: #F8F6F1;
            }

            QLabel {
                border: 1px solid #aaa;
            }
            
            #Banner {
                border-top-left-radius: 20px;
                border-top-right-radius: 20px;
                border-bottom-left-radius: 0px;
                border-bottom-right-radius: 0px;
                border: 0px solid #ccc;
                background-color: white;
            }
       
            #Profilepic {
                width: 111px; 
                height: 111px;
                border-radius: 50%;
                border: 2px solid #ccc;
                background-position: center;
                background-repeat: no-repeat;
                background-color: white;
            }
            
            #searchBarFrame {
                border: 2px solid #2596be;
                border-radius: 10px;
                padding: 5px;
                background-color: white;
            }
            
            #searchIcon {
               margin-left: 10px;
               margin-right: 5px;
            }
            
            #searchInput {
                border: 1px solid #ccc;
                background-color: white;
                font-size: 16px;
                padding: 5px 10px;
                color: black;
                min-height: 35px;
            }
                           
            QLineEdit{
                background: white;       
            }
                           
            #searchInput:focus {
                outline: none;
                border: 2px solid blue;
                background-color: #f0f8ff;
            }
            """
        )

        self.retranslateUi()

        QMetaObject.connectSlotsByName(self)

    # setupUi

    def retranslateUi(self):
        self.setWindowTitle(QCoreApplication.translate("HomePage", "Form", None))
        self.Banner.setText("")
        self.Profilepic.setText("")
        self.collectionText.setText(
            QCoreApplication.translate("HomePage", "My Collection", None)
        )
        self.collectionIcon.setText("")
        self.recommendText.setText(
            QCoreApplication.translate("HomePage", "Recommended folder for you", None)
        )
        self.lineEdit.setText("")

    # retranslateUi
