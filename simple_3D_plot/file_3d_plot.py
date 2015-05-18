# coding:utf-8
# !/usr/bin/env python

__author__ = 'XingHua'

"""

"""

from mpl_toolkits.mplot3d import Axes3D
import matplotlib
# from mayavi import mlab
import vtk
import numpy as np
from matplotlib import cm
from matplotlib import pyplot as plt


if __name__ == "__main__":
    filename = "3.txt"
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')

    data = np.loadtxt(filename)
    print "data.shape is ", data.shape
    X = np.arange(0, data.shape[1])
    Y = np.arange(0, data.shape[0])
    X, Y = np.meshgrid(X, Y)
    # ax.plot_wireframe(X,Y,data)
    # data[]=data[]*0
    # data[]=data[]*0

    OE_surf1 = ax.plot_surface(X, Y, data, label="", alpha=1, linewidth=0, rstride=1, cstride=1,
                               cmap=cm.coolwarm)  #antialiased=False,

    # X=np.arange(-10,data.shape[1]+10)
    # Y=np.arange(-10,data.shape[0]+10)
    # X,Y=np.meshgrid(X,Y)
    # print X.shape,Y.shape
    # Z=np.zeros(X.shape[0]*X.shape[1]).reshape(X.shape[0],X.shape[1])
    # OE_surf = ax.plot_surface(X, Y, Z, label="", rstride=1, cstride=1, alpha=1, linewidth=0,
    #                        cmap=cm.jet,antialiased=False)

    # ax.xscale(1)
    # mlab.mesh(X, Y, data, representation="wireframe", line_width=1.0)
    # ax.plot_surface(X,Y,data)
    ax.set_xlim(-100, 300)
    ax.set_ylim(-150, 250)
    # ax.set_zlim(0,0.004)
    plt.colorbar(OE_surf1)
    # ax.view_init(azim=12, elev=17)
    ax.axis("off")
    plt.show()