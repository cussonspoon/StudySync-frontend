from dataclasses import dataclass
from typing import List, Optional
from datetime import datetime

from dataclasses import dataclass
from typing import List, Optional
from datetime import datetime

@dataclass
class TermWord:
    id: str
    term: str
    definition: str
    created_at: Optional[str] = None
    updated_at: Optional[str] = None

@dataclass
class Flashcard:
    id: str
    name: str
    description: str
    terms: List[TermWord] = None
    created_at: Optional[str] = None
    updated_at: Optional[str] = None
