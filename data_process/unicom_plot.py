# coding:utf-8
#!/usr/bin/env python

__author__ = 'XingHua'

"""

"""

import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import sys
from matplotlib import cm
from matplotlib.ticker import LinearLocator, FormatStrFormatter


if __name__ == "__main__":
    file_name = "tmp_data.txt"
    data = np.loadtxt(file_name, delimiter="\t", dtype=np.int8)
    data_res = []
    print data.shape
    print data[0]

    plt.imshow(data)
    plt.show()
    # for each in xrange(0,67*67*3):
    # data_res.append(data[])
    data_res = data.reshape(67, 67, 3, 3)
    print data_res[0][1]

    txt = ""
    for row in xrange(0, 67):
        for col in xrange(0, 67):
            # print tmp[row][0], tmp[row][1], tmp[row][2]
            for row_index in range(0, 3):
                for col_index in range(0, 3):
                    txt = txt + str((data_res[row][col][row_index][col_index])) + "\t"
                txt = txt + "\n"
        txt = txt + "\n"

    save_file = open("res_tmp1.txt", "w")
    save_file.write(txt)
    save_file.close()



    # x=np.vsplit(data,(13467+1)/2)
    # print x
    #
    # print x[0]
    # print x[1]
    # print x[2]
    # print x[3]

    # res = data.reshape(67*3,67*3)
    # print data.shape
    # plt.imshow(res)
    # plt.show()