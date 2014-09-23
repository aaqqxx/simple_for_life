# coding:utf-8
#!/usr/bin/env python

__author__ = 'XingHua'

"""

"""

import numpy as np
# from mayavi import mlab
import sys
from numpy import cos, sin
import matplotlib as mpl
from get_png_data import get_data_from_png

# matplotlib.use('webagg')

from mpl_toolkits.mplot3d import Axes3D
# import numpy as np
import matplotlib.pyplot as plt


txt_num = 19


def get_I_Ophir(filename_list):
    res = []
    for each in filename_list:
        sum = np.loadtxt(each, dtype=float).sum()
        res.append(sum)
    return res


# I_ophir = np.array(
# [0.36, 0.32, 0.34, 0.37, 0.33, 0.40, 0.33, 0.38, 0.34, 0.39, 0.32, 0.42, 0.34, 0.36, 0.41, 0.38, 0.32, 0.36,
#      0.31])



A = np.zeros((txt_num, 4), dtype=float)

if __name__ == "__main__":
    if len(sys.argv) == 2:
        filename = sys.argv[1]
        print filename
    else:
        filename = r'./test'
    filename_list_png = []
    filename_list_txt = []

    for each in xrange(1, txt_num + 1):
        filename = filename + str(each)
        # print filename
        filename_list_png.append(filename + r".png")
        filename_list_txt.append(filename + r".txt")
        filename = r"./test"
    # print filename_list

    I_ophir = get_I_Ophir(filename_list_txt)
    print I_ophir
    I = []
    for each in filename_list_png:
        print each
        # data = np.loadtxt(each, delimiter=',', usecols=(2,), dtype=float)
        data = get_data_from_png(each)
        data = data.reshape(512,512).T
        I.append(data.reshape(-1))
    I = np.array(I)
    print 'I[-1] is \n',len( I[-1]), I[-1]

    # print "I shape is", I.shape
    for i in xrange(0, txt_num):
        I[i, :] = I[i, :] / I_ophir[i]
        pass

    alpha = 0. / 180 * np.pi
    theta0 = 0. / 180 * np.pi
    delta = 90. / 180 * np.pi
    p = 10000.
    q = (p - 1) / (p + 1)

    r = 2 * np.sqrt(p) / (p + 1)

    for each in xrange(1, txt_num + 1):
        theta = (each - 1) * 20. / 180. * np.pi + theta0
        # print "theta is", theta

        A[each - 1, :] = np.array([1,
                                   q * (
                                       cos(2. * alpha) * (
                                           cos(2. * theta) ** 2 + sin(2. * theta) ** 2. * cos(delta)) + sin(
                                           2. * alpha) * sin(
                                           2. * theta) * cos(2. * theta) * (1 - cos(delta))),
                                   q * (cos(2. * alpha) * sin(2. * theta) * cos(2. * theta) * (1 - cos(delta)) + sin(
                                       2. * alpha) * (
                                            sin(2. * theta) ** 2 + cos(2. * theta) ** 2. * cos(delta))),
                                   q * (sin(2. * alpha) * cos(2. * theta) - cos(2. * alpha) * sin(2. * theta)) * sin(
                                       delta)]).transpose()
    # print A.shape, I.shape
    A = np.matrix(A)
    I = np.matrix(I)
    # print "I is \n", I
    # A = np.linalg.inv(A)

    S = A.I * I
    # S= np.dot(A.I,I)
    # print S
    S = np.array(S)
    # S01 = S[1,:]
    S02 = S[0, :].reshape(512, 512)
    S12 = S[1, :].reshape(512, 512)
    S22 = S[2, :].reshape(512, 512)
    S32 = S[3, :].reshape(512, 512)

    S0 = S02 / S02
    S1 = S12 / S02
    S2 = S22 / S02
    S3 = S32 / S02

    RSP_H = 0.5 * (1 + S1 / S0)
    RSP_V = 0.5 * (1 - S1 / S0)
    DOP = np.sqrt(S1 * S1 + S2 * S2 + S3 * S3) / S0

    print "RSP_H is\n", RSP_H
    print "RSP_V is \n", RSP_V
    print "DOP is \n", DOP

    fig = plt.figure()
    ax = fig.add_subplot(221)
    im = ax.imshow(S0)
    plt.colorbar(im)
    plt.title("SO")

    ax = fig.add_subplot(222)
    im = ax.imshow(S1)
    plt.colorbar(im)
    plt.title("S1")

    ax = fig.add_subplot(223)
    im = ax.imshow(S2)
    plt.colorbar(im)
    plt.title("S2")

    ax = fig.add_subplot(224)
    im = ax.imshow(S3)
    plt.colorbar(im)
    plt.title("S3")

    fig = plt.figure()
    ax = fig.add_subplot(221)

    im = ax.imshow(RSP_H)
    plt.colorbar(im)
    plt.title("RSP_H")

    ax = fig.add_subplot(222)
    im = ax.imshow(RSP_V)
    plt.colorbar(im)
    plt.title("RSP_V")

    ax = fig.add_subplot(223)
    im = ax.imshow(DOP)
    plt.colorbar(im)
    plt.title("DOP")

    X = range(0, 512)
    Y = range(0, 512)
    X, Y = np.meshgrid(X, Y)
    # s = mlab.mesh(X, Y, DOP * 100, line_width=1.0)
    # mlab.show()
    # plt.colorbar()
    plt.show()






