__author__ = 'XingHua'
# -*- coding: UTF-8 -*-
import sys
import IL_data_analysis_mainwindow

from PyQt4 import QtGui, uic

class MainWindow(QtGui.QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        uic.loadUi("mainWindow.ui", self)
app = QtGui.QApplication(sys.argv)
mainWindow = MainWindow()
mainWindow.show()
app.exec_()