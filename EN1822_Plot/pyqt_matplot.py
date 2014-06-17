__author__ = 'SIOM'
"""
An example of how to use Basemap in pyqt4 application.

Copyright(C) 2011 dbzhang800#gmail.com
"""

from matplotlib.backends.backend_qt4agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
from mpl_toolkits.basemap import Basemap
from PyQt4 import QtGui

class Widget(FigureCanvas):
    def __init__(self, parent=None, width=5, height=4, dpi=100):
        fig = Figure(figsize=(width, height), dpi=100)
        FigureCanvas.__init__(self, fig)
        self.setParent(parent)
        self.axes = fig.add_subplot(111)

        map = Basemap(ax=self.axes)
        map.drawcoastlines()
        map.drawcountries()
        map.drawmapboundary()
        map.fillcontinents(color='coral', lake_color='aqua')
        map.drawmapboundary(fill_color='aqua')

        self.setWindowTitle("PyQt4 and Basemap -- dbzhang800")

if __name__ == "__main__":
    import sys
    app = QtGui.QApplication(sys.argv)
    w = Widget()
    w.show()
    sys.exit(app.exec_())