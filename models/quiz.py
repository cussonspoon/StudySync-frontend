from dataclasses import dataclass
from typing import List, Optional
from datetime import datetime

@dataclass
class Question:
    id: int
    text: str
    options: List[str]
    correct_answer: int
    explanation: Optional[str] = None

@dataclass
class Quiz:
    id: int
    title: str
    description: str
    questions: List[Question]
    created_at: datetime
    updated_at: datetime
    time_limit: Optional[int] = None  # in minutes
    passing_score: Optional[float] = None  # percentage

    def calculate_score(self, answers: List[int]) -> float:
        """Calculate the score based on user's answers"""
        if len(answers) != len(self.questions):
            raise ValueError("Number of answers must match number of questions")
        
        correct_answers = sum(1 for q, a in zip(self.questions, answers) if q.correct_answer == a)
        return (correct_answers / len(self.questions)) * 100

    def is_passed(self, score: float) -> bool:
        """Check if the quiz was passed based on passing score"""
        if self.passing_score is None:
            return True
        return score >= self.passing_score 