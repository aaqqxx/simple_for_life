# coding:utf-8
#!/usr/bin/env python

__author__ = 'SAF'
import sys
from PyQt4 import QtGui


app = QtGui.QApplication(sys.argv)
label = QtGui.QLabel("Hello QT!") #这里我没有办法让CSDN不将其解释为HTML。。。所以，参考界面的源代码看看是什么吧
label.show()

sys.exit(app.exec_())