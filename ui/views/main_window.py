# -*- coding: utf-8 -*-

from PySide6.QtCore import QCoreApplication, QDir, QMetaObject, QRect, QSize
from PySide6.QtGui import QFont, QIcon, QPixmap
from PySide6.QtWidgets import (
    QFrame,
    QLabel,
    QPushButton,
    QScrollArea,
    QStackedWidget,
    QWidget,
    QMainWindow,
)

from ui.views.home import HomePage
from ui.views.collection import CollectionPage
from ui.views.statistic import StatPage
from ui.views.notification import NotificationPage
from ui.views.community import CommunityPage
from ui.views.folder import FolderDetailPage


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1300, 831)
        MainWindow.setMinimumSize(QSize(1300, 831))
        MainWindow.setMaximumSize(QSize(1300, 831))

        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")

        self.sidebar = QFrame(self.centralwidget)
        self.sidebar.setGeometry(QRect(0, 0, 91, 831))
        self.sidebar.setFrameShape(QFrame.Shape.StyledPanel)
        self.sidebar.setObjectName("sidebar")
        self.sidebar.setStyleSheet(
            """
            QFrame {
                background-color: #F8F6F1;
            }
            """
        )

        self.top = QFrame(self.sidebar)
        self.top.setGeometry(QRect(10, 10, 71, 121))
        self.top.setFrameShape(QFrame.Shape.NoFrame)
        self.top.setObjectName("top")

        self.logo = QLabel(self.top)
        self.logo.setGeometry(QRect(10, 10, 61, 71))
        img_path = QDir.currentPath() + "/static/images/logo.png"
        self.logo.setPixmap(QPixmap(img_path))
        self.logo.setScaledContents(True)
        self.logo.setObjectName("logo")

        self.menus = QFrame(self.sidebar)
        self.menus.setGeometry(QRect(10, 140, 71, 471))
        self.menus.setFrameShape(QFrame.Shape.NoFrame)
        self.menus.setObjectName("menus")
        font = QFont()
        font.setKerning(True)
        self.menus.setFont(font)

        # Menu buttons
        self.home = self.createMenuButton("home", "home.png", QRect(10, 20, 51, 61))
        self.collection = self.createMenuButton(
            "collection", "collection.png", QRect(10, 110, 51, 61)
        )
        self.stats = self.createMenuButton("stats", "stat.png", QRect(10, 200, 51, 61))
        self.noti = self.createMenuButton("noti", "noti.png", QRect(10, 290, 51, 61))
        self.community = self.createMenuButton(
            "community", "community.png", QRect(10, 380, 51, 61)
        )

        # Add test button to sidebar
        self.test_folder = QPushButton(self.menus)
        self.test_folder.setText("Test Folder")
        self.test_folder.setGeometry(QRect(10, 470, 51, 61))
        self.test_folder.setObjectName("test_folder")
        self.test_folder.setStyleSheet(
            """
            QPushButton {
                background-color: #87db8a;
                border: none;
                border-radius: 10px;
                padding: 5px;
                color: black;
                font-size: 10px;
            }
            QPushButton:hover {
                background-color: #79AD47;
            }
        """
        )

        self.bottom = QFrame(self.sidebar)
        self.bottom.setGeometry(QRect(10, 620, 71, 141))
        self.bottom.setFrameShape(QFrame.Shape.NoFrame)
        self.bottom.setObjectName("bottom")

        self.logout = QPushButton(self.bottom)
        self.logout.setGeometry(QRect(0, 70, 71, 61))
        icon = QIcon()
        img_path = QDir.currentPath() + "/static/images/logout.png"
        icon.addFile(img_path, QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.logout.setIcon(icon)
        self.logout.setIconSize(QSize(50, 50))
        self.logout.setObjectName("logout")

        # Content Area
        self.contentArea = QStackedWidget(self.centralwidget)
        self.contentArea.setGeometry(QRect(90, 0, 1300, 831))
        self.contentArea.setObjectName("contentArea")

        # Pages
        self.page_home_scroll = self.createScrollPage(HomePage())
        self.page_collection_scroll = self.createScrollPage(CollectionPage())
        self.page_stats_scroll = self.createScrollPage(StatPage())
        self.page_noti_scroll = self.createScrollPage(NotificationPage())
        self.page_community_scroll = self.createScrollPage(CommunityPage())
        self.page_folder_scroll = self.createScrollPage(FolderDetailPage())

        self.contentArea.addWidget(self.page_home_scroll)
        self.contentArea.addWidget(self.page_collection_scroll)
        self.contentArea.addWidget(self.page_stats_scroll)
        self.contentArea.addWidget(self.page_noti_scroll)
        self.contentArea.addWidget(self.page_community_scroll)
        self.contentArea.addWidget(self.page_folder_scroll)

        # Connect back button in FolderDetailPage to return to collection
        folder_page = self.page_folder_scroll.widget()
        back_btn = folder_page.findChild(QPushButton)
        if back_btn:
            back_btn.clicked.connect(
                lambda: self.contentArea.setCurrentWidget(self.page_collection_scroll)
            )

        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)
        QMetaObject.connectSlotsByName(MainWindow)

    def createMenuButton(self, name, icon_file, geometry):
        button = QPushButton(self.menus)
        button.setObjectName(name)
        button.setGeometry(geometry)
        icon = QIcon()
        img_path = QDir.currentPath() + f"/static/images/{icon_file}"
        icon.addFile(img_path, QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        button.setIcon(icon)
        button.setIconSize(QSize(50, 50))

        # Add hover effect with shadow
        button.setStyleSheet(
            f"""
            QPushButton {{
                background-color: transparent;
                border: none;
                border-radius: 10px;
                padding: 5px;
            }}
            QPushButton:hover {{
                background-color: grey;
                border-radius: 10px;
                qproperty-icon: url({img_path});
                box-shadow: 0 2px 5px rgba(0, 0, 0, 0.2);
            }}
            QPushButton:pressed {{
                background-color: grey;
            }}
        """
        )
        return button

    def createScrollPage(self, pageWidget):
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setWidget(pageWidget)
        return scroll

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(
            QCoreApplication.translate("MainWindow", "Study Sync", None)
        )
        self.logo.setText("")
        self.home.setText("")
        self.collection.setText("")
        self.stats.setText("")
        self.noti.setText("")
        self.community.setText("")
        self.logout.setText("")

        self.logout.setText("")


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        # Connect menu buttons
        self.ui.home.clicked.connect(
            lambda: self.ui.contentArea.setCurrentWidget(self.ui.page_home_scroll)
        )
        self.ui.collection.clicked.connect(
            lambda: self.ui.contentArea.setCurrentWidget(self.ui.page_collection_scroll)
        )
        self.ui.stats.clicked.connect(
            lambda: self.ui.contentArea.setCurrentWidget(self.ui.page_stats_scroll)
        )
        self.ui.noti.clicked.connect(
            lambda: self.ui.contentArea.setCurrentWidget(self.ui.page_noti_scroll)
        )
        self.ui.community.clicked.connect(
            lambda: self.ui.contentArea.setCurrentWidget(self.ui.page_community_scroll)
        )

        # Connect test folder button directly to page switch
        self.ui.test_folder.clicked.connect(
            lambda: self.ui.contentArea.setCurrentWidget(self.ui.page_folder_scroll)
        )

        # Initialize folder page only once
        self.folder_page = FolderDetailPage()
        self.ui.page_folder_scroll.setWidget(self.folder_page)

        # Get the CollectionPage widget and connect folder click
        collection_page = self.ui.page_collection_scroll.widget()
        collection_page.folder_clicked.connect(self.show_folder_page)

    def show_folder_page(self):
        print("Showing folder page")
        self.ui.contentArea.setCurrentWidget(self.ui.page_folder_scroll)
