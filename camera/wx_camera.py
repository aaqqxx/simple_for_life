# coding:utf-8
#!/usr/bin/env python

__author__ = 'XingHua'

"""
闲着没事做，前段时间买了个摄像头，在ubuntu上用。打开cheese这个软件，一片空白，怎么不能用阿！
google一番，装上gspca，还是不能用！
用lsusb命令查看下
lingshangwen@eagle:~$ lsusb
Bus 005 Device 001: ID 0000:0000
Bus 004 Device 001: ID 0000:0000
Bus 003 Device 001: ID 0000:0000
Bus 002 Device 002: ID 0c45:5208 Microdia
Bus 002 Device 001: ID 0000:0000
Bus 001 Device 006: ID 058f:3820 Alcor Micro Corp.
Bus 001 Device 005: ID 0a12:0001 Cambridge Silicon Radio, Ltd Bluetooth Dongle (HCI mode)
Bus 001 Device 004: ID 05e3:0606 Genesys Logic, Inc. D-Link DUB-H4 USB 2.0 Hub
Bus 001 Device 001: ID 0000:0000
摄像头已经被识别出来，怎么就是不能用阿!!!!!!

还是自己动手，用python+opencv写段简单的代码吧，然后就有了下面的代码：
"""

import wx
from cv2.cv import *
from cv2.highgui import *

class MyFrame(wx.Frame):
    def __init__(self):
        wx.Frame.__init__(self, None, -1, 'camera')
        self.SetClientSize((640, 480))

        self.cap = CreateCameraCapture(0)
        self.Bind(wx.EVT_IDLE, self.onIdle)

    def onIdle(self, event):
        img = QueryFrame(self.cap)
        self.displayImage(img)
        event.RequestMore()

    def displayImage(self, img, offset=(0,0)):
        bitmap = wx.BitmapFromBuffer(img.width, img.height, img.imageData)
        dc = wx.ClientDC(self)
        dc.DrawBitmap(bitmap, offset[0], offset[1], False)

if __name__=="__main__":
    app = wx.App()
    frame = MyFrame()
    frame.Show(True)
    app.MainLoop()