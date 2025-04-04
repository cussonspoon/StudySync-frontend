# call folder api

from typing import List
import requests
from dotenv import load_dotenv
from models.folder import CreateFolder, Folder
from models.quiz import Quiz
from models.user import User
import os

# CRUD folders
load_dotenv()
API_BASE_URL = os.getenv("BASE_URL")

class FolderService:
    def __init__(self, folder_data: Folder):
        self._folder = folder_data
        self._items = []
        if folder_data is not None:  # Only fetch items if we have a folder
            self._items = self.fetch_items()

    def fetch_items(self):
        """Fetch all items in a folder"""
        try:
            print(f"Fetching items for folder ID: {self._folder.id}")
            response = requests.get(f"{API_BASE_URL}/folder/{self._folder.id}")
            print(f"Response status: {response.status_code}")
            print(f"Response content: {response.text}")

            if response.status_code == 200:
                items = response.json()
                print(f"Parsed items: {items}")
                return items
            else:
                print(f"Error fetching items: {response.status_code}")
                print(f"Error response: {response.text}")
                return []
        except Exception as e:
            print(f"Exception while fetching items: {str(e)}")
            return []

    def create_folder(self, folder_data: CreateFolder, user_id: str) -> Folder:
        """Create a new folder"""
        try:
            response = requests.post(
                f"{API_BASE_URL}/folder?user_id={user_id}",
                json={
                    "name": folder_data.name,
                    "accesss": folder_data.accesss,  # Changed from access to accesss
                    "total_items": folder_data.total_items,
                    "total_likes": folder_data.total_likes,
                    "img_url": folder_data.img_url,
                },
            )

            if response.status_code == 200:
                folder_data = response.json()
                # Convert collaborations data to User objects
                collaborations = [
                    User(**user_data)
                    for user_data in folder_data.get("collaborations", [])
                ]

                # Create a new Folder object with the response data
                folder = Folder(
                    id=folder_data.get("id", ""),
                    name=folder_data.get("name", ""),
                    total_items=folder_data.get("total_items", 0),
                    img_url=folder_data.get("img_url", ""),
                    access=folder_data.get(
                        "accesss", ""
                    ),  # Note: API returns as accesss
                    created_at=folder_data.get("created_at", ""),
                    collaborations=collaborations,
                )
                self._folder = folder  # Update the current folder
                return folder
            else:
                print(f"Error creating folder: {response.status_code}")
                print(f"Error response: {response.text}")
                raise Exception(f"Failed to create folder: {response.text}")
        except Exception as e:
            print(f"Exception while creating folder: {str(e)}")
            raise

    def update_folder(self, name: str = None, access: str = None, img_url: str = None):
        """Update folder properties"""
        try:
            # Build update data with only provided values
            update_data = {}
            if name is not None:
                update_data["name"] = name
            if access is not None:
                update_data["accesss"] = access  # Note: API uses "accesss" with 3 's'
            if img_url is not None:
                update_data["img_url"] = img_url
            if "total_items" in self._folder.__dict__:
                update_data["total_items"] = self._folder.total_items
            if "total_likes" in self._folder.__dict__:
                update_data["total_likes"] = self._folder.total_likes

            response = requests.patch(
                f"{API_BASE_URL}/folder/{self._folder.id}", json=update_data
            )

            if response.status_code == 200:
                folder_data = response.json()
                # Update the current folder object with new data
                self._folder.name = folder_data.get("name", self._folder.name)
                self._folder.access = folder_data.get("accesss", self._folder.access)
                self._folder.img_url = folder_data.get("img_url", self._folder.img_url)
                return self._folder
            else:
                raise Exception(f"Failed to update folder: {response.text}")
        except Exception as e:
            print(f"Error updating folder: {str(e)}")
            raise

    # add
    def add_folder_collaborations(self, user_name: str):
        """Add collaborator to folder"""
        try:
            response = requests.post(
                f"{API_BASE_URL}/folder/{self._folder.id}/collaborations",
                json={"user_name": user_name},
            )

            if response.status_code == 200:
                return response.json()
            else:
                raise Exception(f"Failed to add collaborator: {response.text}")
        except Exception as e:
            print(f"Error adding collaborator: {str(e)}")
            raise

    def delete_folder(self):
        """Delete a folder"""
        try:
            response = requests.delete(f"{API_BASE_URL}/folder/{self._folder.id}")

            if response.status_code == 200:
                return True
            else:
                raise Exception(f"Failed to delete folder: {response.text}")
        except Exception as e:
            print(f"Error deleting folder: {str(e)}")
            raise

    @staticmethod
    def get_folder_by_id(folder_id: str) -> Folder:
        """Get folder by ID"""
        try:
            response = requests.get(f"{API_BASE_URL}/folder/{folder_id}")

            if response.status_code == 200:
                folder_data = response.json()
                # Convert collaborations data to User objects
                collaborations = [
                    User(**user_data)
                    for user_data in folder_data.get("collaborations", [])
                ]

                return Folder(
                    id=folder_data.get("id", ""),
                    name=folder_data.get("name", ""),
                    total_items=folder_data.get("total_items", 0),
                    img_url=folder_data.get("img_url", ""),
                    access=folder_data.get(
                        "accesss", ""
                    ),  # Note: API returns as accesss
                    created_at=folder_data.get("created_at", ""),
                    collaborations=collaborations,
                )
            else:
                raise Exception(f"Failed to get folder: {response.text}")
        except Exception as e:
            print(f"Error getting folder: {str(e)}")
            raise

    # add
    @staticmethod
    def get_folder_by_name(name: str) -> List[Folder]:
        """Search folders by name"""
        try:
            response = requests.get(
                f"{API_BASE_URL}/folder/search", params={"name": name}
            )

            if response.status_code == 200:
                folders_data = response.json()
                folders = []

                for folder_data in folders_data:
                    # Convert collaborations data to User objects
                    collaborations = [
                        User(**user_data)
                        for user_data in folder_data.get("collaborations", [])
                    ]

                    folder = Folder(
                        id=folder_data.get("id", ""),
                        name=folder_data.get("name", ""),
                        total_items=folder_data.get("total_items", 0),
                        img_url=folder_data.get("img_url", ""),
                        access=folder_data.get(
                            "accesss", ""
                        ),  # Note: API returns as accesss
                        created_at=folder_data.get("created_at", ""),
                        collaborations=collaborations,
                    )
                    folders.append(folder)
                return folders
            else:
                raise Exception(f"Failed to search folders: {response.text}")
        except Exception as e:
            print(f"Error searching folders: {str(e)}")
            raise

    @staticmethod
    def get_user_folders(user_id: str) -> List[Folder]:
        """Get folders for a specific user"""
        try:
            response = requests.get(
                f"{API_BASE_URL}/user/{user_id}/folders"
            )  # Updated endpoint

            if response.status_code == 200:
                user_data = response.json()
                folders_data = user_data.get(
                    "folders", []
                )  # Get folders array from response
                folders = []

                for folder_data in folders_data:
                    # Convert collaborations data to User objects
                    collaborations = [
                        User(**user_data)
                        for user_data in folder_data.get("collaborations", [])
                    ]

                    folder = Folder(
                        id=folder_data.get("id", ""),
                        name=folder_data.get("name", ""),
                        total_items=folder_data.get("total_items", 0),
                        img_url=folder_data.get("img_url", ""),
                        access=folder_data.get(
                            "accesss", ""
                        ),  # Note: API returns as accesss
                        created_at=folder_data.get("created_at", ""),
                        collaborations=collaborations,
                    )
                    folders.append(folder)
                return folders
            else:
                raise Exception(f"Failed to get user folders: {response.text}")
        except Exception as e:
            print(f"Error getting user folders: {str(e)}")
            raise

    # add
    @staticmethod
    def get_public_folders() -> List[Folder]:
        """Get all public folders"""
        try:
            response = requests.get(f"{API_BASE_URL}/folder/public")

            if response.status_code == 200:
                folders_data = response.json()
                folders = []

                for folder_data in folders_data:
                    # Convert collaborations data to User objects
                    collaborations = [
                        User(**user_data)
                        for user_data in folder_data.get("collaborations", [])
                    ]

                    folder = Folder(
                        id=folder_data.get("id", ""),
                        name=folder_data.get("name", ""),
                        total_items=folder_data.get("total_items", 0),
                        img_url=folder_data.get("img_url", ""),
                        access=folder_data.get(
                            "accesss", ""
                        ),  # Note: API returns as accesss
                        created_at=folder_data.get("created_at", ""),
                        collaborations=collaborations,
                    )
                    folders.append(folder)
                return folders
            else:
                raise Exception(f"Failed to get public folders: {response.text}")
        except Exception as e:
            print(f"Error getting public folders: {str(e)}")
            raise


# def get_folders():
#     # response = requests.get("http://127.0.0.1:5000/folders")
#     folders = [
#             {
#                 "name": "Folder 1",
#                 "count": "10",
#                 "date": "2024-01-01",
#                 "avatar": "static/images/profile.jpg",
#                 "image": "static/images/pic1.jpg",
#             },
#             {
#                 "name": "Folder 2",
#                 "count": "15",
#                 "date": "2024-01-02",
#                 "avatar": "static/images/profile.jpg",
#                 "image": "static/images/pic2.jpg",
#             },
#             {
#                 "name": "Folder 3",
#                 "count": "20",
#                 "date": "2024-01-03",
#                 "avatar": "static/images/profile.jpg",
#                 "image": "static/images/pic3.jpg",
#             },
#             {
#                 "name": "Folder 4",
#                 "count": "25",
#                 "date": "2024-01-04",
#                 "avatar": "static/images/profile.jpg",
#                 "image": "static/images/pic1.jpg",
#             },
#             {
#                 "name": "Folder 5",
#                 "count": "30",
#                 "date": "2024-01-05",
#                 "avatar": "static/images/profile.jpg",
#                 "image": "static/images/pic2.jpg",
#             },
#             {
#                 "name": "Folder 6",
#                 "count": "35",
#                 "date": "2024-01-06",
#                 "avatar": "static/images/profile.jpg",
#                 "image": "static/images/pic3.jpg",
#             },
#             {
#                 "name": "Folder 7",
#                 "count": "40",
#                 "date": "2024-01-07",
#                 "avatar": "static/images/profile.jpg",
#                 "image": "static/images/pic1.jpg",
#             },
#             {
#                 "name": "Folder 8",
#                 "count": "45",
#                 "date": "2024-01-08",
#                 "avatar": "static/images/profile.jpg",
#                 "image": "static/images/pic2.jpg",
#             },
#             {
#                 "name": "Folder 9",
#                 "count": "50",
#                 "date": "2024-01-09",
#                 "avatar": "static/images/profile.jpg",
#                 "image": "static/images/pic3.jpg",
#             },
#             {
#                 "name": "Folder 10",
#                 "count": "55",
#                 "date": "2024-01-10",
#                 "avatar": "static/images/profile.jpg",
#                 "image": "static/images/pic1.jpg",
#             },
#         ]
#     return folders
#     # return response.json()

# def create_folder(folder):
#     return folder

# def update_folder(folder):
#     return folder

# def delete_folder(folder):
#     return folder

# def search_folder(folder_name):
#     #implement search folder api

#     folder = [{
#         "name": "History",
#         "count": "10",
#         "date": "2024-01-01",
#         "avatar": "static/images/profile.jpg",
#         "image": "static/images/pic1.jpg",
#     }, {
#         "name": "History123",
#         "count": "10",
#         "date": "2024-01-01",
#         "avatar": "static/images/profile.jpg",
#         "image": "static/images/pic1.jpg"}]

#     if folder_name == "History":
#         return folder
#     else:
#         return []
