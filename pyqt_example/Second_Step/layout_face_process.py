# coding:utf-8
#!/usr/bin/env python

__author__ = 'SAF'
#!/usr/bin/env python
# PyQt tutorial 3
"""
面向过程的方式大概的思路就像是生成一个默认的widget，
然后通过函数调用，通过子widget按钮的创建去修饰这个widget，然后显示。
"""

import sys
from PyQt4 import QtCore, QtGui


app = QtGui.QApplication(sys.argv)

window = QtGui.QWidget()
window.resize(200, 120)

quit = QtGui.QPushButton("Quit", window)
quit.setFont(QtGui.QFont("Times", 18, QtGui.QFont.Bold))
quit.setGeometry(10, 40, 180, 40)
QtCore.QObject.connect(quit, QtCore.SIGNAL("clicked()"),
                       app, QtCore.SLOT("quit()"))

window.show()
sys.exit(app.exec_())