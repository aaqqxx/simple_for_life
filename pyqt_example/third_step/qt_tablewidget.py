# coding:utf-8
#!/usr/bin/env python

__author__ = 'SAF'

from PyQt4.QtGui import *
from PyQt4.QtCore import *


class MyDialog(QDialog):
    def __init__(self, parent=None):
        super(MyDialog, self).__init__(parent)
        # 构造了一个QTableWidget的对象，并且设置为4行，3列
        self.MyTable = QTableWidget(4, 3)
        #设置表格的表头
        self.MyTable.setHorizontalHeaderLabels([u'姓名', u'身高',u'体重'])
        # 生成一个QTableWidgetItem的对象，并让其名为“松鼠”
        newItem = QTableWidgetItem(u"松鼠")
        # 将刚才生成的Item加载到第0行、0列处
        self.MyTable.setItem(0, 0, newItem)

        newItem = QTableWidgetItem("10cm")
        self.MyTable.setItem(0, 1, newItem)

        newItem = QTableWidgetItem("60g")
        self.MyTable.setItem(0, 2, newItem)

        layout = QHBoxLayout()
        layout.addWidget(self.MyTable)
        self.setLayout(layout)

        self.MyTable.setEditTriggers(QAbstractItemView.NoEditTriggers)   #MyTable是上面代码中生成的QTableWidget对象


if __name__ == '__main__':
    import sys

    app = QApplication(sys.argv)
    myWindow = MyDialog()
    myWindow.show()
    sys.exit(app.exec_())