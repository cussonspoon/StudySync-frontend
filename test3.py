import sys
from PySide6.QtWidgets import (
    QApplication,
    QWidget,
    QPushButton,
    QVBoxLayout,
    QHBoxLayout,
    QLineEdit,
    QLabel,
    QFrame,
    QScrollArea,
    QSizePolicy
)
from PySide6.QtCore import Qt
from PySide6.QtGui import QFont


class ToDoApp(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("To-Do List")
        self.resize(400, 500)

        # ✅ Main Layout (Manages everything)
        self.layout = QVBoxLayout(self)

        # ✅ Scroll Area (Contains tasks)
        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)

        # ✅ Scroll Widget (Container for Tasks)
        self.scroll_widget = QWidget()
        self.task_container = QVBoxLayout(self.scroll_widget)  # ✅ Layout for tasks

        # ✅ Ensure scroll area contains the task container
        self.scroll_area.setWidget(self.scroll_widget)

        # ✅ Add Task Button (Above Scroll Area)
        self.add_task_btn = QPushButton("Add Task")
        self.add_task_btn.clicked.connect(self.add_task)

        # ✅ Add widgets to main layout
        self.layout.addWidget(self.add_task_btn)
        self.layout.addWidget(self.scroll_area)

    def add_task(self):
        """Adds a new task with a delete button."""
        task_frame = QFrame()
        task_frame.setFrameShape(QFrame.Box)
        task_frame.setStyleSheet("background-color: #F7F7F7; padding: 5px;")
        task_frame.setFixedHeight(70)

        task_layout = QHBoxLayout(task_frame)

        # Task Input Field
        task_input = QLineEdit()
        task_input.setPlaceholderText("Enter your task here...")
        task_input.setFont(QFont("Arial", 12))

        # Status Label
        status_label = QLabel("In Progress")
        status_label.setFont(QFont("Arial", 12))
        status_label.setStyleSheet("color: green;")

        # Delete Button
        delete_btn = QPushButton("❌")
        delete_btn.setFixedSize(25, 25)
        delete_btn.setStyleSheet("border: none; font-size: 14px; color: red;")
        delete_btn.clicked.connect(lambda: self.delete_task(task_frame))

        # Add widgets to horizontal layout
        task_layout.addWidget(task_input)
        task_layout.addWidget(status_label)
        task_layout.addWidget(delete_btn)

        # ✅ Add Task to the Layout
        self.task_container.addWidget(task_frame)

        # ✅ Dynamically Adjust Scroll Widget Height
        self.adjust_scroll_height()

    def delete_task(self, task_frame):
        """Deletes a task from the layout."""
        for i in reversed(range(self.task_container.count())): 
            item = self.task_container.itemAt(i)
            if item.widget() == task_frame: 
                item.widget().deleteLater()
                break

        self.adjust_scroll_height()  # ✅ Update height after deletion

    def adjust_scroll_height(self):
        """Dynamically adjusts the scroll area height to prevent expansion."""
        total_height = sum(self.task_container.itemAt(i).widget().height() for i in range(self.task_container.count()))
        self.scroll_widget.setMinimumHeight(total_height)  # ✅ Adjust height dynamically


# Run Application
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = ToDoApp()
    window.show()
    sys.exit(app.exec())