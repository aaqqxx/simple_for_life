# coding:utf-8
#!/usr/bin/env python

__author__ = 'XingHua'

"""

"""

from mpl_toolkits.mplot3d import Axes3D
from matplotlib import cm
from matplotlib.ticker import LinearLocator, FormatStrFormatter
import matplotlib.pyplot as plt
import numpy as np
import sys

from a20140618_174809_483 import get_20140618_174809_483Data


# def get_data(file_name=ur'.\20140711_105711_789.txt'):
#     data_all = np.loadtxt(file_name)
#     return data_all
#     pass

if __name__ == "__main__":
    if len(sys.argv) == 2:
        filename= sys.argv[1]
        print filename
    else:
        filename=ur'.\20140711_105711_789.txt'

    Z_data = np.array(np.loadtxt(filename)).reshape(512, 512)
    fig = plt.figure()
    ax = fig.gca(projection='3d')
    X = np.arange(0, 512, 1)
    # print len(X)
    Y = np.arange(0, 512, 1)
    X, Y = np.meshgrid(X, Y)
    R = np.sqrt(X ** 2 + Y ** 2)
    Z = np.sin(R)
    surf = ax.plot_surface(X, Y, Z_data, rstride=1, cstride=1, cmap=cm.coolwarm,
                           linewidth=0, antialiased=False)
    # ax.set_zlim(-1.01, 1.01)

    ax.zaxis.set_major_locator(LinearLocator(10))
    ax.zaxis.set_major_formatter(FormatStrFormatter('%.02f'))

    fig.colorbar(surf, shrink=0.5, aspect=5)

    plt.show()