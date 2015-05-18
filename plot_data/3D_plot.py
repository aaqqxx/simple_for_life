# coding:utf-8
# !/usr/bin/env python

__author__ = 'XingHua'

"""

"""
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import sys
from matplotlib import cm
from matplotlib.ticker import LinearLocator, FormatStrFormatter
from decimal import Decimal
from PIL import Image
import StringIO
from numpy import exp
import random


def measure(n, sigma):
    "Measurement model, return two coupled measurements."
    m1 = np.random.normal(size=n)
    m2 = np.random.normal(scale=0.5, size=n)
    return m1 + m2, m1 - m2


def tmp(n, mean, sigma):
    res = []
    for each in xrange(n):
        res.append(random.gauss(mean, sigma))
    res = np.array(res)
    res.resize(np.sqrt(res.size), np.sqrt(res.size))
    return res
    pass


print random.gauss(0, 1)
plt.imshow(tmp(100, 0, 1).reshape(10, 10))
plt.show()


def twoD_Gaussian((x, y), amplitude, xo, yo, sigma_x, sigma_y, theta, offset):
    xo = float(xo)
    yo = float(yo)
    a = (np.cos(theta) ** 2) / (2 * sigma_x ** 2) + (np.sin(theta) ** 2) / (2 * sigma_y ** 2)
    b = -(np.sin(2 * theta)) / (4 * sigma_x ** 2) + (np.sin(2 * theta)) / (4 * sigma_y ** 2)
    c = (np.sin(theta) ** 2) / (2 * sigma_x ** 2) + (np.cos(theta) ** 2) / (2 * sigma_y ** 2)
    g = offset + amplitude * np.exp(- (a * ((x - xo) ** 2) + 2 * b * (x - xo) * (y - yo)
                                       + c * ((y - yo) ** 2)))
    return g.ravel()


def out_put_photo(filename, data):
    # save_path=""
    # mpl.rcParams['figure.subplot.left'] = 0
    # mpl.rcParams['figure.subplot.right'] = 1
    # mpl.rcParams['figure.subplot.bottom'] = 0
    # mpl.rcParams['figure.subplot.top'] = 1
    # # mpl.rcParams['figure.subplot.wspace'] = 0
    # # mpl.rcParams['figure.subplot.hspace'] = 0
    # fig, ax = plt.subplots(figsize=(data.shape[0], data.shape[1]), dpi=100)
    # ax.imshow(data, plt.cm.gray)
    # ax.spines['right'].set_visible(False)
    # ax.spines['top'].set_visible(False)
    # ax.spines['left'].set_visible(False)
    # ax.spines['bottom'].set_visible(False)
    # ax.xaxis.set_major_locator(plt.NullLocator())
    # ax.yaxis.set_major_locator(plt.NullLocator())
    # fig.savefig(filename)

    im = Image.new('L', (data.shape[0], data.shape[1]))
    im.putdata(np.floor(data).astype('uint8').ravel())
    im.save(filename)
    print filename
    pass


if __name__ == "__main__":
    X = np.linspace(-1.2 * np.pi, 1.2 * np.pi, 512)
    Y = np.linspace(-1.2 * np.pi, 1.2 * np.pi, 512)

    # Z=[]
    # for x in X:
    #     for y in Y:
    #         z = 3 * (1 - x) ^ 2 * exp(-(x ^ 2) - (y + 1) ^ 2) - 10 * (x / 5 - x ^ 3 - x ^ 5) * exp(-x ^ 2 - x ^ 2) - 1 / 3 * exp(-(x + 1) ^ 2 - y ^ 2)
    #
    #         Z.append(z)
    # Z = np.array(Z)
    # Z.reshape(X.size, Y.size)

    print X.shape, Y.shape
    Z = np.ones(X.size * Y.size).reshape(X.size, Y.size)
    print Z.shape

    X, Y = np.meshgrid(X, Y)

    gauss_mean = 0
    gauss_sigma = 0.1
    # Z = np.sin(X) / X + np.sin(Y) / Y
    Z = 3 * (1 - X) ** 2 * exp(-(X ** 2) - (Y + 1) ** 2) - 10 * (X / 5 - X ** 3 - Y ** 5) * exp(
        -X ** 2 - Y ** 2) - 1 / 3 * exp(-(X + 1) ** 2 - Y ** 2)  #+ tmp(X.size,gauss_mean,gauss_sigma)*0.35
    f0 = 80
    # fringe_data= 1 + 2*np.cos(2*np.pi*f0*X+10*(np.sin(X)/X+np.sin(Y)/Y) + np.pi*1.5)

    for xiangwei in np.arange(0, 2, 0.5):
        fringe_data = 1 + 2 * np.cos(2 * np.pi * f0 * X + 10 * (Z) + np.pi * xiangwei)

        #
        fringe_data_fft = np.fft.fft(fringe_data)
        # plt.plot(fringe_data_fft)
        # plt.show()
        fig = plt.figure()
        ax = Axes3D(fig)
        # surf=ax.plot_surface(X, Y, Z,  label="qiangdu",cmap=cm.coolwarm)
        surf = ax.plot_surface(X, Y, Z, label="qiangdu", linewidth=0.0, cmap=cm.coolwarm)
        # ax.zaxis.set_major_locator(LinearLocator(10))
        # ax.zaxis.set_major_formatter(FormatStrFormatter('%.02f'))
        # fig.colorbar(surf, shrink=0.5, aspect=5)

        # surf = ax.plot_wireframe(X, Y, Z, label="qiangdu")
        # surf = ax.plot_surface(X, Y, Z, label="qiangdu", cmap=cm.coolwarm)
        # surf = ax.plot_surface(X, Y, fringe_data, label="qiangdu", cmap=cm.coolwarm)
        plt.show()
        fringe_data = fringe_data.transpose()
        fringe_data_8bit = (fringe_data + 1) * 255 / 4
        print fringe_data.dtype, fringe_data.max(), fringe_data.min(), dir(fringe_data)
        out_put_photo("fringe_%.1fpi.png" % xiangwei, fringe_data)
        # fig = plt.figure()
        plt.imshow(fringe_data, cmap=cm.gray)
        plt.axis("off")
        # plt.savefig("fringe0.png")

        plt.show()
