# from services.folder_service import get_folders, create_folder
# from services.task_service import get_tasks
# from services.task_service import create_task
# from services.folder_service import search_folder
from services.folder_service import get_modes, create_mode


class Folder_Controller:
    def __init__(self, folder_page, ui):
        self.folder_page = folder_page
        self.ui = ui  # Store the UI reference
        self.folder_page.set_controller(self)
        self.loadModes()

    def loadModes(self):
        folders = get_modes()  # API call
        self.collection_page.folders = folders
        self.collection_page.update_folders(folders)  # Update the UI with new folders

    def createMode(self, mode):
        print("Inside createFolder method")  # Debug print
        # Create a new folder with default values
        new_mode = {
            "name": "Untitled",
            "date": "Just now",
            "mode": mode,
            "image": "static/images/folderimgplaceholder.jpg",
        }

        try:
            # Call the service to create the folder
            created_mode = create_mode(new_mode)
            print("Created new mode:", created_mode)  # Debug print

            # Reload folders to show the new folder
            self.loadModes()
            self.navigate_to_mode(new_mode["name"], 0, new_mode["date"])

        except Exception as e:
            print(f"Error creating folder: {e}")  # Debug print

    #need to declare each mode in main_controller.py
    def navigate_to_mode(self, name, mode, date, count=0):
        print(f"Navigating to mode: {name}")
        # Use the UI's contentArea to switch pages
        if mode == "Note":
            self.ui.contentArea.setCurrentWidget(self.ui.page_note_scroll)
            folder_page = self.ui.page_note_scroll.widget()
            folder_page.note_name.setText(f"📝 {name}")
            self.ui.page_note_scroll.show()
            self.ui.page_note_scroll.widget().show()
        elif mode == "Flashcard":
            self.ui.contentArea.setCurrentWidget(self.ui.page_flashcard_scroll)
            folder_page = self.ui.page_flashcard_scroll.widget()
            folder_page.flashcard_name.setText(f"🗂️ {name}")
            self.ui.page_flashcard_scroll.show()
            self.ui.page_flashcard_scroll.widget().show()
        elif mode == "Quiz": 
            self.ui.contentArea.setCurrentWidget(self.ui.page_quiz_scroll)
            folder_page = self.ui.page_quiz_scroll.widget()
            folder_page.quiz_name.setText(f"❓ {name}")
            self.ui.page_quiz_scroll.show()
            self.ui.page_quiz_scroll.widget().show()
