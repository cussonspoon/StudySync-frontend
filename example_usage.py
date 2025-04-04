from utils.session_manager import SessionManager


def get_current_user_id():
    # Get the singleton instance of SessionManager
    session_manager = SessionManager.get_instance()

    # Get the current user
    current_user = session_manager.get_current_user()

    if current_user:
        return current_user.id
    else:
        print("No user is logged in")
        return None


# Example usage:
if __name__ == "__main__":
    # Get user ID
    user_id = get_current_user_id()

    if user_id:
        print(f"Current user ID: {user_id}")
        # Use the user_id for whatever you need
        # For example: fetch user's folders
        # folders = FolderService.get_user_folders(user_id)
    else:
        print("Please log in first")
