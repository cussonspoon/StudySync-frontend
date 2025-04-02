
# collection service 
# get collections, create collection, delete collection, update collection

import requests

BASE_URL = "http://localhost:8000"

def get_collections():
    response = requests.get(f"{BASE_URL}/collections")
    return response.json()