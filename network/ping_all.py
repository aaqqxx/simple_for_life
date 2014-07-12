# coding:utf-8
#!/usr/bin/env python

'''
用来检测同一网段的IP，mac地址
'''

__author__ = 'SAF'

import threading
import os
from time import sleep
import time
import matplotlib
# matplotlib.use('TkAgg')
import matplotlib.pyplot as plt

from mayavi import mlab

import numpy as np
import re
from mpl_toolkits.mplot3d import Axes3D

from ip2mac import IP2MAC


def ping(ip, usedIP):
    x = os.popen("ping %s -n 1" % str(ip))
    res = x.readlines()
    if check_res(res):
        for each in res:
            # print ip, res[3].decode('gbk'),
            usedIP.append(ip)
            return
    else:
        # print ip, "can't reach"
        pass


def check_res(res):
    for each in res:
        if "TTL" in each:
            return True
        else:
            continue


def is_off_line(use_able_ip_nums, threshold):
    if use_able_ip_nums < threshold:
        return True
    else:
        return False


def get_ip_last_num(ips):
    res = []
    for each in ips:
        res.append(int(re.search("\d+$", each).group()))
    return res


def get_y(row_nums=16):
    res = []
    tmp = np.zeros(row_nums)
    for each in range(row_nums):
        res.append(list(tmp + each))
    return np.array(res).reshape(-1)


def res_3d_bar_show(xx, yy, zz):
    tmp = range(len(xx))
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    # zz=sorted(set(range(256)).intersection(set(zz)))
    for each in zz:
        tmp[each] = 1
    ax.bar3d(xx, yy, np.zeros(len(xx)), 1, 1, tmp, 'b', alpha=0.8)
    fig.show()


if __name__ == "__main__":
    ips = []
    for i in xrange(1, 255):
        ips.append("192.168.14.%d" % i)
    ip_nums_file = open(r'ip_nums_file', 'a')
    last_time = 100
    # while last_time:
    # print ips
    used_ip = []
    for each in ips:
        t = threading.Timer(0, ping, args=[each, used_ip])
        t.start()
    # ping("192.168.14.1")

    txt = "at " + time.ctime() + ' total used ip is ' + str(len(used_ip)) + '\n'

    print txt,
    if is_off_line(len(used_ip), 10):
        print "the net work is down...."
        ip_nums_file.write(txt + "the network may be down!")
    # print used_ip
    tmp = [int(re.search("\d+$", each).group()) for each in used_ip]
    print tmp

    tmp = np.zeros(16 * 16)
    for each in get_ip_last_num(used_ip):
        tmp[each] = 1
    # fig = plt.figure()
    # ax = fig.add_subplot(111, projection='3d')

    # print tmp
    # ax.bar3d(range(16)*16, get_y(), np.zeros(16*16), 1, 1, tmp, 'b', alpha=0.8)
    #
    # fig.show()

    mlab.barchart(range(16) * 16, get_y(), tmp + 0.01)
    # last_time = last_time - 1

    #必须加入show()才能正常显示。。
    mlab.show()

    #     sleep(30)
    # ip_nums_file.close()

    # while (1):
    # g = IP2MAC()
    # for each in used_ip:
    # print each, g.getMac(each)

    # # used_ip.sort()
    # for each in used_ip:
    #     print each