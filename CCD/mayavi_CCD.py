# coding:utf-8
#!/usr/bin/env python

__author__ = 'XingHua'

"""

"""

import numpy as np
from mayavi import mlab
import sys

if __name__ == "__main__":
    if len(sys.argv) == 2:
        filename= sys.argv[1]
        print filename
    else:
        filename=ur'.\20140711_105711_789.txt'

    Z_data = np.array(np.loadtxt(filename)).reshape(512, 512)

    X = np.arange(0, 512, 1)
    # print len(X)
    Y = np.arange(0, 512, 1)
    X, Y = np.meshgrid(X, Y)
    # pl = mlab.surf(X, Y, Z_data, warp_scale="auto")
    # s = mlab.mesh(X, Y, Z_data, representation="wireframe", line_width=1.0 )
    s = mlab.mesh(X, Y, Z_data,  line_width=1.0 )
    # ax.set_zlim(-1.01, 1.01)
    # mlab.axes(xlabel='x', ylabel='y', zlabel='z')
    # ax.zaxis.set_major_locator(LinearLocator(10))
    # ax.zaxis.set_major_formatter(FormatStrFormatter('%.02f'))
    mlab.show()



