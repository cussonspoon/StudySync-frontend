from services.folder_service import FolderService
from services.task_service import get_tasks
from services.task_service import create_task
from services.folder_service import search_folder
from utils.global_vars import get_current_user
from models.folder import CreateFolder


class Collection_Controller:
    def __init__(self, collection_page, ui):
        self.collection_page = collection_page
        self.ui = ui  # Store the UI reference
        self.collection_page.set_controller(self)
        self.loadFolders()

    def loadFolders(self, folders=None):
        if folders is None:
            # Get current user and their folders
            current_user = get_current_user()
            if current_user:
                folders = FolderService.get_user_folders(current_user.id)
            else:
                folders = []

        self.collection_page.folders = folders
        self.collection_page.update_folders(folders)  # Update the UI with new folders

    def createFolder(self):
        print("Inside createFolder method")  # Debug print
        # Get current user
        current_user = get_current_user()
        if not current_user:
            print("No user logged in")
            return

        # Create a new folder with default values
        folder_data = CreateFolder(
            name="New Folder",
            accesss="private",  # Default access level
            total_items=0,
            total_likes=0,
            img_url="static/images/folderimgplaceholder.jpg",
        )

        try:
            # Create a FolderService instance with None as initial folder data
            folder_service = FolderService(None)
            # Call the service to create the folder
            created_folder = folder_service.create_folder(folder_data, current_user.id)
            print("Created new folder:", created_folder)  # Debug print

            # Reload folders to show the new folder
            self.loadFolders()
            self.navigate_to_folder(created_folder)

        except Exception as e:
            print(f"Error creating folder: {e}")  # Debug print

    def navigate_to_folder(self, folder):
        print(f"Type of folder: {type(folder)}")
        print(f"Navigating to folder: {folder.name}")
        # Use the UI's contentArea to switch pages
        self.ui.contentArea.setCurrentWidget(self.ui.page_folder_scroll)
        folder_page = self.ui.page_folder_scroll.widget()

        folder_page.folder_name.setText(f"📁 {folder.name}")
        folder_page.folder_id = folder.id
        folder_page.folder_total_items = folder.count
        folder_page.folder_created_at = folder.date
        folder_page.folder_img_url = folder.img_url
        folder_page.update_created_label()

        # Load the folder's items after setting up the page
        folder_page.load_items()

        self.ui.page_folder_scroll.show()
        self.ui.page_folder_scroll.widget().show()
