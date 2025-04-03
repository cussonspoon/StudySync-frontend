from dataclasses import dataclass
from datetime import datetime
from typing import Dict, Any, Optional, List

@dataclass
class User:
    id: int
    username: str
    hashed_password: str
    salt: str
    banner_img: str
    profile_img: str
    created_at: datetime

    @staticmethod
    def from_dict(data: Dict[str, Any]) -> 'User':
        return User(
            id=data.get('id', 0),
            username=data.get('username', ''),
            hashed_password=data.get('hashed_password', ''),
            salt=data.get('salt', ''),
            banner_img=data.get('banner_img', ''),
            profile_img=data.get('profile_img', ''),
            created_at=datetime.fromisoformat(data['created_at']) if isinstance(data.get('created_at'), str) else data.get('created_at', datetime.now())
        )

@dataclass
class UserStatistics:
    folders_created: int
    notes_created: int
    quizzes_taken: int
    quiz_score: float
    total_posts: int
    total_replies: int

    @staticmethod
    def from_dict(data: Dict[str, Any]) -> 'UserStatistics':
        return UserStatistics(
            folders_created=data.get('folders_created', 0),
            notes_created=data.get('notes_created', 0),
            quizzes_taken=data.get('quizzes_taken', 0),
            quiz_score=data.get('quiz_score', 0.0),
            total_posts=data.get('total_posts', 0),
            total_replies=data.get('total_replies', 0)
        )

@dataclass
class Activity:
    activity_type: str
    description: str
    timestamp: datetime

    @staticmethod
    def from_dict(data: Dict[str, Any]) -> 'Activity':
        return Activity(
            activity_type=data.get('activity_type', ''),
            description=data.get('description', ''),
            timestamp=datetime.fromisoformat(data['timestamp']) if isinstance(data.get('timestamp'), str) else data.get('timestamp', datetime.now())
        )

# Sample user data
SAMPLE_USER_DATA = {
    "users": [
        {
            "id": 1,
            "username": "johndoe",
            "hashed_password": "hashedpassword123",
            "salt": "randomsalt123",
            "banner_img": "static/images/default_banner.png",
            "profile_img": "static/images/logo.png",
            "created_at": "2024-01-15T08:30:00"
        },
        {
            "id": 2,
            "username": "janesmith",
            "hashed_password": "hashedpassword456",
            "salt": "randomsalt456",
            "banner_img": "static/images/default_banner.png",
            "profile_img": "static/images/default_profile.png",
            "created_at": "2024-01-20T14:45:00"
        }
    ]
}

# Sample statistics data
SAMPLE_STATISTICS = {
    1: {
        "folders_created": 15,
        "notes_created": 45,
        "quizzes_taken": 30,
        "quiz_score": 85.5,
        "total_posts": 25,
        "total_replies": 42
    },
    2: {
        "folders_created": 8,
        "notes_created": 25,
        "quizzes_taken": 15,
        "quiz_score": 78.3,
        "total_posts": 12,
        "total_replies": 28
    }
}

# Sample activity data
SAMPLE_ACTIVITIES = {
    1: [
        {
            "activity_type": "folder_created",
            "description": "Created new folder 'Study Materials'",
            "timestamp": "2024-02-10T14:30:00"
        },
        {
            "activity_type": "quiz_completed",
            "description": "Completed quiz 'Python Basics' with score 90%",
            "timestamp": "2024-02-10T12:00:00"
        },
        {
            "activity_type": "note_created",
            "description": "Added new note 'Database Design'",
            "timestamp": "2024-02-09T15:20:00"
        },
        {
            "activity_type": "post_created",
            "description": "Posted in 'Programming Help' forum",
            "timestamp": "2024-02-08T09:45:00"
        }
    ]
}

def get_user_by_id(user_id: int) -> Optional[User]:
    """Get a user by their ID from the sample data."""
    for user_data in SAMPLE_USER_DATA["users"]:
        if user_data["id"] == user_id:
            return User.from_dict(user_data)
    return None

def get_user_statistics(user_id: int) -> Optional[UserStatistics]:
    """Get statistics for a specific user."""
    if user_id in SAMPLE_STATISTICS:
        return UserStatistics.from_dict(SAMPLE_STATISTICS[user_id])
    return None

def get_user_activities(user_id: int) -> List[Activity]:
    """Get recent activities for a specific user."""
    activities = SAMPLE_ACTIVITIES.get(user_id, [])
    return [Activity.from_dict(activity) for activity in activities] 