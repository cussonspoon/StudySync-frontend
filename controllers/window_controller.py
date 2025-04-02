# controllers/home_controller.py

from ui.views.home import HomePage
from ui.views.collection import CollectionPage
from ui.views.statistic import StatPage
from ui.views.notification import NotificationPage
from ui.views.community import CommunityPage
from ui.views.components.folder import Folder
from services.folder_service import get_folders
from controllers.home_controller import HomeController
from enum import Enum


class Page(Enum):
    HOME = 0
    COLLECTION = 1
    STAT = 2
    NOTIFICATION = 3
    COMMUNITY = 4


class WindowController:
    def __init__(self, ui):
        self.ui = ui
        # Initialize HomeController first
        self.home_controller = HomeController(self.ui.page_home_scroll.widget())

        # Then setup pages and connect signals
        self.setupPages()
        self.ui.home.clicked.connect(lambda: self.switchPage(Page.HOME.value))
        self.ui.collection.clicked.connect(
            lambda: self.switchPage(Page.COLLECTION.value)
        )
        self.ui.stats.clicked.connect(lambda: self.switchPage(Page.STAT.value))
        self.ui.noti.clicked.connect(lambda: self.switchPage(Page.NOTIFICATION.value))
        self.ui.community.clicked.connect(lambda: self.switchPage(Page.COMMUNITY.value))

    def setupPages(self):
        self.pages = {
            Page.HOME: self.ui.page_home_scroll,
            Page.COLLECTION: self.ui.page_collection_scroll,
            Page.STAT: self.ui.page_stats_scroll,
            Page.NOTIFICATION: self.ui.page_noti_scroll,
            Page.COMMUNITY: self.ui.page_community_scroll,
        }
        self.switchPage(Page.HOME.value)  # Start with home page (index 0)

    def switchPage(self, index):
        self.ui.contentArea.setCurrentIndex(index)
        if index == Page.HOME.value:
            self.home_controller.loadFolders()  # Load folders when switching to home page
