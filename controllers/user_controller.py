from PySide6.QtCore import QObject, QJsonDocument
from PySide6.QtNetwork import QNetworkReply
from .base_controller import BaseController
from models.user import User
from typing import Optional
from utils.session_manager import SessionManager
# Example of how to use the UserController
class UserController(BaseController):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.current_user = None
        self.session_manager = SessionManager.get_instance()
        self.current_user = self.session_manager.get_current_user()
        print(self.current_user)

    def fetch_user_data(self, user_id):
        """Fetch user data synchronously from the server."""
        url = f"{self.SERVER_URL}/quiz/b6e3886a-7c02-40f5-bdf6-fb8b50c9118c/questions"  # Assuming the API endpoint is '/user'
        # Add user_id as a query parameter if required by the API
        data = {"id": str(user_id)}  # Convert to string for QUrlQuery compatibility
        reply = self.perform_get_request_sync(url)
        
        # Parse the JSON response
        json_doc = QJsonDocument.fromJson(reply.readAll())
        if json_doc.isNull():
            raise ValueError("Invalid JSON response from server")
        
        questions = json_doc.array()
        # Convert QJsonArray to list of dicts
        questions_list = [questions.at(i).toVariant() for i in range(questions.size())]
        # print(f"Fetched user data: {questions_list[0]}")
        return questions_list
    
    def fetch_question_data(self, question_id):
        url = f"{self.SERVER_URL}/quiz/b6e3886a-7c02-40f5-bdf6-fb8b50c9118c/questions/{question_id}"
        reply = self.perform_get_request_sync(url)
        json_doc = QJsonDocument.fromJson(reply.readAll())
        if json_doc.isNull():
            raise ValueError("Invalid JSON response from server")
        return json_doc.object()
    
    def post_user(self):
        data = {
            "username": "string123",
            "is_superuser": False,
            "banner_img": "string",
            "profile_img": "string",
            "password": "stringst"
        }
        url = f"{self.SERVER_URL}/auth/register"
        reply = self.perform_post_request_sync(url, data=data)
        json_doc = QJsonDocument.fromJson(reply.readAll())
        if json_doc.isNull():
            raise ValueError("Invalid JSON response from server")
        return json_doc.object()

    def login(self, username: str, password: str) -> bool:
        """Logs in a user with username and password."""
        try:
            response = self.perform_post_request_sync(
                f"{self.SERVER_URL}/auth/login",
                {"username": username, "password": password}
            )
            json_doc = QJsonDocument.fromJson(response.readAll())
            if json_doc.isNull():
                raise ValueError("Invalid JSON response from server")
            response = json_doc.object()
            print(response)
            if response and isinstance(response, dict):
                # Store the current user
                self.current_user = User.from_dict(response)
                return User.from_dict(response)
            return None
        except Exception as e:
            print("Login error:", str(e))
            return None

    def register(self, username: str, password: str) -> Optional[User]:
        """Register a new user with username and password."""
        data = {
            "username": username,
            "password": password,
            "is_superuser": False,
            "banner_img": "string",
            "profile_img": "string",
        }
        try:
            response = self.perform_post_request_sync(
                f"{self.SERVER_URL}/auth/register", data=data
            )

            json_doc = QJsonDocument.fromJson(response.readAll())
            if json_doc.isNull():
                raise ValueError("Invalid JSON response from server")
            response = json_doc.object()
            print(response)
            if response:
                return User.from_dict(response)
            return None
        except Exception as e:
            print(f"Registration error: {str(e)}")
            return None

    def get_current_user(self) -> Optional[User]:
        """Get the current logged-in user."""
        try:
            response = self.perform_get_request_sync("auth/me")
            if response and "user" in response:
                return User.from_dict(response["user"])
            return None
        except Exception as e:
            print(f"Get current user error: {str(e)}")
            return None

    def get_user_stats(self, user_id: str):
        """Get the stats of a user."""
        url = f"{self.SERVER_URL}/user/{user_id}/stats"
        reply = self.perform_get_request_sync(url)
        json_doc = QJsonDocument.fromJson(reply.readAll())
        if json_doc.isNull():
            raise ValueError("Invalid JSON response from server")
        return json_doc.object()

    def logout(self) -> bool:
        """Logout the current user."""
        try:
            response = self.perform_post_request_sync("auth/logout")
            return response is not None
        except Exception as e:
            print(f"Logout error: {str(e)}")
            return False
