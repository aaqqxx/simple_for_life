#!/usr/bin/python
# coding:GBK

__author__ = 'XingHua'

"""

"""

from PyQt4.QtGui import *
import sys

#QTextCodec.setCodecForTr(QTextCodec.codecForName("utf8"))

class MyQQ(QTabWidget):
    def __init__(self, parent=None):
        super(MyQQ, self).__init__(parent)
        toolbox1 = QToolBox()
        toolbox2 = QToolBox()
        self.addTab(toolbox1, ur"联系人")
        self.addTab(toolbox2, ur"群/讨论组")
        tabWidget = QTabWidget(self)
        w1 = QWidget()
        w2 = QWidget()
        w3 = QWidget()
        tabWidget.addTab(w1, "General")
        tabWidget.addTab(w2, "Permissions")
        tabWidget.addTab(w3, "Applications")
        tabWidget.setGeometry(100, 100, 380, 500)
        tabWidget.resize(380, 500)


app = QApplication(sys.argv)
myqq = MyQQ()
myqq.setWindowTitle("QQ2012")
myqq.resize(500, 600)
myqq.show()
app.exec_()