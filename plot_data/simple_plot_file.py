# coding:utf-8
#!/usr/bin/env python

__author__ = 'XingHua'

"""

"""

import matplotlib.pyplot as plt
import sys

if __name__=="__main__":
    if(len(sys.argv) == 3):
        filename=sys.argv[2]
    else:
        filename = r"../EN1822_Plot/Data8H55M37S.txt"
    plt.plotfile(filename, cols=(2,),delimiter=" ")
    plt.show()
