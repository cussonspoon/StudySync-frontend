import sys
from PySide6.QtGui import QPixmap
from PySide6.QtWidgets import QMainWindow, QApplication, QLabel
from PySide6.QtCore import (QDir)

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.title = "Image Viewer"
        self.setWindowTitle(self.title)

        label = QLabel(self)
        img_path = QDir.currentPath() + "/static/images/banner.jpg"

        pixmap = QPixmap(img_path)
        label.setPixmap(pixmap)
        label.setScaledContents(True)
        self.setCentralWidget(label)
        # self.resize(pixmap.width(), pixmap.height())

        self.setStyleSheet(
            """
            QLabel {
                border-top-left-radius: 20px;
                border-top-right-radius: 20px;
                border-bottom-left-radius: 0px;
                border-bottom-right-radius: 0px;
                border: 0px solid #ccc;
            }
            """
        )


app = QApplication(sys.argv)
w = MainWindow()
w.show()
sys.exit(app.exec())