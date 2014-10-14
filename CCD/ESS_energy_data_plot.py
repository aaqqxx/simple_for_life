# coding:utf-8
#!/usr/bin/env python

__author__ = 'XingHua'

"""

"""

import numpy as np
# from mayavi import mlab
import sys

import matplotlib
matplotlib.use('webagg')

from mpl_toolkits.mplot3d import Axes3D
# import numpy as np
import matplotlib.pyplot as plt

z_factor = 1
# 数据源为Ophir,EDU,BMU。
data_source_num = 3
skiprows = 25
OEB_list_start_num = 4



# def is_reject(data,data_all):
#
# return True

def reject_outliers(data_all):
    m = 2
    u = np.mean(data_all)
    s = np.std(data_all)
    # filtered = [e for e in data if (u - 2 * s < e < u + 2 * s)]
    filtered_index = [index for index, e in enumerate(data_all) if (u - m * s < e < u + m * s)]
    print 'filtere_index', filtered_index
    return filtered_index


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

    def list_all_member(self):
        for name, value in vars(self).items():
            print('%s=%s' % (name, value))


def point_num2list(point_num):
    return range(point_num * data_source_num, point_num * data_source_num + data_source_num)


def data_process(data_all, Sampling_cnt=10):
    res = []
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

        point_data = PointDataStruct(Energy_data_list[OEB_list_start_num:-1])
        point_data.OE = point_data.data_process()
        point_data.OEB_list = point_data.OEB_list_reject_outliers()
        # point_data.pos=0
        # point_data.OEB_list = Energy_data_list
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
        self.Ophir_avg = 0
        self.EDU_avg = 0
        self.BMU_avg = 0
        # self.OEB_list = OEB_list  # Energy_data
        self.OEB_list = OEB_list
        self.OEB_list_for_avg = self.OEB_list_reject_outliers()
        # print '@@@@@',len(self.OEB_list)
        # self.OEB_list_reject_outliers(OEB_list)
        # print "OEB list is ", OEB_list
        # print "len(OEB_list) IS ",len(OEB_list)
        self.get_all_avg()

    def get_all_avg(self):
        Ophir_list = []
        EDU_list = []
        BMU_list = []

        print "OEB_list_for_avg element len is", len(self.OEB_list_for_avg)
        for each in self.OEB_list_for_avg:
            Ophir_list.append(each.Ophir)
            EDU_list.append(each.EDU)
            BMU_list.append(each.BMU)

        Ophir_list = np.array(Ophir_list)
        EDU_list = np.array(EDU_list)
        BMU_list = np.array(BMU_list)
        self.Ophir_avg = Ophir_list.mean()
        self.EDU_avg = EDU_list.mean()
        self.BMU_avg = BMU_list.mean()
        print "Ophir_avg = ", Ophir_list.mean()
        print "self.EDU_avg = ", EDU_list.mean()
        print "self.BMU_avg = ", BMU_list.mean()


    def data_process(self):
        self.OE = 0
        for i in xrange(len(self.OEB_list)):
            self.OE += self.OEB_list[i].Ophir / self.OEB_list[i].EDU
        # print 'in data_process OE is',self.OE
        return self.OE


    def get_unusul_index(self, data_array):
        # print "Ophir data is", e
        unusual_index = []
        m = 2
        u = np.mean(data_array)
        s = np.std(data_array)
        for index, each in enumerate(data_array):
            if not (u - 2 * s < each < u + 2 * s):
                # print "OEB_list_reject_outliers index is ", index

                # Ophir_index.append(index)
                unusual_index.append(index)
        # 去除异常数据索引列表中相同的元素。
        unusual_index = list(set(unusual_index))
        unusual_index.sort()
        return unusual_index


    def OEB_list_reject_outliers(self):
        """
        共采样点数个数据。一个采样点3个数据，Ophir,EDU,BMU.
        处理OEB_list将异常点去除。返回之后的OEB_list.
        分别处理Ophir、EDU、BMU的数据，将各列表异常点的标号得到，然后对这些标号求并集。
        将得到的并集标号与整个标号求差集，得到正常数据的标号，最后分别将这些标号中的数据添加到新的列表中。
        :param OEB_list:
        :return:
        """
        # print len(OEB_list)

        unusual_index = []
        # Ophir_index = []
        # EDU_index = []
        # BMU_index = []

        raw_Ophir_list = []
        raw_EDU_list = []
        raw_BMU_list = []

        for each in self.OEB_list:
            raw_Ophir_list.append(each.Ophir)
            raw_EDU_list.append(each.EDU)
            raw_BMU_list.append(each.BMU)

        # print raw_Ophir_list

        data_list = [raw_Ophir_list, raw_EDU_list, raw_BMU_list]

        for e in data_list:
            """
            e分别为Ophir,EDU,BMU的采样点数个数据。
          """
            # print "Ophir data is", e
            unusual_index.extend(self.get_unusul_index(e))

        unusual_index = list(set(unusual_index))
        unusual_index.sort()

        if not len(unusual_index) == 0:
            print "unusual_index is ", unusual_index
        # print "OVER"

        offset = 0
        for unsusul in unusual_index:
            # print 'unsul is', unsusul
            # del OEB_list[ususul]
            self.OEB_list.pop(unsusul + offset)
            offset = offset - 1
        if not len(self.OEB_list) == 10:
            print "len(OEB_list)", len(self.OEB_list)
        return self.OEB_list

        # return self.OEB_list


def get_scan_param(file_name=ur'./ESS_energy_data'):
    fd = open(file_name, 'r')
    need_line = range(18, 27)
    data = []
    for each in range(1, 27):
        txt = fd.readline()
        if each in need_line:
            data.append(int(txt.split()[2]))
    scan_param = Scanning_param_struct()
    scan_param.X_scanning_step = data[0]
    scan_param.Y_scanning_step = data[1]
    scan_param.X_scanning_cnt = data[2]
    scan_param.Y_scanning_cnt = data[3]
    scan_param.X_scanning_start_position = data[4]
    scan_param.Y_scanning_start_position = data[5]
    scan_param.X_scanning_range = data[6]
    scan_param.Y_scanning_range = data[7]
    scan_param.Sampling_cnt = data[8]

    print "scan param is:\n", scan_param.list_all_member()
    return scan_param


if __name__ == "__main__":
    if len(sys.argv) == 2:
        filename = sys.argv[1]
        print filename
    else:
        filename = ur'./ESS_energy_data'

    # data_dict = {"OEB_list": range(0, data_source_num)}
    # print data_dict["OEB_list"]

    scan_param = get_scan_param(filename)

    cols = range(1, scan_param.Sampling_cnt + 1)
    # cols = range(1, 4)
    # Z_data = np.loadtxt(filename, skiprows=28, usecols=(), delimiter='\t', comments="#")
    Z_data = np.loadtxt(filename, skiprows=29, usecols=cols, delimiter='\t', unpack=False, comments="P")
    # print Z_data.shape, len(Z_data), type(Z_data)
    # print Z_data[point_num2list(1)]
    scan_data = data_process(Z_data)
    data_for_plot = []
    for each in scan_data:
        # data_for_plot.append(each.Ophir_avg)
        data_for_plot.append(each.OE)
    print data_for_plot, len(data_for_plot)

    # print Z_data[data_dict[0:data_source_num]
    data_for_plot = np.array(data_for_plot)
    # print data_for_plot.shape
    data_for_plot = data_for_plot.reshape(scan_param.Y_scanning_cnt, scan_param.X_scanning_cnt)
    # print data_for_plot
    # print data_for_plot.shape
    # X = np.arange(0, data_for_plot.shape[1] * scan_param.X_scanning_step, scan_param.X_scanning_step)
    # Y = np.arange(0, data_for_plot.shape[0] * scan_param.Y_scanning_step, scan_param.Y_scanning_step)

    # data_raw = np.loadtxt(r'e:\IL_data.txt', dtype=float)
    # data_for_plot = data_raw[:, range(1, 12)]

    X = np.linspace(scan_param.X_scanning_start_position,
                    scan_param.X_scanning_start_position - scan_param.X_scanning_range, scan_param.X_scanning_cnt)
    Y = np.linspace(scan_param.Y_scanning_start_position,
                    scan_param.Y_scanning_start_position + scan_param.Y_scanning_range, scan_param.Y_scanning_cnt)

    # Y_profile_for_plot = []
    # for each in range(data_for_plot.shape[0]):
    #     Y_profile_for_plot.append(data_for_plot[each, :].mean())
    # Y_pos =data_raw[:,0]
    # print "Y_profile_for_plot, Y_pos is :\n", Y_profile_for_plot, Y_pos
    # print len(Y_profile_for_plot), len(Y_pos)
    # plt.plot(Y_pos, Y_profile_for_plot)
    # plt.xlabel("Y avg profile")

    print "X Y", X, Y
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
    plt.xlabel("x (mm)")
    plt.ylabel("y (mm)")
    # ax.set_xlim()
    # ax.set_ylim()

    # 调整视角，使初始视角为我们想要的视角。X向左为正方向，Y向下为正方向。
    ax.view_init(30, 75)
    ax.set_zlabel(r"Ophir/EDU")

    plt.show()