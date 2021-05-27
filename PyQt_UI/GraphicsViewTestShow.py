from PyQt5.QtCore import pyqtSlot
from PyQt5.QtGui import QImage, QPixmap
from PyQt5.QtWidgets import *
import cv2
from PyQt_UI.GraphicViewTest import  Ui_MainWindow


class picturezoom(QMainWindow, Ui_MainWindow):
    """
    Class documentation goes here.
    """

    def __init__(self, parent=None):
        """
        Constructor

        @param parent reference to the parent widget
        @type QWidget
        """
        super(picturezoom, self).__init__(parent)
        self.setupUi(self)
        img = cv2.imread("../images/1-8/outline8_3.jpg")  # 读取图像
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)  # 转换图像  通道
        x = img.shape[1]  # 获取图像大小
        y = img.shape[0]
        self.zoomscale = 1  # 图片放缩尺度
        frame = QImage(img, x, y,x*3, QImage.Format_RGB888)
        pix = QPixmap.fromImage(frame)
        self.item = QGraphicsPixmapItem(pix)  # 创建像素图元

        self.scene = QGraphicsScene()  # 创建场景
        self.scene.addItem(self.item)
        self.ImgView.setScene(self.scene)
        #self.picshow.setScene(self.scene)  # 将场景添加至视图

        self.item.mousePressEvent=self.getPos

    def getPos(self, event):
            x = event.pos().x()
            y = event.pos().y()
            print("xxxxx%s" % x)
            print("yyyyy%s" % y)
            NowCorrdinate = '横坐标：' + str(int(x)) + ' 纵坐标: ' + str(int(y))
            QMessageBox.about(self, '当前坐标', NowCorrdinate)

    @pyqtSlot()
    def on_button_lessen_clicked(self):
            """
            点击缩小图像
            """
            # TODO: not implemented yet
            self.zoomscale = self.zoomscale - 0.05
            if self.zoomscale <= 0:
                self.zoomscale = 0.2
            self.item.setScale(self.zoomscale)  # 缩小图像


    @pyqtSlot()
    def on_button_Amplify_clicked(self):
            """
            点击方法图像
            """
            # TODO: not implemented yet
            self.zoomscale = self.zoomscale + 0.05
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