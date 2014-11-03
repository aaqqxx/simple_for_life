# coding:utf-8
#!/usr/bin/env python

__author__ = 'XingHua'

"""

"""
import numpy as np
import math
import matplotlib as mpl
import matplotlib.pyplot as plt
import pylab
import numpy.random


def test1():
    # Create the colormap:
    halfpurples = {'blue': [(0.0, 1.0, 1.0), (0.000001, 0.78431373834609985, 0.78431373834609985),
                            (0.25, 0.729411780834198, 0.729411780834198), (0.5,
                                                                           0.63921570777893066, 0.63921570777893066),
                            (0.75,
                             0.56078433990478516,
                             0.56078433990478516),
                            (1.0, 0.49019607901573181,
                             0.49019607901573181)],

                   'green': [(0.0, 1.0, 1.0), (0.000001,
                                               0.60392159223556519, 0.60392159223556519), (0.25,
                                                                                           0.49019607901573181,
                                                                                           0.49019607901573181), (0.5,
                                                                                                                  0.31764706969261169,
                                                                                                                  0.31764706969261169),
                             (0.75,
                              0.15294118225574493, 0.15294118225574493), (1.0, 0.0, 0.0)],

                   'red': [(0.0, 1.0, 1.0), (0.000001,
                                             0.61960786581039429, 0.61960786581039429), (0.25,
                                                                                         0.50196081399917603,
                                                                                         0.50196081399917603), (0.5,
                                                                                                                0.41568627953529358,
                                                                                                                0.41568627953529358),
                           (0.75,
                            0.32941177487373352, 0.32941177487373352), (1.0,
                                                                        0.24705882370471954, 0.24705882370471954)]}

    halfpurplecmap = mpl.colors.LinearSegmentedColormap('halfpurples', halfpurples, 256)

    # Create x,y arrays of normally distributed points
    npts = 1000
    x = numpy.random.standard_normal(npts)
    y = numpy.random.standard_normal(npts)

    #Set bin numbers in both axes
    nxbins = 25
    nybins = 25

    #Set the cutoff for resolving the individual points
    minperbin = 1

    #Make the density histrogram
    H, yedges, xedges = np.histogram2d(y, x, bins=(nybins, nxbins))
    #Reorient the axes
    H = H[::-1]

    extent = [xedges[0], xedges[-1], yedges[0], yedges[-1]]

    #Compute all bins where the density plot value is below (or equal to) the threshold
    lowxleftedges = [[xedges[i] for j in range(len(H[:, i])) if H[j, i] <= minperbin] for i in range(len(H[0, :]))]
    lowxrightedges = [[xedges[i + 1] for j in range(len(H[:, i])) if H[j, i] <= minperbin] for i in range(len(H[0, :]))]
    lowyleftedges = [[yedges[-(j + 2)] for j in range(len(H[:, i])) if H[j, i] <= minperbin] for i in
                     range(len(H[0, :]))]
    lowyrightedges = [[yedges[-(j + 1)] for j in range(len(H[:, i])) if H[j, i] <= minperbin] for i in
                      range(len(H[0, :]))]

    #Flatten and convert to numpy array
    lowxleftedges = np.asarray([item for sublist in lowxleftedges for item in sublist])
    lowxrightedges = np.asarray([item for sublist in lowxrightedges for item in sublist])
    lowyleftedges = np.asarray([item for sublist in lowyleftedges for item in sublist])
    lowyrightedges = np.asarray([item for sublist in lowyrightedges for item in sublist])

    #Find all points that lie in these regions
    lowdatax = [[x[i] for j in range(len(lowxleftedges)) if
                 lowxleftedges[j] <= x[i] and x[i] <= lowxrightedges[j] and lowyleftedges[j] <= y[i] and y[i] <=
                 lowyrightedges[j]] for i in range(len(x))]
    lowdatay = [[y[i] for j in range(len(lowyleftedges)) if
                 lowxleftedges[j] <= x[i] and x[i] <= lowxrightedges[j] and lowyleftedges[j] <= y[i] and y[i] <=
                 lowyrightedges[j]] for i in range(len(y))]

    #Flatten and convert into numpy array
    lowdatax = np.asarray([item for sublist in lowdatax for item in sublist])
    lowdatay = np.asarray([item for sublist in lowdatay for item in sublist])

    #Plot
    fig1 = plt.figure()
    ax1 = fig1.add_subplot(111)
    ax1.plot(lowdatax, lowdatay, linestyle='.', marker='o', mfc='k', mec='k')
    cp1 = ax1.imshow(H, interpolation='nearest', extent=extent, cmap=halfpurplecmap, vmin=minperbin)
    fig1.colorbar(cp1)

    fig1.savefig('contourtest1.png')


def test2():
    import numpy as np
    import math
    import matplotlib as mpl
    import matplotlib.pyplot as plt
    import pylab
    import numpy.random

    # Create the colormap:
    halfpurples = {'blue': [(0.0, 1.0, 1.0), (0.000001, 0.78431373834609985, 0.78431373834609985),
                            (0.25, 0.729411780834198, 0.729411780834198), (0.5,
                                                                           0.63921570777893066, 0.63921570777893066), (
                                0.75,
                                0.56078433990478516, 0.56078433990478516), (
                                1.0, 0.49019607901573181,
                                0.49019607901573181)],

                   'green': [(0.0, 1.0, 1.0), (0.000001,
                                               0.60392159223556519, 0.60392159223556519), (0.25,
                                                                                           0.49019607901573181,
                                                                                           0.49019607901573181),
                             (0.5,
                              0.31764706969261169, 0.31764706969261169), (0.75,
                                                                          0.15294118225574493, 0.15294118225574493),
                             (1.0, 0.0, 0.0)],

                   'red': [(0.0, 1.0, 1.0), (0.000001,
                                             0.61960786581039429, 0.61960786581039429), (0.25,
                                                                                         0.50196081399917603,
                                                                                         0.50196081399917603),
                           (0.5,
                            0.41568627953529358, 0.41568627953529358), (0.75,
                                                                        0.32941177487373352, 0.32941177487373352), (1.0,
                                                                                                                    0.24705882370471954,
                                                                                                                    0.24705882370471954)]}

    halfpurplecmap = mpl.colors.LinearSegmentedColormap('halfpurples', halfpurples, 256)

    #Create x,y arrays of normally distributed points
    npts = 100000
    x = numpy.random.standard_normal(npts)
    y = numpy.random.standard_normal(npts)

    #Set bin numbers in both axes
    nxbins = 100
    nybins = 100

    #Set the cutoff for resolving the individual points
    minperbin = 1

    #Make the density histrogram
    H, yedges, xedges = np.histogram2d(y, x, bins=(nybins, nxbins))
    #Reorient the axes
    H = H[::-1]

    extent = [xedges[0], xedges[-1], yedges[0], yedges[-1]]

    #Figure out which bin each x,y point is in
    xbinsize = xedges[1] - xedges[0]
    ybinsize = yedges[1] - yedges[0]
    xi = ((x - xedges[0]) / xbinsize).astype(np.integer)
    yi = nybins - 1 - ((y - yedges[0]) / ybinsize).astype(np.integer)

    #Subtract one from any points exactly on the right and upper edges of the region
    xim1 = xi - 1
    yim1 = yi - 1
    xi = np.where(xi < nxbins, xi, xim1)
    yi = np.where(yi < nybins, yi, yim1)

    #Get all points with density below the threshold
    lowdensityx = x[H[yi, xi] <= minperbin]
    lowdensityy = y[H[yi, xi] <= minperbin]

    #Plot
    fig1 = plt.figure()
    ax1 = fig1.add_subplot(111)
    ax1.plot(lowdensityx, lowdensityy, linestyle='.', marker='o', mfc='k', mec='k', ms=3)
    cp1 = ax1.imshow(H, interpolation='nearest', extent=extent, cmap=halfpurplecmap, vmin=minperbin)
    fig1.colorbar(cp1)

    fig1.savefig('contourtest2.png')


if __name__ == "__main__":
    test2()