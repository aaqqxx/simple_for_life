# coding:utf-8
#!/usr/bin/env python

__author__ = 'XingHua'

"""

"""
from PyQt4 import QtGui, QtCore
from matplotlib.backends.backend_qt4agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt4agg import NavigationToolbar2QT as NavigationToolbar
from mpl_toolkits.mplot3d import Axes3D, axes3d
from matplotlib.figure import Figure
import matplotlib.pyplot as plt


class MyMplCanvas(FigureCanvas):
    """Ultimately, this is a QWidget (as well as a FigureCanvasAgg, etc.)."""

    def __init__(self, parent=None, width=5, height=4, dpi=100):
        fig = Figure(figsize=(width, height), dpi=dpi)
        self.axes = fig.add_subplot(111)
        # We want the axes cleared every time plot() is called
        # self.axes.hold(False)
        self.compute_initial_figure()
        FigureCanvas.__init__(self, fig)
        self.setParent(parent)

    def compute_initial_figure(self):
        pass


class base_2Dplot_Widget(QtGui.QWidget):
    def __init__(self, parent=None, filename="ESS_energy_data20141115_with_pianzhen_100Hz_25"):
        super(base_2Dplot_Widget, self).__init__(parent)
        vbox = QtGui.QVBoxLayout(self)
        self.canvas = MyMplCanvas(self, width=6, height=4, dpi=100)
        self.mplt_toolbar = NavigationToolbar(self.canvas, self)
        vbox.addWidget(self.mplt_toolbar)
        vbox.addWidget(self.canvas)
        self.setLayout(vbox)
        self.axes = self.canvas.axes
        # self.compute_initial_figure(filename)
        pass


class My3DMplCanvas(FigureCanvas):
    """Ultimately, this is a QWidget (as well as a FigureCanvasAgg, etc.)."""

    def __init__(self, parent=None, width=5, height=4, dpi=100):
        # self.fig = Figure(figsize=(width, height), dpi=dpi)
        self.fig = Figure()
        FigureCanvas.__init__(self, self.fig)
        self.axes = self.fig.add_subplot(111, projection="3d")
        # self.compute_initial_figure()
        self.setParent(parent)

    def compute_initial_figure(self):
        X, Y, Z = axes3d.get_test_data(0.05)
        self.axes.plot_surface(X, Y, Z, rstride=8, cstride=5, alpha=0.3)
        cset = self.axes.contourf(X, Y, Z, zdir='z', offset=-100, cmap=cm.coolwarm)
        cset = self.axes.contourf(X, Y, Z, zdir='x', offset=-40, cmap=cm.coolwarm)
        cset = self.axes.contourf(X, Y, Z, zdir='y', offset=40, cmap=cm.coolwarm)

        self.axes.set_xlabel('X')
        self.axes.set_xlim(-40, 40)
        self.axes.set_ylabel('Y')
        self.axes.set_ylim(-40, 40)
        self.axes.set_zlabel('Z')
        self.axes.set_zlim(-100, 100)
        plt.show()
        pass


class base_3Dplot_Widget(QtGui.QWidget):
    def __init__(self, parent=None, filename="ESS_energy_data20141115_with_pianzhen_100Hz_25"):
        super(base_3Dplot_Widget, self).__init__(parent)
        vbox = QtGui.QVBoxLayout(self)
        self.canvas = My3DMplCanvas(self, width=5, height=4, dpi=100)
        self.mplt_toolbar = NavigationToolbar(self.canvas, self)
        vbox.addWidget(self.mplt_toolbar)
        vbox.addWidget(self.canvas)
        self.setLayout(vbox)
        self.axes = self.canvas.axes
        # self.compute_initial_figure(filename)
        pass

    def compute_initial_figure(self, filename):
        X, Y, Z = axes3d.get_test_data(0.05)
        self.axes.plot_surface(X, Y, Z, rstride=8, cstride=8, alpha=0.3)
        cset = self.axes.contourf(X, Y, Z, zdir='z', offset=-100, cmap=cm.coolwarm)
        cset = self.axes.contourf(X, Y, Z, zdir='x', offset=-40, cmap=cm.coolwarm)
        cset = self.axes.contourf(X, Y, Z, zdir='y', offset=40, cmap=cm.coolwarm)

        self.axes.set_xlabel('X')
        self.axes.set_xlim(-40, 40)
        self.axes.set_ylabel('Y')
        self.axes.set_ylim(-40, 40)
        self.axes.set_zlabel('Z')
        self.axes.set_zlim(-100, 100)
        plt.show()
        pass