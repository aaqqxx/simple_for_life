# coding:utf-8
#!/usr/bin/env python

__author__ = 'XingHua'

"""

"""

import re
from PyQt4 import QtGui
from PyQt4.QtCore import SIGNAL, SLOT, pyqtSignal
from ESS_energy_data_plot import *
from IL_base_plot_widget import base_2Dplot_Widget


class ESS_2D_line_plot_widget(QtGui.QWidget):
    def __init__(self, parent=None, filename="ESS_energy_data20141115_with_pianzhen_100Hz_25"):
        super(ESS_2D_line_plot_widget, self).__init__(parent)
        QtGui.QWidget.__init__(self, parent)
        # self.setGeometry(20, 120, 800, 600)
        self.filename = filename
        vspacer = QtGui.QSpacerItem(0, 40, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)

        self.axis_comboBox = QtGui.QComboBox()
        self.axis_comboBox.addItem("X")
        self.axis_comboBox.addItem("Y")
        self.coordinate_doubleSpinBox = QtGui.QDoubleSpinBox()
        self.label = QtGui.QLabel("mm")
        self.hlayout = QtGui.QHBoxLayout()
        self.hlayout.addItem(vspacer)
        self.hlayout.addWidget(self.axis_comboBox)
        self.hlayout.addWidget(self.coordinate_doubleSpinBox)
        self.hlayout.addWidget(self.label)
        self.plot_PBtn = QtGui.QPushButton("Plot")
        self.hlayout.addWidget(self.plot_PBtn)

        self.hlayout.setStretch(2, 1)
        self.hlayout.setStretch(0, 4)
        self.plot_area = base_2Dplot_Widget()
        self.vlayout = QtGui.QVBoxLayout()
        self.vlayout.addLayout(self.hlayout)
        self.vlayout.addWidget(self.plot_area)
        self.vlayout.setStretch(1, 1)

        self.left_widget = QtGui.QWidget()
        self.left_widget.setLayout(self.vlayout)

        self.Ophir_check_box = QtGui.QCheckBox("Ophir")
        self.EDU_check_box = QtGui.QCheckBox("EDU")
        self.BMU1_check_box = QtGui.QCheckBox("BMU1")
        # self.BMU2_check_box = QtGui.QCheckBox("BMU2")
        self.OE_check_box = QtGui.QCheckBox("OE")
        self.OB_check_box = QtGui.QCheckBox("OB")
        self.OE_check_box.setChecked(True)

        self.checkbox_widget = QtGui.QWidget()
        self.checkbox_layout = QtGui.QVBoxLayout()
        vspacer = QtGui.QSpacerItem(0, 300, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.checkbox_layout.addItem(vspacer)
        self.checkbox_layout.addWidget(self.OE_check_box)
        self.checkbox_layout.addWidget(self.Ophir_check_box)
        self.checkbox_layout.addWidget(self.EDU_check_box)
        self.checkbox_layout.addWidget(self.BMU1_check_box)
        # self.checkbox_layout.addWidget(self.BMU2_check_box)
        self.checkbox_layout.addWidget(self.OB_check_box)

        self.checkbox_list = []
        self.checkbox_list.append(self.OE_check_box)
        self.checkbox_list.append(self.Ophir_check_box)
        self.checkbox_list.append(self.EDU_check_box)
        self.checkbox_list.append(self.BMU1_check_box)
        self.checkbox_list.append(self.OB_check_box)
        for each in self.checkbox_list:
            self.connect(each, SIGNAL('stateChanged(int)'), self.update_plot)
        for each in self.checkbox_list[:3]:
            each.setChecked(True)
        self.checkbox_layout.addItem(vspacer)
        # vspacer.expandingDirections()

        self.checkbox_widget.setLayout(self.checkbox_layout)

        self.main_split = QtGui.QSplitter()

        self.main_split.addWidget(self.left_widget)
        self.main_split.addWidget(self.checkbox_widget)

        self.main_layout = QtGui.QHBoxLayout()
        self.main_layout.addWidget(self.main_split)

        self.setLayout(self.main_layout)
        if __name__ == "__main__":
            self.connect_sig_slot()

        self.x, self.y, self.z = [0, 1, 2], [2, 4, 9], [2, 2.2, 3]

    def connect_sig_slot(self):
        self.signal1 = pyqtSignal()
        self.signal2 = pyqtSignal(int, name="wokao")
        self.connect(self.plot_PBtn, SIGNAL("clicked()"), self.update_sig)
        # self.connect(self, SIGNAL("update_plot_sig"), self.update_plot)
        pass

    def init_data(self, filename):
        pass


    def get_plot_data(self, dir, value):
        pass

    def get_data_index(self):
        pass

    def update_sig(self):
        print "update sig"
        self.emit(SIGNAL("update_plot_sig"), self.x, self.y, self.z)

    def plot(self):
        # print "update plot\n", "x\n",x,"y\n", y,"z\n", OE
        self.plot_area.canvas.axes.clear()

        if unicode(self.axis_comboBox.currentText()) == "X":
            self.plot_area.axes.plot(self.Y, self.OE, label="OE")
            self.plot_area.axes.plot(self.Y, self.Ophir, label="Ophir")
            self.plot_area.axes.plot(self.Y, self.EDU, label="EDU")
            self.plot_area.axes.plot(self.Y, self.BMU1, label="BMU1")
            self.plot_area.axes.set_title(
                self.filename + "\n" + self.axis_comboBox.currentText() + "=" + str(self.X[0]))
            if self.OB.mean() <= 100:
                self.plot_area.axes.plot(self.Y, self.OB, label="OB")
            else:
                self.plot_area.axes.plot(self.Y, np.zeros(self.Y.size).reshape(self.Y.shape), label="OB")
        else:
            self.plot_area.axes.plot(self.X, self.OE, label="OE")
            self.plot_area.axes.plot(self.X, self.Ophir, label="Ophir")
            self.plot_area.axes.plot(self.X, self.EDU, label="EDU")
            self.plot_area.axes.plot(self.X, self.BMU1, label="BMU1")
            if self.OB.mean() <= 100:
                self.plot_area.axes.plot(self.X, self.OB, label="OB")
            else:
                self.plot_area.axes.plot(self.X, np.zeros(self.X.size).reshape(self.X.shape), label="OB")
            self.plot_area.axes.set_title(
                self.filename + "\n" + self.axis_comboBox.currentText() + "=" + str(self.Y[0]))
        self.plot_area.axes.legend()
        self.update_plot()
        self.plot_area.canvas.draw()
        pass

    def update_plot(self):
        print "in update plot !"
        max_list = []
        for index, each in enumerate(self.checkbox_list):
            if each.isChecked():
                # print "isChecked",index
                self.plot_area.axes.lines[index].set_visible(True)
                max_list.append(self.plot_area.axes.lines[index].get_ydata().max())
            else:
                self.plot_area.axes.lines[index].set_visible(False)
        self.plot_area.axes.set_ylim(0, max(max_list) * 1.1)
        self.plot_area.canvas.draw()
        pass


if __name__ == "__main__":
    print "@@"
    qApp = QtGui.QApplication(sys.argv)
    zz = ESS_2D_line_plot_widget()
    zz.show()
    sys.exit(qApp.exec_())

