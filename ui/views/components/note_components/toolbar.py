from PySide6.QtWidgets import QToolBar, QComboBox, QFontComboBox
from PySide6.QtCore import Qt
from PySide6.QtGui import QFont, QAction

class FloatingToolBar(QToolBar):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setMovable(False)
        self.setFloatable(False)
        self.setStyleSheet("""
            QToolBar {
                background-color: white;
                border: 1px solid #E0E0E0;
                border-radius: 8px;
                padding: 5px;
                box-shadow: 0 2px 4px rgba(0,0,0,0.1);
            }
            QToolButton {
                border: none;
                padding: 5px;
                border-radius: 4px;
                min-width: 24px;
                min-height: 24px;
            }
            QToolButton:hover {
                background-color: #F0F0F0;
            }
            QToolButton:checked {
                background-color: #E0E0E0;
            }
            QComboBox {
                border: 1px solid #E0E0E0;
                border-radius: 4px;
                padding: 2px;
                min-width: 100px;
            }
            QSpinBox {
                border: 1px solid #E0E0E0;
                border-radius: 4px;
                padding: 2px;
                min-width: 60px;
            }
        """)
        self.setupActions()

    def setupActions(self):
        # Block type selector
        self.block_type = QComboBox()
        self.block_type.addItems(["Text", "Heading 1", "Heading 2", "Heading 3", "To-do", "Callout", "Quote"])
        self.block_type.currentTextChanged.connect(self.parent().setBlockType)
        self.addWidget(self.block_type)

        self.addSeparator()

        # Font family
        self.font_combo = QFontComboBox()
        self.font_combo.currentFontChanged.connect(self.parent().setFontFamily)
        self.addWidget(self.font_combo)

        # Font size with both combo and spinbox functionality
        self.font_size = QComboBox()
        self.font_size.setEditable(True)
        self.font_size.setFixedWidth(70)
        sizes = ["8", "9", "10", "11", "12", "14", "16", "18", "20", "24", "28", "32", "36", "48", "72"]
        self.font_size.addItems(sizes)
        self.font_size.setCurrentText("12")
        
        # Connect both editing finished and selection change
        self.font_size.currentTextChanged.connect(self.handleFontSizeChange)
        self.font_size.setStyleSheet("""
            QComboBox {
                border: 1px solid #E0E0E0;
                border-radius: 4px;
                padding: 2px 5px;
            }
            QComboBox::drop-down {
                border: none;
                width: 20px;
            }
            QComboBox::down-arrow {
                width: 12px;
                height: 12px;
            }
        """)
        self.addWidget(self.font_size)

        # Text alignment
        self.alignment_combo = QComboBox()
        self.alignment_combo.addItems(["Left", "Center", "Right"])
        self.alignment_combo.currentTextChanged.connect(self.parent().setAlignment)
        self.addWidget(self.alignment_combo)

        self.addSeparator()

        # Text formatting actions
        actions = [
            ("B", "Bold", self.parent().setBold),
            ("I", "Italic", self.parent().setItalic),
            ("U", "Underline", self.parent().setUnderline),
            ("S", "Strikethrough", self.parent().setStrikethrough)
        ]

        for text, tooltip, slot in actions:
            action = QAction(text, self)
            action.setCheckable(True)
            action.setToolTip(tooltip)
            action.triggered.connect(slot)
            self.addAction(action)

        # Color actions
        color_action = QAction("Color", self)
        color_action.setToolTip("Text Color")
        color_action.triggered.connect(self.parent().setTextColor)
        self.addAction(color_action)

        bg_color_action = QAction("BG", self)
        bg_color_action.setToolTip("Background Color")
        bg_color_action.triggered.connect(self.parent().setBackgroundColor)
        self.addAction(bg_color_action)

    def handleFontSizeChange(self, text):
        try:
            size = int(text.replace('pt', ''))
            if 1 <= size <= 400:  # Reasonable size limits
                self.parent().setFontSize(size)
        except ValueError:
            # If conversion fails, ignore the change
            pass 