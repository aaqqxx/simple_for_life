# coding:utf-8
#!/usr/bin/env python

__author__ = 'SAF'

import sys
from PyQt4 import QtCore, QtGui

from ui_gongzi import Ui_gongzi

class Gongzi(QtGui.QWidget):
        def __init__(self, parent=None):
                QtGui.QWidget.__init__(self, parent)
                self.ui = Ui_gongzi()
                self.ui.setupUi(self)

#                self.ui.pushButton.setObjectName("pushButton1")
# 调用类的事件
#                self.ui.pushButton.connect(self.ui.pushButton,
#                        QtCore.SIGNAL("clicked()"),
#                        self,QtCore.SLOT("close()"))

# 按按钮以后把lineEdit 的内容显示到lable
                self.ui.pushButton.connect(self.ui.pushButton,
                        QtCore.SIGNAL("clicked()"),self.printa)


# lineEdit 取输入的字段用下面的操作
# a = QtCore.QString(win.text())
                self.value = QtCore.QString(self.ui.lineEdit.text())
# lable 输出内容
#                self.ui.label.setText(QtGui.QApplication.translate(self.value)
                self.ui.label.setText(QtGui.QApplication.translate("gongzi",
                        "%s" % self.value, None, QtGui.QApplication.UnicodeUTF8))


        def printa(self):
                print "%s" % self.value
                self.value = QtCore.QString(self.ui.lineEdit.text())
                self.ui.label.setText(QtGui.QApplication.translate("gongzi",
                   "%s" % self.value, None, QtGui.QApplication.UnicodeUTF8))
if __name__ == "__main__":
        app = QtGui.QApplication(sys.argv)
        gongzi = Gongzi()
#        gongzi.ui.pushButton.connect(gongzi.ui.pushButton,
#                        QtCore.SIGNAL("clicked()"),
#                        gongzi.ui.pushButton,QtCore.SLOT("close"))
        gongzi.show()
        sys.exit(app.exec_())