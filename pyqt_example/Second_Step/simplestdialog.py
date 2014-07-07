# coding:utf-8
#!/usr/bin/env python

__author__ = 'SAF'
import sys
from PyQt4 import QtCore, QtGui


app = QtGui.QApplication(sys.argv)

dialog = QtGui.QDialog()
quit = QtGui.QPushButton("Quit", dialog)
QtCore.QObject.connect(quit, QtCore.SIGNAL("clicked()"),
                       app, QtCore.SLOT("quit()"))

dialog.show()
sys.exit(app.exec_())