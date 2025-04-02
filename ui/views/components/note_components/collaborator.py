from PySide6.QtWidgets import QFrame, QHBoxLayout, QLabel, QPushButton
from PySide6.QtGui import QFont

class CollaboratorChip(QFrame):
    def __init__(self, name, color, parent=None):
        super().__init__(parent)
        self.setFixedHeight(40)
        layout = QHBoxLayout(self)
        layout.setContentsMargins(8, 2, 8, 2)
        layout.setSpacing(4)

        # Name label
        self.label = QLabel(name)
        self.label.setFont(QFont("Arial", 12))
        layout.addWidget(self.label)

        # Close button
        self.close_btn = QPushButton("×")
        self.close_btn.setFixedSize(16, 16)
        self.close_btn.clicked.connect(self.deleteLater)
        layout.addWidget(self.close_btn)

        # Styling
        self.setStyleSheet(f"""
            CollaboratorChip {{
                background-color: {color};
                border-radius: 14px;
            }}
            QLabel {{
                color: #333333;
                background: transparent;
            }}
            QPushButton {{
                background: transparent;
                border: none;
                color: #666666;
                font-size: 14px;
            }}
            QPushButton:hover {{
                color: #333333;
            }}
        """) 