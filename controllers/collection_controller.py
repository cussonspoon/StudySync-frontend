from services.folder_service import get_folders
from services.task_service import get_tasks
from services.task_service import create_task
from services.folder_service import search_folder


class Collection_Controller:
    def __init__(self, collection_page):
        self.collection_page = collection_page
        self.loadFolders()

    def loadFolders(self):
        folders = get_folders()  # API call
        self.collection_page.folders = folders
        self.collection_page.update_folders(folders)  # Update the UI with new folders

    def createFolder(self):
        print("Creating new folder")
        # Add folder creation logic here
        # After creating folder, reload the folders
        self.loadFolders()
