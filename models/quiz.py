from dataclasses import dataclass
from typing import List, Optional
from datetime import datetime

@dataclass
class Choice:
    id: str
    choice: str
    question_id: str
    is_answer: bool

@dataclass
class Question:
    id: str
    question: str
    quiz_id: str
    created_at: str
    choices: List[Choice] = None

@dataclass
class Quiz:
    id: str
    title: str
    quiz_type: str = None
    mode: str = None
    total_questions: int = None
    total_likes: int = None
    total_points: int = None
    points_to_pass: int = None
    time_limit: int = None
    folder_id: str = None
    created_at: str = None

    # def calculate_score(self, answers: List[int]) -> float:
    #     """Calculate the score based on user's answers"""
    #     if len(answers) != len(self.questions):
    #         raise ValueError("Number of answers must match number of questions")
        
    #     correct_answers = sum(1 for q, a in zip(self.questions, answers) if q.correct_answer == a)
    #     return (correct_answers / len(self.questions)) * 100

    # def is_passed(self, score: float) -> bool:
    #     """Check if the quiz was passed based on passing score"""
    #     if self.passing_score is None:
    #         return True
    #     return score >= self.passing_score 
    
