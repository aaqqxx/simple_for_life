# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'IL_data_process.ui'
#
# Created: Tue Dec 09 13:54:00 2014
# by: PyQt4 UI code generator 4.9.6
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

try:
    _encoding = QtGui.QApplication.UnicodeUTF8

    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig)


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName(_fromUtf8("MainWindow"))
        MainWindow.resize(1190, 842)
        self.centralwidget = QtGui.QWidget(MainWindow)
        self.centralwidget.setObjectName(_fromUtf8("centralwidget"))
        self.verticalLayout = QtGui.QVBoxLayout(self.centralwidget)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.tabWidget = QtGui.QTabWidget(self.centralwidget)
        self.tabWidget.setBaseSize(QtCore.QSize(1000, 0))
        self.tabWidget.setObjectName(_fromUtf8("tabWidget"))
        self.tab = QtGui.QWidget()
        self.tab.setObjectName(_fromUtf8("tab"))
        self.tabWidget.addTab(self.tab, _fromUtf8(""))
        self.tab_2 = QtGui.QWidget()
        self.tab_2.setObjectName(_fromUtf8("tab_2"))
        self.comboBox = QtGui.QComboBox(self.tab_2)
        self.comboBox.setGeometry(QtCore.QRect(931, 91, 32, 20))
        self.comboBox.setObjectName(_fromUtf8("comboBox"))
        self.comboBox.addItem(_fromUtf8(""))
        self.comboBox.addItem(_fromUtf8(""))
        self.doubleSpinBox = QtGui.QDoubleSpinBox(self.tab_2)
        self.doubleSpinBox.setGeometry(QtCore.QRect(969, 91, 91, 20))
        self.doubleSpinBox.setObjectName(_fromUtf8("doubleSpinBox"))
        self.label = QtGui.QLabel(self.tab_2)
        self.label.setGeometry(QtCore.QRect(1068, 91, 16, 16))
        self.label.setObjectName(_fromUtf8("label"))
        self.tabWidget.addTab(self.tab_2, _fromUtf8(""))
        self.tab_3 = QtGui.QWidget()
        self.tab_3.setObjectName(_fromUtf8("tab_3"))
        self.widget_4 = QtGui.QWidget(self.tab_3)
        self.widget_4.setGeometry(QtCore.QRect(50, 100, 811, 591))
        self.widget_4.setObjectName(_fromUtf8("widget_4"))
        self.label_4 = QtGui.QLabel(self.tab_3)
        self.label_4.setGeometry(QtCore.QRect(70, 53, 16, 16))
        self.label_4.setObjectName(_fromUtf8("label_4"))
        self.label_3 = QtGui.QLabel(self.tab_3)
        self.label_3.setGeometry(QtCore.QRect(70, 27, 16, 16))
        self.label_3.setObjectName(_fromUtf8("label_3"))
        self.doubleSpinBox_3 = QtGui.QDoubleSpinBox(self.tab_3)
        self.doubleSpinBox_3.setGeometry(QtCore.QRect(100, 27, 81, 20))
        self.doubleSpinBox_3.setObjectName(_fromUtf8("doubleSpinBox_3"))
        self.label_2 = QtGui.QLabel(self.tab_3)
        self.label_2.setGeometry(QtCore.QRect(185, 27, 16, 16))
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.doubleSpinBox_4 = QtGui.QDoubleSpinBox(self.tab_3)
        self.doubleSpinBox_4.setGeometry(QtCore.QRect(100, 53, 81, 20))
        self.doubleSpinBox_4.setObjectName(_fromUtf8("doubleSpinBox_4"))
        self.label_5 = QtGui.QLabel(self.tab_3)
        self.label_5.setGeometry(QtCore.QRect(185, 53, 16, 16))
        self.label_5.setObjectName(_fromUtf8("label_5"))
        self.tabWidget.addTab(self.tab_3, _fromUtf8(""))
        self.tab_4 = QtGui.QWidget()
        self.tab_4.setObjectName(_fromUtf8("tab_4"))
        self.widget_3 = QtGui.QWidget(self.tab_4)
        self.widget_3.setGeometry(QtCore.QRect(80, 90, 651, 531))
        self.widget_3.setObjectName(_fromUtf8("widget_3"))
        self.tabWidget.addTab(self.tab_4, _fromUtf8(""))
        self.tab_5 = QtGui.QWidget()
        self.tab_5.setObjectName(_fromUtf8("tab_5"))
        self.tabWidget.addTab(self.tab_5, _fromUtf8(""))
        self.tab_6 = QtGui.QWidget()
        self.tab_6.setObjectName(_fromUtf8("tab_6"))
        self.tabWidget.addTab(self.tab_6, _fromUtf8(""))
        self.tab_7 = QtGui.QWidget()
        self.tab_7.setObjectName(_fromUtf8("tab_7"))
        self.tabWidget.addTab(self.tab_7, _fromUtf8(""))
        self.verticalLayout.addWidget(self.tabWidget)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtGui.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1190, 21))
        self.menubar.setObjectName(_fromUtf8("menubar"))
        self.menuFile = QtGui.QMenu(self.menubar)
        self.menuFile.setObjectName(_fromUtf8("menuFile"))
        self.menu_Tool = QtGui.QMenu(self.menubar)
        self.menu_Tool.setObjectName(_fromUtf8("menu_Tool"))
        self.menuHelp = QtGui.QMenu(self.menubar)
        self.menuHelp.setObjectName(_fromUtf8("menuHelp"))
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtGui.QStatusBar(MainWindow)
        self.statusbar.setObjectName(_fromUtf8("statusbar"))
        MainWindow.setStatusBar(self.statusbar)
        self.toolBar = QtGui.QToolBar(MainWindow)
        self.toolBar.setObjectName(_fromUtf8("toolBar"))
        MainWindow.addToolBar(QtCore.Qt.TopToolBarArea, self.toolBar)
        self.actionOpen = QtGui.QAction(MainWindow)
        self.actionOpen.setObjectName(_fromUtf8("actionOpen"))
        self.menuFile.addAction(self.actionOpen)
        self.menubar.addAction(self.menuFile.menuAction())
        self.menubar.addAction(self.menu_Tool.menuAction())
        self.menubar.addAction(self.menuHelp.menuAction())

        self.retranslateUi(MainWindow)
        self.tabWidget.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(_translate("MainWindow", "IL_Data_Process", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab), _translate("MainWindow", "ESS_3D_surface", None))
        self.comboBox.setItemText(0, _translate("MainWindow", "X", None))
        self.comboBox.setItemText(1, _translate("MainWindow", "Y", None))
        self.label.setText(_translate("MainWindow", "mm", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_2), _translate("MainWindow", "ESS_3D_line", None))
        self.label_4.setText(_translate("MainWindow", "Y", None))
        self.label_3.setText(_translate("MainWindow", "X", None))
        self.label_2.setText(_translate("MainWindow", "mm", None))
        self.label_5.setText(_translate("MainWindow", "mm", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_3), _translate("MainWindow", "ESS_2D_point", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_4), _translate("MainWindow", "Z_Scan_2D_line", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_5), _translate("MainWindow", "Z_Scan_2D_point", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_6), _translate("MainWindow", "VA_2D_line", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_7), _translate("MainWindow", "VA_2D_point", None))
        self.menuFile.setTitle(_translate("MainWindow", "File", None))
        self.menu_Tool.setTitle(_translate("MainWindow", "&Tool", None))
        self.menuHelp.setTitle(_translate("MainWindow", "Help", None))
        self.toolBar.setWindowTitle(_translate("MainWindow", "toolBar", None))
        self.actionOpen.setText(_translate("MainWindow", "Open", None))


import IL_data_process_rc
