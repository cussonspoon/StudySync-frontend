from PySide6.QtCore import Qt, QSize
from PySide6.QtGui import QPixmap, QPainter, QPainterPath, QColor
from PySide6.QtWidgets import QLabel


class ShapedImageLabel(QLabel):
    CIRCLE = "circle"
    ROUNDED_RECT_TOP = "rounded_rect_top"
    ROUNDED_RECT = "rounded_rect"

    def __init__(
        self,
        pos_x=0,
        pos_y=0,
        width=101,
        height=101,
        img_path="",
        shape="circle",
        corner_radius=50,
        parent=None,
    ):
        super().__init__(parent)
        self.width = width
        self.height = height
        self.shape = shape
        self.corner_radius = corner_radius
        # add function here
        self.setFixedSize(self.width, self.height)
        self.setShapedImage(img_path)

    def setShapedImage(self, img_path):
        pixmap = QPixmap(img_path)

        high_rez = QSize(self.width, self.height)
        scaled_pixmap = pixmap.scaled(
            high_rez, Qt.KeepAspectRatioByExpanding, Qt.SmoothTransformation
        )

        shaped_pixmap = QPixmap(self.width, self.height)
        # shaped_pixmap.fill(QColor(255, 255, 255))
        shaped_pixmap.fill(Qt.transparent)


        painter = QPainter(shaped_pixmap)
        painter.setRenderHint(QPainter.Antialiasing)
        path = QPainterPath()

        pixmap = pixmap.scaled(high_rez)

        if self.shape == self.CIRCLE:
            path.addEllipse(0, 0, self.width, self.height)
        elif self.shape == self.ROUNDED_RECT_TOP:
            path.moveTo(0, self.height)
            path.lineTo(0, self.corner_radius) 
            path.quadTo(0, 0, self.corner_radius, 0) 
            path.lineTo(self.width - self.corner_radius, 0) 
            path.quadTo(
                self.width, 0, self.width, self.corner_radius
            )  
            path.lineTo(self.width, self.height)  
            path.lineTo(0, self.height) 
        elif self.shape == self.ROUNDED_RECT:
            path.addRoundedRect(
                0, 0, self.width, self.height, self.corner_radius, self.corner_radius
            )

        painter.setClipPath(path)
        painter.setOpacity(1)
        painter.drawPixmap(0, 0, scaled_pixmap)
        painter.end()

        self.setPixmap(shaped_pixmap)


