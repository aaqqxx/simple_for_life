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
from PIL import Image
from mayavi import mlab


# def get_data(file_name=ur'.\20140711_105711_789.txt'):
# data_all = np.loadtxt(file_name)
# return data_all
#     pass

def get_data_from_png(file_name):
    # res = []
    im = Image.open(file_name)
    print im.mode, im.size, im.format
    print dir(im)

    # im.show()
    # data.save("tmp.png")
    # print dir(im)
    data = list(im.getdata())
    # print data[0:10]
    #print dir(data)
    data = np.array(data)
    # for each in data:
    #     res.append(each.mean())
    return data


if __name__ == "__main__":
    if len(sys.argv) == 2:
        filename = sys.argv[1]
        print filename
    else:
        # filename=ur'.\20140711_105711_789.txt'
        filename = r"WineBottle.png"
    # Z_data = np.array(np.loadtxt(filename)).reshape(512, 512)
    Z_data = np.array(get_data_from_png(filename))
    Z_data_fft = []
    Z_data_freq = []

    # fig = plt.figure()
    # ax = fig.gca(projection='3d')
    X = np.arange(0, 577, 1)
    # X = np.linspace(0, 40, 577)
    # print len(X)
    Y = np.arange(0, 723, 1)
    X, Y = np.meshgrid(X, Y)
    # R = np.sqrt(X ** 2 + Y ** 2)
    # Z = np.sin(R)

    # for index, each in enumerate(Z_data):
    #     if each > 150:
    #         Z_data[index] = 150
    print X.shape, Y.shape, Z_data.shape

    for each in Z_data.reshape(723, 577):
        Z_data_fft.append(np.fft.fftshift(np.fft.fft(each)).real)
        # Z_data_freq.append(np.fft.fftfreq(each))


    Z_data_fft = np.log(np.array(Z_data_fft).reshape(-1))
    # Z_data_fft = np.array(Z_data_fft).reshape(-1)
    for index, each in enumerate(Z_data_fft):
        if each > 147135 * 0.01:
            Z_data_fft[index] = 147135 * 0.01
        if each < -16893 * 0.02:
            Z_data_fft[index] = 0

    print "max is ", max(Z_data_fft)
    print "min is ", min(Z_data_fft)
    # p = mlab.mesh(X, Y, Z_data.reshape(723, 577), representation="wireframe", line_width=1.0)
    p = mlab.mesh(X, Y, Z_data_fft.reshape(723, 577), representation="wireframe", line_width=1.0)
    # surf = ax.plot_surface(X, Y, Z_data.reshape(723,577), rstride=1, cstride=1, cmap=cm.coolwarm,
    #                        linewidth=0, antialiased=False)
    # ax.set_zlim(-1.01, 1.01)
    #
    # ax.zaxis.set_major_locator(LinearLocator(10))
    # ax.zaxis.set_major_formatter(FormatStrFormatter('%.02f'))

    # fig.colorbar(surf, shrink=0.5, aspect=5)

    # dir(p)
    mlab.show()
    # plt.show()