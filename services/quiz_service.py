from typing import List, Optional
from datetime import datetime
from models.quiz import Quiz, Question, Choice
import requests

API_BASE_URL = "http://localhost:8000"


class QuizService:
    def __init__(self, quiz_data: Quiz):
        self._quiz = quiz_data
        self._questions = []  # Initialize as empty list
        self._questions = self.fetch_questions()  # Fetch questions immediately

    def fetch_questions(self) -> List[Question]:
        """Fetch all questions"""
        try:
            id = self._quiz.id
            print(f"Fetching questions for quiz ID: {id}")
            response = requests.get(f"{API_BASE_URL}/quiz/{id}/questions")
            print(f"Response status: {response.status_code}")
            print(f"Response content: {response.text}")

            if response.status_code == 200:
                questions = response.json()
                print(f"Parsed questions: {questions}")
                question_objects = []
                for question in questions:
                    try:
                        # Convert choices to Choice objects
                        choices = []
                        for choice_data in question.get("choices", []):
                            choice = Choice(
                                id=choice_data.get("id", ""),
                                choice=choice_data.get("choice", ""),
                                is_answer=choice_data.get("is_answer", False),
                                question_id=choice_data.get("question_id", ""),
                            )
                            choices.append(choice)

                        # Create Question object with converted choices
                        question_obj = Question(
                            id=question.get("id", ""),
                            question=question.get("question", ""),
                            quiz_id=question.get("quiz_id", ""),
                            created_at=question.get("created_at", ""),
                            choices=choices,
                        )
                        question_objects.append(question_obj)
                        print(f"Created question object: {question_obj}")
                    except Exception as e:
                        print(f"Error processing question: {str(e)}")
                        continue

                print(f"Total questions created: {len(question_objects)}")
                return question_objects
            else:
                print(f"Error fetching questions: {response.status_code}")
                print(f"Error response: {response.text}")
                return []
        except Exception as e:
            print(f"Exception while fetching questions: {str(e)}")
            return []

    def create_question(self, question: Question) -> Question:
        """Create a new question"""
        response = requests.post(
            f"{API_BASE_URL}/question", json={"question": question}
        )
        question = response.json()
        return Question(**question)

    def create_choice(self, question_id: str, choice: Choice) -> Choice:
        """Create a new choice"""
        response = requests.post(
            f"{API_BASE_URL}/choice",
            json={"question_id": question_id, "choice": choice},
        )
        choice = response.json()
        return Choice(**choice)

    def create_quiz(self, title: str) -> Quiz:
        """Create a new quiz"""
        try:
            response = requests.post(
                f"{API_BASE_URL}/quiz",
                json={"title": title, "quiz_type": "quiz", "mode": "normal"},
            )

            if response.status_code == 200:
                quiz_data = response.json()
                # Create a new Quiz object with the response data
                quiz = Quiz(
                    id=quiz_data.get("id", ""),
                    title=quiz_data.get("title", ""),
                    quiz_type=quiz_data.get("quiz_type", "quiz"),
                    mode=quiz_data.get("mode", "normal"),
                )
                return quiz
            else:
                print(f"Error creating quiz: {response.status_code}")
                print(f"Error response: {response.text}")
                raise Exception(f"Failed to create quiz: {response.text}")
        except Exception as e:
            print(f"Exception while creating quiz: {str(e)}")
            raise

    def get_quiz(self, quiz_id: int) -> Optional[Quiz]:
        """Get a quiz by ID"""
        return next((q for q in self._quizzes if q.id == quiz_id), None)

    def get_all_quizzes(self) -> List[Quiz]:
        """Get all quizzes"""
        response = requests.get(f"{API_BASE_URL}/quiz")
        quizzes = response.json()
        return [Quiz(**quiz) for quiz in quizzes]

    def update_quiz(
        self,
        quiz_id: int,
        title: Optional[str] = None,
        description: Optional[str] = None,
        time_limit: Optional[int] = None,
        passing_score: Optional[float] = None,
    ) -> Optional[Quiz]:
        """Update a quiz's details"""
        quiz = self.get_quiz(quiz_id)
        if not quiz:
            return None

        if title:
            quiz.title = title
        if description:
            quiz.description = description
        if time_limit is not None:
            quiz.time_limit = time_limit
        if passing_score is not None:
            quiz.passing_score = passing_score

        quiz.updated_at = datetime.now()
        return quiz

    def delete_quiz(self, quiz_id: int) -> bool:
        """Delete a quiz"""
        quiz = self.get_quiz(quiz_id)
        if quiz:
            self._quizzes.remove(quiz)
            return True
        return False
