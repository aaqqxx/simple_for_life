# coding:utf-8
#!/usr/bin/env python

__author__ = 'XingHua'

"""

"""
import numpy as np

import matplotlib

# uncomment the following to use wx rather than wxagg
# matplotlib.use('WX')
#from matplotlib.backends.backend_wx import FigureCanvasWx as FigureCanvas

# comment out the following to use wx rather than wxagg
matplotlib.use('WXAgg')
from matplotlib.backends.backend_wxagg import FigureCanvasWxAgg as FigureCanvas

from matplotlib.backends.backend_wx import NavigationToolbar2Wx

from matplotlib.figure import Figure
from mpl_toolkits.mplot3d import Axes3D
import wx


class CanvasFrame(wx.Frame):
    def __init__(self):
        wx.Frame.__init__(self, None, -1,
                          'CanvasFrame', size=(550, 350))

        self.SetBackgroundColour(wx.NamedColor("WHITE"))

        self.figure = Figure()
        self.axes = Axes3D(self.figure)

        xs = np.random.rand(100)
        ys = np.random.rand(100)
        zs = np.random.rand(100)

        self.canvas = FigureCanvas(self, -1, self.figure)
        self.axes.mouse_init()
        self.axes.scatter(xs, ys, zs)

        self.sizer = wx.BoxSizer(wx.VERTICAL)
        self.sizer.Add(self.canvas, 1, wx.LEFT | wx.TOP | wx.GROW)
        self.SetSizer(self.sizer)
        self.Fit()

        self.add_toolbar()  # comment this out for no toolbar


    def add_toolbar(self):
        self.toolbar = NavigationToolbar2Wx(self.canvas)
        self.toolbar.Realize()
        if wx.Platform == '__WXMAC__':
            # Mac platform (OSX 10.3, MacPython) does not seem to cope with
            # having a toolbar in a sizer. This work-around gets the buttons
            # back, but at the expense of having the toolbar at the top
            self.SetToolBar(self.toolbar)
        else:
            # On Windows platform, default window size is incorrect, so set
            # toolbar width to figure width.
            tw, th = self.toolbar.GetSizeTuple()
            fw, fh = self.canvas.GetSizeTuple()
            # By adding toolbar in sizer, we are able to put it at the bottom
            # of the frame - so appearance is closer to GTK version.
            # As noted above, doesn't work for Mac.
            self.toolbar.SetSize(wx.Size(fw, th))
            self.sizer.Add(self.toolbar, 0, wx.LEFT | wx.EXPAND)
        # update the axes menu on the toolbar
        self.toolbar.update()


    def OnPaint(self, event):
        self.canvas.draw()


class App(wx.App):
    def OnInit(self):
        'Create the main window and insert the custom frame'
        frame = CanvasFrame()
        frame.Show(True)

        return True


app = App(0)
app.MainLoop()