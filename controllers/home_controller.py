from services.folder_service import get_folders
from services.task_service import get_tasks
from services.task_service import create_task
from services.folder_service import search_folder


class HomeController:
    def __init__(self, homepage):
        self.homepage = homepage
        self.loadFolders()
        self.loadTasks()

    def loadFolders(self):
        folders = get_folders()  # API call
        self.homepage.folders = folders

        # Update the collections and recommendFolders components
        if hasattr(self.homepage, "collections"):
            self.homepage.collections.update_folders(folders)
        if hasattr(self.homepage, "recommendFolders"):
            self.homepage.recommendFolders.update_folders(folders)

    # task management with UI
    def loadTasks(self):
        tasks = get_tasks()  # Get tasks from service
        self.homepage.tasks = tasks
        self.homepage.update_tasks(tasks)  # Update UI with new tasks

    def createTask(self):
        # Create a new task
        new_task = {"task_detail": "", "status": "In progress"}
        # Add to service
        created_task = create_task(new_task)
        print("Created new task")  # Debug print
        # No need to reload tasks here since we already added the UI

    def updateTask(self, text):
        # Update task with new text
        print(f"Updating task: {text}")  # Debug print
        # Will implement actual update later

    def deleteTask(self):
        # Delete task
        print("Deleting task")  # Debug print
        # Will implement actual delete later

    def searchFolders(self, search_text):
        # Call the search service
        results = search_folder(search_text)
        return results

    # def setupSearch(self):
    #     self.home_page.searchBar.textChanged.connect(self.searchFolders)

    # def loadFolders(self):
    #     folders = get_folders()
    #     self.home_page.updateFolders(folders)

    # def searchFolders(self, text):
    #     # Filter folder logic
    #     pass
