# coding:utf-8
#!/usr/bin/env python

__author__ = 'XingHua'

"""

"""

import numpy as np
from mayavi import mlab
import sys
from mpl_toolkits.mplot3d import Axes3D
# import numpy as np
import matplotlib.pyplot as plt

z_factor = 1
x_steps = 8
y_steps = 1

data_source_num = 3


def reject_outliers(data):
    m = 2
    u = np.mean(data)
    s = np.std(data)
    filtered = [e for e in data if (u - 2 * s < e < u + 2 * s)]
    return filtered


class Scanning_param_struct:
    def __init__(self):
        self.X_scanning_step = 8
        self.Y_scanning_step = 1
        self.X_scanning_cnt = 15
        self.Y_scanning_cnt = 51
        self.X_scanning_start_position = 0
        self.Y_scanning_start_position = 0
        self.X_scanning_range = 112
        self.Y_scanning_range = 50
        self.Sampling_cnt = 10


def point_num2list(point_num):
    return range(point_num * data_source_num, point_num * data_source_num + data_source_num)


def data_process(data_all, Sampling_cnt=10):
    # PointData 的list
    res = []
    # point_data_list=[]
    # point_data = PointDataStruct()
    print "point_num is", len(data_all) / Sampling_cnt / data_source_num
    data_all = np.array(data_all)
    print 'data_all.shape is', data_all.shape
    for each in xrange(np.array(data_all).shape[0] / data_source_num):
        Ophir = data_all[point_num2list(each)][0]
        EDU = data_all[point_num2list(each)][1]
        BMU = data_all[point_num2list(each)][2]
        # print Ophir
        Energy_data_list = []
        for i in xrange(len(Ophir)):
            Energy_data = Energy_data_struct()
            Energy_data.Ophir = Ophir[i]
            Energy_data.EDU = EDU[i]
            Energy_data.BMU = BMU[i]
            Energy_data_list.append(Energy_data)

        point_data = PointDataStruct(Energy_data_list)
        point_data.OE = point_data.data_process()
        # point_data.pos=0
        point_data.OEB_list = Energy_data_list
        res.append(point_data)
    # print len(res), res[0].OEB_list[0].Ophir, res[0].OEB_list[0].EDU, res[0].OEB_list[0].BMU, res[0].OE
    # print len(res), res[0].OEB_list[0].Ophir, res[0].OEB_list[0].EDU, res[0].OEB_list[0].BMU, res[1].OE
    return res


class Pos:
    def __init__(self):
        self.x = 0
        self.y = 0
        self.z = 0

    pass


class Energy_data_struct:
    def __init__(self):
        self.Ophir = 0.0
        self.EDU = 0.0
        self.BMU = 0.0


class PointDataStruct:
    """
    该点的所有信息:坐标，3个能量值，处理之后的OE（Ophir/EDU),采样点数个能量值(一个能量值对应3组数据，Ophir,EDU,BMU)。
    """

    def __init__(self, OEB_list):
        self.pos = Pos()
        self.OE = 0
        self.OEB_list = OEB_list  # Energy_data

    def data_process(self):
        self.OE = 0
        for i in xrange(len(self.OEB_list)):
            self.OE += self.OEB_list[i].Ophir / self.OEB_list[i].EDU
        # print 'in data_process OE is',self.OE
        return self.OE


if __name__ == "__main__":
    if len(sys.argv) == 2:
        filename = sys.argv[1]
        print filename
    else:
        filename = ur'./Z_scan_data'

    data_dict = {"OEB_list": range(0, data_source_num)}
    print data_dict["OEB_list"]

    cols = range(1, 11)
    # cols = range(1, 4)
    # Z_data = np.loadtxt(filename, skiprows=28, usecols=(), delimiter='\t', comments="#")
    Z_data = np.loadtxt(filename, skiprows=28, usecols=cols, delimiter='\t', unpack=False, comments="P")
    print Z_data.shape, len(Z_data), type(Z_data)
    print Z_data[point_num2list(1)]
    scan_data = data_process(Z_data)
    data_for_plot = []
    for each in scan_data:
        data_for_plot.append(each.OE)
    print data_for_plot, len(data_for_plot)

    # print Z_data[data_dict[0:data_source_num]
    data_for_plot = np.array(data_for_plot)
    print data_for_plot.shape
    data_for_plot = data_for_plot.reshape(51, 15)
    print data_for_plot
    print data_for_plot.shape
    X = np.arange(0, data_for_plot.shape[1] * x_steps, x_steps)
    Y = np.arange(0, data_for_plot.shape[0] * y_steps, y_steps)
    X, Y = np.meshgrid(X, Y)
    # pl = mlab.surf(X, Y, data_for_plot*z_factor, warp_scale="auto")
    # pl = mlab.surf(X, Y, data_for_plot*z_factor)
    # s = mlab.mesh(X, Y, data_for_plot*z_factor,  line_width=1.0 )
    # p = mlab.mesh(X, Y, data_for_plot * z_factor, representation="wireframe", line_width=1.0)
    # # mlab.axes(xlabel='x', ylabel='y', zlabel='z')
    # mlab.show()

    fig = plt.figure()
    ax = Axes3D(fig)
    ax.plot_wireframe(X, Y, data_for_plot * z_factor)
    plt.show()