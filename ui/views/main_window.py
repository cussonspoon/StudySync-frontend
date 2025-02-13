# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'study-sync.ui'
##
## Created by: Qt User Interface Compiler version 6.8.0
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale, QDir, 
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
    QFont, QFontDatabase, QGradient, QIcon,
    QImage, QKeySequence, QLinearGradient, QPainter,
    QPalette, QPixmap, QRadialGradient, QTransform)
from PySide6.QtWidgets import (QApplication, QFrame, QLabel, QMainWindow,
    QPushButton, QScrollArea, QScrollBar, QSizePolicy, QStackedWidget,
    QWidget)



from ui.views.home import HomePage
from ui.views.collection import CollectionPage
from ui.views.statistic import StatPage
from ui.views.notification import NotificationPage
from ui.views.community import CommunityPage

from enum import Enum

class Page(Enum): 
    HOME = 1
    COLLECTION = 2
    STAT = 3
    NOTIFICATION = 4
    COMMUNITY = 5


class Ui_MainWindow(object):

    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(1228, 831)
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.sidebar = QFrame(self.centralwidget)
        self.sidebar.setObjectName(u"sidebar")
        self.sidebar.setGeometry(QRect(0, 0, 91, 831))
        self.sidebar.setFrameShape(QFrame.Shape.StyledPanel)
        self.sidebar.setFrameShadow(QFrame.Shadow.Raised)
        self.sidebar.setLineWidth(0)

        self.top = QFrame(self.sidebar)
        self.top.setObjectName(u"top")
        self.top.setGeometry(QRect(10, 10, 71, 121))
        self.top.setFrameShape(QFrame.Shape.NoFrame)
        self.top.setFrameShadow(QFrame.Shadow.Raised)

        self.logo = QLabel(self.top)
        self.logo.setObjectName(u"logo")
        self.logo.setGeometry(QRect(10, 10, 61, 71))
        img_path = QDir.currentPath() + "/static/images/logo.png"
        self.logo.setPixmap(QPixmap(img_path))
        self.logo.setScaledContents(True)
        self.logo.setIndent(0)

        self.menus = QFrame(self.sidebar)
        self.menus.setObjectName(u"menus")
        self.menus.setGeometry(QRect(10, 140, 71, 471))
        font = QFont()
        font.setKerning(True)
        self.menus.setFont(font)
        self.menus.setFrameShape(QFrame.Shape.NoFrame)
        self.menus.setFrameShadow(QFrame.Shadow.Raised)
        self.menus.setLineWidth(0)

        self.home = QPushButton(self.menus)
        self.home.setObjectName(u"home")
        self.home.setGeometry(QRect(10, 20, 51, 61))
        icon = QIcon()
        img_path = QDir.currentPath() + "/static/images/home.png"
        icon.addFile(img_path, QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.home.setIcon(icon)
        self.home.setIconSize(QSize(50, 50))

        self.collection = QPushButton(self.menus)
        self.collection.setObjectName(u"collection")
        self.collection.setGeometry(QRect(10, 110, 51, 61))
        icon1 = QIcon()
        img_path = QDir.currentPath() + "/static/images/collection.png"
        icon1.addFile(img_path, QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.collection.setIcon(icon1)
        self.collection.setIconSize(QSize(50, 50))

        self.stats = QPushButton(self.menus)
        self.stats.setObjectName(u"stats")
        self.stats.setGeometry(QRect(10, 200, 51, 61))
        icon2 = QIcon()
        img_path = QDir.currentPath() + "/static/images/stat.png"
        icon2.addFile(img_path, QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.stats.setIcon(icon2)
        self.stats.setIconSize(QSize(50, 50))

        self.noti = QPushButton(self.menus)
        self.noti.setObjectName(u"noti")
        self.noti.setGeometry(QRect(10, 290, 51, 61))
        icon3 = QIcon()
        img_path = QDir.currentPath() + "/static/images/noti.png"
        icon3.addFile(img_path, QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.noti.setIcon(icon3)
        self.noti.setIconSize(QSize(50, 50))

        self.community = QPushButton(self.menus)
        self.community.setObjectName(u"community")
        self.community.setGeometry(QRect(10, 380, 51, 61))
        icon4 = QIcon()
        img_path = QDir.currentPath() + "/static/images/community.png"
        icon4.addFile(img_path, QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.community.setIcon(icon4)
        self.community.setIconSize(QSize(50, 50))

        self.bottom = QFrame(self.sidebar)
        self.bottom.setObjectName(u"bottom")
        self.bottom.setGeometry(QRect(10, 620, 71, 141))
        self.bottom.setFrameShape(QFrame.Shape.NoFrame)
        self.bottom.setFrameShadow(QFrame.Shadow.Raised)

        self.logout = QPushButton(self.bottom)
        self.logout.setObjectName(u"logout")
        self.logout.setGeometry(QRect(0, 70, 71, 61))
        icon5 = QIcon()
        img_path = QDir.currentPath() + "/static/images/logout.png"
        icon5.addFile(img_path, QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.logout.setIcon(icon5)
        self.logout.setIconSize(QSize(50, 50))

        self.contentArea = QStackedWidget(self.centralwidget)
        self.contentArea.setGeometry(QRect(90, 0, 1138, 831))
        self.contentArea.setObjectName("contentArea")
        # self.setStyleSheet("background-color: #F8F6F1; ")


        self.page_home = HomePage()
        self.page_home.setObjectName("homePage")

        self.page_home_scroll = QScrollArea()
        self.page_home_scroll.setWidgetResizable(True)
        self.page_home_scroll.setWidget(self.page_home)

        self.page_collection_scroll = QScrollArea()
        self.page_collection_scroll.setWidgetResizable(True)
        self.page_collection = CollectionPage()
        self.page_collection.setObjectName("collectionPage")
        self.page_collection_scroll.setWidget(self.page_collection)

        self.page_stats_scroll = QScrollArea()
        self.page_stats_scroll.setWidgetResizable(True)
        self.page_stats = StatPage()
        self.page_stats.setObjectName("statsPage")
        self.page_stats_scroll.setWidget(self.page_stats)

        self.page_noti_scroll = QScrollArea()
        self.page_noti_scroll.setWidgetResizable(True)
        self.page_noti = NotificationPage()
        self.page_noti.setObjectName("notification")
        self.page_noti_scroll.setWidget(self.page_noti)

        self.page_community_scroll = QScrollArea()
        self.page_community_scroll.setWidgetResizable(True)
        self.page_community = CommunityPage()
        self.page_community.setObjectName("communityPage")
        self.page_community_scroll.setWidget(self.page_community)

        self.contentArea.addWidget(self.page_home_scroll)
        self.contentArea.addWidget(self.page_collection_scroll)
        self.contentArea.addWidget(self.page_stats_scroll)
        self.contentArea.addWidget(self.page_noti_scroll)
        self.contentArea.addWidget(self.page_community_scroll)

        MainWindow.setCentralWidget(self.centralwidget)

        self.home.clicked.connect(lambda: self.switchPage(Page.HOME))
        self.collection.clicked.connect(lambda: self.switchPage(Page.COLLECTION))
        self.stats.clicked.connect(lambda: self.switchPage(Page.STAT))
        self.noti.clicked.connect(lambda: self.switchPage(Page.NOTIFICATION))
        self.community.clicked.connect(lambda: self.switchPage(Page.COMMUNITY))

        self.retranslateUi(MainWindow)
        QMetaObject.connectSlotsByName(MainWindow)

    def switchPage(self, page: Page): 
        self.contentArea.setCurrentIndex(page.value - 1)


    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"MainWindow", None))
        self.logo.setText("")
        self.home.setText("")
        self.collection.setText("")
        self.stats.setText("")
        self.noti.setText("")
        self.community.setText("")
        self.logout.setText("")
    # retranslateUi

    






