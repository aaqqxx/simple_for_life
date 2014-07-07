# coding:utf-8
#!/usr/bin/env python

__author__ = 'SAF'

import sys
from PyQt4 import QtCore, QtGui


class MyDialog(QtGui.QDialog):
    def __init__(self, parent=None):
        QtGui.QDialog.__init__(self, parent)

        self.quit = QtGui.QPushButton("Quit")

        self.change = QtGui.QPushButton("Change")
        self.change.setEnabled(False)

        # funny widget
        self.lcd = QtGui.QLCDNumber(2)

        self.slider = QtGui.QSlider(QtCore.Qt.Horizontal)
        self.slider.setRange(0, 99)
        self.slider.setValue(0)

        # self.lineEdit = QtGui.QLineEdit()
        # 比如，lineEdit widget可以输入任何形式的字符，
        # 而不仅仅是数字，这在我们这个例子中应该是不允许的，
        # 在Qt中也提供了一种远胜MFC的限制方式，
        # 不用继承并实现一个自己的lineEdit widget就能实现非常 复杂的限制功能，
        # 这和STL中泛型的算法思维有点类似。这就是Qt 中的Validator，
        # 功能强大到你甚至可以很简单的就使用正则表达式去限制lineEdit。。。。
        # 呵呵，强大。。。这里我根据需要，使用QIntValidator就足够了。
        intValidator = QtGui.QIntValidator(0, 99, self)
        self.lineEdit = QtGui.QLineEdit()
        self.lineEdit.setValidator(intValidator)

        self.connect(self.quit, QtCore.SIGNAL("clicked()"),
                     QtGui.qApp, QtCore.SLOT("quit()"))
        self.connect(self.lineEdit, QtCore.SIGNAL("textChanged(const QString&)"),
                     self.enableChangeButton)
        self.connect(self.slider, QtCore.SIGNAL("valueChanged(int)"),
                     self.SliderChange)
        self.connect(self.change, QtCore.SIGNAL("clicked()"),
                     self.Change)

        self.rightLayout = QtGui.QVBoxLayout()
        self.rightLayout.addWidget(self.lineEdit)
        self.rightLayout.addWidget(self.change)

        self.leftLayout = QtGui.QVBoxLayout()
        self.leftLayout.addWidget(self.lcd)
        self.leftLayout.addWidget(self.slider)

        self.layout = QtGui.QHBoxLayout()
        self.layout.addWidget(self.quit)
        self.layout.addLayout(self.leftLayout)
        self.layout.addLayout(self.rightLayout)

        self.setLayout(self.layout);

    def enableChangeButton(self, text):
        self.change.setEnabled(text.isEmpty() == False)

    def Change(self):
        value = int(self.lineEdit.text())
        self.lcd.display(value)
        self.slider.setValue(value)

    def SliderChange(self):
        value = self.slider.value()
        self.lcd.display(value)
        self.lineEdit.setText(str(value))


app = QtGui.QApplication(sys.argv)
dialog = MyDialog()
dialog.show()
sys.exit(app.exec_())