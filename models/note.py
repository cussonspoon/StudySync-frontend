
from dataclasses import dataclass
from typing import List, Optional
from datetime import datetime
from models.user import User


@dataclass
class CreateNote:
    name: str
    content: str
    owner_id: str
    folder_id: str

@dataclass
class UpdateNote:
    name: str = None
    content: str = None
    owner_id: str = None
    folder_id: str = None
