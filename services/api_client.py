# Handles GET, POST requests to FastAPI backend
# main API call

import requests

BASE_URL = "http://localhost:8000"  # FastAPI backend URL

def fetch_quiz(quiz_id):
    """Fetch quiz details from backend API."""
    response = requests.get(f"{BASE_URL}/quizzes/{quiz_id}")
    return response.json() if response.status_code == 200 else None
