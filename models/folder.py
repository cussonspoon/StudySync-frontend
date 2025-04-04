from dataclasses import dataclass
from typing import List, Optional
from datetime import datetime
from models.user import User


@dataclass
class Folder:
    id: str
    name: str
    total_items: int
    img_url: str
    access: str
    created_at: str
    collaborations: List[User]


@dataclass
class CreateFolder:
    name: str
    accesss: str
    total_items: int
    total_likes: int
    img_url: str
