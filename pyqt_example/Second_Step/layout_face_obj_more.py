# coding:utf-8
#!/usr/bin/env python

__author__ = 'SAF'

# PyQt tutorial 4 ext objWindow

import sys
from PyQt4 import QtCore, QtGui


class MyWidget(QtGui.QWidget):
    def __init__(self, parent=None):
        QtGui.QWidget.__init__(self, parent)

        self.setFixedSize(200, 120)

        self.quit = QtGui.QPushButton("Quit", self)
        self.quit.setGeometry(62, 40, 75, 30)
        self.quit.setFont(QtGui.QFont("Times", 18, QtGui.QFont.Bold))

        # self.connect(self.quit, QtCore.SIGNAL("clicked()"), QtGui.qApp, QtCore.SLOT("quit()"))
        self.connect(self.quit, QtCore.SIGNAL("clicked()"), self, QtCore.SLOT("close()"))


app = QtGui.QApplication(sys.argv)
widget = MyWidget()
widget.move(350, 50)
widget.setWindowTitle("A Widget")
widget.show()
anotherWidget = MyWidget()
anotherWidget.move(50, 50)
anotherWidget.setWindowTitle("Another Widget")
anotherWidget.show()
sys.exit(app.exec_())