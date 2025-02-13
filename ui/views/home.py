# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'home-test.ui'
##
## Created by: Qt User Interface Compiler version 6.8.0
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################


#just for testing 
from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
    QFont, QFontDatabase, QGradient, QIcon,
    QImage, QKeySequence, QLinearGradient, QPainter,
    QPalette, QPixmap, QRadialGradient, QTransform)
from PySide6.QtWidgets import (QApplication, QPushButton, QSizePolicy, QWidget, QVBoxLayout)

class HomePage(QWidget):
    def __init__(self):
        super().__init__()
        self.setupUi() 

    def setupUi(self):
        if not self.objectName():
            self.setObjectName(u"Form")
        self.resize(1138, 831)
        self.setStyleSheet(u"QWidget {\n"
"	background-color: #F8F6F1; \n"
"}\n"
"\n"
"QPushButton {\n"
"    background-color: #2596be;\n"
"    color: white;\n"
"    border: 2px solid #1f7a8c;\n"
"    border-radius: 10px;\n"
"    padding: 10px 20px;\n"
"    font-size: 16px;\n"
"    font-weight: bold;\n"
"    qproperty-iconSize: 24px 24px;\n"
"}\n"
"")
        layout = QVBoxLayout()
        self.pushButton = QPushButton("Go to Dashboard")
        self.pushButton.setObjectName(u"pushButton")
        self.pushButton.setGeometry(QRect(420, 360, 291, 61))

        # self.retranslateUi(Form)
        layout.addWidget(self.pushButton)
        self.setLayout(layout)

        # QMetaObject.connectSlotsByName(Form)
    # setupUi

    def retranslateUi(self, Form):
        Form.setWindowTitle(QCoreApplication.translate("Form", u"Form", None))
        self.pushButton.setText(QCoreApplication.translate("Form", u"PushButton", None))
    # retranslateUi

