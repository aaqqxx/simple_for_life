# coding:utf-8
#!/usr/bin/env python

__author__ = 'XingHua'

"""

"""
import sys
from PyQt4 import QtCore, QtGui


class FindDialog(QtGui.QDialog):
    def __init__(self, parent=None):
        QtGui.QDialog.__init__(self, parent)

        self.label_layer = QtGui.QLabel(self.tr("  Layer  "))
        self.lineedit_layer = QtGui.QLineEdit()
        self.label_layer.setBuddy(self.lineedit_layer)

        self.label_field = QtGui.QLabel(self.tr("  Field  "))
        self.lineedit_field = QtGui.QLineEdit()
        self.label_field.setBuddy(self.lineedit_field)

        self.label = QtGui.QLabel(self.tr("  Find:  "))
        self.lineEdit = QtGui.QLineEdit()
        self.label.setBuddy(self.lineEdit)

        self.caseCheckBox = QtGui.QCheckBox(self.tr("Match &case"))
        self.fromStartCheckBox = QtGui.QCheckBox(self.tr("Search from &start"))
        self.fromStartCheckBox.setChecked(True)

        self.findButton = QtGui.QPushButton(self.tr("&Find"))
        self.findButton.setDefault(True)

        self.closeButton = QtGui.QPushButton(self.tr("Close"))

        self.moreButton = QtGui.QPushButton(self.tr("&More"))
        self.moreButton.setCheckable(True)
        self.moreButton.setAutoDefault(False)

        self.extension = QtGui.QWidget()

        self.wholeWordsCheckBox = QtGui.QCheckBox(self.tr("&Whole words"))
        self.backwardCheckBox = QtGui.QCheckBox(self.tr("Search &backward"))
        self.searchSelectionCheckBox = QtGui.QCheckBox(self.tr("Search se&lection"))

        self.connect(self.closeButton, QtCore.SIGNAL("clicked()"),
                     self, QtCore.SLOT("close()"))
        self.connect(self.moreButton, QtCore.SIGNAL("toggled(bool)"),
                     self.extension, QtCore.SLOT("setVisible(bool)"))

        extensionLayout = QtGui.QVBoxLayout()
        extensionLayout.setMargin(0)
        extensionLayout.addWidget(self.wholeWordsCheckBox)
        extensionLayout.addWidget(self.backwardCheckBox)
        extensionLayout.addWidget(self.searchSelectionCheckBox)
        self.extension.setLayout(extensionLayout)

        botLayout = QtGui.QHBoxLayout()
        midLayout = QtGui.QHBoxLayout()
        topLayout = QtGui.QHBoxLayout()

        botLayout.addWidget(self.label)
        botLayout.addWidget(self.lineEdit)

        topLayout.addWidget(self.label_layer)
        topLayout.addWidget(self.lineedit_layer)
        midLayout.addWidget(self.label_field)
        midLayout.addWidget(self.lineedit_field)


        leftLayout = QtGui.QVBoxLayout()
        leftLayout.addLayout(topLayout)
        leftLayout.addLayout(midLayout)
        leftLayout.addLayout(botLayout)
        leftLayout.addWidget(self.caseCheckBox)
        leftLayout.addWidget(self.fromStartCheckBox)
        leftLayout.addStretch(1)

        rightLayout = QtGui.QVBoxLayout()
        rightLayout.addWidget(self.findButton)
        rightLayout.addWidget(self.closeButton)
        rightLayout.addWidget(self.moreButton)
        rightLayout.addStretch(1)

        mainLayout = QtGui.QGridLayout()
        mainLayout.setSizeConstraint(QtGui.QLayout.SetFixedSize)
        mainLayout.addLayout(leftLayout, 0, 0)
        mainLayout.addLayout(rightLayout, 0, 1)
      #  mainLayout.addWidget(self.extension, 1, 0, 1, 2)
        self.setLayout(mainLayout)
        self.setWindowTitle(self.tr("Extension"))
        self.extension.hide()

if __name__=="__main__":
    qApp = QtGui.QApplication(sys.argv)
    aw = FindDialog()
    aw.show()
    sys.exit(qApp.exec_())