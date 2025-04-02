from dataclasses import dataclass
from typing import List
from datetime import datetime

@dataclass
class TermWord:
    id: int
    word: str
    definition: str
    created_at: datetime
    updated_at: datetime

@dataclass
class Flashcard:
    id: int
    name: str
    description: str
    terms: List[TermWord]
    created_at: datetime
    updated_at: datetime

# Sample data
SAMPLE_FLASHCARDS = [
    Flashcard(
        id=1,
        name="Programming Fundamentals",
        description="Basic programming concepts and terminology",
        terms=[
            TermWord(
                id=1,
                word="Variable",
                definition="A container for storing data values in programming",
                created_at=datetime.now(),
                updated_at=datetime.now()
            ),
            TermWord(
                id=2,
                word="Function",
                definition="A reusable block of code that performs a specific task",
                created_at=datetime.now(),
                updated_at=datetime.now()
            ),
            TermWord(
                id=3,
                word="Loop",
                definition="A programming structure that repeats a block of code",
                created_at=datetime.now(),
                updated_at=datetime.now()
            )
        ],
        created_at=datetime.now(),
        updated_at=datetime.now()
    ),
    Flashcard(
        id=2,
        name="Python Basics",
        description="Essential Python programming concepts",
        terms=[
            TermWord(
                id=4,
                word="List Comprehension",
                definition="A concise way to create lists based on existing lists",
                created_at=datetime.now(),
                updated_at=datetime.now()
            ),
            TermWord(
                id=5,
                word="Dictionary",
                definition="A data structure that stores key-value pairs",
                created_at=datetime.now(),
                updated_at=datetime.now()
            )
        ],
        created_at=datetime.now(),
        updated_at=datetime.now()
    )
]

def get_sample_flashcards() -> List[Flashcard]:
    """Get the list of sample flashcards."""
    return SAMPLE_FLASHCARDS

def get_flashcard_by_id(flashcard_id: int) -> Flashcard:
    """Get a specific flashcard by its ID."""
    for flashcard in SAMPLE_FLASHCARDS:
        if flashcard.id == flashcard_id:
            return flashcard
    return None 