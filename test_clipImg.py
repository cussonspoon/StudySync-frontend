
import sys
from PySide6.QtCore import Qt
from PySide6.QtGui import QPixmap, QPainter, QPainterPath
from PySide6.QtWidgets import QApplication, QLabel, QWidget, QVBoxLayout


class CircularImageLabel(QLabel):
    def __init__(self, img_path, size=101, parent=None):
        super().__init__(parent)
        self.size = size  # Set the size of the circular image
        self.setFixedSize(self.size, self.size)  # Ensure QLabel is square
        self.setCircularImage(img_path)

    def setCircularImage(self, img_path):
        """Loads an image and applies a circular mask using QPainter."""
        pixmap = QPixmap(img_path).scaled(
            self.size, self.size, Qt.KeepAspectRatioByExpanding, Qt.SmoothTransformation
        )

        # Create a transparent pixmap to draw on
        circular_pixmap = QPixmap(self.size, self.size)
        circular_pixmap.fill(Qt.transparent)

        # Create a painter to apply the circular mask
        painter = QPainter(circular_pixmap)
        painter.setRenderHint(QPainter.Antialiasing)
        path = QPainterPath()
        path.addEllipse(0, 0, self.size, self.size)  # Circular path
        painter.setClipPath(path)  # Clip the image to the circular shape
        painter.drawPixmap(0, 0, pixmap)  # Draw the clipped image
        painter.end()

        self.setPixmap(circular_pixmap)  # Set the final circular image


class MainWindow(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("QPainter Circular Image Example")
        self.setGeometry(100, 100, 400, 300)

        # Create the circular image QLabel
        self.circular_label = CircularImageLabel("./static/images/profile.jpg")

        # Layout
        layout = QVBoxLayout(self)
        layout.addWidget(self.circular_label)

        self.setLayout(layout)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
