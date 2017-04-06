# coding:utf-8
# !/usr/bin/env python

__author__ = 'SAF'

# PyQt tutorial 4 ext objWindow

import sys
from PyQt4 import QtCore, QtGui
import numpy as np
# import IL_data_analysis_mainwindow
import time
from types import coroutine



@coroutine
def switch():
    yield


def run(coros):
    """Execute a list of co-routines until all have completed."""
    # Copy argument list to avoid modification of arguments.
    coros = list(coros)

    while len(coros):
        # Copy the list for iteration, to enable removal from original
        # list.
        for coro in list(coros):
            try:
                coro.send(None)
            except StopIteration:
                coros.remove(coro)


async def test2(self):
    print("begin sleep 4s..")
    await time.sleep(4)
    print("sleep over")

class MyWidget(QtGui.QWidget):
    def __init__(self, parent=None):
        QtGui.QWidget.__init__(self, parent)

        # self.setFixedSize(200, 120)

        self.length_label = QtGui.QLabel("Length")
        self.width_label = QtGui.QLabel("Width")
        self.height_label = QtGui.QLabel("Height")
        self.path_label = QtGui.QLabel("Path")

        self.length_Ledit = QtGui.QLineEdit(self)
        self.width_Ledit = QtGui.QLineEdit(self)
        self.height_Ledit = QtGui.QLineEdit(self)

        self.label = QtGui.QLabel(self)
        self.label.setGeometry(QtCore.QRect(19, 129, 80, 80))
        self.label.setPixmap(QtGui.QPixmap(":/open/contourtest.png"))

        self.glayout = QtGui.QGridLayout()
        self.hlayout = QtGui.QHBoxLayout()
        # self.hlayout1 = QtGui.QHBoxLayout()
        self.vlayout = QtGui.QVBoxLayout(self)

        self.glayout.addWidget(self.length_label, 0, 0, 1, 1)
        self.glayout.addWidget(self.width_label, 1, 0, 1, 1)
        self.glayout.addWidget(self.height_label, 2, 0, 1, 1)

        self.glayout.addWidget(self.length_Ledit, 0, 1, 1, 2)
        self.glayout.addWidget(self.width_Ledit, 1, 1, 1, 2)
        self.glayout.addWidget(self.height_Ledit, 2, 1, 1, 2)

        self.sapcer_item = QtGui.QSpacerItem(1, 1)

        self.file_path_Ledit = QtGui.QLineEdit()
        self.explorer_Btn = QtGui.QPushButton("explorer")
        self.save_Btn = QtGui.QPushButton("save")
        self.hlayout.addWidget(self.path_label)
        self.hlayout.addWidget(self.file_path_Ledit, 2)
        self.hlayout.addWidget(self.explorer_Btn)
        self.hlayout.addWidget(self.save_Btn)

        self.vlayout.addWidget(self.label)
        self.vlayout.addLayout(self.glayout)
        self.vlayout.addLayout(self.hlayout)
        # self.quit = QtGui.QPushButton("Quit", self)
        # self.quit.setGeometry(62, 40, 75, 30)
        # self.quit.setFont(QtGui.QFont("Times", 18, QtGui.QFont.Bold))

        # self.connect(self.quit, QtCore.SIGNAL("clicked()"), QtGui.qApp, QtCore.SLOT("quit()"))
        # self.connect(self.quit, QtCore.SIGNAL("clicked()"), self, QtCore.SLOT("close()"))
        # self.connect(self.open_Btn, QtCore.SIGNAL("clicked()"), self, QtCore.SLOT("on_openfile_clicked()"))
        # self.explorer_Btn.clicked.connect(self.on_openfile_clicked)
        self.explorer_Btn.clicked.connect(self.test)
        self.save_Btn.clicked.connect(self.on_savefile_clicked)

    def on_openfile_clicked(self):
        dlg = QtGui.QFileDialog(self)
        self.filename = dlg.getSaveFileName()
        self.file_path_Ledit.setText(self.filename)

    def on_savefile_clicked(self):
        length = self.length_Ledit.text()
        width = self.width_Ledit.text()
        # height =
        np.savetxt(str(self.filename), [2, 3, 4, ])
        pass

    def test(self):
        # run([self.test1])
        data = self.test1()
        print(dir(data))
        try:
            data.send(None)
        except StopIteration:
            pass
        print("over")
        time.sleep(5)
        return 0

    async def test1(self):
        print("begin sleep 4s..")
        switch()
        await self.sim()
        switch()
        print("sleep over")
        return 10

    async def sim(self):
        switch()
        time.sleep(4)
        return 9




app = QtGui.QApplication(sys.argv)
widget = MyWidget()
# widget.move(350, 50)
widget.setWindowTitle("A Widget")
widget.show()

sys.exit(app.exec_())
