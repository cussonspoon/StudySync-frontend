import requests

class Folder:
    def __init__(self, name, count, date, avatar, image):
        self.name = name
        self.count = count
        self.date = date
        self.avatar = avatar
        self.image = image

class FolderModel:
    def __init__(self):
        self.folders = []

    def fetch_folders(self):
        try:
            response = requests.get("http://127.0.0.1:5000/folders")
            response.raise_for_status()
            data = response.json()
            self.folders = [Folder(**item) for item in data]
        except Exception as e:
            print(f"Error fetching folders: {e}")
