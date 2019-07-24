from PyQt5 import sip
import sys
from PyQt5.QtWidgets import QApplication, QWidget, QDesktopWidget, QPushButton, QLabel, QLineEdit, QTextBrowser, QFormLayout
from PyQt5 import QtGui
import masterkeyGen


def checkHexElement(datalist):
    hex_element = ['0','1','2','3','4','5','6','7','8','9','A','B','C','D','E','F','a','b','c','d','e','f']
    for ele in datalist:
        if ele not in hex_element:
            return False
    return True


class Example(QWidget):

    def __init__(self, size, title):
        super().__init__()
        self.initUi(size, title)

    def initUi(self, size, title):

        self.resize(size[0], size[1])

        self.setMyLocation()

        self.addMyWidget()

        self.setWindowTitle(title)

        self.show()

    def setMyLocation(self):
        # 获得主窗体的几何信息
        winRectangle = self.frameGeometry()
        # 获取显示器的分辨率，然后得到屏幕中间点的位置
        screenCenterPoint = QDesktopWidget().availableGeometry().center()
        # 把主窗体的中心点放置到屏幕的中心位置
        winRectangle.moveCenter(screenCenterPoint)
        # 把主窗口的左上角移动到其主窗体的左上角
        self.move(winRectangle.topLeft())

    def addMyWidget(self):
        startTitle = QLabel('MAC起始地址')
        endTitle = QLabel('MAC结束地址')
        self.startBox = QLineEdit()
        self.endBox = QLineEdit()
        genButton = QPushButton('生成Masterkey')
        self.feedback = QTextBrowser()
        # self.startBox.setMinimumHeight(30)
        # self.endBox.setMinimumHeight(30)
        # genButton.setMinimumHeight(30)

        font = QtGui.QFont()
        font.setFamily('微软雅黑')
        font.setBold(False)
        font.setPointSize(12)

        startTitle.setFont(font)
        endTitle.setFont(font)
        self.startBox.setFont(font)
        self.endBox.setFont(font)
        genButton.setFont(font)
        genButton.setStyleSheet("QPushButton{padding: 6px; font: 12; background-color:rgb(76,171,187)}")
        font.setPointSize(9)
        self.feedback.setFont(font)

        formlayout = QFormLayout()
        formlayout.addRow(startTitle, self.startBox)
        formlayout.addRow(endTitle, self.endBox)
        formlayout.addRow(genButton)
        formlayout.addRow(self.feedback)

        # 设置外边距--控件到窗口边框的距离(左上右下)
        formlayout.setContentsMargins(50,20,50,40)
        # 设置内边距---控件之间的距离
        formlayout.setSpacing(20)

        self.setLayout(formlayout)

        genButton.clicked.connect(self.on_click)

    def on_click(self):
        
        mac_start = self.startBox.text()
        mac_end = self.endBox.text()

        if len(mac_start) != 12 or len(mac_end) != 12:
            self.feedback.setText("<font color=red>请输入正确的MAC地址</font>")
            return

        if checkHexElement(list(mac_start)) == False or checkHexElement(list(mac_end)) == False:
            self.feedback.setText("<font color=red>请输入正确的MAC地址</font>")            
            return

        mac_start = int(mac_start, 16)
        mac_end = int(mac_end, 16)
        if mac_start > mac_end:
            self.feedback.setText('<font color=red>请输入正确的MAC地址范围</font>')
            return

        masterkey = masterkeyGen.Masterkey()
        num = masterkey.generate(mac_start, mac_end)
        file_path = masterkey.save('mac_masterkey.xlsx')

        self.feedback.setText('<font color=black>{} masterkey has been write to:\n{}</font>'.format(num, file_path))


if __name__ == "__main__":

    # 创建pyqt5应用对象
    app = QApplication(sys.argv)

    # 修改空间位置到坐标(300, 300)
    ex = Example([480,320], 'Remotec masterkey generator')

    sys.exit(app.exec_())
