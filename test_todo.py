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
    QScrollArea
)
from PySide6.QtCore import Qt, QRect
from PySide6.QtGui import QFont, QColor


#put stuff in scroll area
class ToDoApp(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("To-Do List")
        # self.setFixedSize(400, 500)
        self.setGeometry(100, 100, 400, 500)

        self.layout = QVBoxLayout(self)

        #Scrollable 
        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area.setFixedSize(380, 400) 
        
        self.scroll_widget = QWidget()
        self.task_container = QVBoxLayout(self.scroll_widget)
        
        self.scroll_area.setWidget(self.scroll_widget)

        # Add Task Button
        self.add_task_btn = QPushButton("Add Task")
        self.add_task_btn.clicked.connect(self.add_task)

        self.task_container.setSpacing(0)
        self.task_container.setAlignment(Qt.AlignTop)  
        self.layout.setSpacing(0)

        self.layout.addWidget(self.add_task_btn)
        self.layout.addWidget(self.scroll_area)

    def add_task(self):
        """Adds a new task with a circle button, text box, and status label."""

        task_frame = QFrame()
        # task_frame.setFrameShape(QFrame.Box)
        task_frame.setFixedHeight(70)
        task_frame.setStyleSheet("background-color: #F7F7F7; padding: 5px;")

        task_layout = QHBoxLayout(task_frame)

        # Circle Button (Leftmost)
        circle_btn = QPushButton("●")
        circle_btn.setFixedSize(20, 20)
        circle_btn.setStyleSheet("color: gray; border: none; font-size: 18px;")
        circle_btn.clicked.connect(lambda: self.toggle_status(status_label))

        # Task Input Field
        task_input = QLineEdit()
        task_input.setPlaceholderText("Enter your task here...")
        task_input.setFont(QFont("Arial", 12))

        task_input.setStyleSheet(
            """
            QLineEdit {
                border: 1px solid white;
                border-radius: 4px;
                padding: 5px;
                font-size: 12px;
                color: black;
                outline: none; /* Prevents the blue border */
            }
            QLineEdit:focus {
                border: 1px solid gray; /* Keeps the same border when clicked */
                outline: none;
            }
        """
        )

        # Status Label (Rightmost)
        status_label = QLabel("In Progress")
        status_label.setFont(QFont("Arial", 12))
        status_label.setStyleSheet("color: green;")

        cancel_btn = QPushButton("x")
        cancel_btn.setFixedSize(30, 30)
        cancel_btn.setStyleSheet("color: gray; border: none; font-size: 18px;")
        cancel_btn.clicked.connect(lambda: self.delete_task(task_frame))

        separator = QFrame()
        separator.setFrameShape(QFrame.HLine)

        # Add widgets to horizontal layout
        # task_frame.addWidget(task_frame)
        task_layout.addWidget(circle_btn)
        task_layout.addWidget(task_input)
        task_layout.addWidget(status_label)
        task_layout.addWidget(cancel_btn)
        task_layout.addWidget(separator)

        self.task_container.insertWidget(self.task_container.count(), task_frame)
        # spacer = QSpacerItem(0, 0, QSizePolicy.Minimum, QSizePolicy.Fixed)
        # self.task_container.addItem(spacer)

    def toggle_status(self, label):
        """Toggles the status between 'In Progress' (green) and 'Done' (red)."""
        if label.text() == "In Progress":
            label.setText("Done")
            label.setStyleSheet("color: red;")
        else:
            label.setText("In Progress")
            label.setStyleSheet("color: green;")

    def delete_task(self, task_frame):
        for i in reversed(range(self.task_container.count())): 
            item = self.task_container.itemAt(i)
            if item.widget() == task_frame: 
                item.widget().deleteLater()
                break

# Run Application
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = ToDoApp()
    window.show()
    sys.exit(app.exec())


