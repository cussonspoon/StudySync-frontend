from services.folder_service import get_folders, create_folder
from services.task_service import get_tasks
from services.task_service import create_task
from services.folder_service import search_folder


class Collection_Controller:
    def __init__(self, collection_page, ui):
        self.collection_page = collection_page
        self.ui = ui  # Store the UI reference
        self.collection_page.set_controller(self)
        self.loadFolders()

    def loadFolders(self):
        folders = get_folders()  # API call
        self.collection_page.folders = folders
        self.collection_page.update_folders(folders)  # Update the UI with new folders

    def createFolder(self):
        print("Inside createFolder method")  # Debug print
        # Create a new folder with default values
        new_folder = {
            "name": "New Folder",
            "count": "0 items",
            "date": "Just now",
            "avatar": "static/images/logo.png",
            "image": "static/images/folderimgplaceholder.jpg",
        }

        try:
            # Call the service to create the folder
            created_folder = create_folder(new_folder)
            print("Created new folder:", created_folder)  # Debug print

            # Reload folders to show the new folder
            self.loadFolders()
        except Exception as e:
            print(f"Error creating folder: {e}")  # Debug print

    def navigate_to_folder(self, name, count, date):
        print(f"Navigating to folder: {name}")
        # Use the UI's contentArea to switch pages
        self.ui.contentArea.setCurrentWidget(self.ui.page_folder_scroll)
        folder_page = self.ui.page_folder_scroll.widget()
        folder_page.folder_name.setText(f"📁 {name}")
        self.ui.page_folder_scroll.show()
        self.ui.page_folder_scroll.widget().show()
