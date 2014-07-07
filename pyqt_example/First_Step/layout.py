# coding:utf-8
#!/usr/bin/env python

__author__ = 'SAF'
import sys
from PyQt4 import QtCore, QtGui

app = QtGui.QApplication(sys.argv)

window = QtGui.QWidget()

spinBox = QtGui.QSpinBox()
slider = QtGui.QSlider(QtCore.Qt.Horizontal)
spinBox.setRange(0, 130)
slider.setRange(0, 130)

QtCore.QObject.connect(spinBox, QtCore.SIGNAL("valueChanged(int)"),
                       slider, QtCore.SLOT("setValue(int)"))
QtCore.QObject.connect(slider, QtCore.SIGNAL("valueChanged(int)"),
                       spinBox, QtCore.SLOT("setValue(int)"))
spinBox.setValue(35)

layout = QtGui.QHBoxLayout()
layout.addWidget(spinBox)
layout.addWidget(slider)
window.setLayout(layout)

window.show()
sys.exit(app.exec_())