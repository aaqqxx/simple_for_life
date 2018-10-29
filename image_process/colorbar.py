# coding:utf-8
#!/usr/bin/env python

__author__ = 'XingHua'

"""

"""

import matplotlib.pyplot as plt
import matplotlib
from PIL import Image

if __name__ == '__main__':
    filename = r"G:\project\Axion_test\images\20161116\len\4.jpg"

    pic = Image.open(filename)
    fig = plt.figure(dpi=300)
    ax = fig.add_subplot(111)
    cmap = matplotlib.cm.jet
    im = ax.imshow(pic,cmap=cmap)

    plt.colorbar(im)
    # plt.title("SO")
    plt.show()