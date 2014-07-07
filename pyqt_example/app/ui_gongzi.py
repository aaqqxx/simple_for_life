# coding:utf-8
#!/usr/bin/env python

__author__ = 'SAF'
# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'untitled.ui'
#
# Created: Mon Aug 14 14:26:51 2006
#      by: PyQt4 UI code generator 4.0.1
#
# WARNING! All changes made in this file will be lost!

import sys
from PyQt4 import QtCore, QtGui

class Ui_gongzi(object):
    def setupUi(self, gongzi):
        gongzi.setObjectName("gongzi")
        gongzi.resize(QtCore.QSize(QtCore.QRect(0,0,400,300).size()).expandedTo(gongzi.minimumSizeHint()))

        self.verticalLayout = QtGui.QWidget(gongzi)
        self.verticalLayout.setGeometry(QtCore.QRect(20,120,160,80))
        self.verticalLayout.setObjectName("verticalLayout")

        self.vboxlayout = QtGui.QVBoxLayout(self.verticalLayout)
        self.vboxlayout.setMargin(0)
        self.vboxlayout.setSpacing(6)
        self.vboxlayout.setObjectName("vboxlayout")

        self.lineEdit = QtGui.QLineEdit(self.verticalLayout)
        self.lineEdit.setObjectName("lineEdit")
        self.vboxlayout.addWidget(self.lineEdit)

        self.verticalLayout_2 = QtGui.QWidget(gongzi)
        self.verticalLayout_2.setGeometry(QtCore.QRect(20,20,160,80))
        self.verticalLayout_2.setObjectName("verticalLayout_2")

        self.vboxlayout1 = QtGui.QVBoxLayout(self.verticalLayout_2)
        self.vboxlayout1.setMargin(0)
        self.vboxlayout1.setSpacing(6)
        self.vboxlayout1.setObjectName("vboxlayout1")

        self.label = QtGui.QLabel(self.verticalLayout_2)
        self.label.setObjectName("label")
        self.vboxlayout1.addWidget(self.label)

        self.verticalLayout_3 = QtGui.QWidget(gongzi)
        self.verticalLayout_3.setGeometry(QtCore.QRect(260,130,111,71))
        self.verticalLayout_3.setObjectName("verticalLayout_3")

        self.vboxlayout2 = QtGui.QVBoxLayout(self.verticalLayout_3)
        self.vboxlayout2.setMargin(0)
        self.vboxlayout2.setSpacing(6)
        self.vboxlayout2.setObjectName("vboxlayout2")

        self.pushButton = QtGui.QPushButton(self.verticalLayout_3)
        self.pushButton.setObjectName("pushButton")
        self.vboxlayout2.addWidget(self.pushButton)

        self.retranslateUi(gongzi)
        QtCore.QMetaObject.connectSlotsByName(gongzi)

    def retranslateUi(self, gongzi):
        gongzi.setWindowTitle(QtGui.QApplication.translate("gongzi", "Form", None, QtGui.QApplication.UnicodeUTF8))
        self.lineEdit.setText(QtGui.QApplication.translate("gongzi", "1111111111", None, QtGui.QApplication.UnicodeUTF8))
#        self.label.setText(QtGui.QApplication.translate("gongzi", "TextLabel", None, QtGui.QApplication.UnicodeUTF8))
        self.pushButton.setText(QtGui.QApplication.translate("gongzi", "PushButton", None, QtGui.QApplication.UnicodeUTF8))