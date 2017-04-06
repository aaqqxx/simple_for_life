#!/usr/bin/env python
# -*- coding: utf-8 -*-
__author__ = 'XingHua'

import pythoncom
import pyHook
import time
import pyhk
import os
import sys
import ctypes
from ctypes import wintypes
import win32con
import win32api


class CInspectKeyAndMouseEvent:
    '''
    Function:键盘和鼠标监控类
    Input：NONE
    Output: NONE
    author: socrates
    blog:http://blog.csdn.net/dyx1024
    date:2012-03-09
    '''
    def __init__(self, filename):
        '初始化'
        self.filename = filename

    def open_file(self):
        '打开文件'
        self.fobj = open(self.filename,  'w')

    def close_file(self):
        '关闭文件'
        self.fobj.close()

    def IsNotWriteLog(self):
        '是否记录日志'
        return  self.bFlag

    def IsExitCommand(self, event):
        '''
                     是否当前按下了程序定义的热键'
                      如果按下了ALT+F2，将记录日志的状态位置为True,不记录日志,
                     如果按下了ALT+F1，将记录日志状态位置为False,表示记录日志
        '''
        if event.Alt == 32 and str(event.Key) == 'F2':
            self.bFlag = True
            print time.strftime('[%Y-%m-%d %H:%M:%S]: ',time.localtime(time.time()))+ ' stop write log'
        elif  event.Alt == 32 and str(event.Key) == 'F1':
            self.bFlag = False
            print time.strftime('[%Y-%m-%d %H:%M:%S]: ',time.localtime(time.time()))+ ' start write log'

    def onMouseEvent(self, event):
        "处理鼠标事件"

        #判断是否要记录日志
        if self.IsNotWriteLog():
            return True

        self.fobj.writelines('-' * 20 + 'MouseEvent Begin' + '-' * 20 + '\n')
        self.fobj.writelines("Current Time:%s\n" % time.strftime('[%Y-%m-%d %H:%M:%S]: ',time.localtime(time.time())))
        self.fobj.writelines("MessageName:%s\n" % str(event.MessageName))
        self.fobj.writelines("Message:%d\n" % event.Message)
        self.fobj.writelines("Time_sec:%d\n" % event.Time)
        self.fobj.writelines("Window:%s\n" % str(event.Window))
        self.fobj.writelines("WindowName:%s\n" % str(event.WindowName))
        self.fobj.writelines("Position:%s\n" % str(event.Position))
        self.fobj.writelines('-' * 20 + 'MouseEvent End' + '-' * 20 + '\n')
        return True

    def onKeyboardEvent(self, event):

        #处理按下的热键
        self.IsExitCommand(event)

        #判断是否要记录日志
        if self.IsNotWriteLog():
            return True

        self.fobj.writelines('-' * 20 + 'Keyboard Begin' + '-' * 20 + '\n')
        self.fobj.writelines("Current Time:%s\n" % time.strftime('[%Y-%m-%d %H:%M:%S]: ',time.localtime(time.time())))
        self.fobj.writelines("MessageName:%s\n" % str(event.MessageName))
        self.fobj.writelines("Message:%d\n" % event.Message)
        self.fobj.writelines("Time:%d\n" % event.Time)
        self.fobj.writelines("Window:%s\n" % str(event.Window))
        self.fobj.writelines("WindowName:%s\n" % str(event.WindowName))
        self.fobj.writelines("Ascii_code: %d\n" % event.Ascii)
        self.fobj.writelines("Ascii_char:%s\n" % chr(event.Ascii))
        self.fobj.writelines("Key:%s\n" % str(event.Key))
        self.fobj.writelines('-' * 20 + 'Keyboard End' + '-' * 20 + '\n')
        return True

    #默认记录
    bFlag = False



def InspectKeyAndMouseEvent():
    "启动监控"
    my_event = CInspectKeyAndMouseEvent("e:\\hook_log.txt")
    my_event.open_file()

    #创建hook句柄
    hm = pyHook.HookManager()

    #监控键盘
    hm.KeyDown = my_event.onKeyboardEvent
    hm.HookKeyboard()

    #监控鼠标
    hm.MouseAll = my_event.onMouseEvent
    hm.HookMouse()

    #循环获取消息
    pythoncom.PumpMessages()
    my_event.close_file()

def handle_start_InspecEvent():
    "开始监控（按下Ctrl + F1）"
    print time.strftime('[%Y-%m-%d %H:%M:%S]: ',time.localtime(time.time()))+ ' start write log'
    InspectKeyAndMouseEvent()

#def handle_stop_InspecEvent():
#    "停止监控  (按下Ctrl + F2)"
#    InspectKeyAndMouseEvent(False)


if __name__ == "__main__":
    '''
    Function:通过快捷键控制程序运行
    Input：NONE
    Output: NONE
    author: socrates
    blog:http://blog.csdn.net/dyx1024
    date:2012-03-09
    '''

    byref = ctypes.byref
    user32 = ctypes.windll.user32

    #定义快捷键
    HOTKEYS = {
               1 : (win32con.VK_F1, win32con.MOD_ALT)
#               2 : (win32con.VK_F2, win32con.MOD_ALT)
               }

    #快捷键对应的驱动函数
    HOTKEY_ACTIONS = {
        1 : handle_start_InspecEvent,
#        2 : handle_stop_InspecEvent
        }

    #注册快捷键
    for id, (vk, modifiers) in HOTKEYS.items ():
        if not user32.RegisterHotKey (None, id, modifiers, vk):
            print "Unable to register id", id

    #启动监听
    try:
        msg = wintypes.MSG ()
        while user32.GetMessageA (byref (msg), None, 0, 0) != 0:
            if msg.message == win32con.WM_HOTKEY:
                action_to_take = HOTKEY_ACTIONS.get (msg.wParam)
                if action_to_take:
                    action_to_take ()

            user32.TranslateMessage (byref (msg))
            user32.DispatchMessageA (byref (msg))

    finally:
        for id in HOTKEYS.keys ():
            user32.UnregisterHotKey (None, id)
