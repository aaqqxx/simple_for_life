# -*- coding: gbk -*-
'''
MAC��ַ�޸���for xp V1.0
С���壺http://www.cnblogs.com/xiaowuyi
'''

from _winreg import *
import sys
import os
import locale
import codecs


mackey = "SYSTEM\\CurrentControlSet\\Control\\Class\\{4D36E972-E325-11CE-BFC1-08002bE10318}"


def readinfo(ethernetname):  # ��ȡ��ǰ�����豸��ѡ��Ҫ�޸ĵ��豸

    key = OpenKey(HKEY_LOCAL_MACHINE, mackey)
    countkey = QueryInfoKey(key)[0]
    keylist = []  # ��ȡ{4D36E972-E325-11CE-BFC1-08002bE10318}�Ӽ��б�
    mackeylist = []

    for i in range(int(countkey)):
        name = EnumKey(key, i)  # ��ȡ�Ӽ���
        keylist.append(name)
    CloseKey(key)

    for t in keylist:
        # print "t is ",t
        mackey_zi = mackey + '\\' + t

        try:
            key = OpenKey(HKEY_LOCAL_MACHINE, mackey_zi)
            # print key
            value, type = QueryValueEx(key, "DriverDesc")
            # �г���mac��ַ������������Ӧע����еı��
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
        d = raw_input(u'�������ѡ�����������ţ�ע�ⰴ��ʽ��дÿ��ð��ǰ�����֣�:')
        print "you input is:",d
        if d in mackeylist:
            judge = False
        else:
            print u"��������������룡"
    return d


def readipconfig():  # ��ȡipconfig��Ϣ���г���ǰ������ַ
    t = "Physical Address"
    t = u"�����ַ"
    u = "Description"
    u = u"����"
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


def modifymac(newmac):  # �޸�mac��ַ
    mackey_fix = mackey + '\\' + newmac
    key = OpenKey(HKEY_LOCAL_MACHINE, mackey_fix, 0, KEY_ALL_ACCESS)

    judge = True
    while judge:
        inputmac = raw_input('�������޸ĺ��MAC��ַ�����硰011D00003F21����:')
        mjudge = judgemac(inputmac)
        if len(inputmac) == 12 and mjudge == True:
            judge = False
    print '���������MAC��ַ��%s' % inputmac
    SetValueEx(key, "NetworkAddress", 0, REG_SZ, inputmac)  # ����ע���ֵ
    print 'MAC��ַ���޸ĳɹ�,��������Ч��'
    CloseKey(key)


def judgemac(inputmac):  # �ж������mac��ַ�Ƿ�Ϸ�
    judgechar = True
    charlist = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', 'A', 'B', 'C', 'D', 'E', 'F', 'a', 'b', 'c', 'd', 'e',
                'f']
    for char_i in inputmac:
        if char_i not in charlist:
            print 'MAC��ַ��ʽ�������������롣'
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
        print "��֧�ֵ�ǰϵͳ"
