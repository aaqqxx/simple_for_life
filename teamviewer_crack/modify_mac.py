# -*- coding: gbk -*-
'''
MAC地址修改器for xp V1.0
小五义：http://www.cnblogs.com/xiaowuyi
'''

from _winreg import *
import sys
import os
import locale
import codecs


mackey = "SYSTEM\\CurrentControlSet\\Control\\Class\\{4D36E972-E325-11CE-BFC1-08002bE10318}"


def readinfo(ethernetname):  # 读取当前网络设备并选择要修改的设备

    key = OpenKey(HKEY_LOCAL_MACHINE, mackey)
    countkey = QueryInfoKey(key)[0]
    keylist = []  # 获取{4D36E972-E325-11CE-BFC1-08002bE10318}子键列表
    mackeylist = []

    for i in range(int(countkey)):
        name = EnumKey(key, i)  # 获取子键名
        keylist.append(name)
    CloseKey(key)

    for t in keylist:
        # print "t is ",t
        mackey_zi = mackey + '\\' + t

        try:
            key = OpenKey(HKEY_LOCAL_MACHINE, mackey_zi)
            # print key
            value, type = QueryValueEx(key, "DriverDesc")
            # 列出有mac地址的网卡，及对应注册表中的编号
            print value
            if ethernetname.has_key(value.decode("gbk")):
                mackeylist.append(t)
                print '%s: %s  MAC:%s' % (t, value, ethernetname[value])
            else:
                pass
        except:
            value = 'None'
    CloseKey(key)
    judge = True
    while judge:
        d = raw_input(u'请从上面选择您的网卡号（注意按格式填写每行冒号前的数字）:')
        print "you input is:",d
        if d in mackeylist:
            judge = False
        else:
            print u"输入错误，重新输入！"
    return d


def readipconfig():  # 读取ipconfig信息，列出当前网卡地址
    t = "Physical Address"
    t = u"物理地址"
    u = "Description"
    u = u"描述"
    keyphy = ''
    macfact = {}
    print os.popen("ipconfig /all").readlines()
    for line in os.popen("ipconfig /all"):
        # print line,
        if u.encode(codecs.lookup(locale.getpreferredencoding()).name) in line:
            print keyphy
            keyphy=line.split(":")[1].strip()
        if keyphy !='' and (t.encode(codecs.lookup(locale.getpreferredencoding()).name) in line):
            macfact[keyphy]=line.split(":")[1].strip()
    # for key in macfact.keys():
    #     print key,macfact[key]
    return macfact


def modifymac(newmac):  # 修改mac地址
    mackey_fix = mackey + '\\' + newmac
    key = OpenKey(HKEY_LOCAL_MACHINE, mackey_fix, 0, KEY_ALL_ACCESS)

    judge = True
    while judge:
        inputmac = raw_input('请输入修改后的MAC地址：（如“011D00003F21”）:')
        mjudge = judgemac(inputmac)
        if len(inputmac) == 12 and mjudge == True:
            judge = False
    print '您输入的新MAC地址是%s' % inputmac
    SetValueEx(key, "NetworkAddress", 0, REG_SZ, inputmac)  # 设置注册表值
    print 'MAC地址已修改成功,重启后生效。'
    CloseKey(key)


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


if __name__ == '__main__':
    # print sys.getdefaultencoding()
    # print sys.getfilesystemencoding()
    # import locale
    # import codecs
    # #
    # print locale.getpreferredencoding();
    # print codecs.lookup(locale.getpreferredencoding()).name
    if sys.platform == "win32":
        iplist = readipconfig()
        m=readinfo(iplist)
        modifymac(m)
        pass
    else:
        print "不支持当前系统"
