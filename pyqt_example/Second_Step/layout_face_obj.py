# coding:utf-8
#!/usr/bin/env python

__author__ = 'SAF'

"""
面向对象的方式大概思路就像是先描述我们想要的widget是有一个子widget按钮的，大小是多少。。。。。
然后直接创建一个我们描述过的想要的widget，将其显示。
"""
import sys
from PyQt4 import QtCore, QtGui


class MyWidget(QtGui.QWidget):
    def __init__(self, parent=None):
        QtGui.QWidget.__init__(self, parent)

        self.setFixedSize(200, 120)

        self.quit = QtGui.QPushButton("Quit", self)
        self.quit.setGeometry(62, 40, 75, 30)
        self.quit.setFont(QtGui.QFont("Times", 18, QtGui.QFont.Bold))

        self.connect(self.quit, QtCore.SIGNAL("clicked()"),
                     QtGui.qApp, QtCore.SLOT("quit()"))


app = QtGui.QApplication(sys.argv)
widget = MyWidget()
widget.show()
sys.exit(app.exec_())