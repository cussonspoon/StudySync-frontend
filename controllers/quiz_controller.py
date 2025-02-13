# Calls quiz API, fetches questions, sends answers

from services.api_client import fetch_quiz
from views.quiz_view import QuizView

class QuizController:
    def __init__(self):
        self.view = QuizView()
        self.view.load_quiz_button.clicked.connect(self.load_quiz)

    def load_quiz(self):
        quiz_id = 1  # Example ID
        quiz_data = fetch_quiz(quiz_id)
        if quiz_data:
            self.view.display_quiz(quiz_data)
