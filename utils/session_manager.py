from typing import Optional
from models.user import User


class SessionManager:
    _instance = None
    _current_user: Optional[User] = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(SessionManager, cls).__new__(cls)
        return cls._instance

    @classmethod
    def get_instance(cls) -> 'SessionManager':
        if cls._instance is None:
            cls._instance = SessionManager()
        return cls._instance

    def set_current_user(self, user: User) -> None:
        """Set the current logged-in user."""
        self._current_user = user

    def get_current_user(self) -> Optional[User]:
        """Get the current logged-in user."""
        return self._current_user

    def clear_session(self) -> None:
        """Clear the current session (logout)."""
        self._current_user = None

    def is_logged_in(self) -> bool:
        """Check if a user is currently logged in."""
        return self._current_user is not None 