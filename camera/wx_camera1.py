# coding:utf-8
#!/usr/bin/env python

__author__ = 'XingHua'

# -*- coding: utf-8 -*-

###########################################################################
## Python code generated with wxFormBuilder (version Jun 30 2011)
## http://www.wxformbuilder.org/
##
## PLEASE DO "NOT" EDIT THIS FILE!
###########################################################################

import wx
import wx.xrc
import VideoCapture
###########################################################################
## Class MyFrame1
###########################################################################
class MyFrame1 ( wx.Frame ):

    def __init__( self, parent ):
        wx.Frame.__init__ ( self, parent, id = wx.ID_ANY, title = wx.EmptyString, pos = wx.DefaultPosition, size = wx.Size( 566,535 ), style = wx.DEFAULT_FRAME_STYLE|wx.TAB_TRAVERSAL )

        self.SetSizeHintsSz( wx.DefaultSize, wx.DefaultSize )

        bSizer1 = wx.BoxSizer( wx.VERTICAL )

        self.m_panel1 = wx.Panel( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
        bSizer1.Add( self.m_panel1, 1, wx.EXPAND |wx.ALL, 5 )

        self.m_button3 = wx.Button( self, wx.ID_ANY, u"MyButton", wx.DefaultPosition, wx.DefaultSize, 0 )
        bSizer1.Add( self.m_button3, 0, wx.ALL, 5 )

        self.SetSizer( bSizer1 )
        self.Layout()

        self.Centre( wx.BOTH )

        # Connect Events
        self.m_button3.Bind( wx.EVT_BUTTON, self.OnButton )
        #self.m_panel1.Bind(wx.EVT_IDLE,self.OnIdel)
        self.timer=wx.Timer(self)
        self.Bind(wx.EVT_TIMER,self.OnIdel,self.timer)
    def OnIdel(self,evnet):
        #cam = VideoCapture.Device()
        self.cam.saveSnapshot('test.jpg')
        img=wx.Image("test.jpg",wx.BITMAP_TYPE_ANY).ConvertToBitmap()
        dc=wx.ClientDC(self.m_panel1)
        dc.DrawBitmap(img,0,0,False)

    def OnButton( self, event ):
        self.cam = VideoCapture.Device()
        #cam.saveSnapshot('test.jpg')
        self.timer.Start(100)
        event.Skip()
if __name__=='__main__':
    app=wx.App()
    frame=MyFrame1(None)
    frame.Show(True)
    app.MainLoop()