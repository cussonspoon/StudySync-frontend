from PySide6.QtWidgets import (
    QDialog,
    QVBoxLayout,
    QHBoxLayout,
    QPushButton,
    QTextEdit,
    QLabel,
    QWidget,
    QMenu,
    QFontComboBox,
    QSpinBox,
    QColorDialog,
    QToolBar,
    QComboBox,
    QCheckBox,
    QFrame,
    QScrollArea,
    QToolButton,
)
from PySide6.QtCore import Qt, QPoint, QSize
from PySide6.QtGui import (
    QFont,
    QTextCharFormat,
    QColor,
    QIcon,
    QAction,
    QTextListFormat,
    QTextBlockFormat,
    QTextFormat,
    QTextCursor,
)

from ui.views.components.note_components.toolbar import FloatingToolBar
from ui.views.components.note_components.collaborator import CollaboratorChip
from ui.views.components.note_components.menu import NotionStyleMenu
from ui.views.components.note_components.buttons import BackButton, ConversionButton


class BlockTypeButton(QToolButton):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setText("+")
        self.setStyleSheet(
            """
            QToolButton {
                background-color: transparent;
                border: none;
                padding: 4px 8px;
                font-size: 20px;
                color: #666;
            }
            QToolButton:hover {
                background-color: #F0F0F0;
                border-radius: 4px;
            }
        """
        )
        self.setCursor(Qt.PointingHandCursor)


class popup_notewindow(QDialog):
    def __init__(self, parent=None):
        super().__init__(
            parent,
            Qt.WindowSystemMenuHint | Qt.WindowTitleHint | Qt.WindowCloseButtonHint,
        )
        self.setModal(True)
        self.setWindowTitle("New Note")
        self.setFixedSize(1000, 800)
        self.setupUi()
        self.toolbar = None

    def setupUi(self):
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)

        # Top bar with back button and conversion options
        top_bar = QWidget()
        top_bar.setFixedHeight(50)
        top_bar.setStyleSheet("background-color: #FFFFFF;")
        top_layout = QHBoxLayout(top_bar)
        top_layout.setContentsMargins(10, 0, 10, 0)

        # Back button
        back_btn = BackButton()
        back_btn.clicked.connect(self.close)
        top_layout.addWidget(back_btn)

        # Conversion buttons on the right
        conversion_layout = QHBoxLayout()
        flashcard_btn = ConversionButton("Convert to Flashcard")
        quiz_btn = ConversionButton("Convert to Quiz")
        conversion_layout.addWidget(flashcard_btn)
        conversion_layout.addWidget(quiz_btn)

        top_layout.addStretch()
        top_layout.addLayout(conversion_layout)
        main_layout.addWidget(top_bar)

        # Content area
        content_widget = QWidget()
        content_widget.setStyleSheet("background-color: #F7F6F3;")
        content_layout = QVBoxLayout(content_widget)
        content_layout.setContentsMargins(100, 20, 100, 20)
        content_layout.setSpacing(20)

        # Title input
        self.title_input = QTextEdit()
        self.title_input.setPlaceholderText("New Note")
        self.title_input.setFixedHeight(50)
        self.title_input.setFont(QFont("Arial", 24))
        self.title_input.setStyleSheet(
            """
            QTextEdit {
                background-color: transparent;
                border: none;
                padding: 0px;
            }
        """
        )
        content_layout.addWidget(self.title_input)

        # Owner and collaborators section
        collab_widget = QWidget()
        collab_layout = QVBoxLayout(collab_widget)
        collab_layout.setContentsMargins(0, 0, 0, 0)
        collab_layout.setSpacing(8)

        # Owner section
        owner_section = QWidget()
        owner_layout = QVBoxLayout(owner_section)
        owner_layout.setContentsMargins(0, 0, 0, 0)
        owner_layout.setSpacing(8)
        owner_layout.setAlignment(Qt.AlignLeft)

        # Owner label
        owner_label = QLabel("Owner")
        owner_label.setStyleSheet("color: #666666; font-size: 13px;")
        owner_layout.addWidget(owner_label)

        # Owner chip container
        owner_chip_container = QWidget()
        owner_chip_layout = QHBoxLayout(owner_chip_container)
        owner_chip_layout.setContentsMargins(0, 0, 0, 0)
        owner_chip_layout.setSpacing(0)
        owner_chip_layout.setAlignment(Qt.AlignLeft)

        # Owner chip
        owner_chip = CollaboratorChip("Jane", "#FFD9B3")
        owner_chip_layout.addWidget(owner_chip)
        owner_chip_layout.addStretch()

        owner_layout.addWidget(owner_chip_container)
        collab_layout.addWidget(owner_section)

        # Collaborators section
        collab_section = QWidget()
        collab_section_layout = QVBoxLayout(collab_section)
        collab_section_layout.setContentsMargins(0, 0, 0, 0)
        collab_section_layout.setSpacing(8)

        # Collaborators label
        collab_label = QLabel("Collaborators")
        collab_label.setStyleSheet("color: #666666; font-size: 13px;")
        collab_section_layout.addWidget(collab_label)

        # Collaborator chips
        chips_widget = QWidget()
        chips_layout = QHBoxLayout(chips_widget)
        chips_layout.setContentsMargins(0, 0, 0, 0)
        chips_layout.setSpacing(8)
        chips_layout.setAlignment(Qt.AlignLeft)

        # Collaborator chips
        collab_chip1 = CollaboratorChip("John", "#C8E6C9")
        collab_chip2 = CollaboratorChip("Jake", "#BBDEFB")
        chips_layout.addWidget(collab_chip1)
        chips_layout.addWidget(collab_chip2)

        # Add collaborator button
        add_collab_btn = QPushButton("+")
        add_collab_btn.setFixedSize(28, 28)
        add_collab_btn.setStyleSheet(
            """
            QPushButton {
                background-color: transparent;
                border: 1px dashed #666666;
                border-radius: 14px;
                color: #666666;
                font-size: 16px;
            }
            QPushButton:hover {
                background-color: #F0F0F0;
            }
        """
        )
        chips_layout.addWidget(add_collab_btn)
        chips_layout.addStretch()

        collab_section_layout.addWidget(chips_widget)
        collab_layout.addWidget(collab_section)
        content_layout.addWidget(collab_widget)

        # Main content input
        self.content_input = QTextEdit()
        self.content_input.setPlaceholderText("Start typing...")
        self.content_input.setStyleSheet(
            """
            QTextEdit {
                background-color: transparent;
                border: none;
                font-size: 14px;
                line-height: 1.5;
            }
        """
        )
        self.content_input.setContextMenuPolicy(Qt.CustomContextMenu)
        self.content_input.customContextMenuRequested.connect(self.showContextMenu)
        content_layout.addWidget(self.content_input)

        main_layout.addWidget(content_widget)

    def showContextMenu(self, position):
        menu = NotionStyleMenu()

        # Turn into submenu
        turn_into = menu.addMenu("Turn into")
        for block_type in [
            "Text",
            "Heading 1",
            "Heading 2",
            "Heading 3",
            "To-do",
            "Callout",
            "Quote",
        ]:
            action = turn_into.addAction(block_type)
            action.triggered.connect(lambda checked, t=block_type: self.setBlockType(t))

        menu.addSeparator()

        # Font family submenu
        font_menu = menu.addMenu("Font")
        common_fonts = [
            ("Default", "Arial"),
            ("Serif", "Times New Roman"),
            ("Monospace", "Consolas"),
            ("Sans Serif", "Helvetica"),
            ("Casual", "Comic Sans MS"),
            ("Cursive", "Brush Script MT"),
            ("Code", "Courier New"),
        ]
        for display_name, font_name in common_fonts:
            action = font_menu.addAction(display_name)
            action.setFont(QFont(font_name))
            action.triggered.connect(
                lambda checked, f=font_name: self.setFontFamily(QFont(f))
            )

        # Font size submenu
        size_menu = menu.addMenu("Size")
        size_categories = [
            ("Small", [8, 9, 10, 11]),
            ("Medium", [12, 14, 16, 18]),
            ("Large", [20, 24, 28, 32]),
            ("Extra Large", [36, 48, 72]),
        ]
        for category, sizes in size_categories:
            category_menu = size_menu.addMenu(category)
            for size in sizes:
                action = category_menu.addAction(f"{size}pt")
                action.triggered.connect(lambda checked, s=size: self.setFontSize(s))

        # Color submenu
        color_menu = menu.addMenu("Color")
        text_color = color_menu.addAction("Text color")
        text_color.triggered.connect(self.setTextColor)
        highlight = color_menu.addAction("Highlight")
        highlight.triggered.connect(self.setBackgroundColor)

        # Style submenu
        style_menu = menu.addMenu("Style")
        bold = style_menu.addAction("Bold")
        bold.triggered.connect(self.setBold)
        italic = style_menu.addAction("Italic")
        italic.triggered.connect(self.setItalic)
        underline = style_menu.addAction("Underline")
        underline.triggered.connect(self.setUnderline)
        strikethrough = style_menu.addAction("Strikethrough")
        strikethrough.triggered.connect(self.setStrikethrough)

        menu.addSeparator()

        # Alignment submenu
        align_menu = menu.addMenu("Align")
        align_left = align_menu.addAction("Left")
        align_left.triggered.connect(lambda: self.setAlignment("Left"))
        align_center = align_menu.addAction("Center")
        align_center.triggered.connect(lambda: self.setAlignment("Center"))
        align_right = align_menu.addAction("Right")
        align_right.triggered.connect(lambda: self.setAlignment("Right"))

        menu.exec_(self.content_input.mapToGlobal(position))

    def showToolbar(self):
        if self.content_input.textCursor().hasSelection():
            if not self.toolbar:
                self.toolbar = FloatingToolBar(self)
                self.toolbar.hide()

            cursor = self.content_input.textCursor()
            rect = self.content_input.cursorRect(cursor)
            pos = self.content_input.mapToGlobal(rect.topLeft())
            self.toolbar.move(pos.x(), pos.y() - self.toolbar.height() - 5)
            self.toolbar.show()
        elif self.toolbar:
            self.toolbar.hide()

    def setBlockType(self, block_type):
        cursor = self.content_input.textCursor()
        block_format = QTextBlockFormat()
        char_format = QTextCharFormat()

        # Clear any existing formatting
        block_format.setAlignment(Qt.AlignLeft)
        char_format.setFontWeight(QFont.Normal)
        char_format.setFontPointSize(12)

        if block_type.startswith("Heading"):
            level = int(block_type[-1])
            font_size = {1: 24, 2: 20, 3: 16}[level]
            char_format.setFontPointSize(font_size)
            char_format.setFontWeight(QFont.Bold)

        elif block_type == "To-do":
            cursor.insertText("☐ ")

        elif block_type == "Callout":
            block_format.setBackground(QColor("#F5F5F5"))
            block_format.setLeftMargin(20)
            cursor.insertText("💡 ")

        elif block_type == "Quote":
            block_format.setLeftMargin(20)
            char_format.setFontItalic(True)
            cursor.insertText("> ")

        cursor.mergeBlockFormat(block_format)
        cursor.mergeCharFormat(char_format)

    def setFontFamily(self, font):
        self.content_input.setFontFamily(font.family())

    def setFontSize(self, size):
        self.content_input.setFontPointSize(size)

    def setBold(self):
        self.content_input.setFontWeight(
            QFont.Bold
            if self.content_input.fontWeight() == QFont.Normal
            else QFont.Normal
        )

    def setItalic(self):
        self.content_input.setFontItalic(not self.content_input.fontItalic())

    def setUnderline(self):
        self.content_input.setFontUnderline(not self.content_input.fontUnderline())

    def setStrikethrough(self):
        format = self.content_input.currentCharFormat()
        format.setFontStrikeOut(not format.fontStrikeOut())
        self.content_input.setCurrentCharFormat(format)

    def setAlignment(self, alignment):
        if alignment == "Left":
            self.content_input.setAlignment(Qt.AlignLeft)
        elif alignment == "Center":
            self.content_input.setAlignment(Qt.AlignCenter)
        elif alignment == "Right":
            self.content_input.setAlignment(Qt.AlignRight)

    def setTextColor(self):
        color = QColorDialog.getColor()
        if color.isValid():
            self.content_input.setTextColor(color)

    def setBackgroundColor(self):
        color = QColorDialog.getColor()
        if color.isValid():
            self.content_input.setTextBackgroundColor(color)

    def getNoteData(self):
        return {
            "title": self.title_input.toPlainText(),
            "content": self.content_input.toHtml(),  # Using HTML to preserve formatting
        }

    def closeEvent(self, event):
        """Handle window closing (X button or back arrow)"""
        if hasattr(self, "note_id") and hasattr(self, "folder_id"):
            # Get parent widget (FolderDetailPage)
            parent = self.parent()
            if parent:
                # Save changes
                parent.save_note_changes(self)
                # Refresh folder contents
                parent.load_items()
        super().closeEvent(event)
