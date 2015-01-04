# coding:utf-8
#!/usr/bin/env python

__author__ = 'XingHua'

"""

"""
# -*- coding: utf-8 -*-

import sys, os, random
from PyQt4 import QtGui, QtCore
from mpl_toolkits.mplot3d import Axes3D, axes3d
from matplotlib import cm

import numpy as np
from matplotlib.backends.backend_qt4agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
from matplotlib.animation import FuncAnimation
from NPulses_energy_plot import *
from ui_IL_data_process import Ui_MainWindow
from ESS_data_plot_widget import ESS_data_plot_widget
from IL_base_plot_widget import base_3Dplot_Widget, MyMplCanvas

from matplotlib.backends.backend_qt4agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt4agg import NavigationToolbar2QT as NavigationToolbar
from matplotlib.figure import Figure
# from mpl_toolkits.basemap import Basemap
from PyQt4 import QtGui
from ESS_2D_line_plot_widget import ESS_2D_line_plot_widget
from PyQt4.QtCore import SIGNAL, SLOT
from ESS_2D_point_plot_widget import ESS_2D_point_plot_widget
from VA_2D_line_plot_widget import VA_2D_line_plot_widget
from VA_2D_point_plot_widget import VA_2D_point_plot_widget

label_list = ["line_1", "line_2", "line_3"]


class AnimationWidget(QtGui.QWidget):
    def __init__(self, parent=None):
        QtGui.QWidget.__init__(self, parent)

        self.check_box_vbox = QtGui.QVBoxLayout()
        self.check_box_canv_hbox = QtGui.QHBoxLayout()

        vbox = QtGui.QVBoxLayout()
        self.canvas = MyMplCanvas(self, width=5, height=4, dpi=100)
        self.mpl_toolbar = NavigationToolbar(self.canvas, self)

        self.first_show()

        self.check_box_list = []

        self.Ophir_check_box = QtGui.QCheckBox("Ophir")
        self.EDU_check_box = QtGui.QCheckBox("EDU")
        self.BMU1_check_box = QtGui.QCheckBox("BMU1")
        self.BMU2_check_box = QtGui.QCheckBox("BMU2")
        self.OE_check_box = QtGui.QCheckBox("OE")

        self.ini_checkbox()
        # self.check_box.setInputContext("2")

        self.hbox = QtGui.QHBoxLayout()
        self.start_button = QtGui.QPushButton("Show All", self)
        self.stop_button = QtGui.QPushButton("Clear", self)
        self.start_button.clicked.connect(self.on_start)
        self.stop_button.clicked.connect(self.on_stop)
        self.hbox.addWidget(self.start_button)
        self.hbox.addWidget(self.stop_button)

        self.hbox.addWidget(self.Ophir_check_box)
        self.hbox.addWidget(self.EDU_check_box)
        self.hbox.addWidget(self.BMU1_check_box)
        self.hbox.addWidget(self.BMU2_check_box)
        self.hbox.addWidget(self.OE_check_box)

        self.scrollArea = QtGui.QScrollArea(self)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Ignored, QtGui.QSizePolicy.Ignored)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        # sizePolicy.setHeightForWidth(self.scrollArea.sizePolicy().hasHeightForWidth())
        self.scrollArea.setSizePolicy(sizePolicy)
        # self.scrollArea.setAutoFillBackground(True)
        # self.scrollArea.setStyleSheet("border: 1px solid blue")
        self.scrollArea.setWidgetResizable(True)
        self.scrollArea.setObjectName("scrollArea")
        self.gridLayoutWidget = QtGui.QWidget()
        # self.gridLayoutWidget.setGeometry(QtCore.QRect(0, 0, 667, 551))
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Ignored, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.gridLayoutWidget.sizePolicy().hasHeightForWidth())
        self.gridLayoutWidget.setSizePolicy(sizePolicy)
        self.gridLayoutWidget.setLayoutDirection(QtCore.Qt.LeftToRight)
        # self.gridLayoutWidget.setAutoFillBackground(True)
        # self.gridLayoutWidget.setStyleSheet("border: 1px solid red")
        # self.gridLayoutWidget.setObjectName("gridLayoutWidget")
        self.gridLayoutWidget.setLayout(self.check_box_vbox)
        self.scrollArea.setWidget(self.gridLayoutWidget)

        self.horizontal_splitter = QtGui.QSplitter()
        self.horizontal_splitter.addWidget(self.scrollArea)
        self.horizontal_splitter.addWidget(self.canvas)

        self.check_box_canv_hbox.addWidget(self.scrollArea)
        self.check_box_canv_hbox.addWidget(self.canvas)
        self.check_box_canv_hbox.setStretch(0, 1)
        self.check_box_canv_hbox.setStretch(1, 10)
        # self.check_box_canv_hbox.addStretch()

        vbox.addWidget(self.mpl_toolbar)
        vbox.addWidget(self.horizontal_splitter)
        vbox.addLayout(self.hbox)
        self.setLayout(vbox)

        self.x = np.linspace(0, 5 * np.pi, 400)
        self.p = 0.0
        self.y = np.sin(self.x + self.p)
        # self.line, = self.canvas.axes.plot(self.x, self.y, animated=True, lw=2)

        self.visable_line = []
        print len(self.check_box_list)

        for each in self.check_box_list:
            self.connect(each, QtCore.SIGNAL('stateChanged(int)'), self.set_visable_line)

        self.connect(self.Ophir_check_box, QtCore.SIGNAL('stateChanged(int)'), self.set_visable_line)
        self.connect(self.EDU_check_box, QtCore.SIGNAL('stateChanged(int)'), self.set_visable_line)
        self.connect(self.BMU1_check_box, QtCore.SIGNAL('stateChanged(int)'), self.set_visable_line)
        self.connect(self.BMU2_check_box, QtCore.SIGNAL('stateChanged(int)'), self.set_visable_line)
        self.connect(self.OE_check_box, QtCore.SIGNAL('stateChanged(int)'), self.set_visable_line)

        self.canvas.draw()


    def ini_checkbox(self):
        for index, each in enumerate(self.line_labels):
            self.check_box_list.append(QtGui.QCheckBox(each))
            self.check_box_vbox.addWidget(self.check_box_list[index])
        pass

    def update_line(self, i):
        self.p += 0.1
        y = np.sin(self.x + self.p)
        self.line.set_ydata(y)
        return [self.line]

    def set_visable_line(self, i):
        self.visable_line = []
        self.canvas.axes.clear()
        for index, each in enumerate(self.check_box_list):
            print index, each.isChecked()
            if each.isChecked():
                if self.Ophir_check_box.isChecked():
                    self.visable_line.append(self.canvas.axes.plot(self.sdata.data[index].raw_Ophir,
                                                                   label=self.line_labels[index] + "_Ophir",
                                                                   visible=True)[0])
                if self.EDU_check_box.isChecked():
                    self.visable_line.append(
                        self.canvas.axes.plot(self.sdata.data[index].raw_EDU, label=self.line_labels[index] + "_EDU",
                                              visible=True)[0])
                if self.BMU1_check_box.isChecked():
                    self.visable_line.append(
                        self.canvas.axes.plot(self.sdata.data[index].raw_BMU1, label=self.line_labels[index] + "_BMU1",
                                              visible=True)[0])
                if self.BMU2_check_box.isChecked():
                    self.visable_line.append(
                        self.canvas.axes.plot(self.sdata.data[index].raw_BMU2, label=self.line_labels[index] + "_BMU2",
                                              visible=True)[0])
                if self.OE_check_box.isChecked():
                    self.visable_line.append(self.canvas.axes.plot(
                        np.array(self.sdata.data[index].raw_Ophir) / np.array(self.sdata.data[index].raw_EDU),
                        label=self.line_labels[index] + "_OE", visible=True)[0])
        # self.canvas.axes.legend()
        # plt.figlegend(self.canvas.axes.get_lines(),label_list,"upper right")
        self.canvas.draw()
        return self.visable_line

    def on_start(self):
        # self.ani = FuncAnimation(self.canvas.figure, self.set_visable_line,
        # blit=True, interval=1)
        for each in self.check_box_list:
            each.setChecked(True)

        self.EDU_check_box.setChecked(True)
        self.Ophir_check_box.setChecked(True)
        self.BMU1_check_box.setChecked(True)
        self.BMU2_check_box.setChecked(True)
        self.OE_check_box.setChecked(True)
        # x = QtGui.QInputContext("2")
        # self.check_box.setInputContext(self.tr("&Whole words"))
        # plt.plot(self.sdata.get_surface_data("x",0))
        # plt.show()

    def first_show(self):
        sdata = Scanning_params_data_struct()
        sdata.init_data(filename)
        sdata.data.sort(cmp_data_point_pos)

        sdata.skip_first_N_pulses(0)
        # sdata.outlier_rejection()

        scan_param = get_scan_param(filename)

        X = []
        Y = []
        Z = []

        for each in sdata.data:
            X.append(each.pos[0])
            Y.append(each.pos[1])
            Z.append(each.pos[2])

        main_labels = ['Pos_' + str(x) + "_" + str(y) for x in X for y in Y]
        labels = ['Pos_' + str(x) + "_" + str(y) + "_" + name for x in X for y in Y for name in
                  ["Ophir", "EDU", "BMU1", "BMU2"]]
        self.line_labels = main_labels[:max(sdata.X_cnt, sdata.Y_cnt)]
        # visiable_status = []
        #
        # for x in X:
        # for y in Y:
        # for name in ["Ophir", "EDU", "BMU1", "BMU2"]:
        # visiable_status.append(False)

        self.sdata = sdata


    def on_stop(self):
        # self.ani._stop()
        self.canvas.axes.clear()
        self.canvas.draw()
        for each in self.check_box_list:
            # self.EDU_check_box.setChecked()
            each.setChecked(False)
        self.EDU_check_box.setChecked(False)
        self.Ophir_check_box.setChecked(False)
        self.BMU1_check_box.setChecked(False)
        self.BMU2_check_box.setChecked(False)
        self.OE_check_box.setChecked(False)


class IL_data_process_MainWindow(Ui_MainWindow):
    def __init__(self, parent=None):
        super(IL_data_process_MainWindow, self).__init__()
        self.setupUi(parent)
        self.mpl_widget = AnimationWidget()
        # self.mpl_widget1 = ESS_3Dplot_Widget(self.widget_5)
        # self.mpl_widget2 = ESS_3Dplot_Widget(self.widget)
        print "before"
        self.hlayout = QtGui.QHBoxLayout()
        self.ESS_2D_point_widget = ESS_2D_point_plot_widget()
        self.hlayout.addWidget(self.ESS_2D_point_widget)
        self.tab_3.setLayout(self.hlayout)
        # self.mpl_widget2 = ESS_2D_line_plot_widget()
        print "after"
        # self.hlayout = QtGui.QHBoxLayout(self.centralwidget)
        # self.hlayout.addChildWidget(self.treeWidget)
        # self.hlayout.addChildWidget(self.tabWidget)
        # self.centralwidget.setLayout(self.hlayout)
        # self.widget.set
        # self.tab_2.setl

        self.hlayout = QtGui.QHBoxLayout()
        # print "**"*50,dir(self.tab)

        self.ESS_3d_wireframe_widget = ESS_data_plot_widget()
        self.hlayout.addWidget(self.ESS_3d_wireframe_widget)
        self.tab.setLayout(self.hlayout)

        self.ESS_2D_line_widget = ESS_2D_line_plot_widget()

        hlayout = QtGui.QHBoxLayout()
        hlayout.addWidget(self.ESS_2D_line_widget)
        self.tab_2.setLayout(hlayout)

        # self.tabWidget.addTab(self.mpl_widget, "2D")

        hlayout = QtGui.QHBoxLayout()
        self.VA_2D_line_widget = VA_2D_line_plot_widget()
        hlayout.addWidget(self.VA_2D_line_widget)
        self.tab_6.setLayout(hlayout)

        hlayout = QtGui.QHBoxLayout()
        self.VA_2D_point_widget = VA_2D_point_plot_widget()
        hlayout.addWidget(self.VA_2D_point_widget)
        self.tab_7.setLayout(hlayout)

        # self.tab_4.hide()
        # self.tab_5.hide()
        # self.tab_7.close()
        self.init_sig_slot()


    def init_ESS_2D_line_widget_data(self, filename=''):
        print "in main window"
        if self.ESS_2D_line_widget.axis_comboBox.currentText() == "X":
            x_index = self.get_x_index(self.ESS_2D_line_widget.coordinate_doubleSpinBox.value())
            self.ESS_2D_line_widget.X = self.ESS_3d_wireframe_widget.X[:, x_index]
            self.ESS_2D_line_widget.Y = self.ESS_3d_wireframe_widget.Y[:, x_index]
            self.ESS_2D_line_widget.OE = self.ESS_3d_wireframe_widget.raw_OE_avg_list[:, x_index]
            self.ESS_2D_line_widget.Ophir = self.ESS_3d_wireframe_widget.raw_Ophir_avg_list[:, x_index]
            self.ESS_2D_line_widget.EDU = self.ESS_3d_wireframe_widget.raw_EDU_avg_list[:, x_index]
            self.ESS_2D_line_widget.BMU1 = self.ESS_3d_wireframe_widget.raw_BMU1_avg_list[:, x_index]
            self.ESS_2D_line_widget.OB = self.ESS_3d_wireframe_widget.raw_OB_avg_list[:, x_index]

        else:
            y_index = self.get_y_index(self.ESS_2D_line_widget.coordinate_doubleSpinBox.value())
            self.ESS_2D_line_widget.X = self.ESS_3d_wireframe_widget.X[y_index]
            self.ESS_2D_line_widget.Y = self.ESS_3d_wireframe_widget.Y[y_index]
            self.ESS_2D_line_widget.OE = self.ESS_3d_wireframe_widget.raw_OE_avg_list[y_index]
            self.ESS_2D_line_widget.Ophir = self.ESS_3d_wireframe_widget.raw_Ophir_avg_list[y_index]
            self.ESS_2D_line_widget.EDU = self.ESS_3d_wireframe_widget.raw_EDU_avg_list[y_index]
            self.ESS_2D_line_widget.BMU1 = self.ESS_3d_wireframe_widget.raw_BMU1_avg_list[y_index]
            self.ESS_2D_line_widget.OB = self.ESS_3d_wireframe_widget.raw_BMU2_avg_list[y_index]

        self.ESS_2D_line_widget.plot()

        # if self.ESS_2D_line_widget.axis_comboBox.currentText() == "X":
        # x_index = self.get_x_index(self.ESS_2D_line_widget.coordinate_doubleSpinBox.value())
        #     self.ESS_2D_line_widget.update_plot(self.ESS_3d_wireframe_widget.X[:,x_index],
        #                                         self.ESS_3d_wireframe_widget.Y[:,x_index],
        #                                         self.ESS_3d_wireframe_widget.raw_Ophir_avg_list[:,x_index])
        #
        # else:
        #     print "Y shape ",self.ESS_3d_wireframe_widget.Y.shape
        #     print self.ESS_3d_wireframe_widget.X
        #     print self.ESS_3d_wireframe_widget.Y
        #     y_index = self.get_y_index(self.ESS_2D_line_widget.coordinate_doubleSpinBox.value())
        #     self.ESS_2D_line_widget.update_plot(self.ESS_3d_wireframe_widget.X[0],
        #                                         self.ESS_3d_wireframe_widget.Y[y_index],
        #                                         self.ESS_3d_wireframe_widget.raw_Ophir_avg_list[y_index])
        pass

    def init_ESS_2D_point_widget_data(self):
        x = self.ESS_2D_point_widget.x_coordinate_doubleSpinBox.value()
        y = self.ESS_2D_point_widget.y_coordinate_doubleSpinBox.value()
        z = 90

        self.ESS_2D_point_widget.Ophir = np.array(
            self.ESS_3d_wireframe_widget.sdata_info.get_point_data([x, y, z]).raw_Ophir)
        self.ESS_2D_point_widget.EDU = np.array(
            self.ESS_3d_wireframe_widget.sdata_info.get_point_data([x, y, z]).raw_EDU)
        self.ESS_2D_point_widget.BMU1 = np.array(
            self.ESS_3d_wireframe_widget.sdata_info.get_point_data([x, y, z]).raw_BMU1)
        self.ESS_2D_point_widget.OE = self.ESS_2D_point_widget.Ophir / self.ESS_2D_point_widget.EDU
        self.ESS_2D_point_widget.OB = self.ESS_2D_point_widget.Ophir / self.ESS_2D_point_widget.BMU1

        self.ESS_2D_point_widget.plot()
        pass

    def init_VA_2D_point_widget_data(self):
        x = 0
        y = 0
        angle = self.VA_2D_point_widget.angle_coordinate_doubleSpinBox.value()

        self.VA_2D_point_widget.Ophir = np.array(
            self.VA_2D_line_widget.sdata_info.get_point_data([x, y, angle]).raw_Ophir)
        self.VA_2D_point_widget.EDU = np.array(self.VA_2D_line_widget.sdata_info.get_point_data([x, y, angle]).raw_EDU)
        self.VA_2D_point_widget.BMU1 = np.array(
            self.VA_2D_line_widget.sdata_info.get_point_data([x, y, angle]).raw_BMU1)
        self.VA_2D_point_widget.OE = self.VA_2D_point_widget.Ophir / self.VA_2D_point_widget.EDU
        self.VA_2D_point_widget.OB = self.VA_2D_point_widget.Ophir / self.VA_2D_point_widget.BMU1

        self.VA_2D_point_widget.plot()
        pass

    def get_x_index(self, x):
        # print self.ESS_3d_wireframe_widget.sdata_info.X_start_position
        # print self.ESS_3d_wireframe_widget.sdata_info.X_end_position
        # print self.ESS_3d_wireframe_widget.sdata_info.X_step
        # print self.ESS_3d_wireframe_widget.sdata_info.X_start_position
        # print self.ESS_3d_wireframe_widget.sdata_info.X_start_position
        # print "x=",x,"x_start = ",self.ESS_3d_wireframe_widget.sdata_info.X_start_position,"x_step=",self.ESS_3d_wireframe_widget.sdata_info.X_step
        # print self.ESS_3d_wireframe_widget.X[0][0]
        # 选择按从小到大排序后的，X坐标的最小值作为起点，获取x_index
        index = np.abs((x - self.ESS_3d_wireframe_widget.X[0][0]) / self.ESS_3d_wireframe_widget.sdata_info.X_step)
        print "get_x_index=", index
        return index
        pass

    def get_y_index(self, y):
        # print self.ESS_3d_wireframe_widget.sdata_info.Y_start_position
        # print self.ESS_3d_wireframe_widget.sdata_info.Y_end_position
        # print self.ESS_3d_wireframe_widget.sdata_info.Y_step
        # 选择按从小到大排序后的，Y坐标的最小值作为起点，获取y_index
        index = (y - self.ESS_3d_wireframe_widget.Y[0][0]) / self.ESS_3d_wireframe_widget.sdata_info.Y_step
        print "get_y_index", index
        return index
        pass

    def init_sig_slot(self):
        self.centralwidget.connect(self.ESS_2D_line_widget.plot_PBtn, SIGNAL("clicked()"),
                                   self.init_ESS_2D_line_widget_data)
        self.centralwidget.connect(self.ESS_2D_point_widget.plot_PBtn, SIGNAL("clicked()"),
                                   self.init_ESS_2D_point_widget_data)

        self.ESS_2D_line_widget.connect_sig_slot()
        self.ESS_2D_point_widget.connect_sig_slot()

        self.centralwidget.connect(self.VA_2D_point_widget.plot_PBtn, SIGNAL("clicked()"),
                                   self.init_VA_2D_point_widget_data)
        # def


class test_MainWindow(QtGui.QMainWindow):
    def __init__(self):
        # ...
        # Creating tabs and using tab widget as a Central widget

        self.tabs = QtGui.QTabWidget()
        self.tabs.TabShape(QtGui.QTabWidget.Rounded)
        self.tabs.addTab(self.basicMode(), "Basic")  # index = 0
        self.tabs.addTab(self.bulbMode(), "Bulb")  # index = 1
        self.tabs.addTab(self.timedMode(), "Timed")  # index = 2
        self.tabs.addTab(self.viewerMode(), "Viewer")  # index = 3
        self.tabs.addTab(self.systemMode(), "System")  # index = 4

        self.setCentralWidget(self.tabs)
        # ...
        self.tabVisibility()
        # ...

    def tabVisibility(self):
        count = self.tabs.count()  # Number of tabs, used for failsafe!
        # if USEFULLSCREEN != True and count == 5: # Removing systemMode if not fullscreen
        # self.tabs.removeTab(count-1)
        #
        # if CURRENT_REMOTETYPE == "Olympus_RM-1" and USEFULLSCREEN == True and count < 5: # Includes Viewer tab, only if it is not there!
        # self.tabs.removeTab((count-1))
        #     self.tabs.addTab(self.viewerMode(), "Viewer")
        #     self.tabs.addTab(self.systemMode(), "System")
        #
        # elif CURRENT_REMOTETYPE == "Olympus_RM-1" and USEFULLSCREEN != True and count == 3: # Includes Viewer tab, only if it is not there!
        #     self.tabs.addTab(self.viewerMode(), "Viewer")
        #
        # elif CURRENT_REMOTETYPE != "Olympus_RM-1" and count == 5:
        #     self.tabs.removeTab(3)

    def settingsDialog(self):
        # ...
        pass

    def setSettings(self):
        # ...
        # self.tabVisibility() # Handling visibility of tabs
        # settings.sync()
        # self.dialog.accept()
        pass


class SettingsDialog(QtGui.QDialog):
    def setSettings(self):
        # ...
        # MainWindow().tabHandler("settings")
        # settings.sync()
        #
        # self.accept()
        pass


if __name__ == "__main__":
    qApp = QtGui.QApplication(sys.argv)
    filename = r"./ESS_energy_data20141020_4"
    # aw = AnimationWidget(filename)
    # aw.show()

    a = QtGui.QMainWindow()
    xx = IL_data_process_MainWindow(a)
    # xx.setupUi(a)
    a.show()

    # xx = IL_data_process_MainWindow()
    # xx.show()
    sys.exit(qApp.exec_())