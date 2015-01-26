# coding:utf-8
#!/usr/bin/env python

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


def get_info(filename):
    info = np.loadtxt(filename, delimiter="\t", dtype=float, skiprows=1)
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
    for x_index in xrange(z_data_input.shape[1]):
        for y_index in xrange(z_data_input.shape[0]):
            for index in range(len(_min)):
                if _min[index] <= np.sqrt((x_index * 1.5 + x_start_pos + 0.75) ** 2 + (
                                    y_index * 1.5 + y_start_pos + 0.75) ** 2) < \
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
    data = np.loadtxt(filename, delimiter="\t", usecols=range(0, 20))
    for index, each in enumerate(data[0]):
        res_dict[each] = data[1:, index]
    res_dict[1] = []
    return res_dict
    pass


# print "get qiangdu dict",sorted(get_qiangdu_dict().keys())

def get_new_data(qiangdu):
    res = np.ones(50 * 50, dtype=np.bool)
    # if qiangdu==1:
    # # res[res.size/2]=0
    # return res.reshape(50,50)
    qiangdu_dict = get_qiangdu_dict()
    for each in qiangdu_dict[qiangdu]:
        if each < 2500:
            res[each] = 0
    return res.reshape(50, 50)
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

plt.show()

# for each in sorted(get_qiangdu_dict().keys()):
# im=plt.imshow(get_new_data(each))
# plt.title(str(each))
#     plt.colorbar(im)
#     plt.show()

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


def get_sum_at_col(data_2D, col_start_index=67 * 50 / 2 - 50, width=50, height=50, step=50):
    res = []
    print "data_2D.shape is", data_2D.shape
    for row_index in xrange(data_2D.shape[0] / step):
        print "data_2D area is",data_2D[row_index:row_index + height, col_start_index:col_start_index + width]
        res.append(data_2D[row_index:row_index + height, col_start_index:col_start_index + width].sum())
    print res
    return res
    pass


data_tmp = np.arange(0, 81).reshape(9, 9)
get_shape_array_jiugong(data_tmp, 3, 3)





# for each in qiangdu_value_dict.keys():
# for each in np.arange(1,0.92-0.004,-0.004):
# print "each =", each
# #浮点数的精度问题。。。
# get_new_data(np.round(each*1000)/1000)

# zzz=get_new_data(0.92)
# print "zzz is ",zzz
# plt.imshow(get_new_data(0.92),cmap=plt.cm.gray,interpolation='nearest')
# plt.show()






if __name__ == "__main__":
    if len(sys.argv) == 2:
        filename = sys.argv[1]
        print filename
    else:
        # filename = ur'./data/20141024/EDU_Ophir_NPulse_energy_data_20141024_4'
        # filename = ur'/home/aaqqxx/IL/server/data_analysis/data/20141024/ESS_energy_data20141024_PM7_bak'
        filename = ur'data_info.txt'

    x_start_pos = -100.5 / 2
    x_end_pos = 100.5 / 2
    x_step = 1.5

    y_start_pos = -100.5 / 2
    y_end_pos = 100.5 / 2
    y_step = 1.5

    X = get_x(x_start_pos, x_end_pos, x_step)
    Y = get_y(y_start_pos, y_end_pos, y_step)
    Z = init_z_data()

    _min, _max, _value = get_info(filename)
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
    print "Z[34,34] IS", Z[34, 34]

    plt.plot(Z[:, Z.shape[1] / 2])
    plt.show()

    im = plt.imshow(Z, cmap=plt.cm.gray)
    plt.title("67*67_2D")
    plt.colorbar(im)
    plt.show()

    tmp = []
    i = 0
    print "begin 50*50 replace"
    for data_array in Z:
        for data in data_array:
            tmp.append(get_new_data(data))

    tmp = np.array(tmp)
    print "tmp.shape is", tmp.shape

    res1 = []
    min_row_size = 50
    min_col_size = 50
    cnt = 0

    a_res = np.ones(67 * min_row_size * 67 * min_col_size).reshape(67 * min_row_size, 67 * min_col_size)
    for row in xrange(0, 67):
        for col in xrange(0, 67):
            a_res[row * min_row_size:row * min_row_size + min_row_size,
            col * min_col_size:col * min_col_size + min_col_size] = tmp[cnt]
            cnt = cnt + 1
    print "50*50 replace over"
    # txt = ""
    # save_file = open("data_50_50.txt", "w")
    # print "begin save black point pos..."
    # for row_index, each in enumerate(a_res):
    # for col_index, each1 in enumerate(each):
    #         if each1 == 0:
    #             # print "row_index and col_index is", row_index, col_index
    #             txt = str(row_index * 0.03) + " " + str(col_index * 0.03) + "\n"
    #             save_file.write(txt)
    # print "save black point pos Over"
    # save_file.close()

    fig, ax = plt.subplots()
    im = ax.imshow(a_res, cmap=plt.cm.gray)

    ax.axis("off")
    # ax.invert_yaxis()
    # plt.colorbar(im)
    # plt.legend()
    # ax.spines['left'].set_position(('outward', 1000))
    # ax.spines['bottom'].set_position(('outward', 100))
    # ax.spines['right'].set_visible(False)
    # ax.spines['top'].set_visible(False)
    # ax.spines['left'].set_visible(False)
    # ax.spines['bottom'].set_visible(False)
    # plt.savefig("res1.svg")
    plt.show()

    b_res = get_sum_at_col(a_res, 0)
    plt.plot(b_res)
    plt.title("50*50 data sum in middle cols")
    plt.show()

    img = Image.open("res11.png")
    xxx = img.convert("1").tobitmap()
    # xxx=img.tobitmap()
    img1 = Image.open(StringIO.StringIO(xxx))
    img1.show()
    # img.show()

    #
    # tmp=np.hsplit(tmp,67)
    # tmp=np.array(tmp)
    # tmp=np.hsplit(tmp,67)
    # tmp=np.array(tmp)
    res1 = a_res.reshape(67 * 50, 67 * 50)

    print "len of res1 is", len(res1)
    # res1 = np.array(res1).reshape(67*3,67*3)

    fig, ax = plt.subplots()

    im = ax.imshow(res1, cmap=plt.cm.gray)

    print "res1 shape is", res1.shape
    # plt.savefig("qiangdu.png")
    plt.colorbar(im)
    plt.show()
    # np.savetxt("tmp.txt",tmp,"%.6f",delimiter="\t")


    # pass