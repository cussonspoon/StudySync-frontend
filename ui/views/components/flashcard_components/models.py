from dataclasses import dataclass
from typing import List
from datetime import datetime

@dataclass
class TermWord:
    id: int
    term: str
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
                term="Variable",
                definition="A container for storing data values in programming",
                created_at=datetime.now(),
                updated_at=datetime.now()
            ),
            TermWord(
                id=2,
                term="Function",
                definition="A reusable block of code that performs a specific task",
                created_at=datetime.now(),
                updated_at=datetime.now()
            ),
            TermWord(
                id=3,
                term="Loop",
                definition="A programming structure that repeats a block of code",
                created_at=datetime.now(),
                updated_at=datetime.now()
            ),
            TermWord(
                id=4,
                term="Array",
                definition="A data structure that stores a collection of elements in a contiguous block of memory",
                created_at=datetime.now(),
                updated_at=datetime.now()
            ),
            TermWord(
                id=5,
                term="Object",
                definition="An instance of a class that bundles data and methods that operate on that data",
                created_at=datetime.now(),
                updated_at=datetime.now()
            ),
            TermWord(
                id=6,
                term="Class",
                definition="A blueprint for creating objects that defines their properties and behaviors",
                created_at=datetime.now(),
                updated_at=datetime.now()
            ),
            TermWord(
                id=7,
                term="Inheritance",
                definition="A mechanism that allows a class to inherit properties and methods from another class",
                created_at=datetime.now(),
                updated_at=datetime.now()
            ),
            TermWord(
                id=8,
                term="Polymorphism",
                definition="The ability of different classes to be treated as instances of the same class through inheritance",
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
                id=9,
                term="List Comprehension",
                definition="A concise way to create lists based on existing lists",
                created_at=datetime.now(),
                updated_at=datetime.now()
            ),
            TermWord(
                id=10,
                term="Dictionary",
                definition="A data structure that stores key-value pairs",
                created_at=datetime.now(),
                updated_at=datetime.now()
            ),
            TermWord(
                id=11,
                term="Generator",
                definition="A function that returns an iterator using the yield keyword",
                created_at=datetime.now(),
                updated_at=datetime.now()
            ),
            TermWord(
                id=12,
                term="Decorator",
                definition="A design pattern that allows adding new functionality to existing objects without modifying their structure",
                created_at=datetime.now(),
                updated_at=datetime.now()
            ),
            TermWord(
                id=13,
                term="Lambda",
                definition="An anonymous function that can have any number of arguments but can only have one expression",
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