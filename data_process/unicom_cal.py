# coding:utf-8

__author__ = 'XingHua'

import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from matplotlib import cm
from unicom_polar_dikaer_3D import get_new_data, out_put_photo
import datetime

def get_z(x, y):
    # print x.shape, x.size
    # print x
    # print y
    shape = x.shape
    x = x.flatten()
    y = y.flatten()
    z = np.sin(0.018371886863 * (x)) * 0.08 + 0.92
    # z = z.flatten()
    for each in xrange(len(x)):
        if np.abs(x[each]) > 85:
            z[each] = 1
    for each in xrange(len(y)):
        if np.abs(y[each]) > 35:
            z[each] = 1
    z = np.round(z,9)
    return z.reshape(shape)
    pass


if __name__ == '__main__':
    x_start = -90.
    x_end = 90.
    x_step = 1
    y_start = 0
    y_end = 0
    y_step = 1
    X = np.arange(x_start, x_end + x_step, x_step)
    Y = np.arange(y_start, y_end + y_step, y_step)
    print X,Y
    X, Y = np.meshgrid(X, Y)
    Z = get_z(X, Y)
    # print Z[1][5]
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

    stime=datetime.datetime.now()

    """
    开始替换元素:原始算法

    tmp = []
    i = 0
    # print "begin 50*50 replace"

    #1mmx1mm的范围使用200x200的数据进行填充
    min_row_size = 200
    min_col_size = 200

    print "begin %d*%d replace" % (min_row_size, min_row_size)
    # for data_array in Z:
    # for data in data_array:
    # tmp.append(get_new_data(data, min_row_size, min_col_size))

    for each in Z.flatten():
        tmp.append(get_new_data(each, min_row_size, min_col_size,file_name="LocalCordi20150901-2.txt"))

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
    print "%d*%d replace over" % (min_row_size, min_row_size)
"""


    """
    开始替换元素:优化算法
    """
    min_row_size = 200
    min_col_size = 200
    a_res = np.ones((Z.shape[0]*min_row_size,Z.shape[1]*min_col_size))
    print "begin %d*%d replace" % (min_row_size, min_row_size)
    for row in xrange(0, X.shape[0]):
        for col in xrange(0, X.shape[1]):
                a_res[row * min_row_size:row * min_row_size + min_row_size,
                    col * min_col_size:col * min_col_size + min_col_size] = get_new_data(Z[row][col], min_row_size, min_col_size,file_name="LocalCordi20150901-2.txt")
    print "%d*%d replace over" % (min_row_size, min_row_size)



    etime = datetime.datetime.now()
    print "past time : ",(etime-stime).total_seconds()

    # fig = plt.Figure(figsize=(120 / 25.4, 120 / 25.4), dpi=25.4 * 20)
    # fig = plt.Figure()
    # ax = plt.subplot(111)
    # fig, ax = plt.subplots()
    # im = ax.imshow(a_res, cmap=plt.cm.gray)
    # plt.colorbar(im)
    print "a_res.shape is ", a_res.shape
    np.savetxt("final_1mm.txt", a_res, fmt="%.4f", delimiter="\t")
    # ax.axis("off")
    # plt.savefig("res1.tif")
    # plt.savefig("res1.png")
    # plt.savefig("res1.pdf")
    # plt.show()

    # out_put_photo("unicom_res.tif", a_res)

    index = []

    row_index2mm = 1./min_row_size
    mm2row_index = min_row_size
    col_index2mm = 1./min_col_size
    mm2col_index = min_col_size

    for row_index in xrange(0, X.shape[0] * min_row_size):
        for col_index in xrange(0, X.shape[1] * min_row_size):
            if a_res[row_index, col_index] == 0:
                index.append([row_index * row_index2mm, col_index * col_index2mm])
    index = np.array(index)
    np.savetxt("unicom_top_left_1mm_v1.2.txt", index, fmt="%.3f", delimiter="\t")
    index += row_index2mm / 2
    np.savetxt("unicom_center_1mm_v1.2.txt", index, fmt="%.3f", delimiter="\t")

    pass
