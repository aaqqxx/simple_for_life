# coding:utf-8
#!/usr/bin/env python

__author__ = 'XingHua'

"""

"""
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.colors as colors
import matplotlib.cm as cmx

from mayavi import mlab

# my data
dat = [2.31778665482167e-310, 0.006232785101850947, 0.0285075971030949, 0.0010248181570355695, 0.0048776795767614825, 0.02877090365176044, 0.002459331469834533, 0.0008594610645495889, 0.002919824084878003, 0.000968081117692596, 0.0, 0.0, 0.0319623949119874, 0.00568752311279771, 0.009994801469036968, 0.03248018520506219, 0.006686905726805326, 0.005987863156039365, 0.0072955095915350045, 0.005568911905473998, 0.0, 0.0, 0.0, 0.028483143996551524, 0.031030793902192794, 0.06125216053962635, 0.02935971973938871, 0.028507530280092265, 0.030112963748812088, 0.028293406731749605, 0.0, 0.0, 0.0, 0.0, 0.004510645022825792, 0.028998119822468988, 0.0013993630391143715, 0.0010726572949244424, 0.002288215944285159, 0.0006513973584945584, 0.0, 1.1625e-320, 1.15348834e-316, 2.3177866547513e-310, 0.0, 0.03148966953869102, 0.005215047563268979, 0.004491716298086729, 0.006010166308872446, 0.005186976949223524, 0.0, 0.0, 0.0, 0.0, 0.0, 1.107e-320, 0.02983657915729719, 0.028893006725328373, 0.030526067389954753, 0.028629390713739978, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0015217840289869456, 0.002751587509779179, 0.001413669523724954, 1.15348834e-316, 2.3177866547513e-310, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0024680339073824705, 0.0008254364860386303, 0.0, 0.0, 0.0, 9.965e-321, 1.15348834e-316, 2.3177866547513e-310, 0.0, 0.0, 0.0, 0.002621588539481613, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 9.41e-321, 1.15348834e-316, 2.3177866547513e-310]
dat = np.reshape(dat,[10,10],order='F')

lx = len(dat[0])
ly = len(dat[:,0])
n = lx*ly

# generate colors
cm = plt.get_cmap('jet')
vv = range(len(dat))
cNorm = colors.Normalize(vmin=0, vmax=vv[-1])
scalarMap = cmx.ScalarMappable(norm=cNorm, cmap=cm)
colorVals = [scalarMap.to_rgba(i) for i in range(ly)]

# generate plot data
xpos = np.arange(0,lx,1)
ypos = np.arange(0,ly,1)
xpos, ypos = np.meshgrid(xpos+0.25, ypos+0.25)
xpos = xpos.flatten()
ypos = ypos.flatten()
zpos = np.zeros(n)
dx = 0.5*np.ones_like(zpos)
dy = dx.copy()
dz = dat.flatten()
cc = np.tile(range(lx), (ly,1))
cc = cc.T.flatten()

# generate plot
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
opacity = 1

mlab.barchart(xpos,ypos,dz*100)

# for i in range(n):
#     ax.bar3d(xpos[i], ypos[i], zpos[i], dx[i], dy[i], dz[i],
#              color=colorVals[cc[i]], alpha=opacity, zsort='max')
#
# plt.autoscale(enable=True, axis='both', tight=True)
# plt.grid()
# plt.show()