#call folder api

import requests

# CRUD folders

def get_folders():
    # response = requests.get("http://127.0.0.1:5000/folders")
    folders = [
            {
                "name": "Folder 1",
                "count": "10",
                "date": "2024-01-01",
                "avatar": "static/images/profile.jpg",
                "image": "static/images/pic1.jpg",
            },
            {
                "name": "Folder 2",
                "count": "15",
                "date": "2024-01-02",
                "avatar": "static/images/profile.jpg",
                "image": "static/images/pic2.jpg",
            },
            {
                "name": "Folder 3",
                "count": "20",
                "date": "2024-01-03",
                "avatar": "static/images/profile.jpg",
                "image": "static/images/pic3.jpg",
            },
            {
                "name": "Folder 4",
                "count": "25",
                "date": "2024-01-04",
                "avatar": "static/images/profile.jpg",
                "image": "static/images/pic1.jpg",
            },
            {
                "name": "Folder 5",
                "count": "30",
                "date": "2024-01-05",
                "avatar": "static/images/profile.jpg",
                "image": "static/images/pic2.jpg",
            },
            {
                "name": "Folder 6",
                "count": "35",
                "date": "2024-01-06",
                "avatar": "static/images/profile.jpg",
                "image": "static/images/pic3.jpg",
            },
            {
                "name": "Folder 7",
                "count": "40",
                "date": "2024-01-07",
                "avatar": "static/images/profile.jpg",
                "image": "static/images/pic1.jpg",
            },
            {
                "name": "Folder 8",
                "count": "45",
                "date": "2024-01-08",
                "avatar": "static/images/profile.jpg",
                "image": "static/images/pic2.jpg",
            },
            {
                "name": "Folder 9",
                "count": "50",
                "date": "2024-01-09",
                "avatar": "static/images/profile.jpg",
                "image": "static/images/pic3.jpg",
            },
            {
                "name": "Folder 10",
                "count": "55",
                "date": "2024-01-10",
                "avatar": "static/images/profile.jpg",
                "image": "static/images/pic1.jpg",
            },
        ]
    return folders
    # return response.json()

def create_folder(folder):
    return folder

def update_folder(folder):
    return folder

def delete_folder(folder):
    return folder

def search_folder(folder_name): 
    #implement search folder api

    folder = [{
        "name": "History",
        "count": "10",
        "date": "2024-01-01",
        "avatar": "static/images/profile.jpg",
        "image": "static/images/pic1.jpg",
    }, {
        "name": "History123",
        "count": "10",
        "date": "2024-01-01",
        "avatar": "static/images/profile.jpg",
        "image": "static/images/pic1.jpg"}]
    
    if folder_name == "History":
        return folder
    else:
        return []
