from PySide6.QtWidgets import QToolButton, QPushButton

class BackButton(QToolButton):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setText("←")
        self.setStyleSheet("""
            QToolButton {
                background-color: transparent;
                border: 1px solid #E0E0E0;
                border-radius: 4px;
                padding: 4px 8px;
                font-size: 20px;
                color: #333;
            }
            QToolButton:hover {
                background-color: #F0F0F0;
            }
        """)
        self.setFixedSize(32, 32)

class ConversionButton(QPushButton):
    def __init__(self, text, parent=None):
        super().__init__(text, parent)
        self.setStyleSheet("""
            QPushButton {
                background-color: #F5F5F5;
                border: none;
                border-radius: 4px;
                padding: 8px 16px;
                color: #666;
                font-size: 13px;
            }
            QPushButton:hover {
                background-color: #E8E8E8;
            }
        """) 