# coding:utf-8
#!/usr/bin/env python

__author__ = 'SAF'

import sys
from PyQt4 import QtCore, QtGui


class MyDialog(QtGui.QDialog):
    def __init__(self, parent=None):
        QtGui.QDialog.__init__(self, parent)

        self.setFixedSize(200, 120)

        self.quit = QtGui.QPushButton("Quit", self)
        self.quit.setGeometry(62, 40, 75, 30)
        self.quit.setFont(QtGui.QFont("Times", 18, QtGui.QFont.Bold))

        self.connect(self.quit, QtCore.SIGNAL("clicked()"),
                     self, QtCore.SLOT("close()"))


app = QtGui.QApplication(sys.argv)
dialog = MyDialog()
dialog.show()
sys.exit(app.exec_())