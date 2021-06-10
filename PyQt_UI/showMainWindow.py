from PyQt5.QtWidgets import *
from PyQt5.QtGui import QIcon,QImage, QPixmap
from PyQt5.QtCore import QObject , pyqtSignal
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt_UI.MainWindow  import Ui_MainWindow
from PyQt_UI.regionSplit import Ui_Dialog
from PyQt_UI.CoordinateSelectUI import CoordinateSelect_Ui_dialog
from PyQt_UI.HSV_Channel_Select import HSV_Ui_Dialog
import scipy.io as io
import PyQt_UI.utils as utils
import PyQt_UI.algorithms as algorithms
import cv2
import sys
import os
import copy
import numpy as np
import NewLine as nl

class showMainWindow(QMainWindow,Ui_MainWindow):
    # 多继承方式，继承界面父类,分离逻辑代码和界面代码
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUi(self)
        #加载应用程序图标
        icon = QIcon()
        icon.addPixmap(QtGui.QPixmap('../icon/mainWindow.ico'))
        self.setWindowIcon(icon)

        # 成员变量
        self.OrImgitem = QGraphicsPixmapItem()  # 创建像素图元
        self.OrImgscene = QGraphicsScene()  # 创建场景
        self.OrImgzoomscale = 1  # 图片放缩尺度

        # 创建右侧二值化图的像素图元和场景
        self.BinaryImgitem = QGraphicsPixmapItem()  # 创建像素图元
        self.BinaryImgscene = QGraphicsScene()  # 创建场景
        self.BinaryImgzoomscale = 1  # 图片放缩尺度

        self.OrImgitem.mousePressEvent = self.getOrImgPos
        self.BinaryImgitem.mousePressEvent = self.getBinaryImgPos
        self.Threshold = 127
        self.OrImgPath = ''
        self.BinaryImgPath = ''
        self.MergeImgPath=''
        self.localImgPath=''   #局部区域的小图的路径
        self.diffCh=30
        self.bigCh=0     #R通道
        self.smallCh=1   #G通道
        self.curHandleLocalRectangle=np.zeros((1,1,1)) #当前正处理的局部矩阵
        self.globalRectangle=np.zeros((1,1,1))         #读取全局矩阵
        self.golobalBinary=False  #用于判断当前是否已经全局二值化
        self.localBinary=False    #用于判断当前是否已经局部二值化

        #初始化部分界面（单阈值图标）
        # self.slider_BinaryThre.setMinimum(0)
        # self.slider_BinaryThre.setMaximum(255)
        # self.slider_BinaryThre.setValue(127)
        # self.slider_BinaryThre.setSingleStep(1)

        # 实例化子界面,用于显示子界面
        self.regionSplitWindow = regionSplitWindow()

        # 绑定槽函数
        self.openImg.triggered.connect(self.readImg)
        #self.slider_BinaryThre.valueChanged.connect(self.threshold_change)
        #self.button_ThreCon.clicked.connect(self.binaryImg)  #确定二值化按钮
        self.saveImg.triggered.connect(self.saveBinaryImg)
        self.channel_Diff.triggered.connect(self.channel_Difference)
        self.channel_Diff_2.triggered.connect(self.channel_Difference)
        self.regionSplitWindow.button_cancel.clicked.connect(self.closeWindow)
        self.layer_Overlay.triggered.connect(self.layerOverlay)
        self.saveAsTXT.triggered.connect(self.BinaryImgToTxt)
        self.cor_Input.triggered.connect(self.showCoordianteInputDialog)
        self.img_Recover.triggered.connect(self.showRecoverImage)
        self.local_Cover.triggered.connect(self.localCover)
        self.single_Threshold.triggered.connect(self.setSingleThreshold)
        self.single_Threshold_2.triggered.connect(self.setSingleThreshold)

        # SeclectCoordinator
        self.CoordinateSelectDialog = showCorrdinateDialog()
        self.IsShrankFlag = False  # 判断当前界面左侧，显示的图是否为局部的小图

        #self.curHandleImagepath = ''  # 使用全局变量保存当前正在处理的整个大图，与OrImgPath参数功能重叠，注释掉
        #self.label_OrImg.mousePressEvent = self.getPos
        # HSV_Channel_SelectUI
        self.Handle_HSV_M1.triggered.connect(self.showHSVChannelInputDialog)
        self.Handle_HSV_M2.triggered.connect(self.showHSVChannelInputDialog)
        self.HSVChannelUI = showHSV_Channel_SelectUI()


    def readImg(self):
        # 从指定目录打开图片（*.jpg *.gif *.png *.jpeg），返回路径
        image_file, _ = QFileDialog.getOpenFileName(self, '打开图片', '../', 'Image files (*.jpg *.gif *.png *.jpeg)')
        if(image_file==''):
            return 0
        print(image_file)
        img = cv2.imread(image_file)  # 读取图像
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)  # 转换图像  通道

        y = img.shape[0]  # 图像宽
        x = img.shape[1]  # 获取图像大小
        #将OpenCV图片转为Qimage图片
        frame = QImage(img, x, y, x *3, QImage.Format_RGB888)
        pix = QPixmap.fromImage(frame)
        self.OrImgitem.setPixmap(pix)
        self.OrImgscene.addItem(self.OrImgitem)
        self.OrImgView.setScene(self.OrImgscene)  # 将场景添加至视图

        #注意此处的路径关系，将路径和图片保存为全局变量
        self.OrImgPath = image_file
        self.CurHandleImage = cv2.imread(image_file)
        self.IsShrankFlag = False
        self.golobalBinary=True
        self.localBinary=False
        self.curHandleLocalRectangle = cv2.imread(image_file) # 当前正处理的局部矩阵
        self.globalRectangle = cv2.imread(image_file)  # 全局矩阵

        self.OrImgzoomscale=np.minimum(float(self.OrImgView.height()/img.shape[1]),float(self.OrImgView.width()/img.shape[0]))
        self.OrImgitem.setScale(self.OrImgzoomscale)  # 缩小图像
        print(self.OrImgzoomscale)

        # print('globalRectangle.shape:%s',self.globalRectangle.shape)
        # print('curHandleLocalRectangle.shape:%s', self.curHandleLocalRectangle.shape)

    def saveBinaryImg(self):
        #保存（*.jpg *.gif *.png *.jpeg）图片，返回路径
        image_file,_=QFileDialog.getSaveFileName(self,'保存二值化图片','../','Image files (*.jpg *.gif *.png *.jpeg)')
        #设置标签的图片
        #print(image_file)
        if(image_file==''):
            return 0
        img=cv2.imread(self.BinaryImgPath)
        cv2.imwrite(image_file,img)

    def binaryImg(self):
        if not self.IsShrankFlag:
            if(self.OrImgPath==''):
                return 0
            # img,binaryImgPath = nl.image_binarization(self.OrImgPath, self.Threshold)
            img=cv2.imread(self.OrImgPath)
            save_gray=algorithms.image_binarization(img,self.Threshold)
            binaryImgPath =utils.SaveBinaryImage(save_gray,self.OrImgPath)
            binaryImg=cv2.imread(binaryImgPath)  #读取二值化图的路径，为3通道的图
            self.globalRectangle=binaryImg
            binaryImg = cv2.cvtColor(binaryImg, cv2.COLOR_BGR2RGB)
            frame = QImage(binaryImg, binaryImg.shape[1], binaryImg.shape[0], binaryImg.shape[1] * 3, QImage.Format_RGB888)
            pix = QPixmap.fromImage(frame)
            self.BinaryImgitem.setPixmap(pix)
            self.BinaryImgscene.addItem(self.BinaryImgitem)
            self.BinaryImgView.setScene(self.BinaryImgscene)  # 将二值化图片的场景添加至视图
            self.BinaryImgPath = binaryImgPath  #更新单一阈值二值化图片保存的路径
            self.BinaryImgzoomscale = np.minimum(float(self.BinaryImgView.height() / binaryImg.shape[1]),
                                    float(self.BinaryImgView.width() / binaryImg.shape[0]))
            self.BinaryImgitem.setScale(self.BinaryImgzoomscale)  # 缩小图像
            self.localBinary=False
            self.golobalBinary=True
        else:
            img = cv2.imread(self.OrImgPath)
            # 指定阈值 灰度二值化
            n_start_x, n_start_y, n_end_x, n_end_y = self.CoordinateSelectDialog.getCorrdiante()
            rec_img = img[n_start_y:n_end_y, n_start_x:n_end_x, :]
            save_gray = algorithms.image_binarization(rec_img, self.Threshold)
            binaryImgLocalityPath=utils.SaveBinaryLocalityImage(save_gray, self.OrImgPath)
            recimg_binary=cv2.imread(binaryImgLocalityPath)
            self.curHandleLocalRectangle=recimg_binary
            # 将图像转换成QT能够识别的格式
            recimg_binary = cv2.cvtColor(recimg_binary, cv2.COLOR_BGR2RGB)
            frame = QImage(recimg_binary , recimg_binary.shape[1], recimg_binary.shape[0],
                                 recimg_binary.shape[1]*3, QImage.Format_RGB888)
            pix = QPixmap.fromImage(frame)
            self.BinaryImgitem.setPixmap(pix)
            self.BinaryImgscene.addItem(self.BinaryImgitem)
            self.BinaryImgView.setScene(self.BinaryImgscene)
            self.BinaryImgzoomscale = np.minimum(float(self.BinaryImgView.height() / recimg_binary.shape[1]),
                                    float(self.BinaryImgView.width() / recimg_binary.shape[0]))
            self.BinaryImgitem.setScale(self.BinaryImgzoomscale)  # 缩小图像
            self.golobalBinary=False
            self.localBinary=True

    def setSingleThreshold(self):
        num, ok = QInputDialog.getInt(self, '输入阈值范围', '阈值范围0-255',value=self.Threshold,min=0,max=250)
        if ok and num:
            self.Threshold=num
            self.binaryImg()

    def getThreshold(self):
        return self.Threshold

    def threshold_change(self):
        self.Threshold=self.slider_BinaryThre.value()
        self.label_ThresholdValue.setText(str(self.Threshold))
        # print(self.Threshold)

    #子菜单点击槽函数
    def channel_Difference(self):
        # 将子界面的信号与接受数据的函数连接
        self.regionSplitWindow.signal_diffCh.connect(self.getChDiffData)
        self.regionSplitWindow.exec()
        #单个对话框可使用以下代码，无需通过复杂的信号槽传递参数，使用更为简洁方便
        # num, ok = QInputDialog.getInt(self, 'Integer input dialog', '输入数字')
        # num1, ok1 = QInputDialog.getInt(self, 'Integer input dialog', '输入')
        # if ok and num:
        #     self.GetIntlineEdit.setText(str(num))

    # 子界面信号对应的槽函数
    def getChDiffData(self, diffCh):
        #print('diffch的值为：', diffCh)
        d = int(diffCh)
        if (self.OrImgPath == ''):
            QMessageBox.warning(self, "提示", "未读取图层照片,请读取图片后再处理", QMessageBox.Yes | QMessageBox.No, QMessageBox.Yes)
            return 0
        if (not self.IsShrankFlag):
            print('进入全局处理函数')
            # 读取原图的全局变量矩阵，或直接读取路径,
            # 需要注意：如果使用全局变量CurHandleImage,则必须使用copy中的深层拷贝函数，不然在函数传递或处理中，导致原图的数组被修改
            # 直接赋值或者copy.copy函数都是浅拷贝，实则还是指向同一内存地址，1个变量改变则所有变量全部改变。因此，推荐使用读取路径的方式
            # img = cv2.imread(self.OrImgPath)
            img = copy.deepcopy(self.CurHandleImage)
            img = algorithms.ChDiffExtract(img, d)  # 无需返回参数，已经在内存中发生修改
            self.globalRectangle = img
            img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
            frame = QImage(img.data, img.shape[1], img.shape[0], img.shape[1] * 3,
                           QtGui.QImage.Format_RGB888)
            # 默认将处理后的的img图片写入ImgSave对应的目录下
            utils.SaveRGBDiffImage(img,self.OrImgPath)
            # 将图片转成BGR模式; img_rgb.shape[1] * img_rgb.shape[2]必须添加  不然照片是斜着的
            pix = QPixmap.fromImage(frame)
            self.BinaryImgitem.setPixmap(pix)
            self.BinaryImgscene.addItem(self.BinaryImgitem)
            self.BinaryImgView.setScene(self.BinaryImgscene)
        else:
            # 读取局部区域的子图，进行通道差值处理
            image = cv2.imread(self.OrImgPath)
            n_start_x, n_start_y, n_end_x, n_end_y = self.CoordinateSelectDialog.getCorrdiante()
            rec_img = image[n_start_y:n_end_y, n_start_x:n_end_x, :]
            print('已经进入局部处理函数', d)
            # 需要深度copy
            img = copy.deepcopy(rec_img)
            img=algorithms.ChDiffExtract(img, d)
            self.curHandleLocalRectangle=rec_img
            utils.SaveRGBDiffLocalityImage(img,self.OrImgPath)
            # 将图片转成BGR模式
            # 将图片转成BGR模式
            img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
            frame = QImage(img.data, img.shape[1], img.shape[0], img.shape[1] * 3,
                           QtGui.QImage.Format_RGB888)
            pix = QPixmap.fromImage(frame)
            self.BinaryImgitem.setPixmap(pix)
            self.BinaryImgscene.addItem(self.BinaryImgitem)
            self.BinaryImgView.setScene(self.BinaryImgscene)


    def closeWindow(self):
        self.regionSplitWindow.close()

    #OpenCV图片数据格式转为QImage数据格式的函数，同理，数组传递的时候，需要深层拷贝，无需返回值
    def cvimg_to_qtimg(self,cvimg):
        height, width, depth = cvimg.shape
        cvimg = cv2.cvtColor(cvimg, cv2.COLOR_BGR2RGB)
        cvimg = QtGui.QImage(cvimg.data, width, height,width*depth, QtGui.QImage.Format_RGB888)
        return cvimg

    def layerOverlay(self):  #目前，只能单一阈值后，才能进行图层覆盖操作
        #第一种将pyqt的按钮改成中文，比较美观，我使用的是第二种
        # self.messageBox = QMessageBox()
        # self.messageBox.setWindowTitle('图层叠加')
        # icon = QIcon()
        # icon.addPixmap(QtGui.QPixmap('../icon/mainWindow.ico'))
        # self.messageBox.setWindowIcon(icon)
        # self.messageBox.setText('是否将处理后的图层叠加到原图层上？')
        # self.messageBox.addButton(QPushButton('确定'), QMessageBox.YesRole)
        # self.messageBox.addButton(QPushButton('取消'), QMessageBox.NoRole)
        # self.messageBox.exec_()
        # print(self.messageBox.result())
        self.box=QMessageBox(QMessageBox.Question,"图层叠加", "是否将处理后的图层叠加到原图层上？")
        icon = QIcon()
        icon.addPixmap(QtGui.QPixmap('../icon/mainWindow.ico'))
        self.box.setWindowIcon(icon)
        qyes = self.box.addButton(self.tr("确定"), QMessageBox.YesRole)
        qno = self.box.addButton(self.tr("取消"), QMessageBox.NoRole)
        self.box.exec_()
        if self.box.clickedButton() == qyes:
            if(self.OrImgPath==''):
                QMessageBox.warning(self, "提示", "未读取图层照片", QMessageBox.Yes | QMessageBox.No, QMessageBox.Yes)
                return 0
            if(self.golobalBinary):
                orImg = cv2.imread(self.OrImgPath)
                binbaryImg = cv2.imread(self.BinaryImgPath)
                #将二值化图片改成黄色
                np.where(binbaryImg[:, :, 1] > 0, binbaryImg[:, :, 1], 255)
                #np.where(binbaryImg[:, :, 2] > 0, binbaryImg[:, :, 2], 255)
                binbaryImg[:, :, 2] = 0
                binbaryImg[:, :, 0]=0
                #保存图像半透明式覆盖原图层照片及其路径
                img = cv2.addWeighted(orImg, 0.8, binbaryImg, 0.2, 1)
                content, tempfilename = os.path.split(self.OrImgPath)
                filename, extension = os.path.splitext(tempfilename)
                filename = filename + str('_MergeImg') + extension
                filepath = os.path.join(content, filename)
                filepath = filepath.replace('\\', '/')
                self.MergeImgPath=filepath
                cv2.imwrite(filepath,img)
                #显示图片
                MergeImg= cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
                frame = QImage(MergeImg, MergeImg.shape[1], MergeImg.shape[0], MergeImg.shape[1] * 3, QImage.Format_RGB888)
                pix = QPixmap.fromImage(frame)
                self.BinaryImgitem.setPixmap(pix)
                self.BinaryImgscene.addItem(self.BinaryImgitem)
                self.BinaryImgView.setScene(self.BinaryImgscene)  # 将场景添加至视图
            elif(self.localBinary):
                QMessageBox.warning(self, "提示", "请在局部处理结束后再进行图层覆盖", QMessageBox.Yes | QMessageBox.No, QMessageBox.Yes)
                return 0
        else:
            return 0

    def BinaryImgToTxt(self):
        if(self.BinaryImgPath==''):
            return 0
        imgPath, _ = QFileDialog.getSaveFileName(self, '将二值化图片另存为TXT', 'C:\\', 'TXT File (*.txt )')
        if(imgPath==''):
            return 0
        print('开始转化为TXT：')
        img=cv2.imread(self.BinaryImgPath)
        # 彩色通道使用#,这里可以适当修改
        img_b = img[:, :, 0]
        # 单通道使用#
        # img_b = img
        size_x = img_b.shape[1]  # 像数列数
        size_y = img_b.shape[0]  # 像数行数
        boundary = 10
        count = 0
        utils.CreateTxtFileHead(imgPath)
        rec_flag = np.zeros([size_y, size_x])  # 矩阵标志位，标志当前像素点是否被之前的矩阵圈住
        for row_index in range(boundary, size_y - boundary, 1):
            for col_index in range(boundary, size_x - boundary, 1):
                if (rec_flag[row_index, col_index]):
                    continue
                else:
                    col_end = col_index
                    for index in range(col_index, size_x - boundary, 1):
                        if (img_b[row_index, index] < 127):
                            col_end = index
                            break
                    rec_flag[row_index, col_index:col_end] = 1
                    if (col_index == col_end):
                        continue
                    else:
                        utils.CreateTxtFile(imgPath,(-1 * row_index), col_index, col_end)
                        count = count + 1
        utils.CreateTxtFileTail(imgPath)
        QMessageBox.information(self, "提示", "已成功导出TXT版图数据",
                                QMessageBox.Yes | QMessageBox.No, QMessageBox.Yes)
        return 0

    def getPos(self, event):
        x = event.pos().x()
        y = event.pos().y()
        if self.OrImgPath == '':
            return
        label_width = self.label_OrImg.width()
        label_hight = self.label_OrImg.height()
        image_width = self.CurHandleImage.shape[0]
        image_hight = self.CurHandleImage.shape[1]
        real_x = float(x) / float(label_width) * image_width
        real_y = float(y) / float(label_hight) * image_hight
        # print("xxxxx%s" % x)
        # print("yyyyy%s" % y)
        NowCorrdinate = '横坐标：' + str(int(real_x)) + ' 纵坐标: ' + str(int(real_y))
        QMessageBox.about(self, '当前坐标', NowCorrdinate)


    def getOrImgPos(self,event):
        x = event.pos().x()
        y = event.pos().y()
        print(self.OrImgView.width(), self.OrImgView.height(),
              self.BinaryImgView.width(), self.BinaryImgView.height())
        NowCorrdinate = '横坐标：' + str(int(x)) + ' 纵坐标: ' + str(int(y))
        QMessageBox.about(self, '当前坐标', NowCorrdinate)


    def getBinaryImgPos(self,event):
        x = event.pos().x()
        y = event.pos().y()
        print(self.OrImgView.width(), self.OrImgView.height(),
              self.BinaryImgView.width(), self.BinaryImgView.height())
        NowCorrdinate = '横坐标：' + str(int(x)) + ' 纵坐标: ' + str(int(y))
        QMessageBox.about(self, '当前坐标', NowCorrdinate)

    def on_button_AmplifyOrImg_clicked(self):
        """
                    点击方大图像
        """
        self.OrImgzoomscale = self.OrImgzoomscale + 0.025
        if self.OrImgzoomscale >= 3:
            self.OrImgzoomscale = 3
        self.OrImgitem.setScale(self.OrImgzoomscale)  # 放大图像

    def on_button_LessenOrImg_clicked(self):
        """
                  点击缩小图像
        """
        if self.OrImgzoomscale  <= 0.1:
            self.OrImgzoomscale  = 0.02 if(0.02>(self.OrImgzoomscale-0.01)) else (self.OrImgzoomscale-0.01)
        else:
            self.OrImgzoomscale = self.OrImgzoomscale - 0.025
        self.OrImgitem.setScale(self.OrImgzoomscale)  # 缩小图像


    def on_button_AmplifyBinaryImg_clicked(self):
        self.BinaryImgzoomscale = self.BinaryImgzoomscale + 0.025
        if self.BinaryImgzoomscale >= 3:
            self.BinaryImgzoomscale = 3
        self.BinaryImgitem.setScale(self.BinaryImgzoomscale)  # 放大图像

    def on_button_lessenBinaryImg_clicked(self):
        if self.BinaryImgzoomscale <= 0.1:
            self.BinaryImgzoomscale = 0.02 if (0.02 > (self.BinaryImgzoomscale - 0.01)) else (self.BinaryImgzoomscale - 0.01)
        else:
            self.BinaryImgzoomscale = self.BinaryImgzoomscale - 0.025

        self.BinaryImgitem.setScale(self.BinaryImgzoomscale)  # 缩小图像

    def mouseMoveEvent(self, event):
        s = event.windowPos()
        self.setMouseTracking(True)
        print('X:' + str(s.x()))
        print('Y:' + str(s.y()))

    def shrinkImage(self):
        self.IsShrankFlag = True  # 是否当前显示的图是小图
        img = cv2.imread(self.OrImgPath)
        n_start_x, n_start_y, n_end_x, n_end_y = self.CoordinateSelectDialog.getCorrdiante()
        #将局部区域小图的数组定义为私有变量，方便存储
        # self.curHandleLocalRectangle = img[n_start_y:n_end_y, n_start_x:n_end_x, :]
        orgRecImage = img[n_start_y:n_end_y, n_start_x:n_end_x, :]
        #在转换图片格式的时候，必须要将BGR通道，转为RGB通道
        orgRecImage = cv2.cvtColor(orgRecImage, cv2.COLOR_BGR2RGB)
        frame = QImage(orgRecImage, orgRecImage.shape[1], orgRecImage.shape[0],
                       orgRecImage.shape[1] * 3, QImage.Format_RGB888)
        pix = QPixmap.fromImage(frame)
        self.OrImgitem.setPixmap(pix)
        self.OrImgscene.addItem(self.OrImgitem)
        self.OrImgView.setScene(self.OrImgscene)

    def showCoordianteInputDialog(self):
        if self.OrImgPath == '':
            reply = QMessageBox.information(self, '未读取图像', '请先读取图像', QMessageBox.Yes | QMessageBox.No, QMessageBox.Yes)
            if (reply == QMessageBox.Yes):
                self.readImg()
            return 0

        retValue = self.CoordinateSelectDialog.exec_()
        if retValue == QtWidgets.QDialog.Accepted:
            n_start_x, n_start_y, n_end_x, n_end_y = self.CoordinateSelectDialog.getCorrdiante()
            if ((n_end_x < n_start_x) | (n_end_y < n_start_y)):
                reply = QMessageBox.information(self, '错误', '输入的起点坐标必须小于终点坐标', QMessageBox.Yes | QMessageBox.No,
                                             QMessageBox.Yes)
                if (reply == QMessageBox.Yes):
                    self.showCoordianteInputDialog()
                return
            elif ((n_end_x > self.CurHandleImage.shape[0]) | (n_end_y > self.CurHandleImage.shape[1])):
                reply = QMessageBox.information(self, '错误', '输入的坐标超过图片坐标', QMessageBox.Yes | QMessageBox.No,
                                             QMessageBox.Yes)
                if (reply == QMessageBox.Yes):
                    self.showCoordianteInputDialog()
                return
            elif ((n_end_x > n_start_x) & (n_end_y > n_start_y) & (n_end_x < self.CurHandleImage.shape[0]) & (
                    n_end_y < self.CurHandleImage.shape[1])):
                self.shrinkImage()
            else:
                reply = QMessageBox.information(self, '未知错误', '未知错误', QMessageBox.Yes | QMessageBox.No, QMessageBox.Yes)
                print('New error')
                return 0

    def showRecoverImage(self):
        if (self.OrImgPath == ''):
            return
        #先显示左边的原图
        img = cv2.imread(self.OrImgPath)
        RGB_Image = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        frame = QImage(RGB_Image, RGB_Image.shape[1], RGB_Image.shape[0], RGB_Image.shape[1] * 3, QImage.Format_RGB888)
        pix = QPixmap.fromImage(frame)
        self.OrImgitem.setPixmap(pix)
        self.OrImgscene.addItem(self.OrImgitem)
        self.OrImgView.setScene(self.OrImgscene)  # 将场景添加至视图
        self.IsShrankFlag = None

        #同时恢复右边的图像
        if 3==self.globalRectangle.ndim:
            recimg_binary = cv2.cvtColor(self.globalRectangle, cv2.COLOR_BGR2RGB)
            frame = QImage(recimg_binary, recimg_binary.shape[1], recimg_binary.shape[0],
                           recimg_binary.shape[1] * 3, QImage.Format_RGB888)
            pix = QPixmap.fromImage(frame)
            self.BinaryImgitem.setPixmap(pix)
            self.BinaryImgscene.addItem(self.BinaryImgitem)
            self.BinaryImgView.setScene(self.BinaryImgscene)
            print('RGB或HSV图像')
        else:
            print('anoter type')

    def localCover(self):
        if (self.OrImgPath == ''):
            return
        if self.IsShrankFlag:
            n_start_x, n_start_y, n_end_x, n_end_y = self.CoordinateSelectDialog.getCorrdiante()
            #同时恢复右边的图像
            if 2 == self.globalRectangle.ndim:
                 self.globalRectangle[n_start_y:n_end_y, n_start_x:n_end_x]=self.curHandleLocalRectangle
            elif 3==self.globalRectangle.ndim:
                 self.globalRectangle[n_start_y:n_end_y, n_start_x:n_end_x,:] = self.curHandleLocalRectangle
            else:
                print('程序有问题，出错！！！')
            self.showRecoverImage()
            reply =QMessageBox.information(self, '局部覆盖', '局部覆盖完成', QMessageBox.Yes | QMessageBox.No, QMessageBox.Yes)
            self.IsShrankFlag=False


    def showHSVChannelInputDialog(self):
        retValue = self.HSVChannelUI.exec_()
        if retValue == QtWidgets.QDialog.Accepted:
            # [h_1_Start,h_1_End,h_2_Start,h_2_End],[s_1_Start,s_1_End,s_2_Start,s_2_End],[v_1_Start,v_1_End,v_2_Start,v_2_End]=self.HSVChannelUI.getHSVData()
            self.HandleHSVTract()
            QMessageBox.information(self, 'HSV通道颜色提取', '提取完成', QMessageBox.Yes | QMessageBox.No, QMessageBox.Yes)

     #根据HSV通道的值进行滤波
    def HandleHSVTract(self):
        if self.OrImgPath == '':
            reply = QMessageBox.information(self, '未读取图像', '请先读取图像', QMessageBox.Yes | QMessageBox.No, QMessageBox.Yes)
            if (reply == QMessageBox.Yes):
                self.readImg()
            return
        if (not self.IsShrankFlag):
            image = cv2.imread(self.OrImgPath)
            [[h_1_Start, h_1_End, h_2_Start, h_2_End], [s_1_Start, s_1_End, s_2_Start, s_2_End],
            [v_1_Start, v_1_End, v_2_Start, v_2_End]]= self.HSVChannelUI.getHSVData()
            new_image= algorithms.HSV_Line_Tract(image,h_1_Start, h_1_End, h_2_Start, h_2_End,s_1_Start, s_1_End, s_2_Start, s_2_End,v_1_Start, v_1_End, v_2_Start, v_2_End)
            self.globalRectangle=new_image
            utils.SaveHSVTractImage(new_image,self.OrImgPath)
            # 将图片转化成Qt可读格式
            new_image= cv2.cvtColor(new_image, cv2.COLOR_BGR2RGB)
            frame = QtGui.QImage(new_image, new_image.shape[1], new_image.shape[0], new_image.shape[1]*3, QtGui.QImage.Format_RGB888)
            # 加载图片,并自定义图片展示尺寸
            pix = QPixmap.fromImage(frame)
            self.BinaryImgitem.setPixmap(pix)
            self.BinaryImgscene.addItem(self.BinaryImgitem)
            self.BinaryImgView.setScene(self.BinaryImgscene)
        else:
            image = cv2.imread(self.OrImgPath)
            n_start_x, n_start_y, n_end_x, n_end_y = self.CoordinateSelectDialog.getCorrdiante()
            rec_img = image[n_start_y:n_end_y, n_start_x:n_end_x, :]

            [[h_1_Start, h_1_End, h_2_Start, h_2_End], [s_1_Start, s_1_End, s_2_Start, s_2_End],
             [v_1_Start, v_1_End, v_2_Start, v_2_End]] = self.HSVChannelUI.getHSVData()
            new_image = algorithms.HSV_Line_Tract(rec_img, h_1_Start, h_1_End, h_2_Start, h_2_End, s_1_Start, s_1_End,
                                                  s_2_Start, s_2_End, v_1_Start, v_1_End, v_2_Start, v_2_End)
            self.curHandleLocalRectangle = new_image
            utils.SaveHSVTractLocalityImage(new_image, self.OrImgPath)
            # 将图片转化成Qt可读格式
            new_image= cv2.cvtColor(new_image, cv2.COLOR_BGR2RGB)
            frame = QtGui.QImage(new_image, new_image.shape[1], new_image.shape[0], new_image.shape[1] * 3,
                                 QtGui.QImage.Format_RGB888)
            # 加载图片,并自定义图片展示尺寸
            pix = QPixmap.fromImage(frame)
            self.BinaryImgitem.setPixmap(pix)
            self.BinaryImgscene.addItem(self.BinaryImgitem)
            self.BinaryImgView.setScene(self.BinaryImgscene)

#子界面类，用于显示父窗口中的子窗口，解决QInputDialog一次只能输入一个弹窗的困扰
class regionSplitWindow(QDialog,Ui_Dialog):
    #创建信号，用于界面传参
    signal_diffCh=pyqtSignal(str)    #通道差值的信号
    #传递多个参数 用下列代码
    #signal_diffCh = pyqtSignal(str,str)

    # 多继承方式，继承界面父类,分离逻辑代码和界面代码
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUi(self)
        self.setWindowFlags(QtCore.Qt.WindowCloseButtonHint)
        self.setWindowTitle("RGB通道的差值二值化")
        self.button_confirm.clicked.connect(self.dataTrans)

    def dataTrans(self):
        #传递多个参数，用下列代码
        #self.signal_diffCh.emit(str(self.comboBox_bigCh.currentIndex()),
        #                      str(self.comboBox_smallCh.currentIndex()),self.lineEdit_diffCh.text())
        if(not utils.is_number(self.lineEdit_diffCh.text())):
            QMessageBox.information(self, '请重新输入参数', '请输入数字', QMessageBox.Yes | QMessageBox.No, QMessageBox.Yes)
            return
        self.signal_diffCh.emit(self.lineEdit_diffCh.text())

#子界面类  坐标选择
class showCorrdinateDialog(QDialog, CoordinateSelect_Ui_dialog):
    def __init__(self, parent=None):
            super().__init__(parent)
            self.setupUi(self)
            self.corrdinate_start_x = -1
            self.corrdinate_start_y = -1
            self.corrdinate_end_x = -1
            self.corrdinate_end_y = -1

    def getCorrdiante(self):
            return [self.corrdinate_start_x, self.corrdinate_start_y, self.corrdinate_end_x, self.corrdinate_end_y]

    def accept(self):
            Text_Start_x = self.lineEdit_Start_x.text()
            Text_Start_y = self.lineEdit_Start_y.text()
            Text_End_x = self.lineEdit_End_x.text()
            Text_End_y = self.lineEdit_End_y.text()
            if (utils.is_number(Text_Start_x) & utils.is_number(Text_Start_y) & utils.is_number(
                    Text_End_x) & utils.is_number(Text_End_y)):
                self.corrdinate_start_x = int(float(Text_Start_x))
                self.corrdinate_start_y = int(float(Text_Start_y))
                self.corrdinate_end_x = int(float(Text_End_x))
                self.corrdinate_end_y = int(float(Text_End_y))
                super().accept()
            else:
                # 输入的字符串有些不能转换为数字
                print("输入的字符串不能全部转换为数字，请重新输入！")
                reply = QMessageBox.information(self, '错误', '输入的字符串不能全部转换为数字，请重新输入！', QMessageBox.Yes | QMessageBox.No,
                                             QMessageBox.Yes)

#子界面类  HSV算法处理
class showHSV_Channel_SelectUI(QDialog,HSV_Ui_Dialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUi(self)

        #设定默认参数
        self.h_validation_1_start_value=0
        self.h_validation_1_end_value = 0.5
        self.h_validation_2_start_value = 0.56
        self.h_validation_2_end_value = 1

        self.s_validation_1_start_value = 0
        self.s_validation_1_end_value = 1
        self.s_validation_2_start_value = 0
        self.s_validation_2_end_value = 1

        self.v_validation_1_start_value = 0
        self.v_validation_1_end_value = 0.6
        self.v_validation_2_start_value = 0
        self.v_validation_2_end_value = 0.6
        # 初始化H通道的值
        self.H_Valid1_Start.setText(str(self.h_validation_1_start_value))
        self.H_Valid1_End.setText(str(self.h_validation_1_end_value))
        self.H_Valid2_Start.setText(str(self.h_validation_2_start_value))
        self.H_Valid2_End.setText(str(self.h_validation_2_end_value))
        # 初始化S颜色通道的值
        self.S_Valid1_Start.setText(str(self.s_validation_1_start_value))
        self.S_Valid1_End.setText(str(self.s_validation_1_end_value))
        self.S_Valid2_Start.setText(str(self.s_validation_2_start_value ))
        self.S_Valid2_End.setText(str(self.s_validation_2_end_value))
        # 初始化V颜色通道的值
        self.V_Valid1_Start.setText(str(self.v_validation_1_start_value))
        self.V_Valid1_End.setText(str(self.v_validation_1_end_value))
        self.V_Valid2_Start.setText(str(self.v_validation_2_start_value))
        self.V_Valid2_End.setText(str(self.v_validation_2_end_value))



    def getHSVData(self):
        Text_h_validation_1_start = self.H_Valid1_Start.text()
        Text_h_validation_1_end   = self.H_Valid1_End.text()
        Text_h_validation_2_start = self.H_Valid2_Start.text()
        Text_h_validation_2_end   = self.H_Valid2_End.text()

        Text_s_validation_1_start = self.S_Valid1_Start.text()
        Text_s_validation_1_end   = self.S_Valid1_End.text()
        Text_s_validation_2_start = self.S_Valid2_Start.text()
        Text_s_validation_2_end   = self.S_Valid2_End.text()

        Text_v_validation_1_start = self.V_Valid1_Start.text()
        Text_v_validation_1_end   = self.V_Valid1_End.text()
        Text_v_validation_2_start = self.V_Valid2_Start.text()
        Text_v_validation_2_end   = self.V_Valid2_End.text()

        self.h_validation_1_start_value = utils.converStr2float(Text_h_validation_1_start)
        self.h_validation_1_end_value = utils.converStr2float(Text_h_validation_1_end)
        self.h_validation_2_start_value = utils.converStr2float(Text_h_validation_2_start)
        self.h_validation_2_end_value = utils.converStr2float(Text_h_validation_2_end)

        self.s_validation_1_start_value = utils.converStr2float(Text_s_validation_1_start)
        self.s_validation_1_end_value = utils.converStr2float(Text_s_validation_1_end)
        self.s_validation_2_start_value = utils.converStr2float(Text_s_validation_2_start)
        self.s_validation_2_end_value = utils.converStr2float(Text_s_validation_2_end)

        self.v_validation_1_start_value = utils.converStr2float(Text_v_validation_1_start)
        self.v_validation_1_end_value = utils.converStr2float(Text_v_validation_1_end)
        self.v_validation_2_start_value = utils.converStr2float(Text_v_validation_2_start)
        self.v_validation_2_end_value = utils.converStr2float(Text_v_validation_2_end)


        return [[self.h_validation_1_start_value,self.h_validation_1_end_value,self.h_validation_2_start_value,self.h_validation_2_end_value],
                [ self.s_validation_1_start_value,self.s_validation_1_end_value, self.s_validation_2_start_value, self.s_validation_2_end_value],
                [ self.v_validation_1_start_value ,  self.v_validation_1_end_value ,self.v_validation_2_start_value ,   self.v_validation_2_end_value]]


    def accept(self):
          H_Chanel_Input_flag = utils.is_number(self.H_Valid1_Start.text())&utils.is_number(self.H_Valid1_End.text())&utils.is_number(self.H_Valid2_Start.text())&utils.is_number(self.H_Valid2_End.text())
          S_Chanel_Input_flag = utils.is_number(self.S_Valid1_Start.text()) & utils.is_number(self.S_Valid1_End.text()) & utils.is_number(self.S_Valid2_Start.text()) & utils.is_number(self.S_Valid2_End.text())
          V_Chanel_Input_flag = utils.is_number(self.V_Valid1_Start.text()) & utils.is_number(self.V_Valid1_End.text()) & utils.is_number(self.V_Valid2_Start.text()) & utils.is_number(self.V_Valid2_End.text())

          if(H_Chanel_Input_flag&S_Chanel_Input_flag&V_Chanel_Input_flag):
              super().accept()
          else:
            reply = QMessageBox.information(self, '请检查数字输入', '输入的字符串不能全部转换为数字，请重新输入！', QMessageBox.Yes | QMessageBox.No, QMessageBox.Yes)

#中国的墙太厚了，访问GitHub真难

if __name__ == "__main__":
    app = QApplication(sys.argv)
    showMainWindow = showMainWindow()
    showMainWindow.show()
    app.exec_()