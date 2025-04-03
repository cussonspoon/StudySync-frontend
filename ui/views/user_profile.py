from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, 
    QPushButton, QFrame, QScrollArea, QSizePolicy
)
from PySide6.QtCore import Qt, QSize
from PySide6.QtGui import QFont, QPixmap, QIcon
from ui.views.components.user_components.models import get_user_by_id, get_user_statistics, get_user_activities
from datetime import datetime

class UserProfilePage(QWidget):
    def __init__(self):
        super().__init__()
        self.user_id = 1  # Default to first user for demo
        self.user = get_user_by_id(self.user_id)
        self.stats = get_user_statistics(self.user_id)
        self.activities = get_user_activities(self.user_id)
        self.setupUi()
        self.setStyleSheet("""
            QWidget {
                background-color: #FAFAFA;
            }
        """)

    def set_controller(self, controller):
        self.user_profile_controller = controller

    def setupUi(self):
        # Main layout
        layout = QVBoxLayout(self)
        layout.setContentsMargins(40, 40, 40, 40)
        layout.setSpacing(30)

        # Header with title and image
        header_layout = QHBoxLayout()
        header_layout.setSpacing(20)

        # Title
        title_label = QLabel("My Profile")
        title_label.setFont(QFont("Inter", 24, QFont.Weight.Bold))
        title_label.setStyleSheet("color: #1A1A1A;")
        header_layout.addWidget(title_label)

        # Profile image
        image_label = QLabel()
        pixmap = QPixmap(self.user.profile_img if self.user else "static/images/logo.png")
        scaled_pixmap = pixmap.scaled(100, 100, Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation)
        image_label.setPixmap(scaled_pixmap)
        image_label.setFixedSize(100, 100)
        image_label.setStyleSheet("""
            QLabel {
                background-color: white;
                border-radius: 50px;
                border: 2px solid #E0E0E0;
            }
        """)
        header_layout.addWidget(image_label)
        header_layout.addStretch()
        layout.addLayout(header_layout)

        # Scroll area for content
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setStyleSheet("""
            QScrollArea {
                border: none;
                background-color: transparent;
            }
            QScrollBar:vertical {
                border: none;
                background: #F5F5F5;
                width: 10px;
                border-radius: 5px;
            }
            QScrollBar::handle:vertical {
                background: #CCCCCC;
                border-radius: 5px;
            }
            QScrollBar::handle:vertical:hover {
                background: #999999;
            }
        """)

        content_widget = QWidget()
        content_layout = QVBoxLayout(content_widget)
        content_layout.setSpacing(30)

        # Profile Information Section
        profile_section = QFrame()
        profile_section.setStyleSheet("""
            QFrame {
                background-color: white;
                border-radius: 12px;
                box-shadow: 0 2px 4px rgba(0, 0, 0, 0.05);
            }
        """)
        profile_layout = QVBoxLayout(profile_section)
        profile_layout.setContentsMargins(30, 30, 30, 30)
        profile_layout.setSpacing(20)

        # Section title
        profile_title = QLabel("Profile Information")
        profile_title.setFont(QFont("Inter", 18, QFont.Weight.Bold))
        profile_title.setStyleSheet("color: #1A1A1A;")
        profile_layout.addWidget(profile_title)

        # Profile fields
        fields = [
            ("Username", self.user.username if self.user else ""),
            ("Created At", self.user.created_at.strftime("%B %d, %Y") if self.user else ""),
        ]

        for label_text, value_text in fields:
            field_layout = QHBoxLayout()
            
            # Label
            label = QLabel(label_text)
            label.setFont(QFont("Inter", 12))
            label.setStyleSheet("color: #666666;")
            label.setFixedWidth(100)
            field_layout.addWidget(label)
            
            # Value
            value = QLabel(value_text)
            value.setFont(QFont("Inter", 12))
            value.setStyleSheet("color: #1A1A1A;")
            field_layout.addWidget(value)
            field_layout.addStretch()
            
            profile_layout.addLayout(field_layout)

        content_layout.addWidget(profile_section)

        # Statistics Section
        stats_section = QFrame()
        stats_section.setStyleSheet("""
            QFrame {
                background-color: white;
                border-radius: 12px;
                box-shadow: 0 2px 4px rgba(0, 0, 0, 0.05);
            }
        """)
        stats_layout = QVBoxLayout(stats_section)
        stats_layout.setContentsMargins(30, 30, 30, 30)
        stats_layout.setSpacing(20)

        # Section title
        stats_title = QLabel("Statistics")
        stats_title.setFont(QFont("Inter", 18, QFont.Weight.Bold))
        stats_title.setStyleSheet("color: #1A1A1A;")
        stats_layout.addWidget(stats_title)

        # Stats grid
        stats_grid = QHBoxLayout()
        stats_grid.setSpacing(20)

        if self.stats:
            stats = [
                ("Folders", str(self.stats.folders_created)),
                ("Notes", str(self.stats.notes_created)),
                ("Quizzes", str(self.stats.quizzes_taken)),
                ("Posts", str(self.stats.total_posts))
            ]
        else:
            stats = [
                ("Folders", "0"),
                ("Notes", "0"),
                ("Quizzes", "0"),
                ("Posts", "0")
            ]

        for title, value in stats:
            stat_card = QFrame()
            stat_card.setStyleSheet("""
                QFrame {
                    background-color: #F8F9FA;
                    border-radius: 8px;
                }
            """)
            card_layout = QVBoxLayout(stat_card)
            card_layout.setContentsMargins(20, 20, 20, 20)
            card_layout.setSpacing(10)

            value_label = QLabel(value)
            value_label.setFont(QFont("Inter", 24, QFont.Weight.Bold))
            value_label.setStyleSheet("color: #1A1A1A;")
            value_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
            card_layout.addWidget(value_label)

            title_label = QLabel(title)
            title_label.setFont(QFont("Inter", 12))
            title_label.setStyleSheet("color: #666666;")
            title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
            card_layout.addWidget(title_label)

            stats_grid.addWidget(stat_card)

        stats_layout.addLayout(stats_grid)
        content_layout.addWidget(stats_section)

        # Recent Activity Section
        activity_section = QFrame()
        activity_section.setStyleSheet("""
            QFrame {
                background-color: white;
                border-radius: 12px;
                box-shadow: 0 2px 4px rgba(0, 0, 0, 0.05);
            }
        """)
        activity_layout = QVBoxLayout(activity_section)
        activity_layout.setContentsMargins(30, 30, 30, 30)
        activity_layout.setSpacing(20)

        # Section title
        activity_title = QLabel("Recent Activity")
        activity_title.setFont(QFont("Inter", 18, QFont.Weight.Bold))
        activity_title.setStyleSheet("color: #1A1A1A;")
        activity_layout.addWidget(activity_title)

        # Activity items
        for activity in self.activities:
            activity_item = QFrame()
            activity_item.setStyleSheet("""
                QFrame {
                    background-color: #F8F9FA;
                    border-radius: 8px;
                }
            """)
            item_layout = QHBoxLayout(activity_item)
            item_layout.setContentsMargins(20, 15, 20, 15)

            activity_label = QLabel(activity.description)
            activity_label.setFont(QFont("Inter", 12))
            activity_label.setStyleSheet("color: #1A1A1A;")
            item_layout.addWidget(activity_label)

            # Convert timestamp to relative time
            time_diff = datetime.now() - activity.timestamp
            if time_diff.days > 0:
                time_text = f"{time_diff.days} days ago"
            else:
                hours = time_diff.seconds // 3600
                if hours > 0:
                    time_text = f"{hours} hours ago"
                else:
                    minutes = (time_diff.seconds % 3600) // 60
                    time_text = f"{minutes} minutes ago"

            time_label = QLabel(time_text)
            time_label.setFont(QFont("Inter", 12))
            time_label.setStyleSheet("color: #666666;")
            item_layout.addWidget(time_label)

            activity_layout.addWidget(activity_item)

        content_layout.addWidget(activity_section)
        content_layout.addStretch()

        scroll.setWidget(content_widget)
        layout.addWidget(scroll) 