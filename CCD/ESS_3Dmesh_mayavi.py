# coding:utf-8
#!/usr/bin/env python

__author__ = 'XingHua'

"""

"""

import numpy as np
from mayavi import mlab
import sys

z_factor = 100000000
x_steps=8
y_steps=1

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
    #pl = mlab.surf(X, Y, Z_data*z_factor, warp_scale="auto")
    #pl = mlab.surf(X, Y, Z_data*z_factor)
    p = mlab.mesh(X, Y, Z_data*z_factor, representation="wireframe", line_width=1.0 )
    #s = mlab.mesh(X, Y, Z_data*z_factor,  line_width=1.0 )
    # mlab.axes(xlabel='x', ylabel='y', zlabel='z')
    mlab.show()