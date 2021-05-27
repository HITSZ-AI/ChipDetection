from PyQt5.QtCore import pyqtSlot
from PyQt5.QtGui import QImage, QPixmap
from   PyQt_UI.Ui_picshow import Ui_MainWindow
from PyQt5.QtWidgets import *
import cv2


class picturezoom(QMainWindow, Ui_MainWindow):

    def __init__(self, parent=None):
        super(picturezoom, self).__init__(parent)
        self.setupUi(self)
        img = cv2.imread("../images/1-8/outline8_3.jpg")  # 读取图像
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)  # 转换图像通道
        x = img.shape[1]  # 获取图像大小
        y = img.shape[0]
        h=img.shape[2]
        self.zoomscale = 1  # 图片放缩尺度
        #需要加上x*h
        frame = QImage(img, x, y, x*h,QImage.Format_RGB888)
        pix = QPixmap.fromImage(frame)
        self.item = QGraphicsPixmapItem(pix)  # 创建像素图元
        # self.item.setScale(self.zoomscale)
        self.scene = QGraphicsScene()  # 创建场景
        self.scene.addItem(self.item)
        self.picshow.setScene(self.scene)  # 将场景添加至视图
        self.item.mousePressEvent=self.getPos
        #调用fitInView
        #self.picshow.fitInView(QGraphicsPixmapItem(pix))


    def getPos(self, event):
        x = event.pos().x()
        y = event.pos().y()

        print("xxxxx%s" % x)
        print("yyyyy%s" % y)
        NowCorrdinate = '横坐标：' + str(int(x)) + ' 纵坐标: ' + str(int(y))
        QMessageBox.about(self, '当前坐标', NowCorrdinate)

    @pyqtSlot()
    def on_zoomin_clicked(self):
        """
        点击缩小图像
        """
        # TODO: not implemented yet
        self.zoomscale = self.zoomscale - 0.1
        if self.zoomscale <= 0:
            self.zoomscale = 0.2
        self.item.setScale(self.zoomscale)  # 缩小图像

    @pyqtSlot()
    def on_zoomout_clicked(self):
        """
        点击方法图像
        """
        # TODO: not implemented yet
        self.zoomscale = self.zoomscale + 0.1
        if self.zoomscale >= 1.2:
            self.zoomscale = 1.2
        self.item.setScale(self.zoomscale)  # 放大图像


def main():
    import sys
    app = QApplication(sys.argv)
    piczoom = picturezoom()
    piczoom.show()
    app.exec_()


if __name__ == '__main__':
    main()