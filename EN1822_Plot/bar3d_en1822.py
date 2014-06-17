#-*- coding:utf-8 -*-
#!/usr/bin/env python

__author__ = 'aaqqxx'

'''
用于处理EN1822程序中，生成的下游粒子数3D柱状图。
'''
import matplotlib
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patches import Rectangle
import sys
from time import sleep


#plt.ion() # set plot to animated


def plot_bar3_en1822(data_all):
    xx = data_all[:, 0]
    yy = data_all[:, 1]
    zz = data_all[:, 2]

    fig = plt.figure()
    fig.show()
    #ax1=fig.add_subplot(121)
    #ax1.plot(zz)
    #ax1.bar(np.arange(zz.shape[0]),zz)
    #ax2=fig.add_subplot(122,projection='3d')
    ax2 = fig.add_subplot(111, projection='3d')
    ax2.bar3d(xx, yy, np.zeros(xx.shape[0]), 1, 1, zz, 'b', alpha=0.8)

    print len(zz),zz.shape
    for each in xrange(len(zz)):
        fig.canvas.draw()
        #sleep(0.5)
        zz += 100
        print "zz[%d]" % each,zz[each]
        ax2.bar3d(xx, yy, np.zeros(xx.shape[0]), 1, 1, zz, 'b', alpha=0.8)

        #plt.show()
    #fig.show()


def plot_bar3_en1822_1(data_all):
    xx = data_all[:, 0]
    yy = data_all[:, 1]
    zz = data_all[:, 2]

    fig = plt.figure()
    fig.show()
    ax2 = fig.add_subplot(111, projection='3d')
    ax2.bar3d(xx, yy, np.zeros(xx.shape[0]), 1, 1, zz, 'b', alpha=0.8)
    # print len(zz),zz.shape
    # for each in xrange(len(zz)):
    #     plt.draw()
    #     #sleep(0.5)
    #     zz[each] += 100
    #     print "zz[%d]" % each,zz[each]
    #     ax2.bar3d(xx, yy, np.zeros(xx.shape[0]), 1, 1, zz, 'b', alpha=0.8)

    plt.show()
    #fig.show()

if __name__ == '__main__':
    if len(sys.argv) == 1:
        for each in sys.argv:
            print len(sys.argv), each
        data_all = np.loadtxt(ur'.\Data8H55M37S.txt')
    else:
        data_all = np.loadtxt(sys.argv[1])

    #用于模拟扫描到45%时的3D柱状图效果。
    for each in range(len(data_all)):
        if each>len(data_all)*0.45:
            # print data_all[each][2]
            data_all[each][2]=0.1  #等于0的时候有runtime warning
        else:
            data_all[each][2]= data_all[each][2] +30


    plot_bar3_en1822_1(data_all)





