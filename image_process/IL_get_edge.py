# coding:utf-8
#!/usr/bin/env python

__author__ = 'XingHua'

"""

"""

from scipy import misc
import pylab as pl
from glob import glob
import matplotlib.pyplot as plt
from scipy import ndimage
import numpy as np
from scipy import ndimage
import matplotlib.pyplot as plt
# from scikits.image.filter import canny
# from image_source_canny import canny


def main():
    l = misc.lena()
    misc.imsave("lena.png", l)
    # plt.imshow(l, cmap=plt.cm.gray)
    # plt.imshow(l[200:220, 200:220], cmap=plt.cm.gray)
    plt.imshow(l[200:220, 200:220], cmap=plt.cm.gray, interpolation='nearest')
    plt.show()
    # plt.imshow(l, cmap=plt.cm.gray, vmin=30, vmax=200)
    plt.axis('off')
    plt.contour(l, [60, 211], interpolate='nearest')
    plt.show()
    lena = misc.imread("20141125_104452_x65_y23_No1.png")
    # plt.imshow(lena)
    blurred_lena = ndimage.gaussian_filter(lena, sigma=5)
    IL_no1 = plt.imshow(blurred_lena)
    plt.colorbar(IL_no1)
    plt.show()
    print lena.shape, lena.dtype


def plot_find_edges():
    im = np.zeros((256, 256))
    im[64:-64, 64:-64] = 1

    im = ndimage.rotate(im, 15, mode='constant')
    im = misc.imread("20141125_104452_x65_y23_No1.png")
    im = ndimage.gaussian_filter(im, 8)

    sx = ndimage.sobel(im, axis=0, mode='constant')
    sy = ndimage.sobel(im, axis=1, mode='constant')
    sob = np.hypot(sx, sy)

    plt.figure(figsize=(16, 5))
    plt.subplot(141)
    plt.imshow(im, cmap=plt.cm.gray)
    plt.axis('off')
    plt.title('square', fontsize=20)
    plt.subplot(142)
    plt.imshow(sx)
    plt.axis('off')
    plt.title('Sobel (x direction)', fontsize=20)
    plt.subplot(143)
    plt.imshow(sob)
    plt.axis('off')
    plt.title('Sobel filter', fontsize=20)

    im += 0.07 * np.random.random(im.shape)

    im = misc.imread("20141125_104452_x65_y23_No1.png")
    sx = ndimage.sobel(im, axis=0, mode='constant')
    sy = ndimage.sobel(im, axis=1, mode='constant')
    sob = np.hypot(sx, sy)

    plt.subplot(144)
    plt.imshow(sob)
    plt.axis('off')
    plt.title('Sobel for noisy image', fontsize=20)

    plt.subplots_adjust(wspace=0.02, hspace=0.02, top=1, bottom=0, left=0, right=0.9)

    plt.show()


def get_IL_x_edge(filename="20141125_104452_x65_y23_No1.png", y_index=0):
    im = misc.imread(filename)
    # plt.imshow(lena)
    blurred_lena = ndimage.gaussian_filter(im, sigma=5)
    IL_no1 = plt.imshow(blurred_lena)
    plt.title(filename)
    plt.colorbar(IL_no1)
    plt.show()

    x_index_data = blurred_lena[y_index, :]
    plt.plot(x_index_data, label="y=%d" % y_index)
    x_mid_index = get_mid_index(x_index_data)
    plt.plot(x_mid_index, x_index_data[x_mid_index], "o")
    plt.title(filename + "\ny_index=%d, x_mid_index=%d" % (y_index, x_mid_index))

    plt.plot(np.ones(len(np.arange(blurred_lena.min(), blurred_lena.max(), 1))) * 240,
             np.arange(blurred_lena.min(), blurred_lena.max(), 1))
    plt.plot(np.ones(len(np.arange(blurred_lena.min(), blurred_lena.max(), 1))) * 334,
             np.arange(blurred_lena.min(), blurred_lena.max(), 1), 'r')

    # plt.grid()
    plt.show()
    return x_mid_index


def get_IL_y_edge(filename="20141125_104452_x65_y23_No1.png", x_index=0):
    im = misc.imread(filename)
    # plt.imshow(lena)
    blurred_lena = ndimage.gaussian_filter(im, sigma=5)
    # IL_no1=plt.imshow(blurred_lena)
    # plt.colorbar(IL_no1)
    # plt.show()

    y_index_data = blurred_lena[:, x_index]
    plt.plot(y_index_data, label="y=%d" % x_index)
    y_mid_index = get_mid_index(y_index_data)
    plt.plot(y_mid_index, y_index_data[y_mid_index], "o")

    plt.title(filename + "\nx_index=%d, y_mid_index=%d" % (x_index, y_mid_index))
    plt.show()
    return y_mid_index
    pass


def get_mid_index(data):
    max = data.max()
    res = 0
    for index, each in enumerate(data):
        if data[index] > max * 0.5:
            # print "index is ",index
            res = index
            break
    if res == 0:
        for index1, each1 in enumerate(data):
            if data[index1] < max * 0.5:
                res = index1
                break
    return res
    pass


def get_banying(data):
    _data = np.array(data)
    min = _data.min()
    max = _data.max()
    pass


if __name__ == "__main__":
    y_index_list = [0, 511, 511, 0]
    x_index_list = [511, 511, 0, 0]
    # y_index_list = [511,511,511,0]
    # x_index_list = [511,511,0,0]
    file_list = glob("20141125_104452_x65_y23_No1.png")
    file_list.sort()
    print file_list
    for index, each in enumerate(file_list):
        print each, "x mid index is", get_IL_x_edge(each, y_index_list[index])
        print each, "y mid index is", get_IL_y_edge(each, x_index_list[index])
        # main()
