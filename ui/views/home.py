import sys
import os
from PySide6.QtCore import Qt, QDir, QPoint, Signal
from PySide6.QtGui import QFont, QPixmap, QColor
from PySide6.QtWidgets import QGraphicsDropShadowEffect
from PySide6.QtWidgets import (
    QApplication,
    QMainWindow,
    QFrame,
    QLabel,
    QScrollArea,
    QWidget,
    QPushButton,
    QVBoxLayout,
    QHBoxLayout,
    QLineEdit,
    QLabel,
    QFrame,
    QScrollArea,
    QSizePolicy,
    QSpacerItem,
    QGridLayout,
)

from ui.views.components.carousel import HorizontalImageScroller
from utils.ui import Text, Image, SearchBar
from ui.views.components.calendar import CalendarWidget
from ui.views.components.folder import Folder
from utils.global_vars import get_current_user


class HomePage(QWidget):

    def __init__(self):
        super().__init__()
        self.folders = []
        self.tasks = []
        self.search_results = []
        self.setupUi()
        self.setupSearchMechanism()
        self.loadUserData()
        user = get_current_user()
        if user:
            print(f"User ID: {user.id}")
            print(f"Username: {user.username}")
            print(f"Email: {user.email}")

    def setupUi(self):
        self.setObjectName("Form")
        self.setStyleSheet("background-color: #FAFAFA;")

        # Create a container for search frame and shadow
        search_container = QWidget(self)
        search_container_layout = QVBoxLayout(search_container)
        search_container_layout.setContentsMargins(0, 0, 0, 0)
        search_container_layout.setSpacing(0)

        self.searchFrame = QFrame()
        self.searchFrame.setFixedHeight(80)
        self.searchFrame.setStyleSheet(
            "background-color: #F8F6F1; margin: 0px; padding: 0px;"
        )

        # Create shadow frame
        shadow_frame = QFrame()
        shadow_frame.setFixedHeight(2)  # Reduced from 8 to 2
        shadow_frame.setStyleSheet(
            """
            QFrame {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 rgba(0, 0, 0, 0.08),
                    stop:1 rgba(0, 0, 0, 0));
            }
        """
        )

        search_container_layout.addWidget(self.searchFrame)
        search_container_layout.addWidget(shadow_frame)

        search_layout = QVBoxLayout(self.searchFrame)
        search_layout.setAlignment(Qt.AlignCenter)
        self.searchBar = SearchBar(self.searchFrame)
        search_layout.addWidget(self.searchBar)
        self.searchFrame.setLayout(search_layout)

        self.scrollArea = QScrollArea(self)
        self.scrollArea.setWidgetResizable(True)
        self.scrollArea.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        self.scrollArea.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.scrollArea.setStyleSheet("background-color: #F8F6F1;")

        self.scrollAreaWidgetContents = QWidget()
        self.scroll_layout = QVBoxLayout(self.scrollAreaWidgetContents)
        self.scroll_layout.setAlignment(Qt.AlignTop)
        self.scroll_layout.setSpacing(10)

        self.bannerFrame = QFrame(self.scrollAreaWidgetContents)
        self.bannerFrame.setFixedSize(1171, 360)
        self.bannerLayout = QVBoxLayout(self.bannerFrame)
        self.bannerLayout.setContentsMargins(0, 0, 0, 0)
        self.bannerFrame.setStyleSheet("margin: 0px;")
        self.bannerLayout.setAlignment(Qt.AlignTop)

        self.bannerPic = Image(1171, 291, "banner.jpg", self.bannerFrame)
        self.bannerLayout.addWidget(self.bannerPic)

        self.profilePic = Image(91, 91, "profile.jpg", self.bannerFrame)
        self.profilePic.move(30, 250)  # Adjust overlap

        self.bannerPic.setStyleSheet("margin: 0px; padding: 0px;")
        self.profilePic.setStyleSheet("margin: 0px; padding: 0px;")

        self.bannerFrame.setLayout(self.bannerLayout)
        self.scroll_layout.addWidget(self.bannerFrame)
        self.bannerFrame.setStyleSheet("background-color: transparent;")

        collection_layout = QHBoxLayout()
        self.collectionIcon = Image(
            155, 101, "collectionIcon.png", self.scrollAreaWidgetContents
        )
        self.collectionText = Text(
            21, "My Collections", "333333", self.scrollAreaWidgetContents
        )

        collection_layout.addWidget(self.collectionText)
        collection_layout.addWidget(self.collectionIcon)
        collection_layout.addStretch()  # Pushes content to the left

        collection_container = QFrame(self.scrollAreaWidgetContents)
        collection_container.setLayout(collection_layout)
        collection_container.setMaximumWidth(1171)  # Match banner width
        self.scroll_layout.addWidget(collection_container)

        self.collections = HorizontalImageScroller(
            self.folders, self.scrollAreaWidgetContents
        )
        self.collections.setMaximumWidth(1171)  # Match banner width
        self.scroll_layout.addWidget(self.collections)

        spacing_collections = QFrame(self.scrollAreaWidgetContents)
        spacing_collections.setFixedHeight(20)  # 20px spacing
        self.scroll_layout.addWidget(spacing_collections)

        self.recommendsText = Text(
            21, "Recommended folders for you", "333333", self.scrollAreaWidgetContents
        )
        self.scroll_layout.addWidget(self.recommendsText)

        self.recommendFolders = HorizontalImageScroller(
            self.folders, self.scrollAreaWidgetContents
        )
        self.recommendFolders.setMaximumWidth(1171)  # Match banner width
        self.scroll_layout.addWidget(self.recommendFolders)

        spacing_recommended = QFrame(self.scrollAreaWidgetContents)
        spacing_recommended.setFixedHeight(20)  # 20px spacing
        self.scroll_layout.addWidget(spacing_recommended)

        task_layout = QHBoxLayout()
        self.taskText = Text(21, "Task", "333333", self.scrollAreaWidgetContents)
        self.taskImg = Image(141, 130, "task.png", self.scrollAreaWidgetContents)

        task_layout.addWidget(self.taskText)
        task_layout.addWidget(self.taskImg)
        task_layout.addStretch()

        task_container = QFrame(self.scrollAreaWidgetContents)
        task_container.setLayout(task_layout)
        task_container.setMaximumWidth(1171)  # Match banner width
        self.scroll_layout.addWidget(task_container)

        task_n_cal_layout = QHBoxLayout()
        task_n_cal_layout.setSpacing(0)

        self.taskManagement = TaskManagement(
            0, 0, 800, 700, self.tasks, self.scrollAreaWidgetContents
        )
        self.taskManagement.setMinimumHeight(400)
        self.taskManagement.setMaximumWidth(800)  # Limit task management width

        # Create a container for the calendar
        calendar_container = QFrame()
        calendar_container.setStyleSheet(
            """
            QFrame {
                background-color: white;
                border: none;
                border-radius: 5px;
            }
        """
        )
        shadow = QGraphicsDropShadowEffect()
        shadow.setBlurRadius(15)
        shadow.setColor(QColor(0, 0, 0, 80))
        shadow.setOffset(0, 2)
        calendar_container.setGraphicsEffect(shadow)
        calendar_container.setMaximumWidth(350)  # Limit calendar width

        calendar_layout = QVBoxLayout(calendar_container)
        calendar_layout.setContentsMargins(
            10, 10, 10, 10
        )  # Add padding around calendar
        calendar_layout.setAlignment(
            Qt.AlignCenter
        )  # Center the calendar in its container

        self.calendar = CalendarWidget()
        calendar_layout.addWidget(
            self.calendar, alignment=Qt.AlignCenter
        )  # Center the calendar widget

        task_n_cal_layout.addWidget(self.taskManagement)
        task_n_cal_layout.addWidget(calendar_container)
        task_n_cal_layout.setSpacing(0)

        task_n_cal_container = QWidget(self.scrollAreaWidgetContents)
        task_n_cal_container.setLayout(task_n_cal_layout)
        task_n_cal_container.setStyleSheet(
            """
            QWidget {
                border: none;
                border-radius: 10px;
                background-color: #FAFAFA;
            }
        """
        )
        task_n_cal_container.setMaximumWidth(1171)  # Match banner width

        self.scroll_layout.addWidget(task_n_cal_container)
        self.scrollAreaWidgetContents.setLayout(self.scroll_layout)
        self.scrollArea.setWidget(self.scrollAreaWidgetContents)

        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)  # Remove default margins
        main_layout.setSpacing(0)  # Remove spacing between widgets
        main_layout.addWidget(search_container)
        main_layout.addWidget(self.scrollArea)
        self.setLayout(main_layout)
        self.setStyleSheet(
            """
            QWidget {
                background-color: #FAFAFA;
            }

            QScrollArea {
                border: none;
                background-color: #FAFAFA;
            }
            QScrollBar:vertical {
                border: none;
                background-color: transparent;
                width: 6px;
                margin: 0px;
            }
            QScrollBar::handle:vertical {
                background-color: #BDBDBD;
                border-radius: 3px;
                min-height: 30px;
                margin: 2px 0;
            }
            QScrollBar::handle:vertical:hover {
                background-color: #9E9E9E;
            }
            QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {
                height: 0px;
            }
            QScrollBar::add-page:vertical, QScrollBar::sub-page:vertical {
                background: none;
            }
        """
        )

    def set_controller(self, controller):
        self.home_controller = controller
        # Connect the controller to TaskManagement
        if hasattr(self, "taskManagement"):
            self.taskManagement.set_controller(controller)

    def update_scroll_height(self):
        """Adjusts the scroll area height when tasks are added."""
        total_height = self.scroll_layout.sizeHint().height() + 20  # Add extra padding
        self.scrollAreaWidgetContents.setMinimumHeight(total_height)

    def update_tasks(self, tasks):
        """Updates the task list and refreshes the task management UI"""
        self.tasks = tasks
        if hasattr(self, "taskManagement"):
            self.taskManagement.load_tasks(tasks)

    def setupSearchMechanism(self):
        # Create a container for search results that appears below search bar
        self.search_results_container = QFrame(self)
        self.search_results_container.setStyleSheet(
            """
            QFrame {
                background-color: white;
                border: 1px solid #E0E0E0;
                border-radius: 4px;
                z-index: 999;
            }
            """
        )
        self.search_results_container.hide()
        self.search_results_container.raise_()

        self.search_results_layout = QVBoxLayout(self.search_results_container)
        self.search_results_layout.setContentsMargins(0, 0, 0, 0)
        self.search_results_layout.setSpacing(0)

        # Try to find the QLineEdit in the SearchBar
        for child in self.searchBar.children():
            if isinstance(child, QLineEdit):
                child.textChanged.connect(self.on_search_text_changed)
                print("Connected to search input")  # Debug print
                break

        # Add debug prints
        print(
            "SearchBar children:",
            [type(child).__name__ for child in self.searchBar.children()],
        )

    def on_search_text_changed(self, text):
        print(f"Search text changed: {text}")  # Debug print
        if not text:
            self.search_results_container.hide()
            self.show_normal_content()
            return

        # Get search results from service for each character typed
        if self.home_controller:
            print(f"Calling searchFolders with text: {text}")  # Debug print
            self.search_results = self.home_controller.searchFolders(text)
            print(f"Got search results: {self.search_results}")  # Debug print
            self.update_search_results()
        else:
            print("No home_controller available")  # Debug print

    def update_search_results(self):
        # Clear previous results
        while self.search_results_layout.count():
            item = self.search_results_layout.takeAt(0)
            if item.widget():
                item.widget().deleteLater()

        if self.search_results:
            # Show immediate results under search bar
            for folder in self.search_results[:3]:  # Show top 3 results
                result_btn = QPushButton(folder["name"])
                result_btn.setFixedHeight(40)  # Set fixed height for each result
                result_btn.setStyleSheet(
                    """
                    QPushButton {
                        text-align: left;
                        padding: 8px 16px;
                        border: none;
                        background: transparent;
                        font-size: 14px;
                        color: black;
                    }
                    QPushButton:hover {
                        background-color: #F5F5F5;
                    }
                    """
                )
                result_btn.clicked.connect(
                    lambda checked, f=folder: self.show_search_results([f])
                )
                self.search_results_layout.addWidget(result_btn)

            # Show "Show all results" button if there are more results
            if len(self.search_results) > 3:
                show_all_btn = QPushButton(
                    f"Show all {len(self.search_results)} results"
                )
                show_all_btn.setFixedHeight(40)  # Set fixed height
                show_all_btn.setStyleSheet(
                    """
                    QPushButton {
                        text-align: left;
                        padding: 8px 16px;
                        border-top: 1px solid #E0E0E0;
                        background: transparent;
                        color: #1a73e8;
                        font-size: 14px;
                    }
                    QPushButton:hover {
                        background-color: #F5F5F5;
                    }
                    """
                )
                show_all_btn.clicked.connect(
                    lambda: self.show_search_results(self.search_results)
                )
                self.search_results_layout.addWidget(show_all_btn)

            # Calculate total height based on number of items
            num_items = min(len(self.search_results), 3) + (
                1 if len(self.search_results) > 3 else 0
            )
            total_height = num_items * 40  # 40px per item

        else:
            # Show "No results found" message
            no_results = QLabel("No results found")
            no_results.setFixedHeight(40)  # Set fixed height
            no_results.setStyleSheet(
                """
                QLabel {
                    padding: 8px 16px;
                    color: #666666;
                    font-size: 14px;
                }
                """
            )
            self.search_results_layout.addWidget(no_results)
            total_height = 40  # Single item height for no results

        # Position and show the container
        search_bar_pos = self.searchBar.mapTo(self, self.searchBar.rect().bottomLeft())
        self.search_results_container.move(search_bar_pos.x(), search_bar_pos.y() + 5)
        self.search_results_container.setFixedWidth(self.searchBar.width())
        self.search_results_container.setFixedHeight(total_height)  # Set dynamic height
        self.search_results_container.raise_()
        self.search_results_container.show()

    def show_search_results(self, results):
        # Hide the search results dropdown
        self.search_results_container.hide()

        # Hide ALL content first
        self.hide_normal_content()

        # Safely remove existing search results grid
        if (
            hasattr(self, "search_results_grid")
            and self.search_results_grid is not None
        ):
            try:
                self.search_results_grid.hide()
                self.scroll_layout.removeWidget(self.search_results_grid)
                self.search_results_grid.deleteLater()
            except RuntimeError:
                pass
            self.search_results_grid = None

        # Create grid layout for search results
        self.search_results_grid = QWidget(self.scrollAreaWidgetContents)
        self.search_results_grid.setStyleSheet("background-color: transparent;")
        grid_layout = QGridLayout(self.search_results_grid)
        grid_layout.setSpacing(20)
        grid_layout.setContentsMargins(20, 20, 20, 20)

        # Add folders directly to grid, 4 per row
        for i, folder in enumerate(results):
            folder_widget = Folder(
                folder["name"],
                folder["count"],
                folder["date"],
                folder["avatar"],
                folder["image"],
            )
            row = i // 4
            col = i % 4
            grid_layout.addWidget(folder_widget, row, col)

        # Add the grid to the scroll area
        self.scroll_layout.addWidget(self.search_results_grid)

    def hide_normal_content(self):
        # Hide ALL widgets in the main scroll area
        for i in range(self.scroll_layout.count()):
            widget = self.scroll_layout.itemAt(i).widget()
            if widget:
                widget.hide()

    def show_normal_content(self):
        # Show all widgets in the main scroll area
        for i in range(self.scroll_layout.count()):
            widget = self.scroll_layout.itemAt(i).widget()
            if widget and widget != self.search_results_grid:
                widget.show()

        # Safely remove search results grid
        if (
            hasattr(self, "search_results_grid")
            and self.search_results_grid is not None
        ):
            try:
                self.search_results_grid.hide()
                self.scroll_layout.removeWidget(self.search_results_grid)
                self.search_results_grid.deleteLater()
            except RuntimeError:
                pass  # Widget already deleted
            self.search_results_grid = None

    def on_folder_click(self, folder):
        if hasattr(self, "home_controller"):
            self.home_controller.navigate_to_folder(folder)
        else:
            print("No collection controller found")

    def loadUserData(self):
        # Get current user from global
        current_user = get_current_user()
        if current_user:
            print(f"Loading data for user: {current_user.id}")
            print(f"Username: {current_user.username}")
            print(f"Email: {current_user.email}")
            # Now you can use the user information to load user-specific data
            # For example:
            # self.loadUserFolders(current_user.id)
            # self.loadUserPreferences(current_user.id)
        else:
            print("No user logged in")


class TaskManagement(QWidget):
    def __init__(self, pos_x, pos_y, width, length, tasks, parent=None):
        super().__init__(parent)
        self.setWindowTitle("To-Do List")
        self.setGeometry(pos_x, pos_y, width, length)
        self.setFixedSize(width, length)
        self.tasks = tasks
        self.home_controller = None
        self.setupUi()

    def setupUi(self):
        self.layout = QVBoxLayout(self)

        # Scrollable
        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)

        self.scroll_widget = QWidget()
        self.task_container = QVBoxLayout(self.scroll_widget)

        self.scroll_area.setWidget(self.scroll_widget)

        # Add Task Button
        self.add_task_btn = QPushButton("+ Add Task")
        self.add_task_btn.clicked.connect(self.add_task)
        self.add_task_btn.setStyleSheet(
            """
            QPushButton {
                background: transparent;  
                border: none;             
                font-size: 16px;         
                color: grey;          
                padding: 5px;           
                text-align: left;
            }
            QPushButton:hover {
                color: green;           
            }
        """
        )

        self.task_container.setSpacing(2)
        self.task_container.setAlignment(Qt.AlignTop)
        self.layout.setSpacing(0)

        self.layout.addWidget(self.add_task_btn)
        self.layout.addWidget(self.scroll_area)

        # Load initial tasks
        if self.tasks:
            self.load_tasks(self.tasks)

    def set_controller(self, controller):
        self.home_controller = controller

    def load_tasks(self, tasks):
        # Clear existing tasks
        while self.task_container.count():
            item = self.task_container.takeAt(0)
            if item.widget():
                item.widget().deleteLater()

        # Add tasks from the list
        for task in tasks:
            task_ui = TaskUI(task["task_detail"], task["status"], self)
            task_ui.set_controller(self.home_controller)
            self.task_container.addWidget(task_ui)

    def add_task(self):
        if self.home_controller:
            # Create a new task UI first
            task_ui = TaskUI("", "In progress", self)
            task_ui.set_controller(self.home_controller)
            self.task_container.addWidget(task_ui)
            # Then notify the controller
            self.home_controller.createTask()


class TaskUI(QWidget):
    def __init__(self, task_detail="", status="In progress", parent=None):
        super().__init__(parent)
        self.task_detail = task_detail
        self.status = status
        self.home_controller = None
        self.setupUi()

    def set_controller(self, controller):
        self.home_controller = controller

    def setupUi(self):
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)

        task_frame = QFrame()
        task_frame.setObjectName("taskFrame")
        task_frame.setFixedHeight(50)
        task_frame.setStyleSheet(
            "background-color: #F1F0E9; padding: 0px; margin-bottom: 0px; color: black;"
        )

        task_layout = QHBoxLayout(task_frame)
        task_layout.setAlignment(Qt.AlignVCenter)

        # Store circle button as class attribute
        self.circle_btn = QPushButton("○")
        self.circle_btn.setFixedSize(20, 20)
        self.circle_btn.setStyleSheet("color: gray; border: none; font-size: 18px;")
        self.circle_btn.clicked.connect(self.toggle_status)

        self.task_input = QLineEdit()
        if self.task_detail:
            self.task_input.setText(self.task_detail)
        else:
            self.task_input.setPlaceholderText("Enter your task here...")
            # Focus the input when it's a new task
            self.task_input.setFocus()

        self.task_input.setFont(QFont("Arial", 16))
        self.task_input.setMinimumWidth(400)
        self.task_input.setFixedHeight(25)
        self.task_input.textChanged.connect(self.on_text_changed)

        self.task_input.setStyleSheet(
            """
            QLineEdit {
                border: none; 
                padding: 0px;
                color: black;
                outline: none; 
            }
            QLineEdit:focus {
                border: 0px solid #BDB395; 
                outline: none;
            }
        """
        )

        self.status_label = QLabel(self.status)
        self.status_label.setFont(QFont("Arial", 12))
        self.status_label.setStyleSheet("color: green;")

        cancel_btn = QPushButton("✕")
        cancel_btn.setFixedSize(20, 20)
        cancel_btn.setStyleSheet("color: gray; border: none; font-size: 16px;")
        cancel_btn.clicked.connect(self.delete_task)

        separator = QFrame()
        separator.setFrameShape(QFrame.HLine)
        separator.setStyleSheet("background-color: #BDB395; height: 1px; border: none;")

        task_layout.addWidget(self.circle_btn)
        task_layout.addWidget(self.task_input)
        task_layout.addWidget(self.status_label)
        task_layout.addWidget(cancel_btn)
        task_layout.addWidget(separator)

        main_layout.addWidget(task_frame)

    def on_text_changed(self):
        if self.home_controller:
            # Pass the current text to the controller
            text = self.task_input.text()
            self.home_controller.updateTask(text)

    def toggle_status(self):
        if self.home_controller:
            # Pass the current text when updating status
            self.home_controller.updateTask(self.task_input.text())
            current_status = self.status_label.text()

            if current_status == "In progress":
                # Change to Done state
                self.status_label.setText("Done")
                self.status_label.setStyleSheet("color: #FF0000;")  # Bright red
                self.circle_btn.setText("◉")
                self.circle_btn.setStyleSheet(
                    "color: #FF0000; border: none; font-size: 16px;"
                )
            else:
                # Change to In progress state
                self.status_label.setText("In progress")
                self.status_label.setStyleSheet("color: #00AA00;")  # Bright green
                self.circle_btn.setText("○")
                self.circle_btn.setStyleSheet(
                    "color: gray; border: none; font-size: 18px;"
                )

    def delete_task(self):
        if self.home_controller:
            self.home_controller.deleteTask()
            # Remove this task widget from its parent layout
            if self.parent():
                self.parent().layout().removeWidget(self)
                self.deleteLater()  # Schedule this widget for deletion

                self.parent().layout().removeWidget(self)
                self.deleteLater()  # Schedule this widget for deletion
