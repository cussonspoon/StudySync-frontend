from utils.session_manager import SessionManager
from models.user import User


def test_session():
    # Get SessionManager instance
    session_manager = SessionManager.get_instance()

    # Check if there's already a logged in user
    current_user = session_manager.get_current_user()
    if current_user:
        print(f"Already logged in user:")
        print(f"ID: {current_user.id}")
        print(f"Username: {current_user.username}")
    else:
        print("No user currently logged in")

    # Create and set a test user
    print("\nSetting test user...")
    test_user = User(
        id="d592e4a8-6aea-4fa8-92dd-c562db757a0b",
        username="test_user",
        is_superuser=False,
        banner_img="",
        profile_img="",
    )
    session_manager.set_current_user(test_user)

    # Get the user ID after setting
    current_user = session_manager.get_current_user()
    print(f"\nAfter setting test user:")
    print(f"ID: {current_user.id}")
    print(f"Username: {current_user.username}")

    # Clear the session
    print("\nClearing session...")
    session_manager.clear_session()

    # Verify session is cleared
    if session_manager.get_current_user() is None:
        print("Session cleared successfully")
    else:
        print("Session not cleared properly")


if __name__ == "__main__":
    test_session()
