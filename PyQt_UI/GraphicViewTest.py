# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'GraphicViewTest.ui'
#
# Created by: PyQt5 UI code generator 5.9.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(941, 489)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.gridLayout = QtWidgets.QGridLayout(self.centralwidget)
        self.gridLayout.setObjectName("gridLayout")
        self.button_Amplify = QtWidgets.QPushButton(self.centralwidget)
        self.button_Amplify.setMinimumSize(QtCore.QSize(150, 25))
        self.button_Amplify.setMaximumSize(QtCore.QSize(250, 25))
        self.button_Amplify.setObjectName("button_Amplify")
        self.gridLayout.addWidget(self.button_Amplify, 0, 0, 1, 1)
        self.button_lessen = QtWidgets.QPushButton(self.centralwidget)
        self.button_lessen.setMinimumSize(QtCore.QSize(150, 25))
        self.button_lessen.setMaximumSize(QtCore.QSize(250, 25))
        self.button_lessen.setObjectName("button_lessen")
        self.gridLayout.addWidget(self.button_lessen, 0, 1, 1, 1)
        self.pushButton = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton.setMinimumSize(QtCore.QSize(150, 25))
        self.pushButton.setMaximumSize(QtCore.QSize(250, 25))
        self.pushButton.setObjectName("pushButton")
        self.gridLayout.addWidget(self.pushButton, 0, 2, 1, 1)
        self.pushButton_2 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_2.setMinimumSize(QtCore.QSize(150, 25))
        self.pushButton_2.setMaximumSize(QtCore.QSize(250, 25))
        self.pushButton_2.setObjectName("pushButton_2")
        self.gridLayout.addWidget(self.pushButton_2, 0, 3, 1, 1)
        self.ImgView = QtWidgets.QGraphicsView(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(1)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.ImgView.sizePolicy().hasHeightForWidth())
        self.ImgView.setSizePolicy(sizePolicy)
        self.ImgView.setObjectName("ImgView")
        self.gridLayout.addWidget(self.ImgView, 1, 0, 1, 2)
        self.BinaryImgView = QtWidgets.QGraphicsView(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(1)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.BinaryImgView.sizePolicy().hasHeightForWidth())
        self.BinaryImgView.setSizePolicy(sizePolicy)
        self.BinaryImgView.setObjectName("BinaryImgView")
        self.gridLayout.addWidget(self.BinaryImgView, 1, 2, 1, 2)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 941, 23))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.button_Amplify.setText(_translate("MainWindow", "放大"))
        self.button_lessen.setText(_translate("MainWindow", "缩小"))
        self.pushButton.setText(_translate("MainWindow", "PushButton"))
        self.pushButton_2.setText(_translate("MainWindow", "PushButton"))

