from dataclasses import dataclass
from typing import Optional


@dataclass
class User:
    id: str
    username: str
    email: str
    # Add any other user fields you need

@dataclass
class Folder:
    id: str
    name: str
    total_items: int
    created_at: str
    img_url: str

# Global user instance
_current_user: Optional[User] = None
_current_folder: Optional[Folder] = None


def get_current_user() -> Optional[User]:
    """Get the current user information."""
    global _current_user
    return _current_user


def set_current_user(user_data: dict) -> None:
    """Set the current user information."""
    global _current_user
    if user_data:
        _current_user = User(
            id=user_data.get("id"),
            username=user_data.get("username"),
            email=user_data.get("email"),
        )
    else:
        _current_user = None


def clear_current_user() -> None:
    """Clear the current user information."""
    global _current_user
    _current_user = None


def get_current_folder() -> Optional[Folder]:
    """Get the current folder information."""
    global _current_folder
    return _current_folder


def set_current_folder(folder_data: dict) -> None:
    """Set the current folder information."""
    global _current_folder
    if folder_data:
        _current_folder = Folder(
            id=folder_data.get("id"),
            name=folder_data.get("name"),
            total_items=folder_data.get("total_items"),
            created_at=folder_data.get("created_at"),
            img_url=folder_data.get("img_url"),
        )
    else:
        _current_folder = None
    