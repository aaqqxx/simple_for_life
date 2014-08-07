# coding:utf-8
#!/usr/bin/env python

__author__ = 'XingHua'

"""
应用Python的Matplotlib模块绘制三维模型过程中，出现错误。
主要有以下几个方面的问题，
1 matplotlib和python本身的版本问题。我这里采用的是Python2.6和matplotlib-0.99.3.win32-py2.6，对应的
numpy和scipy分别是，scipy-0.8.0-win32-superpack-python2.6，numpy-1.5.0-win32-superpack-python2.6。
2 在matplotlib官网中的一些例子是以前的版本编写的。因此，在新版本的环境运行一直出错
只需要将代码中的
ax = fig.gca(projection='3d')
一行改为如下，
ax = Axes3D(fig)
运行即可。
例二，contour3d_demo3.py
将代码
ax = fig.gca(projection='3d')
改为
ax = axes3d.Axes3D(fig)

总结，这里只是模块做了一些改变。另外，在调用时候也要主要前后环境。
"""

from mpl_toolkits.mplot3d import Axes3D
import numpy as np
import matplotlib.pyplot as plt
import sys

z_factor = 1
x_steps = 8
y_steps = 1

if __name__ == "__main__":
    if len(sys.argv) == 2:
        filename= sys.argv[1]
        print filename
    else:
        filename=ur'./data'

    Z_data = np.loadtxt(filename)
    X = np.arange(0, Z_data.shape[1]*x_steps, x_steps)
    Y = np.arange(0, Z_data.shape[0]*y_steps, y_steps)
    X, Y = np.meshgrid(X, Y)

    fig = plt.figure()
    #ax = fig.gca(projection='3d')
    ax = Axes3D(fig)
    ax.plot_wireframe(X,Y,Z_data*z_factor)

    # ax.set_zlim(-1.01, 1.01)
    # mlab.axes(xlabel='x', ylabel='y', zlabel='z')
    # ax.zaxis.set_major_locator(LinearLocator(10))
    # ax.zaxis.set_major_formatter(FormatStrFormatter('%.02f'))
    plt.show()