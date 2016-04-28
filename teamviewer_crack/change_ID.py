# coding:utf-8
# !/usr/bin/env python

__author__ = 'SAF'

import sys
from PyQt4 import QtCore, QtGui
import numpy as np
# import IL_data_analysis_mainwindow
import time
import os
import shutil
import _winreg
import random


mackey = "SYSTEM\\CurrentControlSet\\Control\\Class\\{4D36E972-E325-11CE-BFC1-08002bE10318}"

def randomMAC():
    mac = [ 0x52, 0x54, 0x00,
        random.randint(0x00, 0x7f),
        random.randint(0x00, 0xff),
        random.randint(0x00, 0xff) ]
    return ':'.join(map(lambda x: "%02x" % x, mac))


def remove_teamviewer_appdir():
    file_name = "test111"
    # print os.path.join(os.environ["appdata"],file_name)
    shutil.rmtree(os.path.join(os.environ["appdata"], file_name))
    pass


def remove_teamvirew_reg():
    software_name = "test111"
    keys = []
    keys.append(_winreg.OpenKey(_winreg.HKEY_CURRENT_USER, r"Software"))
    keys.append(_winreg.OpenKey(_winreg.HKEY_LOCAL_MACHINE, r"Software"))
    print keys
    _winreg.DeleteKey(keys[0], software_name)
    pass


def modifymac(newmac):  # 修改mac地址
    mackey_fix = mackey + '\\' + newmac
    key = _winreg.OpenKey(_winreg.HKEY_LOCAL_MACHINE, mackey_fix, 0, _winreg.KEY_ALL_ACCESS)

    judge = True
    while judge:
        inputmac = raw_input('请输入修改后的MAC地址：（如“011D00003F21”）:')
        mjudge = judgemac(inputmac)
        if len(inputmac) == 12 and mjudge == True:
            judge = False
    print '您输入的新MAC地址是%s' % inputmac
    _winreg.SetValueEx(key, "NetworkAddress", 0, _winreg.REG_SZ, inputmac)  # 设置注册表值
    print 'MAC地址已修改成功,重启后生效。'
    _winreg.CloseKey(key)


def judgemac(inputmac):  # 判断输入的mac地址是否合法
    judgechar = True
    charlist = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', 'A', 'B', 'C', 'D', 'E', 'F', 'a', 'b', 'c', 'd', 'e',
                'f']
    for char_i in inputmac:
        if char_i not in charlist:
            print 'MAC地址格式错误，请重新输入。'
            judgechar = False
            break
    return judgechar


def change_teamviewer_ini():
    pass

def get_mac_address():
    import uuid
    mac=uuid.UUID(int = uuid.getnode()).hex[-12:].upper()
    return '%s:%s:%s:%s:%s:%s' % (mac[0:2],mac[2:4],mac[4:6],mac[6:8],mac[8:10],mac[10:])

if __name__ == '__main__':
    # remove_teamviewer_appdir()
    # remove_teamvirew_reg()
    print get_mac_address()
        # print each
    pass
