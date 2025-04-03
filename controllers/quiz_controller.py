from typing import Dict, List, Optional
from services.quiz_service import QuizService
from models.quiz import Quiz, Question, Choice
from controllers.base_controller import BaseController
from PySide6.QtCore import QJsonDocument

class QuizController(BaseController):
    def __init__(self, quiz: Quiz, parent=None):
        super().__init__(parent)
        self.quiz = quiz
        self.questions: List[Question] = []
    
    def set_quiz(self, quiz: Quiz):
        self.quiz = quiz
        self.quiz_service = QuizService(quiz)
        self.questions = self.quiz_service._questions  # Update questions when quiz changes
    
    def get_quiz(self):
        return self.quiz
    
    def get_questions(self, quiz_id: str):
        url = f"{self.SERVER_URL}/quiz/{quiz_id}/questions"
        reply = self.perform_get_request_sync(url)
        
        # Parse the JSON response
        json_doc = QJsonDocument.fromJson(reply.readAll())
        if json_doc.isNull():
            raise ValueError("Invalid JSON response from server")
        
        # Convert QJsonArray to list of Question objects
        questions_array = json_doc.array()
        self.questions = []
        
        for i in range(questions_array.size()):
            question_obj = questions_array.at(i).toVariant()
            
            # Convert choices to Choice objects
            choices = []
            for choice_data in question_obj.get('choices', []):
                choice = Choice(
                    id=choice_data.get('id', ''),
                    choice=choice_data.get('choice', ''),
                    is_answer=choice_data.get('is_answer', False),
                    question_id=choice_data.get('question_id', '')
                )
                choices.append(choice)
            
            # Create Question object
            question = Question(
                id=question_obj.get('id', ''),
                question=question_obj.get('question', ''),
                quiz_id=question_obj.get('quiz_id', ''),
                created_at=question_obj.get('created_at', ''),
                choices=choices
            )
            self.questions.append(question)

        return self.questions
    
    def set_questions(self, questions: List[Question]):
        self.questions = questions

    def post_question(self, quiz_id: str, question: str):
        url = f"{self.SERVER_URL}/question?quiz_id={quiz_id}"
        data = {
            "question": question,
        }
        reply = self.perform_post_request_sync(url, data)
        json_doc = QJsonDocument.fromJson(reply.readAll())
        if json_doc.isNull():
            raise ValueError("Invalid JSON response from server")
        return json_doc.object()

    def post_choice(self, question_id: str, choice: str, is_answer: bool):
        url = f"{self.SERVER_URL}/choice?question_id={question_id}"
        data = {
            "choice": choice,
            "is_answer": is_answer
        }
        reply = self.perform_post_request_sync(url, data)
        json_doc = QJsonDocument.fromJson(reply.readAll())
        if json_doc.isNull():
            raise ValueError("Invalid JSON response from server")
        return json_doc.object()

