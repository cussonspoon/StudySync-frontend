from dataclasses import dataclass
from datetime import datetime
from typing import Optional

@dataclass
class User:
    """User model class to handle user data."""
    id: str
    username: str
    created_at: str
    profile_img: str
    password: Optional[str] = None  # Optional because we don't want to store passwords in memory

    @classmethod
    def from_dict(cls, data: dict) -> 'User':
        """Creates a User instance from a dictionary."""
        return cls(
            id=data.get("id", ""),
            username=data.get("username", ""),
            created_at=data.get("created_at", ""),
            profile_img=data.get("profile_img", ""),
            password=data.get("password")  # Optional
        )

    def to_dict(self) -> dict:
        """Converts the User instance to a dictionary."""
        data = {
            "id": self.id,
            "username": self.username,
            "created_at": self.created_at,
            "profile_img": self.profile_img
        }
        if self.password:
            data["password"] = self.password
        return data

    def __str__(self) -> str:
        """String representation of the User."""
        return f"User(id={self.id}, username={self.username}, profile_img={self.profile_img}x)"

    @property
    def created_at_datetime(self) -> datetime:
        """Returns the created_at string as a datetime object."""
        return datetime.fromisoformat(self.created_at.replace('Z', '+00:00')) 