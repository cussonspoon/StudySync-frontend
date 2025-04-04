from services.folder_service import FolderService
from models.folder import CreateFolder, Folder
from models.user import User
from utils.session_manager import SessionManager
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()


def test_folder_api():
    # Get current user from session
    session_manager = SessionManager.get_instance()
    current_user = session_manager.get_current_user()

    if not current_user:
        # For testing, create a test user if none is logged in
        test_user = User(
            id="d592e4a8-6aea-4fa8-92dd-c562db757a0b",
            username="test_user",
            is_superuser=False,
            banner_img="",
            profile_img="",
        )
        session_manager.set_current_user(test_user)
        current_user = test_user

    # Test data
    user_id = current_user.id
    test_folder_name = "Test Physics Folder"
    updated_folder_name = "Updated Physics Folder"

    # Ensure API base URL is set
    if not os.getenv("BASE_URL"):
        raise Exception("BASE_URL environment variable is not set")

    created_folder = None

    try:
        print("\n=== Testing Folder API ===")
        print(f"Testing with user: {current_user.username} (ID: {current_user.id})")

        # Show initial folders
        print("\nInitial folders:")
        initial_folders = FolderService.get_user_folders(user_id)
        print(f"Found {len(initial_folders)} folders initially:")
        for folder in initial_folders:
            print(f"- {folder.name}")

        # Clean up any existing test folders
        print("\nCleaning up existing test folders...")
        for folder in initial_folders:
            if folder.name in [test_folder_name, updated_folder_name]:
                folder_service = FolderService(folder)
                folder_service.delete_folder()
                print(f"Deleted existing folder: {folder.name}")

        # 1. Test Create Folder
        print("\n1. Testing Create Folder")
        folder_data = CreateFolder(
            name=test_folder_name,
            accesss="private",
            total_items=0,
            total_likes=0,
            img_url="",
        )
        folder_service = FolderService(None)  # None since we're creating new
        created_folder = folder_service.create_folder(folder_data, user_id)
        print(f"Created folder: {created_folder.name} with ID: {created_folder.id}")

        # 2. Test Get Folder by ID
        print("\n2. Testing Get Folder by ID")
        retrieved_folder = FolderService.get_folder_by_id(created_folder.id)
        print(f"Retrieved folder: {retrieved_folder.name}")

        # 3. Test Update Folder
        print("\n3. Testing Update Folder")
        folder_service = FolderService(created_folder)
        updated_folder = folder_service.update_folder(
            name=updated_folder_name,
            access="public",
            img_url="https://example.com/image.jpg",
        )
        print(f"Updated folder name to: {updated_folder.name}")

        # 4. Test Get User Folders
        print("\n4. Testing Get User Folders")
        user_folders = FolderService.get_user_folders(user_id)
        print(f"Found {len(user_folders)} folders for user")
        for folder in user_folders:
            print(f"- {folder.name}")

        # 5. Test Delete Folder
        print("\n5. Testing Delete Folder")
        folder_service = FolderService(updated_folder)
        result = folder_service.delete_folder()
        print("Successfully deleted folder")

        # 6. Test Get Public Folders
        # print("\n6. Testing Get Public Folders")
        # public_folders = FolderService.get_public_folders()
        # print(f"Found {len(public_folders)} public folders")
        # for folder in public_folders:
        #     print(f"- {folder.name}")

        # 7. Test Add Collaborator
        # print("\n7. Testing Add Collaborator")
        # folder_service = FolderService(new_folder)
        # result = folder_service.add_folder_collaborations("test_user")
        # print("Added collaborator successfully")

        # 8. Test Delete Folder
        # print("\n8. Testing Delete Folder")
        # folder_service = FolderService(new_folder)
        # result = folder_service.delete_folder()
        # print("Deleted folder successfully")

        print("\n=== All tests completed successfully ===")

    except Exception as e:
        print(f"\nError during testing: {str(e)}")
    finally:
        # Clean up the created test folder if it wasn't already deleted
        if created_folder:
            try:
                # Check if folder still exists
                try:
                    FolderService.get_folder_by_id(created_folder.id)
                    # If we get here, folder still exists and needs to be deleted
                    folder_service = FolderService(created_folder)
                    folder_service.delete_folder()
                    print(f"\nCleaned up test folder: {created_folder.name}")
                except:
                    # Folder doesn't exist, which is what we want
                    pass

                # Show final folders
                print("\nFinal folders after cleanup:")
                final_folders = FolderService.get_user_folders(user_id)
                print(f"Found {len(final_folders)} folders:")
                for folder in final_folders:
                    print(f"- {folder.name}")
            except Exception as e:
                print(f"\nError cleaning up test folder: {str(e)}")


if __name__ == "__main__":
    test_folder_api()
