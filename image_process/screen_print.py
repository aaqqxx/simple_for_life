# !/usr/bin/env python
# coding=gb2312

__author__ = 'XingHua'

# ��ģ����Ҫ�ṩץͼ���ܣ�֧����������ץͼ��ʽ��
# 1��ץȡȫ��,��ݼ�CTRL+F1
# 2��ץȡ��ǰ���ڣ���ݼ�CTRL+F2
# 3��ץȡ��ѡ���򣬿�ݼ�CTRL+F3
# ץ��֮�󣬻��Զ���������Ի���ѡ��·�����漴��
# *******************************************
# ���¼�¼
# 0.1 2012-03-10 create by dyx1024
# ********************************************

import pyhk
import wx
import os
import sys
from PIL import ImageGrab
import ctypes
import win32gui
import ctypes.wintypes


def capture_fullscreen():
    '''
    Function:ȫ��ץͼ
    Input��NONE
    Output: NONE
    author: socrates
    blog:http://blog.csdn.net/dyx1024
    date:2012-03-10
    '''
    # ץͼ
    pic = ImageGrab.grab()

    # ����ͼƬ
    save_pic(pic)


def capture_current_windows():
    '''
    Function:ץȡ��ǰ����
    Input��NONE
    Output: NONE
    author: socrates
    blog:http://blog.csdn.net/dyx1024
    date:2012-03-10
    '''
    # ���ڽṹ
    class RECT(ctypes.Structure):
        _fields_ = [('left', ctypes.c_long),
                    ('top', ctypes.c_long),
                    ('right', ctypes.c_long),
                    ('bottom', ctypes.c_long)]

        def __str__(self):
            return str((self.left, self.top, self.right, self.bottom))

    rect = RECT()

    # ��ȡ��ǰ���ھ��
    HWND = win32gui.GetForegroundWindow()

    # ȡ��ǰ��������
    ctypes.windll.user32.GetWindowRect(HWND, ctypes.byref(rect))

    # ��������
    rangle = (rect.left + 2, rect.top + 2, rect.right - 2, rect.bottom - 2)

    # ץͼ
    pic = ImageGrab.grab(rangle)

    # ����
    save_pic(pic)


def capture_choose_windows():
    '''
    Function:ץȡѡ�������û���Լ�д���������QQץͼ����
    Input��NONE
    Output: NONE
    author: socrates
    blog:http://blog.csdn.net/dyx1024
    date:2012-03-10
    '''
    try:
        # ����QQץͼʹ�õ�dll
        dll_handle = ctypes.cdll.LoadLibrary('CameraDll.dll')
    except Exception:
        try:
            # ���dll����ʧ�ܣ����ַ���ʹ�ã�ֱ�����У������ʧ�ܣ��˳�
            os.system("Rundll32.exe CameraDll.dll, CameraSubArea")
        except Exception:
            return
    else:
        try:
            # ����dll�ɹ��������ץͼ������ע:û�з����������������Ĳ�������
            # �����ͣ����Դ����ִ�к�ᱨ����ȱ��4���ֽڣ�����Ӱ��ץͼ���ܣ���
            # ��ֱ�Ӻ�����Щ�쳣
            dll_handle.CameraSubArea(0)
        except Exception:
            return


def save_pic(pic, filename='δ����ͼƬ.png'):
    '''
    Function:ʹ���ļ��Կ򣬱���ͼƬ
    Input��NONE
    Output: NONE
    author: socrates
    blog:http://blog.csdn.net/dyx1024
    date:2012-03-10
    '''
    app = wx.PySimpleApp()

    wildcard = "PNG(*.png)|*.png"
    dialog = wx.FileDialog(None, "Select a place", os.getcwd(),
                           filename, wildcard, wx.SAVE)
    if dialog.ShowModal() == wx.ID_OK:
        pic.save(dialog.GetPath().encode('gb2312'))
    else:
        pass

    dialog.Destroy()


def main():
    '''
    Function:��������ע���ݼ�
    Input��NONE
    Output: NONE
    author: socrates
    blog:http://blog.csdn.net/dyx1024
    date:2012-03-10
    '''

    # ����hotkey���
    hot_handle = pyhk.pyhk()

    # ע��ץȡȫ����ݼ�CTRL+F1
    hot_handle.addHotkey(['Ctrl', 'F1'], capture_fullscreen)

    # ע��ץȡ��ǰ���ڿ�ݼ�CTRL+F2
    hot_handle.addHotkey(['Ctrl', 'F2'], capture_current_windows)

    # ע��ץȡ��ѡ�����ݼ�CTRL+F3
    hot_handle.addHotkey(['Ctrl', 'F3'], capture_choose_windows)

    # ��ʼ����
    hot_handle.start()


if __name__ == "__main__":
    main()
