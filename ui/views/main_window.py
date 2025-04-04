# -*- coding: utf-8 -*-

from PySide6.QtCore import QCoreApplication, QDir, QMetaObject, QSize, Qt
from PySide6.QtGui import QFont, QIcon, QPixmap
from PySide6.QtWidgets import (
    QFrame,
    QLabel,
    QPushButton,
    QScrollArea,
    QStackedWidget,
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
)

from ui.views.home import HomePage
from ui.views.collection import CollectionPage
from ui.views.statistic import StatPage
from ui.views.notification import NotificationPage
from ui.views.community import CommunityPage
from ui.views.user_profile import UserProfilePage
from utils.session_manager import SessionManager


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1300, 831)
        MainWindow.setMinimumSize(QSize(1300, 831))
        MainWindow.setMaximumSize(QSize(1300, 831))

        # Create main layout
        self.main_layout = QHBoxLayout(MainWindow)
        self.main_layout.setContentsMargins(0, 0, 0, 0)
        self.main_layout.setSpacing(0)

        # Create sidebar
        self.sidebar = QFrame(MainWindow)
        self.sidebar.setFixedWidth(91)  # Set fixed width for sidebar
        self.sidebar.setFrameShape(QFrame.Shape.StyledPanel)
        self.sidebar.setObjectName("sidebar")
        self.sidebar.setStyleSheet(
            """
            QFrame {
                background-color: #F8F6F1;
            }
            """
        )

        # Create sidebar layout
        self.sidebar_layout = QVBoxLayout(self.sidebar)
        self.sidebar_layout.setContentsMargins(10, 10, 10, 10)
        self.sidebar_layout.setSpacing(10)

        # Top section
        self.top = QFrame(self.sidebar)
        self.top.setFrameShape(QFrame.Shape.NoFrame)
        self.top.setObjectName("top")
        self.top_layout = QVBoxLayout(self.top)
        self.top_layout.setContentsMargins(0, 0, 0, 0)

        self.logo = QLabel(self.top)
        self.logo.setFixedSize(61, 71)
        img_path = QDir.currentPath() + "/static/images/logo.png"
        self.logo.setPixmap(QPixmap(img_path))
        self.logo.setScaledContents(True)
        self.logo.setObjectName("logo")
        self.top_layout.addWidget(self.logo, alignment=Qt.AlignCenter)
        self.sidebar_layout.addWidget(self.top)

        # Menu section
        self.menus = QFrame(self.sidebar)
        self.menus.setFrameShape(QFrame.Shape.NoFrame)
        self.menus.setObjectName("menus")
        self.menus_layout = QVBoxLayout(self.menus)
        self.menus_layout.setContentsMargins(0, 0, 0, 0)
        self.menus_layout.setSpacing(20)
        self.menus_layout.setAlignment(Qt.AlignCenter)  # Center the menu items

        # Menu buttons
        self.home = self.createMenuButton("home", "home.png")
        self.collection = self.createMenuButton("collection", "collection.png")
        self.stats = self.createMenuButton("stats", "stat.png")
        self.noti = self.createMenuButton("noti", "noti.png")
        self.community = self.createMenuButton("community", "community.png")

        # Add stretch before buttons to center them vertically
        self.menus_layout.addStretch()

        # Add buttons with center alignment
        self.menus_layout.addWidget(self.home, alignment=Qt.AlignCenter)
        self.menus_layout.addWidget(self.collection, alignment=Qt.AlignCenter)
        self.menus_layout.addWidget(self.stats, alignment=Qt.AlignCenter)
        self.menus_layout.addWidget(self.noti, alignment=Qt.AlignCenter)
        self.menus_layout.addWidget(self.community, alignment=Qt.AlignCenter)

        # Add stretch after buttons to center them vertically
        self.menus_layout.addStretch()

        self.sidebar_layout.addWidget(self.menus)

        # Bottom section
        self.bottom = QFrame(self.sidebar)
        self.bottom.setFrameShape(QFrame.Shape.NoFrame)
        self.bottom.setObjectName("bottom")
        self.bottom_layout = QVBoxLayout(self.bottom)
        self.bottom_layout.setContentsMargins(0, 0, 0, 0)

        self.logout = QPushButton(self.bottom)
        self.logout.setFixedSize(71, 61)
        icon = QIcon()
        img_path = QDir.currentPath() + "/static/images/logout.png"
        icon.addFile(img_path, QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.logout.setIcon(icon)
        self.logout.setIconSize(QSize(50, 50))
        self.logout.setObjectName("logout")
        self.bottom_layout.addWidget(self.logout, alignment=Qt.AlignCenter)
        self.sidebar_layout.addWidget(self.bottom)

        # Content Area
        self.contentArea = QStackedWidget(MainWindow)
        self.contentArea.setObjectName("contentArea")

        # Pages
        self.page_home_scroll = self.createScrollPage(HomePage())
        self.page_collection_scroll = self.createScrollPage(CollectionPage())
        self.page_stats_scroll = self.createScrollPage(StatPage())
        self.page_noti_scroll = self.createScrollPage(NotificationPage())
        self.page_community_scroll = self.createScrollPage(CommunityPage())
        self.page_profile_scroll = self.createScrollPage(UserProfilePage())

        self.contentArea.addWidget(self.page_home_scroll)
        self.contentArea.addWidget(self.page_collection_scroll)
        self.contentArea.addWidget(self.page_stats_scroll)
        self.contentArea.addWidget(self.page_noti_scroll)
        self.contentArea.addWidget(self.page_community_scroll)
        self.contentArea.addWidget(self.page_profile_scroll)

        # Connect logo to user profile
        self.logo.mousePressEvent = self.handle_logo_click

        # Add sidebar and content area to main layout
        self.main_layout.addWidget(self.sidebar)
        self.main_layout.addWidget(self.contentArea)

        self.retranslateUi(MainWindow)
        QMetaObject.connectSlotsByName(MainWindow)

    def handle_logo_click(self, event):
        """Handle logo click to show user profile page"""
        # Get the current user from session manager
        session_manager = SessionManager.get_instance()
        current_user = session_manager.get_current_user()
        
        if current_user:
            # Switch to profile page
            self.page_profile_scroll.widget().refresh_data()
            self.contentArea.setCurrentWidget(self.page_profile_scroll)
            # Refresh the profile page data
        else:
            # If no user is logged in, show login page or message
            from PySide6.QtWidgets import QMessageBox
            QMessageBox.warning(
                self.contentArea,
                "Not Logged In",
                "Please log in to view your profile."
            )

    def createMenuButton(self, name, icon_file):
        button = QPushButton(self.menus)
        button.setObjectName(name)
        button.setFixedSize(71, 61)
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
