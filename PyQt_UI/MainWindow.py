# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'MainWindow.ui'
#
# Created by: PyQt5 UI code generator 5.15.2
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1029, 645)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.gridLayout = QtWidgets.QGridLayout(self.centralwidget)
        self.gridLayout.setObjectName("gridLayout")
        self.button_AmplifyBinaryImg = QtWidgets.QPushButton(self.centralwidget)
        self.button_AmplifyBinaryImg.setMinimumSize(QtCore.QSize(50, 15))
        self.button_AmplifyBinaryImg.setMaximumSize(QtCore.QSize(100, 30))
        self.button_AmplifyBinaryImg.setObjectName("button_AmplifyBinaryImg")
        self.gridLayout.addWidget(self.button_AmplifyBinaryImg, 6, 3, 1, 1)
        self.label_OrImg = QtWidgets.QLabel(self.centralwidget)
        self.label_OrImg.setMinimumSize(QtCore.QSize(381, 301))
        self.label_OrImg.setMaximumSize(QtCore.QSize(1000, 750))
        self.label_OrImg.setObjectName("label_OrImg")
        self.gridLayout.addWidget(self.label_OrImg, 5, 0, 1, 3)
        self.button_AmplifyOrImg = QtWidgets.QPushButton(self.centralwidget)
        self.button_AmplifyOrImg.setMinimumSize(QtCore.QSize(50, 15))
        self.button_AmplifyOrImg.setMaximumSize(QtCore.QSize(100, 50))
        self.button_AmplifyOrImg.setObjectName("button_AmplifyOrImg")
        self.gridLayout.addWidget(self.button_AmplifyOrImg, 6, 0, 1, 1)
        self.label_BinaryImg = QtWidgets.QLabel(self.centralwidget)
        self.label_BinaryImg.setMinimumSize(QtCore.QSize(381, 301))
        self.label_BinaryImg.setMaximumSize(QtCore.QSize(1000, 750))
        self.label_BinaryImg.setObjectName("label_BinaryImg")
        self.gridLayout.addWidget(self.label_BinaryImg, 5, 3, 1, 4)
        self.button_LessenOrImg = QtWidgets.QPushButton(self.centralwidget)
        self.button_LessenOrImg.setMinimumSize(QtCore.QSize(50, 15))
        self.button_LessenOrImg.setMaximumSize(QtCore.QSize(100, 50))
        self.button_LessenOrImg.setObjectName("button_LessenOrImg")
        self.gridLayout.addWidget(self.button_LessenOrImg, 6, 1, 1, 1)
        self.slider_BinaryThre = QtWidgets.QSlider(self.centralwidget)
        self.slider_BinaryThre.setMinimumSize(QtCore.QSize(250, 0))
        self.slider_BinaryThre.setMaximumSize(QtCore.QSize(300, 16777215))
        self.slider_BinaryThre.setOrientation(QtCore.Qt.Horizontal)
        self.slider_BinaryThre.setObjectName("slider_BinaryThre")
        self.gridLayout.addWidget(self.slider_BinaryThre, 0, 1, 1, 1)
        self.label_SingleThre = QtWidgets.QLabel(self.centralwidget)
        self.label_SingleThre.setMinimumSize(QtCore.QSize(50, 0))
        self.label_SingleThre.setMaximumSize(QtCore.QSize(100, 16777215))
        self.label_SingleThre.setObjectName("label_SingleThre")
        self.gridLayout.addWidget(self.label_SingleThre, 0, 0, 1, 1)
        self.label_ThresholdValue = QtWidgets.QLabel(self.centralwidget)
        self.label_ThresholdValue.setMaximumSize(QtCore.QSize(80, 16777215))
        self.label_ThresholdValue.setObjectName("label_ThresholdValue")
        self.gridLayout.addWidget(self.label_ThresholdValue, 0, 2, 1, 1)
        self.button_lessenBinaryImg = QtWidgets.QPushButton(self.centralwidget)
        self.button_lessenBinaryImg.setMinimumSize(QtCore.QSize(50, 15))
        self.button_lessenBinaryImg.setMaximumSize(QtCore.QSize(100, 30))
        self.button_lessenBinaryImg.setObjectName("button_lessenBinaryImg")
        self.gridLayout.addWidget(self.button_lessenBinaryImg, 6, 4, 1, 1)
        self.button_ThreCon = QtWidgets.QPushButton(self.centralwidget)
        self.button_ThreCon.setObjectName("button_ThreCon")
        self.gridLayout.addWidget(self.button_ThreCon, 0, 3, 1, 1)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1029, 23))
        self.menubar.setObjectName("menubar")
        self.start = QtWidgets.QMenu(self.menubar)
        self.start.setObjectName("start")
        self.layer_Selected = QtWidgets.QMenu(self.menubar)
        self.layer_Selected.setObjectName("layer_Selected")
        self.layer_M1 = QtWidgets.QMenu(self.layer_Selected)
        self.layer_M1.setObjectName("layer_M1")
        self.layer_M2 = QtWidgets.QMenu(self.layer_Selected)
        self.layer_M2.setObjectName("layer_M2")
        self.img_Processing = QtWidgets.QMenu(self.menubar)
        self.img_Processing.setObjectName("img_Processing")
        self.region_Selected = QtWidgets.QMenu(self.img_Processing)
        self.region_Selected.setObjectName("region_Selected")
        self.setting = QtWidgets.QMenu(self.menubar)
        self.setting.setObjectName("setting")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.openImg = QtWidgets.QAction(MainWindow)
        self.openImg.setObjectName("openImg")
        self.saveImg = QtWidgets.QAction(MainWindow)
        self.saveImg.setObjectName("saveImg")
        self.saveAsTXT = QtWidgets.QAction(MainWindow)
        self.saveAsTXT.setObjectName("saveAsTXT")
        self.layer_Poly = QtWidgets.QAction(MainWindow)
        self.layer_Poly.setObjectName("layer_Poly")
        self.layer_ST = QtWidgets.QAction(MainWindow)
        self.layer_ST.setObjectName("layer_ST")
        self.single_Threshold = QtWidgets.QAction(MainWindow)
        self.single_Threshold.setObjectName("single_Threshold")
        self.channelSplit = QtWidgets.QAction(MainWindow)
        self.channelSplit.setObjectName("channelSplit")
        self.single_Threshold_2 = QtWidgets.QAction(MainWindow)
        self.single_Threshold_2.setObjectName("single_Threshold_2")
        self.channel_Diff = QtWidgets.QAction(MainWindow)
        self.channel_Diff.setObjectName("channel_Diff")
        self.channel_Diff_2 = QtWidgets.QAction(MainWindow)
        self.channel_Diff_2.setObjectName("channel_Diff_2")
        self.img_Recover = QtWidgets.QAction(MainWindow)
        self.img_Recover.setObjectName("img_Recover")
        self.cor_Input = QtWidgets.QAction(MainWindow)
        self.cor_Input.setObjectName("cor_Input")
        self.local_Cover = QtWidgets.QAction(MainWindow)
        self.local_Cover.setObjectName("local_Cover")
        self.action_14 = QtWidgets.QAction(MainWindow)
        self.action_14.setObjectName("action_14")
        self.layer_Overlay = QtWidgets.QAction(MainWindow)
        self.layer_Overlay.setObjectName("layer_Overlay")
        self.start.addAction(self.openImg)
        self.start.addAction(self.saveImg)
        self.start.addAction(self.saveAsTXT)
        self.layer_M1.addAction(self.single_Threshold)
        self.layer_M1.addAction(self.channel_Diff)
        self.layer_M2.addAction(self.single_Threshold_2)
        self.layer_M2.addAction(self.channel_Diff_2)
        self.layer_Selected.addAction(self.layer_M1.menuAction())
        self.layer_Selected.addAction(self.layer_M2.menuAction())
        self.layer_Selected.addAction(self.layer_Poly)
        self.layer_Selected.addAction(self.layer_ST)
        self.region_Selected.addAction(self.cor_Input)
        self.region_Selected.addAction(self.local_Cover)
        self.img_Processing.addAction(self.channelSplit)
        self.img_Processing.addAction(self.region_Selected.menuAction())
        self.img_Processing.addAction(self.layer_Overlay)
        self.img_Processing.addAction(self.img_Recover)
        self.menubar.addAction(self.start.menuAction())
        self.menubar.addAction(self.img_Processing.menuAction())
        self.menubar.addAction(self.layer_Selected.menuAction())
        self.menubar.addAction(self.setting.menuAction())

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.button_AmplifyBinaryImg.setText(_translate("MainWindow", "放大"))
        self.label_OrImg.setText(_translate("MainWindow", "原图"))
        self.button_AmplifyOrImg.setText(_translate("MainWindow", "放大"))
        self.label_BinaryImg.setText(_translate("MainWindow", "二值化图"))
        self.button_LessenOrImg.setText(_translate("MainWindow", "缩小"))
        self.label_SingleThre.setText(_translate("MainWindow", "单一阈值调节"))
        self.label_ThresholdValue.setText(_translate("MainWindow", "127"))
        self.button_lessenBinaryImg.setText(_translate("MainWindow", "缩小"))
        self.button_ThreCon.setText(_translate("MainWindow", "确定"))
        self.start.setTitle(_translate("MainWindow", "开始"))
        self.layer_Selected.setTitle(_translate("MainWindow", "图层选择"))
        self.layer_M1.setTitle(_translate("MainWindow", "M1"))
        self.layer_M2.setTitle(_translate("MainWindow", "M2"))
        self.img_Processing.setTitle(_translate("MainWindow", "图片处理"))
        self.region_Selected.setTitle(_translate("MainWindow", "区域选择"))
        self.setting.setTitle(_translate("MainWindow", "设置"))
        self.openImg.setText(_translate("MainWindow", "打开图片"))
        self.saveImg.setText(_translate("MainWindow", "保存图片"))
        self.saveAsTXT.setText(_translate("MainWindow", "导出TXT"))
        self.layer_Poly.setText(_translate("MainWindow", "Poly"))
        self.layer_ST.setText(_translate("MainWindow", "ST"))
        self.single_Threshold.setText(_translate("MainWindow", "单一阈值"))
        self.channelSplit.setText(_translate("MainWindow", "通道分离"))
        self.single_Threshold_2.setText(_translate("MainWindow", "单一阈值"))
        self.channel_Diff.setText(_translate("MainWindow", "通道差值"))
        self.channel_Diff_2.setText(_translate("MainWindow", "通道差值"))
        self.img_Recover.setText(_translate("MainWindow", "恢复原图"))
        self.cor_Input.setText(_translate("MainWindow", "坐标输入"))
        self.local_Cover.setText(_translate("MainWindow", "局部覆盖"))
        self.action_14.setText(_translate("MainWindow", "自定义阈值"))
        self.layer_Overlay.setText(_translate("MainWindow", "图层叠加"))
