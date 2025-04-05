
from dataclasses import dataclass
from typing import List, Optional
from datetime import datetime
from models.user import User


@dataclass
class Note:
    id: str
    name: str
    content: int
    owner_id: str
    folder_id: str
    created_at: str

@dataclass
class UpdateNote:
    name: str = None
    content: str 
    owner_id: str = None
    folder_id: str = None
