from services.folder_service import get_folders


class HomeController:
    def __init__(self, homepage):
        self.homepage = homepage
        self.loadFolders()

    def loadFolders(self):
        folders = get_folders()  # API call
        self.homepage.folders = folders

        # Update the collections and recommendFolders components
        if hasattr(self.homepage, "collections"):
            self.homepage.collections.update_folders(folders)
        if hasattr(self.homepage, "recommendFolders"):
            self.homepage.recommendFolders.update_folders(folders)

    # def setupSearch(self):
    #     self.home_page.searchBar.textChanged.connect(self.searchFolders)

    # def loadFolders(self):
    #     folders = get_folders()
    #     self.home_page.updateFolders(folders)

    # def searchFolders(self, text):
    #     # Filter folder logic
    #     pass
