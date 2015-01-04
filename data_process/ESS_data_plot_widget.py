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

from IL_base_plot_widget import base_3Dplot_Widget

import logging

logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',
                    datefmt='%a, %d %b %Y %H:%M:%S',
                    filename='ESS_data_plot_widget.log',
                    filemode='w')

logging.debug('This is debug message')
logging.info('This is info message')
logging.warning('This is warning message')


class ESS_data_plot_widget(QtGui.QWidget):
    def __init__(self, parent=None, filename="ESS_energy_data20141115_with_pianzhen_100Hz_25"):
        super(ESS_data_plot_widget, self).__init__(parent)
        QtGui.QWidget.__init__(self, parent)
        # self.setGeometry(20, 120, 800, 600)
        self.file_label = QtGui.QLabel("File name:")

        self.file_name_comboBox = QtGui.QComboBox()
        self.file_name_comboBox.addItem("ESS_energy_data20141115_with_pianzhen_100Hz_25")
        self.file_name_comboBox.setEditable(True)
        self.plot_PBtn = QtGui.QPushButton("Plot")
        self.browse_PBtn = QtGui.QPushButton("Browse")
        self.plot_area = base_3Dplot_Widget()

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
        # vspacer.expandingDirections()

        self.checkbox_widget.setLayout(self.checkbox_layout)
        # self.check_box.setInputContext("2")

        # self.vlayout = QtGui.QHBoxLayout()
        # self.vlayout.addWidget(self.Ophir_check_box)
        # self.vlayout.addWidget(self.EDU_check_box)
        # self.vlayout.addWidget(self.BMU1_check_box)
        # self.vlayout.addWidget(self.BMU2_check_box)
        # self.vlayout.addWidget(self.OE_check_box)
        # self.hbox.addWidget(self)

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
        unit_lines_dict = {"EDU": self.EDU, "Ophir": self.Ophir, "BMU1": self.BMU1, "OB": self.OB, "OE": self.OE}
        if self.OE_check_box.isChecked():
            visible_lines_list.append("OE")
            max_value_list.append(self.raw_OE_avg_list.max())
        if self.OB_check_box.isChecked():
            visible_lines_list.append("OB")
            max_value_list.append(self.raw_OB_avg_list.max())
        if self.Ophir_check_box.isChecked():
            visible_lines_list.append("Ophir")
            max_value_list.append(self.raw_Ophir_avg_list.max())
        if self.BMU1_check_box.isChecked():
            visible_lines_list.append("BMU1")
            max_value_list.append(self.raw_BMU1_avg_list.max())
        if self.EDU_check_box.isChecked():
            visible_lines_list.append("EDU")
            max_value_list.append(self.raw_EDU_avg_list.max())

        for each in unit_lines_dict:
            unit_lines_dict[each].set_visible(False)

        for each in visible_lines_list:
            unit_lines_dict[each].set_visible(True)
            # for e in dir(unit_dict[each]):
            # print e
            # for e in dir(self.plot_area.axes):
            # print e
        if len(max_value_list):
            z_max = max(max_value_list)
            self.plot_area.axes.set_zlim(0, z_max * 1.1)
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

        self.sdata_info = sdata
        print "@@@ x_start=", self.sdata_info.X_start_position

        sdata.skip_first_N_pulses(0)
        # sdata.outlier_rejection()

        raw_Ophir_avg_list = []
        raw_EDU_avg_list = []
        raw_BMU1_avg_list = []
        raw_BMU2_avg_list = []
        raw_OE_avg_list = []
        raw_OB_avg_list = []

        processed_Ophir_avg_list = []
        processed_EDU_avg_list = []
        processed_BMU1_avg_list = []
        processed_BMU2_avg_list = []
        processed_OE_avg_list = []

        X = []
        Y = []
        Z = []

        # print sdata.data[0].pos, len(sdata.data), sdata.data[0].pos[0],dir(sdata.data[0])

        for each in sdata.data:
            X.append(each.pos[0])
            Y.append(each.pos[1])
            Z.append(each.pos[2])

            raw_Ophir_avg_list.append(each.get_raw_Ophir_avg())
            raw_EDU_avg_list.append(each.get_raw_EDU_avg())
            raw_BMU1_avg_list.append(each.get_raw_BMU1_avg())
            raw_BMU2_avg_list.append(each.get_raw_BMU2_avg())

            raw_OE_avg_list.append(each.get_raw_Ophir_avg() / each.get_raw_EDU_avg())

            raw_OB_avg_list.append(each.get_raw_Ophir_avg() / each.get_raw_BMU1_avg())

            processed_Ophir_avg_list.append(each.get_processed_Ophir_avg())
            processed_EDU_avg_list.append(each.get_processed_EDU_avg())
            processed_BMU1_avg_list.append(each.get_processed_BMU1_avg())
            processed_BMU2_avg_list.append(each.get_processed_BMU2_avg())
            processed_OE_avg_list.append(each.get_processed_Ophir_avg() / each.get_processed_EDU_avg())

        X = np.array(X)
        Y = np.array(Y)
        # print "orgin X", X
        # print "orgin Y", Y

        raw_Ophir_avg_list = np.array(raw_Ophir_avg_list)
        processed_Ophir_avg_list = np.array(processed_Ophir_avg_list)
        self.raw_EDU_avg_list = raw_EDU_avg_list = np.array(raw_EDU_avg_list)
        self.raw_OE_avg_list = raw_OE_avg_list = np.array(raw_OE_avg_list)

        self.processed_OE_avg_list = processed_OE_avg_list = np.array(processed_OE_avg_list)
        self.processed_EDU_avg_list = processed_EDU_avg_list = np.array(processed_EDU_avg_list)
        self.raw_BMU1_avg_list = raw_BMU1_avg_list = np.array(raw_BMU1_avg_list)
        self.raw_BMU2_avg_list = raw_BMU2_avg_list = np.array(raw_BMU2_avg_list)
        self.raw_OB_avg_list = raw_OB_avg_list = np.array(raw_OB_avg_list)

        # print sdata.Y_cnt,sdata.X_cnt
        self.X = X = X.reshape(sdata.Y_cnt, sdata.X_cnt)
        self.Y = Y = Y.reshape(sdata.Y_cnt, sdata.X_cnt)
        self.raw_Ophir_avg_list = raw_Ophir_avg_list = raw_Ophir_avg_list.reshape(sdata.Y_cnt, sdata.X_cnt)
        raw_EDU_avg_list = raw_EDU_avg_list.reshape(sdata.Y_cnt, sdata.X_cnt)
        raw_OE_avg_list = raw_OE_avg_list.reshape(sdata.Y_cnt, sdata.X_cnt)
        raw_BMU1_avg_list = raw_BMU1_avg_list.reshape(sdata.Y_cnt, sdata.X_cnt)
        raw_BMU2_avg_list = raw_BMU2_avg_list.reshape(sdata.Y_cnt, sdata.X_cnt)
        raw_OB_avg_list = raw_OB_avg_list.reshape(sdata.Y_cnt, sdata.X_cnt)
        processed_OE_avg_list = processed_OE_avg_list.reshape(sdata.Y_cnt, sdata.X_cnt)
        processed_EDU_avg_list = processed_EDU_avg_list.reshape(sdata.Y_cnt, sdata.X_cnt)

        processed_Ophir_avg_list = processed_Ophir_avg_list.reshape(sdata.Y_cnt, sdata.X_cnt)

        # ax.scatter3D(X.reshape(-1), Y.reshape(-1), np.array(raw_Ophir_avg_list)*100)

        self.raw_EDU_avg_list = raw_EDU_avg_list
        self.raw_OE_avg_list = raw_OE_avg_list
        self.raw_BMU1_avg_list = raw_BMU1_avg_list
        self.raw_BMU2_avg_list = raw_BMU2_avg_list
        self.raw_OB_avg_list = raw_OB_avg_list

        # np.savetxt("Ophir_avg_list.txt", raw_Ophir_avg_list, "%.8f", "\t")
        # np.savetxt("X.txt", X, "%.8f", "\t")
        # np.savetxt("Y.txt", Y, "%.8f", "\t")

        # print processed_OE_avg_list[5:],"\n",processed_OE_avg_list,"\n",processed_OE_avg_list.shape
        # print X[5:]
        # print Y[5:]
        # self.process_Ophir=self.plot_area.axes.plot_wireframe(X[:], Y[:], processed_Ophir_avg_list[:],color="r",label="Ophir")
        # self.process_EDU=ax.plot_wireframe(X[:], Y[:], processed_EDU_avg_list[:],color="g",label="EDU")
        # self.process_OE=ax.plot_wireframe(X[:], Y[:], processed_OE_avg_list[:],color="b",label="OE")

        self.OE = self.plot_area.axes.plot_wireframe(X, Y, raw_OE_avg_list, color="r", label="OE", visible=True)
        self.Ophir = self.plot_area.axes.plot_wireframe(X, Y, raw_Ophir_avg_list, color="b", label="Ophir",
                                                        visible=False)
        self.EDU = self.plot_area.axes.plot_wireframe(X, Y, raw_EDU_avg_list, color="y", label="EDU", visible=False)
        self.BMU1 = self.plot_area.axes.plot_wireframe(X, Y, raw_BMU1_avg_list, color="black", label="BMU1",
                                                       visible=False)
        # self.BMU2 = self.plot_area.axes.plot_wireframe(X, Y, raw_BMU2_avg_list, color="black", label="BMU2",visible = False)


        print X[-1, :]
        print raw_Ophir_avg_list[-1, :]
        if (raw_OB_avg_list.mean() > 1000):
            self.OB = self.plot_area.axes.plot_wireframe(X, Y, np.ones(sdata.Y_cnt * sdata.X_cnt).reshape(sdata.Y_cnt,
                                                                                                          sdata.X_cnt) * 1000)
        else:
            self.OB = self.plot_area.axes.plot_wireframe(X, Y, raw_OB_avg_list, color="violet",
                                                         label="OB", visible=False)

        # print "process OE avg list is",processed_OE_avg_list
        print "raw_OE_avg_list.min() is ", raw_OE_avg_list.min(), raw_OE_avg_list.argmin(), X.reshape(-1)[
            raw_OE_avg_list.argmin()], Y.reshape(-1)[raw_OE_avg_list.argmin()]
        print "mean = ", processed_OE_avg_list[:].mean()
        print "std = ", processed_OE_avg_list[:].std()
        print "std/mean = ", processed_OE_avg_list[:].std() / processed_OE_avg_list[:].mean()

        txt = "mean = " + str(processed_OE_avg_list[:].mean()) + "  std = " + str(
            processed_OE_avg_list[:].std()) + "  std/mean = " + str(
            processed_OE_avg_list[:].std() / processed_OE_avg_list[:].mean())

        self.plot_area.axes.set_xlabel("x")
        self.plot_area.axes.set_ylabel("y")
        self.plot_area.axes.set_title(filename)
        self.plot_area.axes.set_zlabel("intensity")

        self.plot_area.axes.set_xlim(-65, 65)
        self.plot_area.axes.set_ylim(-25, 25)
        self.plot_area.axes.set_zlim(0, raw_OE_avg_list.max() + 0.1)

        self.plot_area.axes.view_init(azim=-113, elev=25)

        print "processed_OE_avg_list.shape is ", processed_OE_avg_list.shape
        self.plot_area.axes.legend()
        self.plot_area.canvas.draw()
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


if __name__ == "__main__":
    qApp = QtGui.QApplication(sys.argv)
    zz = ESS_data_plot_widget()
    zz.show()
    sys.exit(qApp.exec_())


