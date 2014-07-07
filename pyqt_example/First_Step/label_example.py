# coding:utf-8
#!/usr/bin/env python

__author__ = 'SAF'
import sys
from PyQt4 import QtGui


app = QtGui.QApplication(sys.argv)
label = QtGui.QLabel("Hello Qt!")
label.show()

sys.exit(app.exec_())