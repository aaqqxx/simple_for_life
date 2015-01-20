# coding:utf-8
#!/usr/bin/env python

__author__ = 'XingHua'

"""

"""

import numpy as np
import matplotlib.pyplot as plt
from PIL import Image
# import Image
import PIL
import matplotlib as mpl
from glob import glob
# import pyopencv as cv


def get_energy_sum(filename):
    res = np.loadtxt(filename, skiprows=25, comments='T')
    if "Morning" in filename:
        # print res.sum()
        return res.sum()
    else:
        return res[-1]
    pass


def get_data_from_png(filename, row_size=512, col_size=512):
    im = Image.open(filename)
    # print im.mode, im.size, im.format
    # im.show()
    # data.save("tmp.png")
    # print dir(im)
    data = list(im.getdata())
    # print data[0:10]
    # print dir(data)
    data = np.array(data).reshape(row_size, col_size) + 0.0
    return data
    pass


def get_new_pic_data(pic_data, energy_sum):
    # print "raw_data\n",pic_data,energy_sum
    res = pic_data / energy_sum
    xishu = 65535. / res.max()
    res = res * xishu
    # print "res_data\n",res
    res = res / 256
    res = np.int8(res.round())
    # print "res \n",res
    return res
    pass


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
    im.save(filename[:-4] + ".tif")
    print filename[:-4] + ".tif"
    pass


if __name__ == "__main__":
    # file_name = r"E:\aaqqxx\pupil20150110\20150110Afternoon1\pupil_20150110_145913_264"
    png_file_name_list = glob(r"pupil_*.png")
    txt_file_name_list = glob(r"pupil_*.txt")
    png_file_name_list.sort()
    txt_file_name_list.sort()

    # print png_file_name_list
    # print txt_file_name_list
    print "begin photo process"
    cnt = 0
    for png_file, txt_file in zip(png_file_name_list, txt_file_name_list):
        data = get_data_from_png(png_file)
        energy_sum = get_energy_sum(txt_file)
        res_data = get_new_pic_data(data, energy_sum)
        out_put_photo(png_file[:-4] + "_1.png", res_data)
        # break
        cnt = cnt + 1
        print "photo num is ", cnt
    print "Over"
    pass