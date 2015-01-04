# coding:utf-8
#!/usr/bin/env python

__author__ = 'XingHua'

"""

"""

import numpy as np
import matplotlib.pyplot as plt
import logging
from mpl_toolkits.mplot3d import Axes3D
# from mayavi import mlab
import sys



logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',
                    datefmt='%a, %d %b %Y %H:%M:%S',
                    filename='myapp.log',
                    filemode='w')

logging.debug('This is debug message')
logging.info('This is info message')
logging.warning('This is warning message')


z_factor = 100000

class Scanning_param_struct:
    def __init__(self):
        self.X_scanning_start_position = 56
        self.Y_scanning_start_position = -25
        self.Z_scanning_start_position = 0
        self.X_scanning_end_position = -56
        self.Y_scanning_end_position = 25
        self.Z_scanning_end_position = 0
        self.X_scanning_step = 8
        self.Y_scanning_step = 1
        self.Z_scanning_step = 0
        self.X_scanning_cnt = 15
        self.Y_scanning_cnt = 51
        self.Z_scanning_cnt = 0
        self.Sampling_pulse_cnt = 5


    def list_all_member(self):
        for name, value in vars(self).items():
            print('%s=%s' % (name, value))


def get_scan_param(file_name=ur'./ESS_energy_data'):
    fd = open(file_name, 'r')
    need_line = range(22, 35)
    data = []
    for each in range(1, 35):
        txt = fd.readline()
        if each in need_line:
            data.append(float(txt.split()[2]))
    scan_param = Scanning_param_struct()
    scan_param.X_scanning_start_position = data[0]
    scan_param.Y_scanning_start_position = data[1]
    scan_param.Z_scanning_start_position = data[2]
    scan_param.X_scanning_end_position = data[3]
    scan_param.Y_scanning_end_position = data[4]
    scan_param.Z_scanning_end_position = data[5]
    scan_param.X_scanning_step = data[6]
    scan_param.Y_scanning_step = data[7]
    scan_param.Z_scanning_step = data[8]
    scan_param.X_scanning_cnt = int(data[9])
    scan_param.Y_scanning_cnt = int(data[10])
    scan_param.Z_scanning_cnt = int(data[11])
    scan_param.Sampling_pulse_cnt = int(data[12])

    print "scan param is:\n", scan_param.list_all_member()
    # print "###"
    return scan_param


class Scanning_params_data_struct:
    """
    代表整个数据文件，里面有数据文件中的原始数据，也有处理后的数据
    """

    def __init__(self):
        self.X_step = 8
        self.Y_step = 1
        self.Z_step = 0

        self.X_start_position = 0
        self.Y_start_position = 0
        self.Z_start_position = 0
        self.X_end_position = 0
        self.Y_end_position = 0
        self.Z_end_position = 0

        self.X_cnt = 15
        self.Y_cnt = 51
        self.Z_cnt = 0

        self.Sampling_pulse_cnt = 10

        self.data = []

    def init_data(self, filename):
        """
        把所有的原始数据字段都填充，需要数据处理的字段不在此函数中进行
        """
        # pos_all = np.loadtxt(filename, skiprows=25, delimiter='\t', usecols=(1, 2, 3), unpack=False, comments="_",
        # dtype=float)
        #
        # logging.info('pos_all is \n %s' % pos_all, )

        scanning_params = get_scan_param(filename)
        self.X_cnt = scanning_params.X_scanning_cnt
        self.Y_cnt = scanning_params.Y_scanning_cnt
        self.Z_cnt = scanning_params.Z_scanning_cnt
        self.X_start_position = scanning_params.X_scanning_start_position
        self.Y_start_position = scanning_params.Y_scanning_start_position
        self.Z_start_position = scanning_params.Z_scanning_start_position
        self.X_end_position = scanning_params.X_scanning_end_position
        self.Y_end_position = scanning_params.Y_scanning_end_position
        self.Z_end_position = scanning_params.Z_scanning_end_position
        self.X_step = scanning_params.X_scanning_step
        self.Y_step = scanning_params.Y_scanning_step
        self.Z_step = scanning_params.Z_scanning_step
        # cols = range(1, int(scanning_params.Sampling_pulses_cnt) + 1)

        # Sampling_pulse_cnt= scanning_params.Sampling_pulse_cnt

        data_all = np.loadtxt(filename, skiprows=38, delimiter='\t',
                              usecols=range(0, int(scanning_params.Sampling_pulse_cnt) * 4 + 3), unpack=False,
                              dtype=float)
        # print data_all.shape, data_all[0]

        for index, each in enumerate(data_all):
            offset = 0
            raw_Ophir_list = []
            raw_EDU_list = []
            raw_BMU1_list = []
            raw_BMU2_list = []
            for i in xrange(0, int(scanning_params.Sampling_pulse_cnt)):
                # print 3+offset,each[3+offset]
                raw_Ophir_list.append(each[3 + offset])
                raw_EDU_list.append(each[4 + offset])
                raw_BMU1_list.append(each[5 + offset])
                raw_BMU2_list.append(each[6 + offset])
                offset = offset + 4
                # print "offset is",offset
            # print raw_Ophir_list
            point_data = PointDataStruct(each[0:3], raw_Ophir_list, raw_EDU_list,
                                         raw_BMU1_list, raw_BMU2_list)


            self.data.append(point_data)
        pass




    def get_point_data(self, Pos):
        """
        获取某一个位置的所有数据，即获取一个 PointDataStruct 结构
        """
        # print "Pos is", Pos
        for each in self.data:
            # print each, each.pos,
            if Pos[0] == each.pos[0] and Pos[1] == each.pos[1] and Pos[2] == each.pos[2]:
                # print self.data[0].pos,self.data[0].raw_Ophir
                # print each.raw_Ophir
                return each
            else:
                # print "pos not right"
                pass

        pass

    def get_surface_data(self,dir,pos):
        res = []
        if "x" == dir:
            for each in self.data:
                if pos == each.pos[0]:
                    res.append(each)
        if "y" == dir:
            for each in self.data:
                if pos == each.pos[1]:
                    res.append(each)

        return np.array(res)

        pass

    def skip_first_N_pulses(self, num):
        """
        此函数将raw_data跳过头N列，然后将数据存入processed_data列表
        """
        for each in self.data:
            each.processed_Ophir = each.raw_Ophir[num:]
            each.processed_EDU = each.raw_EDU[num:]
            each.processed_BMU1 = each.raw_BMU1[num:]
            each.processed_BMU2 = each.raw_BMU2[num:]
        pass

    def outlier_rejection(self):
        """
        分析processed_data中的数据，剔除异常数值，处理后的数据仍然存在processed_data中，或者说覆盖掉处理前的processed_data
        """
        for each in self.data:
            each.inner_reject_outliers()


        pass


    def list_all_member(self):
        for name, value in vars(self).items():
            print('%s=%s' % (name, value))


# scanning_params



def cmp_data_point_pos(data_point1,data_point2):
    """
    对两个点进行比较，用于递增排序。
    :param data_point1:
    :param data_point2:
    :return:
    """

    data_point1=PointDataStruct(data_point1.pos,data_point1.raw_Ophir,data_point1.raw_EDU,data_point1.raw_BMU1,data_point1.raw_BMU2)
    data_point2=PointDataStruct(data_point2.pos,data_point2.raw_Ophir,data_point2.raw_EDU,data_point2.raw_BMU1,data_point2.raw_BMU2)
    x1=data_point1.pos[0]
    y1=data_point1.pos[1]
    x2=data_point2.pos[0]
    y2=data_point2.pos[1]

    if y1<y2:
        res = -1
    elif y1==y2:
        # res = -cmp(x1,x2)
        # 不要负号代表从小到大排序。
        res = cmp(x1, x2)
    else:
        res = 1
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
        self.BMU1 = 0.0
        self.BMU2 = 0.0


class PointDataStruct:
    """
    该点的所有信息:坐标，3个能量值，处理之后的OE（Ophir/EDU),采样点数个能量值(一个能量值对应3组数据，Ophir,EDU,BMU)。
    目前pos不是Pos的实例，而是一个含有3个元素的列表，分别包含了x,y,z的坐标信息。
    """

    def __init__(self, pos, Ophir, EDU, BMU1, BMU2):
        self.pos = pos

        self.raw_Ophir = Ophir
        self.raw_EDU = EDU
        self.raw_BMU1 = BMU1
        self.raw_BMU2 = BMU2

        # self.raw_OE = np.array(Ophir) / np.array(EDU)

        self.processed_Ophir = Ophir
        self.processed_EDU = EDU
        self.processed_BMU1 = BMU1
        self.processed_BMU2 = BMU2
        self.processed_OE = []


    def get_raw_Ophir_avg(self):
        return np.array(self.raw_Ophir).mean()
        pass

    def get_raw_EDU_avg(self):
        return np.array(self.raw_EDU).mean()
        pass

    def get_raw_BMU1_avg(self):
        return np.array(self.raw_BMU1).mean()
        pass

    def get_raw_BMU2_avg(self):
        return np.array(self.raw_BMU2).mean()
        pass

    def get_raw_OE_avg(self):
        return np.array(self.raw_Ophir) / np.array(self.raw_EDU)
        pass

    def get_processed_Ophir_avg(self):
        # print "np.array(self.processed_Ophir).mean() is",np.array(self.processed_Ophir).mean()
        return np.array(self.processed_Ophir).mean()
        pass

    def get_processed_EDU_avg(self):
        return np.array(self.processed_EDU).mean()
        pass

    def get_processed_BMU1_avg(self):
        return np.array(self.processed_BMU1).mean()
        pass

    def get_processed_BMU2_avg(self):
        return np.array(self.processed_BMU2).mean()
        pass

    def get_processed_OE_avg(self):
        return np.array(self.processed_Ophir) / np.array(self.processed_EDU)
        pass

    def skip_first_N_pulses(self, num):
        """
        此函数将raw_data跳过头N列，然后将数据存入processed_data列表
        """
        self.processed_Ophir = self.raw_Ophir[num:]
        self.processed_EDU = self.raw_EDU[num:]
        self.processed_BMU1 = self.raw_BMU1[num:]
        self.processed_BMU2 = self.raw_BMU2[num:]
        # self.processed_OE = self.raw_Ophir[num:]
        pass

    def outlier_rejection(self):
        """

        """

        pass



    def get_unusul_index(self, data_array):
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



    def inner_reject_outliers(self):
        """
        分析processed_data中的数据，剔除异常数值，处理后的数据仍然存在processed_data中，或者说覆盖掉处理前的processed_data
        共采样点数个数据。一个采样点3个数据，Ophir,EDU,BMU1,BMU2
        处理OEB_list将异常点去除。返回之后的OEB_list.
        分别处理Ophir、EDU、BMU的数据，将各列表异常点的标号得到，然后对这些标号求并集。
        将得到的并集标号与整个标号求差集，得到正常数据的标号，最后分别将这些标号中的数据添加到新的列表中。
        :param OEB_list:
        :return:
        """
        # print len(OEB_list)

        unusual_index = []
        processed_Ophir_list_len = len(self.processed_Ophir)
        # Ophir_index = []
        # EDU_index = []
        # BMU_index = []
        # print raw_Ophir_list

        # data_list = [self.processed_Ophir, self.processed_EDU, self.processed_BMU1, self.processed_BMU2]
        data_list = [self.processed_EDU]

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
            # self.OEB_list.pop(unsusul + offset)
            self.processed_Ophir.pop(unsusul + offset)
            self.processed_EDU.pop(unsusul + offset)
            self.processed_BMU1.pop(unsusul + offset)
            self.processed_BMU2.pop(unsusul + offset)
            offset = offset - 1
        if not len(self.processed_Ophir) == processed_Ophir_list_len:
            print "processed_Ophir_list_len before is %d,then is %d"% (processed_Ophir_list_len,len(self.processed_Ophir))
        # return self.OEB_list
        print "OEB_list_reject_outliers over"



if __name__ == "__main__":
    if len(sys.argv) == 2:
        filename = sys.argv[1]
        print filename
    else:
        # filename = ur'./data/20141024/EDU_Ophir_NPulse_energy_data_20141024_4'
        #filename = ur'/home/aaqqxx/IL/server/data_analysis/data/20141024/ESS_energy_data20141024_PM7_bak'
        filename = ur'./data/20141025/ESS_energy_data20141025_1'

    sdata = Scanning_params_data_struct()
    sdata.init_data(filename)
    sdata.data.sort(cmp_data_point_pos)


    sdata.skip_first_N_pulses(0)
    sdata.outlier_rejection()

    # pos1.z = 0
    # print "sdata.get_point_data(-65,-10,0) is ",sdata.get_point_data([-65,-10,0]).raw_EDU,sdata.get_point_data([-65,-10,0]).raw_Ophir
    #
    # plt.plot(sdata.get_point_data([-65,10,0]).raw_EDU,label="EDU")
    # plt.plot(sdata.get_point_data([-65,10,0]).raw_Ophir,label="Ophir")
    # plt.legend()
    # plt.show()

#    for each in sdata:
#        if

    #point_data = sdata.get_point_data([-56, 5, 0])
    #print "point_data is", point_data.raw_Ophir


    # 所有位置处,Z方向目前不做处理。。。。。仅关心X，Y坐标。
    # X=[]
    # Y=[]
    # Z=[]
    raw_Ophir_avg_list = []
    raw_EDU_avg_list = []
    raw_BMU1_avg_list = []
    raw_BMU2_avg_list = []
    raw_OE_avg_list = []

    processed_Ophir_avg_list = []
    processed_EDU_avg_list = []
    processed_BMU1_avg_list = []
    processed_BMU2_avg_list = []
    processed_OE_avg_list = []


    # 某位置处的Ophir,EDU,BMU1,BMU2,OE的能量列表。
    raw_Ophir_list = []
    raw_EDU_list = []
    raw_BMU1_list = []
    raw_BMU2_list = []
    raw_OE_list = []

    processed_Ophir_list = []
    processed_EDU_list = []
    processed_BMU1_list = []
    processed_BMU2_list = []
    processed_OE_list = []

    X = []
    Y = []
    Z = []

    # print sdata.data[0].pos, len(sdata.data), sdata.data[0].pos[0],dir(sdata.data[0])

    for each in sdata.data:
        X.append(each.pos[0])
        Y.append(each.pos[1])
        Z.append(each.pos[2])

        raw_Ophir_avg_list.append(each.get_raw_Ophir_avg())
        raw_EDU_avg_list.append(each.get_raw_EDU_avg())
        raw_BMU1_avg_list.append(each.get_raw_BMU1_avg())
        raw_BMU2_avg_list.append(each.get_raw_BMU2_avg())

        raw_OE_avg_list.append(each.get_raw_Ophir_avg()/each.get_raw_EDU_avg())

        processed_Ophir_avg_list.append(each.get_processed_Ophir_avg())
        processed_EDU_avg_list.append(each.get_processed_EDU_avg())
        processed_BMU1_avg_list.append(each.get_processed_BMU1_avg())
        processed_BMU2_avg_list.append(each.get_processed_BMU2_avg())
        processed_OE_avg_list.append(each.get_processed_Ophir_avg()/each.get_processed_EDU_avg())



    fig = plt.figure()
    ax = Axes3D(fig)

    # X = np.linspace(-56,56,15)
    # Y = np.linspace(-25,25,51)
    # X= np.arange(56,-57,-8)
    # X= np.arange(56,-57,-8)
    # Y=np.arange(-25,26,1)

    # X,Y = np.meshgrid(X,Y)
    # print "X Y is",X,Y
    X = np.array(X)
    Y= np.array(Y)


    raw_Ophir_avg_list = np.array(raw_Ophir_avg_list)
    processed_Ophir_avg_list = np.array(processed_Ophir_avg_list)
    raw_EDU_avg_list = np.array(raw_EDU_avg_list)
    raw_OE_avg_list = np.array(raw_OE_avg_list)
    processed_OE_avg_list = np.array(processed_OE_avg_list)
    processed_EDU_avg_list = np.array(processed_EDU_avg_list)

    # print sdata.Y_cnt,sdata.X_cnt
    X=X.reshape(sdata.Y_cnt,sdata.X_cnt)
    Y=Y.reshape(sdata.Y_cnt,sdata.X_cnt)
    raw_Ophir_avg_list=raw_Ophir_avg_list.reshape(sdata.Y_cnt,sdata.X_cnt)
    raw_EDU_avg_list = raw_EDU_avg_list.reshape(sdata.Y_cnt,sdata.X_cnt)
    raw_OE_avg_list = raw_OE_avg_list.reshape(sdata.Y_cnt,sdata.X_cnt)
    processed_OE_avg_list = processed_OE_avg_list.reshape(sdata.Y_cnt,sdata.X_cnt)
    processed_EDU_avg_list = processed_EDU_avg_list.reshape(sdata.Y_cnt,sdata.X_cnt)

    processed_Ophir_avg_list = processed_Ophir_avg_list.reshape(sdata.Y_cnt,sdata.X_cnt)
    # print "@@@@@@@@@\n",X.shape,Y.shape
    # ax.plot_wireframe(X.reshape(51,15), Y.reshape(51,15), np.array(raw_Ophir_avg_list).reshape(51,15))
    # ax.plot_wireframe(X.reshape(-1), Y.reshape(-1), raw_Ophir_avg_list)
    # ax.plot_surface(X, Y, np.array(raw_Ophir_avg_list)*100)
    # ax.scatter3D(X.reshape(-1), Y.reshape(-1), np.array(raw_Ophir_avg_list)*100)


    #print processed_OE_avg_list[5:],"\n",processed_OE_avg_list,"\n",processed_OE_avg_list.shape
    #print X[5:]
    #print Y[5:]
    #ax.plot_wireframe(X[:], Y[:], processed_Ophir_avg_list[:],color="r",label="Ophir")


    #ax.plot_wireframe(X[:], Y[:], processed_EDU_avg_list[:],color="g",label="EDU")

    #ax.plot_wireframe(X[:], Y[:], processed_OE_avg_list[:],color="b",label="OE")

    print Y
    # ax.plot_wireframe(X, Y, raw_OE_avg_list, color="r", label="OE")
    ax.plot_wireframe(X.reshape(-1), Y.reshape(-1), raw_OE_avg_list.reshape(-1), color="r", label="OE")
    # ax.plot_wireframe(X, Y, raw_Ophir_avg_list+1.5, color="b", label="Ophir")
    # ax.plot_wireframe(X, Y, raw_EDU_avg_list+2.5, color="g", label="EDU")

    #ax.plot_wireframe(X, Y, processed_OE_avg_list, color="r", label="OE")
    #ax.plot_wireframe(X, Y, processed_Ophir_avg_list, color="b", label="Ophir")
    #ax.plot_wireframe(X, Y, processed_EDU_avg_list, color="g", label="EDU")

    # print "process OE avg list is",processed_OE_avg_list
    print "raw_OE_avg_list.min() is ",raw_OE_avg_list.min(),raw_OE_avg_list.argmin(),X.reshape(-1)[raw_OE_avg_list.argmin()],Y.reshape(-1)[raw_OE_avg_list.argmin()]
    print "mean = ",processed_OE_avg_list[:].mean()
    print "std = ", processed_OE_avg_list[:].std()
    print "std/mean = ", processed_OE_avg_list[:].std()/processed_OE_avg_list[:].mean()

    txt = "mean = "+str(processed_OE_avg_list[:].mean())+"  std = "+ str(processed_OE_avg_list[:].std())+"  std/mean = "+str(processed_OE_avg_list[:].std()/processed_OE_avg_list[:].mean())


    ax.set_xlabel("x")
    ax.set_ylabel("y")
    ax.set_title(txt)
    ax.set_zlabel("intensity")

    ax.set_xlim(-65,65)
    ax.set_ylim(-25,25)
    ax.view_init(azim= -113, elev=25)

    print "processed_OE_avg_list.shape is ",processed_OE_avg_list.shape
    plt.legend()
    plt.show()

    res = []
    for each in processed_OE_avg_list:
        res.append(each.sum())
    print len(res),res
    plt.plot(Y[:,0],res,"-*",markersize=14)
    plt.xlabel(r"Y(mm)")
    plt.ylabel(r"Energy")
    plt.show()

    # plt.plot(processed_OE_avg_list[6],label="")

    # plt.plot(processed_OE_avg_list[5])
    # plt.show()

    # print len(raw_Ophir_avg_list)

    # p = mlab.mesh(X, Y, raw_Ophir_avg_list*100, representation="wireframe", line_width=1.0)
    # mlab.axes(xlabel='x', ylabel='y', zlabel='z')
    # mlab.show()



    # print raw_Ophir_avg_list





