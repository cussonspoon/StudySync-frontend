from dataclasses import dataclass
from datetime import datetime
from typing import Optional

@dataclass
class User:
    """User model class to handle user data."""
    id: str
    name: str
    username: str
    created_at: str
    password: Optional[str] = None  # Optional because we don't want to store passwords in memory

    @classmethod
    def from_dict(cls, data: dict) -> 'User':
        """Creates a User instance from a dictionary."""
        return cls(
            id=data.get("id", ""),
            name=data.get("name", ""),
            username=data.get("username", ""),
            created_at=data.get("created_at", ""),
            password=data.get("password")  # Optional
        )

    def to_dict(self) -> dict:
        """Converts the User instance to a dictionary."""
        data = {
            "id": self.id,
            "name": self.name,
            "username": self.username,
            "created_at": self.created_at
        }
        if self.password:
            data["password"] = self.password
        return data

    def __str__(self) -> str:
        """String representation of the User."""
        return f"User(id={self.id}, name={self.name}, username={self.username})"

    @property
    def created_at_datetime(self) -> datetime:
        """Returns the created_at string as a datetime object."""
        return datetime.fromisoformat(self.created_at.replace('Z', '+00:00')) 