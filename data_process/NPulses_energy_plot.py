# coding:utf-8
#!/usr/bin/env python

__author__ = 'XingHua'
__author__ = 'aaqqxx'

"""

分析对象： ESS_energy_data
具体对象： Y的一行，大约51个点
        或者X的一行，大约最多120个点
        只分析某行或者某列

Pos_X65_Y40
Pos_X-65_Y-30


Pos_-65_30_10_Ophir
Pos_-65_30_10_EDU
Pos_-65_30_10_BMU1
Pos_-65_30_10_BMU2

+P
-N




"""

import numpy as np
# from mayavi import mlab
import sys
from mpl_toolkits.mplot3d import Axes3D
# import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import CheckButtons
from ESS_energy_data_plot import get_scan_param, Scanning_params_data_struct, cmp_data_point_pos


z_factor = 100000000 * 5

# 数据源为Ophir,EDU,BMU。
data_source_num = 3
skiprows = 25
OEBlist_skip_cols = 0



# def is_reject(data,data_all):
#
# return True

def reject_outliers(data_all):
    m = 0.01
    u = np.mean(data_all)
    s = np.std(data_all)
    # filtered = [e for e in data if (u - 2 * s < e < u + 2 * s)]
    filtered_index = [index for index, e in enumerate(data_all) if (u - m * s < e < u + m * s)]
    print 'filtere_index', filtered_index
    return filtered_index


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


        # x_pos = scan_param.X_scanning_start_position
        # y_pos = scan_param.Y_scanning_start_position + scan_param.Y_scanning_step*each
        # z_pos = 58.3
        # point_data = PointDataStruct(Energy_data_list,x_pos,y_pos,z_pos)

        point_data = PointDataStruct(Energy_data_list)
        point_data.OE = point_data.get_OE()

        # point_data.OEB_list = point_data.OEB_list_reject_outliers()
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


def get_unusul_index(data_array):
    # print "Ophir data is", e
    unusual_index = []
    m = 1
    u = np.mean(data_array)
    s = np.std(data_array)
    for index, each in enumerate(data_array):
        if not (u - m * s < each < u + m * s):
            # print "OEB_list_reject_outliers index is ", index

            # Ophir_index.append(index)
            unusual_index.append(index)
    # 去除异常数据索引列表中相同的元素。
    unusual_index = list(set(unusual_index))
    unusual_index.sort()
    return unusual_index


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
        self.Ophir_list = []
        self.EDU_list = []
        self.BMU_list = []
        # self.OEB_list = OEB_list  # Energy_data
        self.OEB_list = OEB_list
        # self.skiped_OEB_list = OEB_list[OEBlist_skip_cols:-1]
        # self.OEB_list_for_get_unusul_index = OEB_list[OEBlist_skip_cols:-1]
        # print 'len(OEB_list) ==', len(self.OEB_list)
        self.OEB_list_for_avg = OEB_list
        # print '@@@@@',len(self.OEB_list)
        # self.OEB_list_reject_outliers(OEB_list)
        # print "OEB list is ", OEB_list
        # print "len(OEB_list) IS ",len(OEB_list)
        self.get_all_avg()

    def get_all_avg(self):


        print "OEB_list_for_avg element len is", len(self.OEB_list_for_avg)
        for each in self.OEB_list_for_avg:
            self.Ophir_list.append(each.Ophir)
            self.EDU_list.append(each.EDU)
            self.BMU_list.append(each.BMU)

        self.Ophir_list = np.array(self.Ophir_list)
        self.EDU_list = np.array(self.EDU_list)
        self.BMU_list = np.array(self.BMU_list)
        self.Ophir_avg = self.Ophir_list.mean()
        self.EDU_avg = self.EDU_list.mean()
        self.BMU_avg = self.BMU_list.mean()
        print "Ophir_avg = ", self.Ophir_list.mean()
        print "self.EDU_avg = ", self.EDU_list.mean()
        print "self.BMU_avg = ", self.BMU_list.mean()


    def get_OE(self):
        self.OE = 0
        for i in xrange(len(self.OEB_list)):
            self.OE += self.OEB_list[i].Ophir / self.OEB_list[i].EDU
        # print 'in data_process OE is',self.OE
        return self.OE
        pass

    def OEB_list_reject_outliers(self, OEB_list_for_reject):
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

        for each in OEB_list_for_reject:
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
            OEB_list_for_reject.pop(unsusul + offset)
            offset = offset - 1
        if not len(OEB_list_for_reject) == 10:
            print "len(OEB_list)", len(OEB_list_for_reject)
        return OEB_list_for_reject

        # return self.OEB_list


def pos2point(pos, start=-65, step=1):
    res = pos - start
    return res


def get_index_from_label(label, scan_dir=0 ,start_pos=-30):
    # scan_dir=0为Y方向， =1 为X方向
    # pos = int(label[4:-3])
    index = int(float(label.split("_")[2]))
    # index = int(label[4:-2])

    # if scan_dir==0:
    # index = pos-scan_param.Y_scanning_start_position/scan_param.Y_scanning_step
    # elif scan_dir==1:
    # index = pos-scan_param.X_scanning_start_position/scan_param.X_scanning_step
    # else:
    # print "Error in get_index_from_label"
    # index = -1
    return np.abs(index - start_pos)


def show_line(label, lines=1):
    lines = zzz.get_lines()
    index = int(get_index_from_label(label))
    print "index,label is", index, label
    print dir(lines[index])
    print lines[index].get_ydata()
    lines[index].set_visible(not lines[index].get_visible())

    plt.draw()


if __name__ == "__main__":
    if len(sys.argv) == 2:
        filename = sys.argv[1]
        print filename
    else:
        filename = ur'data/20141020/ESS_energy_data20141020_4'

    sdata = Scanning_params_data_struct()
    sdata.init_data(filename)
    sdata.data.sort(cmp_data_point_pos)

    sdata.skip_first_N_pulses(0)
    # sdata.outlier_rejection()

    scan_param = get_scan_param(filename)
    cols = range(1, int(scan_param.Sampling_pulse_cnt + 1))

    X = []
    Y = []
    Z = []

    print "-----" * 50, "\n", sdata.data[0].pos, len(sdata.data), sdata.data[0].pos[0], dir(sdata.data[0])

    print "+" * 50, "\n", len(sdata.data[0].raw_Ophir), sdata.data[0].raw_Ophir
    for each in sdata.data:
        X.append(each.pos[0])
        Y.append(each.pos[1])
        Z.append(each.pos[2])

    print "Ophir", sdata.data[0].raw_Ophir
    print "EDU", sdata.data[0].raw_EDU
    plt.plot(sdata.data[0].raw_Ophir, label="Ophir", )
    # plt.plot(sdata.data[0].raw_EDU,label="EDU")
    plt.legend()
    plt.show()


    main_labels = ['Pos_' + str(x) + "_" + str(y) for x in X for y in Y]
    labels = ['Pos_' + str(x) + "_" + str(y) + "_" + name for x in X for y in Y for name in
              ["Ophir", "EDU", "BMU1", "BMU2"]]
    visiable_status = []

    for x in X:
        for y in Y:
            for name in ["Ophir", "EDU", "BMU1", "BMU2"]:
                visiable_status.append(False)

    print visiable_status

    for index, each in enumerate(sdata.data):
        plt.plot(each.raw_Ophir, label=labels[index] + "_Ophir", visible=False)
        plt.plot(each.raw_EDU, label=labels[index] + " _EDU", visible=False)
        plt.plot(each.raw_BMU1, label=labels[index] + "_BMU1", visible=False)
        plt.plot(each.raw_BMU2, label=labels[index] + "_BMU2", visible=False)
    # plt.legend()
    # plt.show()

    print "labels is ", len(labels),labels
    print "visiable_status len is ",len(visiable_status),visiable_status
    zzz = plt.gca()

    print zzz.get_lines()
    # plt.subplots_adjust(left=0.3)
    # rax = plt.axes([0.05,0.4,0.1,0.15])
    rax1 = plt.axes([0.005, 0.4, 0.1, 0.15])

    # rax2 = plt.axes([0.1, 0.1, 0.07, 0.8])
    plt.subplots_adjust(left=0.3)

    print "len(main_labels) is ",len(main_labels)
    check1 = CheckButtons(rax1, main_labels[:len(main_labels) / 12], visiable_status[:len(main_labels) / 12])
    # check2 = CheckButtons(rax2, main_labels[len(main_labels) / 12:], visiable_status[len(main_labels) / 12:])
    check1.on_clicked(show_line)
    # check2.on_clicked(show_line)

    # plt.legend()

    plt.show()


