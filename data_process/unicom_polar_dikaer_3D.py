# coding:utf-8
# !/usr/bin/env python

__author__ = 'XingHua'

"""

"""

import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import sys
from matplotlib import cm
from matplotlib.ticker import LinearLocator, FormatStrFormatter
from decimal import Decimal
from PIL import Image
import StringIO

qiangdu_value_dict = {1: [],
                      0.996: [[249, 249]],
                      0.992: [[125, 249], [375, 249]],
                      0.988: [[249, 125], [125, 375], [375, 375]],
                      0.984: [[125, 125], [125, 375], [375, 125], [375, 375]],
                      0.980: [[125, 125], [125, 375], [249, 249], [375, 125], [375, 375]],
                      0.976: [[125, 125], [125, 249], [125, 375], [375, 125], [375, 250], [375, 375]],
                      0.972: [[125, 125], [125, 24], [125, 375], [249, 249], [375, 125], [375, 249], [375, 375]],
                      0.968: [[125, 125], [125, 249], [125, 375], [187, 249], [312, 249], [375, 125], [375, 250],
                              [375, 375]],
                      0.964: [[125, 125], [125, 249], [125, 375], [249, 125], [249, 249], [249, 375], [375, 125],
                              [375, 249],
                              [375, 375]],
                      0.960: [[125, 125], [125, 249], [125, 375], [249, 100], [249, 200], [249, 300], [249, 400],
                              [375, 125],
                              [375, 249], [375, 375]],
                      0.956: [[125, 100], [125, 200], [125, 300], [125, 400], [249, 125], [249, 249], [249, 375],
                              [375, 100],
                              [375, 200], [375, 300], [375, 400]],
                      0.952: [[125, 100], [125, 200], [125, 300], [125, 400], [249, 100], [249, 200], [249, 300],
                              [249, 400],
                              [375, 100], [375, 200], [375, 300], [375, 400]],
                      0.948: [[83, 125], [83, 249], [83, 375], [166, 166], [166, 332], [249, 125], [249, 249],
                              [249, 375],
                              [333, 166], [333, 332], [415, 125], [415, 249], [415, 375]],
                      0.944: [[100, 100], [100, 200], [100, 300], [100, 400], [200, 125], [200, 249], [200, 375],
                              [300, 125],
                              [300, 249], [300, 375], [400, 100], [400, 200], [400, 300], [400, 400]],
                      0.940: [[125, 83], [125, 166], [125, 249], [125, 333], [125, 415], [249, 83], [249, 166],
                              [249, 249],
                              [249, 333], [249, 415], [375, 83], [375, 166], [375, 249], [375, 333], [375, 415]],
                      0.936: [[100, 100], [100, 200], [100, 300], [100, 400], [200, 100], [200, 200], [200, 300],
                              [200, 400],
                              [300, 100], [300, 200], [300, 300], [300, 400], [400, 100], [400, 200], [400, 300],
                              [400, 400]],
                      0.932: [[83, 125], [83, 249], [83, 375], [166, 100], [166, 200], [166, 300], [166, 400],
                              [249, 125],
                              [249, 249], [249, 375], [333, 100], [333, 200], [333, 300], [333, 400], [415, 125],
                              [415, 249],
                              [415, 375]],
                      0.928: [[83, 100], [83, 200], [83, 300], [83, 400], [166, 125], [166, 249], [166, 375],
                              [249, 100],
                              [249, 200], [249, 300], [249, 400], [333, 125], [333, 249], [333, 375], [415, 100],
                              [415, 200],
                              [415, 300], [415, 400]],
                      0.924: [[83, 100], [83, 200], [83, 300], [83, 400], [166, 100], [166, 200], [166, 300],
                              [166, 400],
                              [249, 125], [249, 249], [249, 375], [333, 100], [333, 200], [333, 300], [333, 400],
                              [415, 100],
                              [415, 200], [415, 300], [415, 400]],
                      0.920: [[83, 100], [83, 200], [83, 300], [83, 400], [166, 100], [166, 200], [166, 300],
                              [166, 400],
                              [249, 100], [249, 200], [249, 300], [249, 400], [333, 100], [333, 200], [333, 300],
                              [333, 400],
                              [415, 100], [415, 200], [415, 300], [415, 400]],
                      }


def get_info(filename, delimeter="\t"):
    info = np.loadtxt(filename, delimiter=delimeter, dtype=float, skiprows=1)
    _min = info[:, 0]
    _max = info[:, 1]
    _value = info[:, 2]
    return _min, _max, _value
    pass


def init_z_data(x_size=67, y_size=67):
    return np.ones(x_size * y_size).reshape(x_size, y_size)
    pass


def get_z(x, y, z_data_input, _min, _max, _value):
    res = z_data_input
    # print res.shape
    x_step_size = 1
    y_step_size = 1
    x_offset = np.sqrt(x_step_size ** 2 + y_step_size ** 2) / 2
    y_offset = np.sqrt(x_step_size ** 2 + y_step_size ** 2) / 2
    for x_index in xrange(z_data_input.shape[1]):
        for y_index in xrange(z_data_input.shape[0]):
            for index in range(len(_min)):
                if _min[index] <= np.sqrt((x_index * x_step_size + x_start_pos + x_offset) ** 2 + (
                                    y_index * y_step_size + y_start_pos + y_offset) ** 2) < \
                        _max[index]:
                    res[y_index, x_index] = _value[index]
                pass
            pass
    return res
    pass


def get_x(x_start=-100.5 / 2, x_end=100.5 / 2, x_step=1.5):
    return np.arange(x_start, x_end, x_step)
    pass


def get_y(y_start=-100.5 / 2, y_end=100.5 / 2, y_step=1.5):
    return np.arange(y_start, y_end, y_step)
    pass


def get_new_data1(qiangdu):
    res = np.ones(500 * 500, dtype=np.bool).reshape(500, 500)
    for each in qiangdu_value_dict[qiangdu]:
        # print 'new data is', each
        res[each[1]][each[0]] = 0
        # res[1][2]=0
    return res
    # print "res=", res
    pass


def get_qiangdu_dict(filename="LocalCordi.txt"):
    res_dict = dict()
    # data = np.loadtxt(filename, delimiter="\t", usecols=range(0, 40))
    data = np.loadtxt(filename, delimiter="\t")
    for index, each in enumerate(data[0]):
        res_dict[each] = data[1:, index]
    res_dict[1] = []
    return res_dict
    pass


# print "get qiangdu dict",sorted(get_qiangdu_dict().keys())

def get_new_data(qiangdu, x_size=20, y_size=20, file_name="LocalCordi_20150814.txt"):
    res = np.ones(x_size * y_size, dtype=np.bool)
    # if qiangdu==1:
    # # res[res.size/2]=0
    # return res.reshape(50,50)
    qiangdu_dict = get_qiangdu_dict(file_name)
    block_size = x_size * y_size
    for each in qiangdu_dict[qiangdu]:
        if each < block_size:
            res[each] = 0
    return res.reshape(x_size, y_size)
    pass


def get_new_data_3(qiangdu):
    res = np.ones(3 * 3, dtype=np.int8).reshape(3, 3)
    if qiangdu == 1:
        res[1][1] = 0
    elif qiangdu < 0.921:
        res[0][0] = 0
        res[1][1] = 0
        res[2][2] = 0
    else:
        res[0][0] = 0
        res[2][2] = 0
        # res[1][2]=0
    return res


# print get_new_data(1)
# print get_new_data(0.92)
# print get_new_data(np.float(0.93))
# print get_new_data(0.98)
# v=get_new_data(1)
# v[25][25]=0
# im=plt.imshow(v,cmap=plt.cm.gray)
# cbar=plt.colorbar(im,)
# cbar.set_ticks(np.linspace(0,1,8))

# plt.show()

# for each in sorted(get_qiangdu_dict().keys()):
# im=plt.imshow(get_new_data(each))
# plt.title(str(each))
# plt.colorbar(im)
# plt.show()

def get_shape_array_jiugong(data_array_2D, row, col):
    row_size = data_array_2D.shape[0]
    col_size = data_array_2D.shape[1]
    col_step = col_size / col
    row_step = row_size / row
    res = []
    tmp = np.split(data_array_2D, np.arange(1 * row, row * row, step=row_step), axis=1)
    # print "tmp is",tmp
    for each in tmp:
        for each1 in np.split(each, np.arange(1 * col, col * col, step=col_step)):
            # print each1
            res.append(each1)

    res = np.array(res)
    return res
    pass


def get_main_shape():
    pass


def get_sum_at_col(data_2D, col_start_index=67 * 50 / 2, width=50, height=50, step=50):
    res = []
    # print "data_2D.shape is", data_2D.shape
    # print "row index start is", np.arange(0, data_2D.shape[0] - height + step, step)
    for row_index in np.arange(0, data_2D.shape[0] - height + step, step):
        # print "data_2D area is", data_2D[row_index:row_index + height, col_start_index:col_start_index + width]
        res.append(data_2D[row_index:row_index + height, col_start_index:col_start_index + width].sum())
    # print res
    return res
    pass


def get_sum_in_circle(data_2D, x_center=60, y_center=30, r=30, mm2index=20):
    """
    :param data_2D:
    :param x_center: mm
    :param y_center: mm
    :param r:
    :param step:
    :return:
    """
    res = []
    x_center = x_center * mm2index
    y_center = y_center * mm2index
    r = r * mm2index

    # print "data_2D.shape is", data_2D.shape
    # print "row index start is", np.arange(0, data_2D.shape[0] - height + step, step)
    # for row_index in np.arange(0, data_2D.shape[0] - height + step, step):
    # print "data_2D area is", data_2D[row_index:row_index + height, col_start_index:col_start_index + width]
    # res.append(data_2D[row_index:row_index + height, col_start_index:col_start_index + width].sum())
    # print res
    print "int get_sum_in_circle, x_center,y_center,r is", x_center, y_center, r
    row_index_list = []
    col_index_list = []
    # for row_index in xrange(0, data_2D.shape[0]):
    # for col_index in xrange(0, data_2D.shape[1]):
    # if data_2D.shape[0]/2 - r<=col_index<=data_2D.shape[0]/2 + r:
    # if (row_index - y_center) ** 2 + (col_index - x_center) ** 2 <= r ** 2:
    #         res.append(data_2D[row_index][col_index])
    #         row_index_list.append(row_index)
    #         col_index_list.append(col_index)
    # for row_index in xrange(data_2D.shape[0]/2 - r, data_2D.shape[0]/2 + r+1):
    for row_index in xrange(0, data_2D.shape[0]):
        for col_index in xrange(data_2D.shape[1] / 2 - r, data_2D.shape[1] / 2 + r + 1):
            if (row_index - y_center) ** 2 + (col_index - x_center) ** 2 <= r ** 2:
                res.append(data_2D[row_index][col_index])
                row_index_list.append(row_index)
                col_index_list.append(col_index)

    print "get_sum_in_circle"
    # 鐢ㄦ潵楠岃瘉璇ュ渾鏄惁姝ｇ‘
    # data_tmp = np.zeros(data_2D.size).reshape(data_2D.shape)
    # for row, col in zip(row_index_list, col_index_list):
    #     data_tmp[row][col] = 1
    # plt.imshow(data_tmp)
    # plt.show()
    res = np.array(res)
    print "circle contain", res.sum(), "white points"
    return res.sum()


get_sum_in_circle(np.zeros(120 * 20 * 120 * 20).reshape(120 * 20, 120 * 20), x_center=60, y_center=30)


def get_sum_in_cols_with_circle_shape(data_2D, col_start_pos=60, r=30, step=1, mm2index=20):
    """

    :param data_2D:
    :param col_start_pos: mm
    :param r: mm
    :param step:mm
    :param mm2index:mm杞崲涓烘暟缁勭殑index
    :return: 鏌愬垪澶勬墍鏈夊渾涓墍鍚�1鐨勫拰鐨勫垪琛�
    """
    res = []
    # col_start_index = col_start_pos*mm2index
    # step = step*mm2index
    # r=r*mm2index
    print "step is", step
    for y_center in np.arange(r, 120 - r, step):
        # print "data_2D area is", data_2D[row_index:row_index + height, col_start_index:col_start_index + width]
        res.append(get_sum_in_circle(data_2D, x_center=col_start_pos, y_center=y_center, mm2index=mm2index, r=r))
    res = np.array(res)
    return res


# data_tmp = np.arange(0, 81).reshape(9, 9)
# get_shape_array_jiugong(data_tmp, 3, 3)





# for each in qiangdu_value_dict.keys():
# for each in np.arange(1,0.92-0.004,-0.004):
# print "each =", each
# #娴偣鏁扮殑绮惧害闂銆傘�傘��
# get_new_data(np.round(each*1000)/1000)

# zzz = get_new_data(0.90,20,20)
# print "zzz is ", zzz
# # print [a for each in zzz]
# plt.imshow(get_new_data(0.90,20,20), cmap=plt.cm.gray, interpolation='nearest')
# plt.show()
#
x_size = 100.
y_size = 100.


# fig = plt.Figure(120/25.4, 120/25.4, 25.4*20)
# fig = plt.Figure(figsize=(10,6), dpi=80)
# # fig = plt.Figure()
# ax = plt.subplot(111)
# # fig, ax = plt.subplots()
# a_res=np.ones(100).reshape(10,10)
# im = ax.imshow(a_res, cmap=plt.cm.gray)
# print "zzz"
# # fig.show()
# plt.show()

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
    im.putdata(np.floor(data * 255).astype('uint8').ravel())
    im.save(filename[:-4] + ".bmp")
    print filename[:-4] + ".bmp"
    pass


if __name__ == "__main__":
    if len(sys.argv) == 2:
        filename = sys.argv[1]
        print filename
    else:
        # filename = ur'./data/20141024/EDU_Ophir_NPulse_energy_data_20141024_4'
        # filename = ur'/home/aaqqxx/IL/server/data_analysis/data/20141024/ESS_energy_data20141024_PM7_bak'
        filename = ur'data_info_small_20150817'

    x_start_pos = -x_size / 2
    x_end_pos = x_size / 2
    x_step = 1

    y_start_pos = -x_size / 2
    y_end_pos = x_size / 2
    y_step = 1

    X = get_x(x_start_pos, x_end_pos, x_step)
    Y = get_y(y_start_pos, y_end_pos, y_step)
    Z = init_z_data(x_size, y_size)

    print "X.shape,Y.shape,Z.shape is ", X.shape, Y.shape, Z.shape

    _min, _max, _value = get_info(filename, delimeter=" ")
    # print _min, "\n", _max, "\n", _value

    data = get_z(X, Y, Z, _min, _max, _value)

    X, Y = np.meshgrid(X, Y)

    fig = plt.figure()
    ax = Axes3D(fig)
    # surf=ax.plot_surface(X, Y, Z,  label="qiangdu",cmap=cm.coolwarm)
    # ax.zaxis.set_major_locator(LinearLocator(10))
    # ax.zaxis.set_major_formatter(FormatStrFormatter('%.02f'))
    # fig.colorbar(surf, shrink=0.5, aspect=5)

    surf = ax.plot_wireframe(X, Y, Z, label="qiangdu", cmap=cm.coolwarm)
    plt.legend()
    plt.xlabel("x")
    plt.ylabel("y")
    plt.show()

    # np.savetxt("67_67_res.txt", Z, "%.3f", delimiter="\t")
    print "%d_%d_res.txt" % (X.shape[0], X.shape[1])
    np.savetxt("%s_%d_%d_res.txt" % (filename, X.shape[0], X.shape[1]), Z, "%.4f", delimiter="\t")
    # print "Z[34,34] IS", Z[34, 34]

    plt.plot(Z[:, Z.shape[1] / 2])
    plt.show()

    res_mid_fit = []
    data_for_mid_fit = Z[:, Z.shape[1] / 2]
    for each in xrange(0, 120 - 60, 1):
        res_mid_fit.append(data_for_mid_fit[each:each + 60].sum() / 60)
    plt.plot(res_mid_fit)
    plt.show()

    im = plt.imshow(Z, cmap=plt.cm.gray)
    plt.title("%s_%d*%d_2D" % (filename, X.shape[0], X.shape[1]))
    plt.colorbar(im)
    plt.show()

    tmp = []
    i = 0
    # print "begin 50*50 replace"

    min_row_size = 100
    min_col_size = 100

    print "begin %d*%d replace" % (min_row_size, min_row_size)
    # for data_array in Z:
    # for data in data_array:
    # tmp.append(get_new_data(data, min_row_size, min_col_size))

    for each in Z.flatten():
        tmp.append(get_new_data(each, min_row_size, min_col_size))

    tmp = np.array(tmp)
    print "tmp.shape is", tmp.shape

    res1 = []
    cnt = 0
    a_res = np.ones(X.shape[0] * min_row_size * X.shape[1] * min_col_size).reshape(X.shape[0] * min_row_size,
                                                                                   X.shape[1] * min_col_size)
    print "X.shape is ", X.shape
    for row in xrange(0, X.shape[0]):
        for col in xrange(0, X.shape[1]):
            a_res[row * min_row_size:row * min_row_size + min_row_size,
            col * min_col_size:col * min_col_size + min_col_size] = tmp[cnt]
            cnt = cnt + 1
    # print "50*50 replace over"
    print "%d*%d replace over" % (min_row_size, min_row_size)

    fig = plt.Figure(figsize=(120 / 25.4, 120 / 25.4), dpi=25.4 * 20)
    # fig = plt.Figure()
    ax = plt.subplot(111)
    # fig, ax = plt.subplots()
    im = ax.imshow(a_res, cmap=plt.cm.gray)
    # plt.colorbar(im)
    print "a_res.shape is ", a_res.shape
    np.savetxt("final.txt", a_res, fmt="%.4f", delimiter="\t")
    ax.axis("off")
    plt.savefig("res1.tif")
    plt.savefig("res1.png")
    # plt.savefig("res1.pdf")
    plt.show()

    out_put_photo("unicom_res.tif", a_res)

    index = []

    index2mm = 0.01
    mm2index = 100
    for row_index in xrange(0, X.shape[0] * min_row_size):
        for col_index in xrange(0, X.shape[1] * min_row_size):
            if a_res[row_index, col_index] == 0:
                index.append([row_index * index2mm, col_index * index2mm])
    index = np.array(index)
    np.savetxt("unicom_top_left_v1.1.txt", index, fmt="%.3f", delimiter="\t")
    index += index2mm / 2
    np.savetxt("unicom_center_v1.1.txt", index, fmt="%.3f", delimiter="\t")

    # for r in xrange(30, 50, 10):
    #     # b_res = get_sum_at_col(a_res, col_start_index=67 * 50 / 2, width=50, height=50, step=step)
    #     b_res = get_sum_in_cols_with_circle_shape(a_res, col_start_pos=a_res.shape[0] * index2mm / 2, r=r,
    #                                               step=1)
    #     plt.plot(b_res / (np.pi * r ** 2 * 20 * 20))
    #     plt.title("%d*%d data sum in middle cols,step="%(min_row_size,min_row_size) + str(1))
    #     plt.savefig(str(1) + "step_size.tif")
    #     plt.show()

    img = Image.open("res11.png")
    xxx = img.convert("1").tobitmap()
    # xxx=img.tobitmap()
    img1 = Image.open(StringIO.StringIO(xxx))
    img1.show()

    res1 = a_res.reshape(x_size * min_col_size, x_size * min_row_size)

    print "len of res1 is", len(res1)
    # res1 = np.array(res1).reshape(67*3,67*3)


    fig, ax = plt.subplots()

    im = ax.imshow(res1, cmap=plt.cm.gray)

    print "res1 shape is", res1.shape
    # plt.savefig("qiangdu.png")
    plt.colorbar(im)
    plt.title("res1_final")
    plt.show()
    # np.savetxt("tmp.txt",tmp,"%.6f",delimiter="\t")


    # pass
