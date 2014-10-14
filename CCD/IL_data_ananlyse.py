# coding:utf-8
#!/usr/bin/env python

__author__ = 'XingHua'

"""
分析word中得到的数据
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


if __name__ == "__main__":
    if len(sys.argv) == 2:
        filename = sys.argv[1]
        print filename
    else:
        filename = ur'.\IL_data.txt'

    data_raw = np.loadtxt(filename, skiprows=1, dtype=float)
    print data_raw.shape
    data_for_plot = data_raw[:, range(1, 12)]
    X = np.array(open(filename).readline().split(), dtype=float)
    Y = data_raw[:, 0]
    X, Y = np.meshgrid(X, Y)
    Z = data_raw[:,range(1,data_raw.shape[1]-1)]
    print X, '\n', Y,'\n', Z[0]


    Y_profile_for_plot = []
    for each in range(data_for_plot.shape[0]):
        Y_profile_for_plot.append(data_for_plot[each, :].mean())
    Y_pos =data_raw[:,0]
    print "Y_profile_for_plot, Y_pos is :\n", Y_profile_for_plot, Y_pos
    print len(Y_profile_for_plot), len(Y_pos)
    plt.plot(Y_pos, Y_profile_for_plot)
    plt.xlabel("Y avg profile")

    fig = plt.figure()
    ax = Axes3D(fig)
    ax.plot_wireframe(X, Y, data_for_plot * z_factor)
    plt.xlabel("x (mm)")
    plt.ylabel("y (mm)")
    ax.view_init(45, 45)
    ax.set_zlabel(r"Ophir/EDU")

    plt.show()