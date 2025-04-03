from PySide6.QtCore import QObject, QJsonDocument
from PySide6.QtNetwork import QNetworkReply
from .base_controller import BaseController

# Example of how to use the UserController
class UserController(BaseController):
    def __init__(self, parent=None):
        super().__init__(parent)

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
        print(f"Fetched user data: {questions_list[0]}")
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
