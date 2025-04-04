from dataclasses import dataclass
from typing import Optional


@dataclass
class User:
    id: str
    username: str
    email: str
    # Add any other user fields you need


# Global user instance
_current_user: Optional[User] = None


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
