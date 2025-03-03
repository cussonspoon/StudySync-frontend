from PySide import QtGui, QtCore


class UberLabel(QtGui.QLabel):
    def __init__(self, img):
        super(UberLabel, self).__init__()
        self.setFrameStyle(QtGui.QFrame.StyledPanel)
        self.pixmap = QtGui.QPixmap(img)
        self.setSizePolicy(QtGui.QSizePolicy.MinimumExpanding, QtGui.QSizePolicy.MinimumExpanding)

    def paintEvent(self, event):
        size = self.size()
        painter = QtGui.QPainter(self)
        point = QtCore.QPoint(0,0)
        scaledPix = self.pixmap.scaled(size, QtCore.Qt.KeepAspectRatio, transformMode = QtCore.Qt.SmoothTransformation)
        point.setX((size.width() - scaledPix.width())/2)
        point.setY((size.height() - scaledPix.height())/2)
        # print point.x(), ' ', point.y()
        painter.drawPixmap(point, scaledPix)

class UberLabelWidget(QtGui.QWidget):
    def __init__(self):
        QtGui.QWidget.__init__(self)
        self.label = UberLabel("/Users/ubertron/Pictures/my_image.jpg")

        vb_layout = QtGui.QVBoxLayout()
        vb_layout.addWidget(self.label)
        self.setStyleSheet("background-color:rgb(253, 105, 102);")
        self.setLayout(vb_layout)

class MyWindow(QtGui.QMainWindow):
    def __init__(self):
        QtGui.QMainWindow.__init__(self)
        self.setGeometry(300, 100, 270, 100)
        self.setWindowTitle('Uber Label Window')
        self.exit = QtGui.QAction('Exit', self)
        self.exit.setStatusTip('Exitgram')
        self.exit.triggered.connect(app.quit)
        menu_bar = self.menuBar()
        file_object = menu_bar.addMenu('&File')
        file_object.addAction(self.exit)
        self.statusBar()
        widget = UberLabelWidget()
        self.setCentralWidget(widget)
        self.label = widget.label


app = QtGui.QApplication([])
win = MyWindow()
win.show()
app.exec_()