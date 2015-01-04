# coding:utf-8
#!/usr/bin/env python

__author__ = 'XingHua'

"""

"""

import sys, os, random
from PyQt4 import QtGui, QtCore
from mpl_toolkits.mplot3d import Axes3D, axes3d

import re
from PyQt4 import QtGui
from PyQt4.QtCore import SIGNAL, SLOT
from ESS_energy_data_plot import *

from IL_base_plot_widget import base_2Dplot_Widget

import logging

logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',
                    datefmt='%a, %d %b %Y %H:%M:%S',
                    filename='ESS_data_plot_widget.log',
                    filemode='w')

logging.debug('This is debug message')
logging.info('This is info message')
logging.warning('This is warning message')


class VA_2D_line_plot_widget(QtGui.QWidget):
    def __init__(self, parent=None, filename="VA_scanning_data20141115_with_pianzhen_4"):
        super(VA_2D_line_plot_widget, self).__init__(parent)
        QtGui.QWidget.__init__(self, parent)
        # self.setGeometry(20, 120, 800, 600)
        self.file_label = QtGui.QLabel("File name:")

        self.file_name_comboBox = QtGui.QComboBox()
        self.file_name_comboBox.addItem("VA_scanning_data20141115_with_pianzhen_4")
        self.file_name_comboBox.setEditable(True)
        self.plot_PBtn = QtGui.QPushButton("Plot")
        self.browse_PBtn = QtGui.QPushButton("Browse")
        self.plot_area = base_2Dplot_Widget()

        self.hlayout = QtGui.QHBoxLayout()
        self.hlayout.addWidget(self.file_label)
        self.hlayout.addWidget(self.file_name_comboBox)
        self.hlayout.addWidget(self.browse_PBtn)
        self.hlayout.addWidget(self.plot_PBtn)
        self.hlayout.setStretch(1, 2)
        # self.hlayout.setMargin(10)

        self.right_layout = QtGui.QVBoxLayout()
        self.right_layout.addLayout(self.hlayout)
        self.right_layout.addWidget(self.plot_area)

        self.left_layout = QtGui.QVBoxLayout()
        # space = QtGui.QSpacerItem()
        label = QtGui.QLabel("Scan param:")
        # self.left_layout.addLayout(space)
        self.left_layout.addWidget(label)
        self.scan_info_LEdit = QtGui.QTextEdit()
        self.left_layout.addWidget(self.scan_info_LEdit)
        label = QtGui.QLabel("Data report:")
        self.left_layout.addWidget(label)
        self.data_report = QtGui.QTextEdit()
        self.left_layout.addWidget(self.data_report)

        self.left_widget = QtGui.QWidget()
        self.left_widget.setLayout(self.left_layout)
        self.right_widget = QtGui.QWidget()
        self.right_widget.setLayout(self.right_layout)

        self.filename = self.file_name_comboBox.currentText()

        self.Ophir_check_box = QtGui.QCheckBox("Ophir")
        self.EDU_check_box = QtGui.QCheckBox("EDU")
        self.BMU1_check_box = QtGui.QCheckBox("BMU1")
        # self.BMU2_check_box = QtGui.QCheckBox("BMU2")
        self.OE_check_box = QtGui.QCheckBox("OE")
        self.OB_check_box = QtGui.QCheckBox("OB")
        self.OE_check_box.setChecked(True)

        self.checkbox_widget = QtGui.QWidget()
        self.checkbox_layout = QtGui.QVBoxLayout()
        vspacer = QtGui.QSpacerItem(40, 300, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.checkbox_layout.addItem(vspacer)
        self.checkbox_layout.addWidget(self.OE_check_box)
        self.checkbox_layout.addWidget(self.Ophir_check_box)
        self.checkbox_layout.addWidget(self.EDU_check_box)
        self.checkbox_layout.addWidget(self.BMU1_check_box)
        # self.checkbox_layout.addWidget(self.BMU2_check_box)
        self.checkbox_layout.addWidget(self.OB_check_box)

        self.checkbox_layout.addItem(vspacer)
        self.checkbox_widget.setLayout(self.checkbox_layout)

        self.hsplitter = QtGui.QSplitter()
        self.hsplitter.addWidget(self.left_widget)
        self.hsplitter.addWidget(self.right_widget)
        self.hsplitter.addWidget(self.checkbox_widget)

        self.main_layout = QtGui.QHBoxLayout()
        self.main_layout.addWidget(self.hsplitter)

        self.setLayout(self.main_layout)
        self.connect_sig_slot()
        self.plot()
        pass

    def connect_sig_slot(self):
        self.connect(self.browse_PBtn, SIGNAL("clicked()"), self.browse)
        self.connect(self.plot_PBtn, SIGNAL("clicked()"), self.plot)

        self.connect(self.OE_check_box, SIGNAL("clicked()"), self.update_plot)
        self.connect(self.OB_check_box, SIGNAL("clicked()"), self.update_plot)
        self.connect(self.Ophir_check_box, SIGNAL("clicked()"), self.update_plot)
        self.connect(self.EDU_check_box, SIGNAL("clicked()"), self.update_plot)
        self.connect(self.BMU1_check_box, SIGNAL("clicked()"), self.update_plot)
        # self.connect(self.BMU2_check_box,SIGNAL("clicked()"),self.update_plot)
        pass

    def init_dat(self):
        pass

    def update_plot(self):
        # print self.filename
        # print "self.EDU_check_box.isChecked() is", self.EDU_check_box.isChecked()
        visible_lines_list = []
        max_value_list = []
        unit_lines_dict = {"EDU": self.EDU_line, "Ophir": self.Ophir_line, "BMU1": self.BMU1_line, "OB": self.OB_line,
                           "OE": self.OE_line}
        if self.OE_check_box.isChecked():
            visible_lines_list.append("OE")
            max_value_list.append(self.OE.max())
        if self.OB_check_box.isChecked():
            visible_lines_list.append("OB")
            max_value_list.append(self.OB.max())
        if self.Ophir_check_box.isChecked():
            visible_lines_list.append("Ophir")
            max_value_list.append(self.Ophir.max())
        if self.BMU1_check_box.isChecked():
            visible_lines_list.append("BMU1")
            max_value_list.append(self.BMU1.max())
        if self.EDU_check_box.isChecked():
            visible_lines_list.append("EDU")
            max_value_list.append(self.EDU.max())

        for each in unit_lines_dict:
            unit_lines_dict[each].set_visible(False)

        for each in visible_lines_list:
            unit_lines_dict[each].set_visible(True)
            # for e in dir(unit_dict[each]):
            # print e
            # for e in dir(self.plot_area.axes):
            # print e
        if len(max_value_list):
            # print "max value list = ",max_value_list
            y_max = max(max_value_list)
            self.plot_area.axes.set_ylim(0, y_max * 1.1)
        # self.plot_area.axes.update_datalim()
        self.plot_area.canvas.draw()

        pass

    def plot(self):
        self.plot_area.canvas.axes.clear()
        filename = unicode(self.filename)
        print "plotting", self.filename
        self.display_scan_info()
        sdata = Scanning_params_data_struct()
        sdata.init_data(filename)
        sdata.data.sort(cmp_data_point_pos)

        sdata.skip_first_N_pulses(0)
        # sdata.outlier_rejection()

        # point_data = sdata.get_point_data([-56, 5, 0])
        # print "point_data is", point_data.raw_Ophir
        self.sdata_info = sdata

        # 所有位置处,Z方向目前不做处理。。。。。仅关心X，Y坐标。
        # X=[]
        # Y=[]
        # Z=[]
        raw_Ophir_avg_list = []
        raw_EDU_avg_list = []
        raw_BMU1_avg_list = []
        raw_BMU2_avg_list = []
        raw_OE_avg_list = []

        processed_Ophir_avg_list = []
        processed_EDU_avg_list = []
        processed_BMU1_avg_list = []
        processed_BMU2_avg_list = []
        processed_OE_avg_list = []


        # 某位置处的Ophir,EDU,BMU1,BMU2,OE的能量列表。
        raw_Ophir_list = []
        raw_EDU_list = []
        raw_BMU1_list = []
        raw_BMU2_list = []
        raw_OE_list = []

        processed_Ophir_list = []
        processed_EDU_list = []
        processed_BMU1_list = []
        processed_BMU2_list = []
        processed_OE_list = []

        X = []
        Y = []
        Z = []

        print sdata.data[0].pos, len(sdata.data), sdata.data[0].pos[0], dir(sdata.data[0])

        for each in sdata.data:
            X.append(each.pos[0])
            Y.append(each.pos[1])
            Z.append(each.pos[2])

            raw_Ophir_avg_list.append(each.get_raw_Ophir_avg())
            raw_EDU_avg_list.append(each.get_raw_EDU_avg())
            raw_BMU1_avg_list.append(each.get_raw_BMU1_avg())
            raw_BMU2_avg_list.append(each.get_raw_BMU2_avg())

            raw_OE_avg_list.append(each.get_raw_Ophir_avg() / each.get_raw_EDU_avg())

            processed_Ophir_avg_list.append(each.get_processed_Ophir_avg())
            processed_EDU_avg_list.append(each.get_processed_EDU_avg())
            processed_BMU1_avg_list.append(each.get_processed_BMU1_avg())
            processed_BMU2_avg_list.append(each.get_processed_BMU2_avg())
            processed_OE_avg_list.append(each.get_processed_Ophir_avg() / each.get_processed_EDU_avg())

        print "@@", sdata.data[-1].raw_Ophir

        X = np.array(X)
        Y = np.array(Y)
        Z = np.array(Z)

        raw_Ophir_avg_list = np.array(raw_Ophir_avg_list)
        processed_Ophir_avg_list = np.array(processed_Ophir_avg_list)
        raw_EDU_avg_list = np.array(raw_EDU_avg_list)
        raw_OE_avg_list = np.array(raw_OE_avg_list)
        raw_BMU1_avg_list = np.array(raw_BMU1_avg_list)
        processed_OE_avg_list = np.array(processed_OE_avg_list)
        processed_EDU_avg_list = np.array(processed_EDU_avg_list)

        print "z is ", Z
        print "raw_Ophir_avg_list is ", raw_Ophir_avg_list.reshape(-1)
        print "raw_EDU_avg_list is ", raw_EDU_avg_list.reshape(-1)

        print "Z[-1] = ", Z[-1]

        print "raw_Ophir_avg_list.reshape(-1)[:-1] is ", raw_Ophir_avg_list.reshape(-1)[:-1]
        print "raw_Ophir_avg_list.reshape(-1)[-1] is ", raw_Ophir_avg_list.reshape(-1)[-1]

        slop = 1
        intercept = 0
        Ophir = raw_Ophir_avg_list.reshape(-1)[:-1]
        BMU = raw_BMU1_avg_list.reshape(-1)[:-1]
        EDU = raw_EDU_avg_list.reshape(-1)[:-1]

        # EDU = raw_EDU_avg_list.reshape(-1)[:-1]*slop + intercept

        self.raw_EDU_avg_list = EDU
        self.raw_OE_avg_list = raw_OE_avg_list[:-1]
        self.raw_BMU1_avg_list = BMU
        self.raw_BMU2_avg_list = raw_BMU2_avg_list[:-1]
        self.raw_Ophir_avg_list = Ophir
        # self.raw_OB_avg_list = raw_OB_avg_list

        Ophir_90_avg = raw_Ophir_avg_list.reshape(-1)[-1]
        BMU_90_avg = raw_BMU1_avg_list.reshape(-1)[-1]
        EDU_90_avg = raw_EDU_avg_list.reshape(-1)[-1]
        # EDU_90_avg = raw_EDU_avg_list.reshape(-1)[-1]*slop + intercept

        self.Ophir = Ophir / Ophir_90_avg
        self.EDU = EDU / EDU_90_avg
        self.BMU1 = BMU / BMU_90_avg
        self.OE = self.Ophir / self.EDU
        self.OB = self.Ophir / self.BMU1

        self.OE_line, = self.plot_area.axes.plot(Z[:-1], self.OE, "*-", label="OE")
        self.Ophir_line, = self.plot_area.axes.plot(Z[:-1], self.Ophir, "*-", label="Ophir")
        self.EDU_line, = self.plot_area.axes.plot(Z[:-1], self.EDU, "*-", label="EDU")
        self.BMU1_line, = self.plot_area.axes.plot(Z[:-1], self.BMU1, "*-", label="BMU")
        self.OB_line, = self.plot_area.axes.plot(Z[:-1], self.OB, "*-", label="OB")

        # VA_90_transmission = Z
        #ax.plot(Z, VA_90_transmission/VA_90_transmission.max(), color="r", label="VA_90")


        #print "mean = ",processed_OE_avg_list[:].mean()
        #print "std = ", processed_OE_avg_list[:].std()
        #print "std/mean = ", processed_OE_avg_list[:].std()/processed_OE_avg_list[:].mean()

        self.plot_area.axes.set_title(filename)

        self.plot_area.axes.set_xlabel("angle")
        self.plot_area.axes.set_ylabel("transmission")
        self.plot_area.axes.set_xlim(Z[:-1].min(), Z[:-1].max())
        self.plot_area.axes.legend()
        self.update_plot()
        # self.plot_area.canvas.draw()
        pass

    def browse(self):
        logging.log(logging.INFO, "browse")
        self.filename = QtGui.QFileDialog.getOpenFileName(self, self.tr("Open IL Data File"), QtCore.QString(),
                                                          self.tr("*"))
        self.file_name_comboBox.setEditText(self.filename)
        self.display_scan_info()

    def display_scan_info(self):
        self.filename = unicode(self.file_name_comboBox.currentText())
        print "file name is", self.filename
        if self.filename != "":
            data_file = open(self.filename)
            data_file_info = ""
            for row in xrange(0, 37):
                data_file_info = data_file_info + data_file.readline()

            res = re.sub(r'[\n]+', r'\n', data_file_info, flags=re.S)
            print res
            self.scan_info_LEdit.append(res[27:])
        pass


if __name__ == "__main__":
    qApp = QtGui.QApplication(sys.argv)
    zz = VA_2D_line_plot_widget()
    zz.show()
    sys.exit(qApp.exec_())


