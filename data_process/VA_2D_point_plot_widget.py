# coding:utf-8
#!/usr/bin/env python

__author__ = 'XingHua'

"""
数据由外界先赋值完毕，然后调用plot或者update_plot，进行绘制。
"""

from PyQt4 import QtGui
from PyQt4.QtCore import SIGNAL, SLOT, pyqtSignal
from ESS_energy_data_plot import *
from IL_base_plot_widget import base_2Dplot_Widget


class VA_2D_point_plot_widget(QtGui.QWidget):
    def __init__(self, parent=None, filename="ESS_energy_data20141115_with_pianzhen_100Hz_25"):
        super(VA_2D_point_plot_widget, self).__init__(parent)
        QtGui.QWidget.__init__(self, parent)
        # self.setGeometry(20, 120, 800, 600)
        self.filename = filename
        vspacer = QtGui.QSpacerItem(0, 40, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        hspacer = QtGui.QSpacerItem(0, 40, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding, )

        # self.x_label = QtGui.QLabel("X(mm):")
        # self.y_label = QtGui.QLabel("Y(mm):")
        self.z_label = QtGui.QLabel("Angle(degree):")
        # self.x_coordinate_doubleSpinBox = QtGui.QDoubleSpinBox()
        # self.y_coordinate_doubleSpinBox = QtGui.QDoubleSpinBox()
        self.angle_coordinate_doubleSpinBox = QtGui.QDoubleSpinBox()
        # self.x_coordinate_doubleSpinBox.setMinimum(-100)
        # self.y_coordinate_doubleSpinBox.setMinimum(-100)
        # self.z_coordinate_doubleSpinBox.setMinimum(-100)
        self.angle_coordinate_doubleSpinBox.setValue(90)
        self.glayout = QtGui.QGridLayout()
        # self.glayout.addWidget(self.x_label, 0, 0)
        # self.glayout.addWidget(self.x_coordinate_doubleSpinBox, 0, 1)
        # self.glayout.addWidget(self.y_label, 1, 0)
        # self.glayout.addWidget(self.y_coordinate_doubleSpinBox, 1, 1)
        self.glayout.addWidget(self.z_label, 2, 0)
        self.glayout.addWidget(self.angle_coordinate_doubleSpinBox, 2, 1)

        self.glayout.setColumnStretch(0, 1)
        self.glayout.setColumnStretch(1, 2)

        self.hlayout = QtGui.QHBoxLayout()
        self.hlayout.addItem(hspacer)

        self.plot_PBtn = QtGui.QPushButton("Plot")
        self.hlayout.addLayout(self.glayout)
        self.hlayout.addWidget(self.plot_PBtn)

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
        self.emit(SIGNAL("update_plot_sig"))

    def plot(self):
        # print "update plot\n", "x\n",x,"y\n", y,"z\n", OE
        self.plot_area.canvas.axes.clear()
        self.plot_area.axes.plot(self.OE, label="OE")
        self.plot_area.axes.plot(self.Ophir, label="Ophir")
        self.plot_area.axes.plot(self.EDU, label="EDU")
        self.plot_area.axes.plot(self.BMU1, label="BMU1")

        if self.OB.mean() <= 100:
            self.plot_area.axes.plot(self.OB, label="OB")
        else:
            self.plot_area.axes.plot(np.zeros(self.BMU1.size).reshape(self.BMU1.shape), label="OB")

        self.plot_area.axes.set_title(
            self.filename + "\nangle=" + str(
                self.angle_coordinate_doubleSpinBox.value()))
        self.plot_area.axes.legend()
        self.update_plot()
        self.plot_area.canvas.draw()
        pass

    def update_plot(self):
        print "in update plot !"
        max_list = []
        for index, each in enumerate(self.checkbox_list):
            if len(self.plot_area.axes.lines) != 0:
                if each.isChecked():
                    # print "isChecked",index
                    self.plot_area.axes.lines[index].set_visible(True)
                    max_list.append(self.plot_area.axes.lines[index].get_ydata().max())
                else:
                    self.plot_area.axes.lines[index].set_visible(False)
        if len(max_list) > 0:
            self.plot_area.axes.set_ylim(0, max(max_list) * 1.1)
        self.plot_area.canvas.draw()
        pass


if __name__ == "__main__":
    print "@@"
    qApp = QtGui.QApplication(sys.argv)
    zz = VA_2D_point_plot_widget()
    zz.show()
    sys.exit(qApp.exec_())