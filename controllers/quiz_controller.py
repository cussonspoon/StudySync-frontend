from typing import Dict, List, Optional
from services.quiz_service import QuizService
from models.quiz import Quiz, Question

class QuizController:
    def __init__(self, quiz: Quiz):
        self.quiz = quiz
        self.questions: List[Question] = []
        self.quiz_service = QuizService(quiz)
        self.questions = self.quiz_service._questions  # Get questions from service
    
    def set_quiz(self, quiz: Quiz):
        self.quiz = quiz
        self.quiz_service = QuizService(quiz)
        self.questions = self.quiz_service._questions  # Update questions when quiz changes
    
    def get_quiz(self):
        return self.quiz
    
    def get_questions(self):
        return self.questions
    
    def set_questions(self, questions: List[Question]):
        self.questions = questions

    # def create_quiz(self, data: Dict) -> Dict:
    #     """Handle quiz creation request"""
    #     try:
    #         quiz = self.quiz_service.create_quiz(
    #             title=data['title'],
    #             description=data['description'],
    #             questions=data['questions'],
    #             time_limit=data.get('time_limit'),
    #             passing_score=data.get('passing_score')
    #         )
    #         return {
    #             'status': 'success',
    #             'data': {
    #                 'id': quiz.id,
    #                 'title': quiz.title,
    #                 'description': quiz.description,
    #                 'question_count': len(quiz.questions)
    #             }
    #         }
    #     except KeyError as e:
    #         return {
    #             'status': 'error',
    #             'message': f'Missing required field: {str(e)}'
    #         }
    #     except Exception as e:
    #         return {
    #             'status': 'error',
    #             'message': str(e)
    #         }

    # def get_quiz(self, quiz_id: int) -> Dict:
    #     """Handle getting a single quiz request"""
    #     quiz = self.quiz_service.get_quiz(quiz_id)
    #     if not quiz:
    #         return {
    #             'status': 'error',
    #             'message': 'Quiz not found'
    #         }
        
    #     return {
    #         'status': 'success',
    #         'data': {
    #             'id': quiz.id,
    #             'title': quiz.title,
    #             'description': quiz.description,
    #             'questions': [
    #                 {
    #                     'id': q.id,
    #                     'text': q.text,
    #                     'options': q.options
    #                 } for q in quiz.questions
    #             ],
    #             'time_limit': quiz.time_limit,
    #             'passing_score': quiz.passing_score
    #         }
    #     }

    # def get_all_quizzes(self) -> Dict:
    #     """Handle getting all quizzes request"""
    #     quizzes = self.quiz_service.get_all_quizzes()
    #     return {
    #         'status': 'success',
    #         'data': [
    #             {
    #                 'id': quiz.id,
    #                 'title': quiz.title,
    #                 'description': quiz.description,
    #                 'question_count': len(quiz.questions)
    #             } for quiz in quizzes
    #         ]
    #     }

    # def update_quiz(self, quiz_id: int, data: Dict) -> Dict:
    #     """Handle quiz update request"""
    #     quiz = self.quiz_service.update_quiz(
    #         quiz_id=quiz_id,
    #         title=data.get('title'),
    #         description=data.get('description'),
    #         time_limit=data.get('time_limit'),
    #         passing_score=data.get('passing_score')
    #     )
        
    #     if not quiz:
    #         return {
    #             'status': 'error',
    #             'message': 'Quiz not found'
    #         }
        
    #     return {
    #         'status': 'success',
    #         'data': {
    #             'id': quiz.id,
    #             'title': quiz.title,
    #             'description': quiz.description,
    #             'time_limit': quiz.time_limit,
    #             'passing_score': quiz.passing_score
    #         }
    #     }

    # def delete_quiz(self, quiz_id: int) -> Dict:
    #     """Handle quiz deletion request"""
    #     if self.quiz_service.delete_quiz(quiz_id):
    #         return {
    #             'status': 'success',
    #             'message': 'Quiz deleted successfully'
    #         }
    #     return {
    #         'status': 'error',
    #         'message': 'Quiz not found'
    #     }

    # def submit_answers(self, quiz_id: int, answers: List[int]) -> Dict:
    #     """Handle quiz submission request"""
    #     quiz = self.quiz_service.get_quiz(quiz_id)
    #     if not quiz:
    #         return {
    #             'status': 'error',
    #             'message': 'Quiz not found'
    #         }

    #     try:
    #         score = quiz.calculate_score(answers)
    #         passed = quiz.is_passed(score)
            
    #         return {
    #             'status': 'success',
    #             'data': {
    #                 'score': score,
    #                 'passed': passed,
    #                 'total_questions': len(quiz.questions)
    #             }
    #         }
    #     except ValueError as e:
    #         return {
    #             'status': 'error',
    #             'message': str(e)
    #         } 