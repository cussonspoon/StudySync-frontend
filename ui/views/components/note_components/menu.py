from PySide6.QtWidgets import QMenu

class NotionStyleMenu(QMenu):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setStyleSheet("""
            QMenu {
                background-color: white;
                border: 1px solid #E0E0E0;
                border-radius: 8px;
                padding: 4px;
            }
            QMenu::item {
                padding: 8px 24px 8px 8px;
                border-radius: 4px;
            }
            QMenu::item:selected {
                background-color: #F0F0F0;
            }
            QMenu::separator {
                height: 1px;
                background: #E0E0E0;
                margin: 4px 0px;
            }
        """) 