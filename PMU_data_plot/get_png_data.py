# coding:utf-8
#!/usr/bin/env python

__author__ = 'XingHua'

"""

"""

#import PIL.Image as Image
from PIL import Image
import sys
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.cbook as cbook

def get_data_from_png(file_name):
    im = Image.open(file_name)
    # print im.mode, im.size, im.format
    # im.show()
    # data.save("tmp.png")
    # print dir(im)
    data = list(im.getdata())
    # print data[0:10]
    #print dir(data)
    data = np.array(data)
    return data
    # return data.reshape(512,512)
    # print data


if __name__ == "__main__":
    if len(sys.argv) == 2:
        file_name = sys.argv[1]
        print file_name
    else:
        file_name = r'20141125_104452_x65_y23_No1.png'

    data = get_data_from_png(file_name)
    print data[:512]

    # datafile = cbook.get_sample_data(file_name, asfileobj=False)
    # print ('loading %s' % datafile[:])


    fig = plt.figure()
    ax = fig.add_subplot(111)
    im = ax.imshow(data.reshape(512,512))
    plt.colorbar(im)
    # a = im.split()
    # for each in a:
    # each.show()
    # print a
    plt.show()



    # r.show()
    # im.show()