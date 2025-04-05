# controllers/home_controller.py

from ui.views.home import HomePage
from ui.views.collection import CollectionPage
from ui.views.statistic import StatPage
from ui.views.notification import NotificationPage
from ui.views.community import CommunityPage
from ui.views.components.folder import Folder
from services.folder_service import FolderService
from controllers.home_controller import HomeController
from enum import Enum
from controllers.collection_controller import Collection_Controller
from utils.global_vars import get_current_user


class Page(Enum):
    HOME = 0
    COLLECTION = 1
    # STAT = 2
    # NOTIFICATION = 3
    # COMMUNITY = 4


class WindowController:
    def __init__(self, ui):
        self.ui = ui
        # Initialize HomeController first
        self.home_controller = HomeController(
            self.ui.page_home_scroll.widget(), self.ui
        )

        # Initialize Collection Controller
        self.collection_controller = Collection_Controller(
            self.ui.page_collection_scroll.widget(),
            self.ui,  # Pass the UI which contains the main window
        )

        # Set controllers on their respective pages
        self.ui.page_home_scroll.widget().set_controller(self.home_controller)
        self.ui.page_collection_scroll.widget().set_controller(
            self.collection_controller
        )

        # Then setup pages and connect signals
        self.setupPages()
        self.ui.home.clicked.connect(lambda: self.switchPage(Page.HOME.value))
        self.ui.collection.clicked.connect(
            lambda: self.switchPage(Page.COLLECTION.value)
        )
        # self.ui.stats.clicked.connect(lambda: self.switchPage(Page.STAT.value))
        # self.ui.noti.clicked.connect(lambda: self.switchPage(Page.NOTIFICATION.value))
        # self.ui.community.clicked.connect(lambda: self.switchPage(Page.COMMUNITY.value))

    def setupPages(self):
        self.pages = {
            Page.HOME: self.ui.page_home_scroll,
            Page.COLLECTION: self.ui.page_collection_scroll,
            # Page.STAT: self.ui.page_stats_scroll,
            # Page.NOTIFICATION: self.ui.page_noti_scroll,
            # Page.COMMUNITY: self.ui.page_community_scroll,
        }
        self.switchPage(Page.HOME.value)  # Start with home page (index 0)

    def switchPage(self, index):
        self.ui.contentArea.setCurrentIndex(index)
        if index == Page.HOME.value:
            # Get current user and load their folders
            current_user = get_current_user()
            if current_user:
                folders = FolderService.get_user_folders(current_user.id)
                self.home_controller.loadFolders(folders)
            self.home_controller.loadTasks()
        elif index == Page.COLLECTION.value:
            # Get current user and load their folders
            current_user = get_current_user()
            if current_user:
                folders = FolderService.get_user_folders(current_user.id)
                self.collection_controller.loadFolders(folders)
