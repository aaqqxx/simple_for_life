# coding:utf-8
#!/usr/bin/env python

__author__ = 'SAF'
#!/usr/bin/env python
import sys
from PyQt4 import QtCore, QtGui


class HelloButton(QtGui.QPushButton):
    def __init__(self, parent=None):
        QtGui.QPushButton.__init__(self, parent)
        self.setText("Hello World")



class HelloWindow(QtGui.QMainWindow):
    def __init__(self, parent=None):
        QtGui.QMainWindow.__init__(self, parent)
        self.button = HelloButton(self)
        self.connect(self.button, QtCore.SIGNAL("clicked()"), self, QtCore.SLOT("close()"))
        self.setCentralWidget(self.button)


def main(args):
    app = QtGui.QApplication(args)
    win = HelloWindow()
    # win.connect(win, QtCore.SIGNAL("clicked()"), win, QtCore.SLOT("close()"))
    # win.connect(win, QtCore.SIGNAL("clicked()"), app, QtCore.SLOT("quit()"))
    win.show()
    # app.connect(app, QtCore.SIGNAL("lastWindowClosed()"),
    #             app, QtCore.SLOT("quit()"))
    app.exec_()


if __name__ == "__main__":
    main(sys.argv)