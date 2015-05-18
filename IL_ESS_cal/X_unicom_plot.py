# coding:utf-8
# !/usr/bin/env python

__author__ = 'XingHua'

"""

"""

from scipy import misc
import pylab as pl
from glob import glob
from scipy import ndimage
import numpy as np
from scipy import ndimage
import matplotlib.pyplot as plt
from mpl_toolkits.axes_grid.axislines import SubplotZero


axis_offset = 0

k = 4
d1 = 7.1 * k
d2 = 7.9 * k
d3 = 8.6 * k
d4 = 9.4 * k


def get_outer_line(data):
    data_max = data.max()
    pos_1000 = -d2 / 2
    data_500 = data_max * 0.500
    pos_500 = -d4 / 2
    # data_005 = data.min()+ 0.005
    data_005 = data.max() * 0.005
    line_k_factor = (data_max - data_500) / ((d4 - d2) / 2)
    B = data_max - (-d2 / 2) * line_k_factor
    a = np.array([[pos_1000, 1], [pos_500, 1]])
    b = np.array([data_max, data_500])
    k, b = np.linalg.solve(a, b)
    print k, b
    pos_005 = (data_005 - b) / k
    pos = np.array([pos_005 - 10, pos_005, pos_500, pos_1000, -pos_1000, -pos_500, -pos_005, -pos_005 + 10])
    res = np.array([data_005, data_005, data_500, data_max, data_max, data_500, data_005, data_005])
    # print pos
    return pos, res
    pass


def get_inner_line(data):
    data_max = data.max()
    data_966 = data_max * 0.966
    pos_966 = -d1 / 2
    data_500 = data_max * 0.500
    pos_500 = -d3 / 2
    # data_min = data.min()
    data_min = data.max() * 0.0
    line_k_factor = (data_966 - data_500) / ((d3 - d1) / 2)
    B = data_966 - (-d1 / 2) * line_k_factor
    a = np.array([[pos_966, 1], [pos_500, 1]])
    b = np.array([data_966, data_500])
    k, b = np.linalg.solve(a, b)
    print k, b
    pos_000 = (data_min - b) / k
    pos = np.array([pos_000 - 10, pos_000, pos_500, pos_966, -pos_966, -pos_500, -pos_000, -pos_000 + 10])
    res = np.array([data_min, data_min, data_500, data_966, data_966, data_500, data_min, data_min])
    return pos, res
    pass


if __name__ == "__main__":
    data_file_name = "x0_OE_avg_list.txt"
    pos_file_name = "x0_OE_pos.txt"
    data = np.loadtxt(data_file_name)
    y_pos = np.loadtxt(pos_file_name)

    fig = plt.figure()
    ax = SubplotZero(fig, 111)
    fig.add_subplot(ax)
    for direction in ["xzero", "yzero"]:
        ax.axis[direction].set_axisline_style("-|>")
        ax.axis[direction].set_visible(True)

    for direction in ["left", "right", "bottom", "top"]:
        ax.axis[direction].set_visible(False)

    ax.spines['right'].set_visible(False)
    ax.spines['top'].set_visible(False)
    y_ticks_ypos = [0.005, 0.5, 0.966 - 0.05, 1, -0.2, -0.3, -0.4, -0.5]
    y_ticks_xpos = [2, 2, -2, -2, 0, 0, 0, 0]
    y_ticks_label = ["0.5%", "50%", "96.6%", "100%", str(d1) + "mm", str(d2) + "mm", str(d3) + "mm", str(d4) + "mm"]
    color_list = ["k"] * 4 + ["r"] * 4

    # ax.set_yticks(y_ticks_pos)
    ax.set_yticks([])
    txt = []
    for index, y in enumerate(y_ticks_ypos):
        txt.append(ax.text(y_ticks_xpos[index], y, y_ticks_label[index],
                           rotation=0, va='bottom', ha='center', color=color_list[index]))

    # ax.set_yticklabels(("0.5%", "50%", "96.6%", "100%"), rotation=180)

    # 画箭头
    arrow_y_pos_list = [-0.2, -0.3, -0.4, -0.5]
    arrow_x_pos_list = [d1 / 2, d2 / 2, d3 / 2, d4 / 2]
    for x, y in zip(arrow_x_pos_list, arrow_y_pos_list):
        ax.annotate("", xytext=(-x, y), xy=(x, y), arrowprops=dict(arrowstyle='<->', ))

    # plt.plot(x_pos, (data-data.min())/(data-data.min()).max())
    ax.plot(y_pos, data)
    outer_line = get_outer_line(data)
    inner_line = get_inner_line(data)
    print outer_line
    print inner_line
    ax.plot(outer_line[0], outer_line[1], "r")
    ax.plot(inner_line[0], inner_line[1], "r")
    # plt.plot(big_line,"r")

    ax.plot([-d4 / 2 - 5, d4 / 2 + 5], [0.5, 0.5], 'k')

    arrow_offset = 0.05
    dist_list = [d1, d2, d3, d4]
    h_line_y_pos = [data.max() * 0.966, data.max() * 1, data.max() * 0.5, data.max() * 0.5]
    for dist, line_y_pos, arrow_y_pos in zip(dist_list, h_line_y_pos, arrow_y_pos_list):
        ax.plot([-dist / 2, -dist / 2], [line_y_pos, arrow_y_pos - arrow_offset], "k--")
        ax.plot([dist / 2, dist / 2], [line_y_pos, arrow_y_pos - arrow_offset], "k--")

    ax.set_ylim(-0.6, 1.1)
    ax.set_xlim(-y_pos.max() * 1.01, y_pos.max() * 1.01)
    ax.text(35 + 1, -0.08, "Y",
            rotation=0, va='bottom', ha='center', )
    ax.set_xticks([])
    plt.show()
    pass

    data_file_name = "y_inter.txt"
    pos_file_name = "y0_xpos.txt"
    data = np.loadtxt(data_file_name)
    x_pos = np.loadtxt(pos_file_name)

    d5 = 26 * k - axis_offset
    ref_factor = 0.976
    ref_line1_x_pos = [-x_pos.max(), -d5 / 2, -d5 / 2, d5 / 2, d5 / 2, x_pos.max()]
    ref_line1_y_pos = [data.max() * 0.005, data.max() * 0.005, data.max() * ref_factor, data.max() * ref_factor,
                       data.max() * 0.005, data.max() * 0.005]

    ref_line2_x_pos = [-x_pos.max(), -d5 / 2, -d5 / 2, d5 / 2, d5 / 2, x_pos.max()]
    ref_line2_y_pos = [data.max() * 0.0, data.max() * 0., data.max() * 1, data.max() * 1, data.max() * 0,
                       data.max() * 0]

    fig = plt.figure()
    ax = SubplotZero(fig, 111)
    fig.add_subplot(ax)

    for direction in ["xzero", "yzero"]:
        ax.axis[direction].set_axisline_style("-|>")
        ax.axis[direction].set_visible(True)

    for direction in ["left", "right", "bottom", "top"]:
        ax.axis[direction].set_visible(False)

    ax.plot(ref_line1_x_pos, ref_line1_y_pos, "r")
    ax.plot(ref_line2_x_pos, ref_line2_y_pos, "r")
    ax.plot([-d5 / 2, -d5 / 2], [1, -0.15], 'k--')
    ax.plot([d5 / 2, d5 / 2], [1, -0.15], 'k--')
    ax.plot(x_pos, data)

    ax.text(7, 1, "100%",
            rotation=0, va='bottom', ha='center', color="k")
    ax.text(7, 0.93, str(ref_factor * 100) + "%",
            rotation=0, va='bottom', ha='center', color="k")

    ax.text(d5 / 2 + 5, 0.005, "0.5%",
            rotation=0, va='bottom', ha='center', color="k")

    ax.text(7, 1.05, "$I(X)/I_{max}$",
            rotation=0, va='bottom', ha='center', color="k")
    ax.text(x_pos.max(), -0.1, "X",
        rotation=0, va='bottom', ha='center', color="k")

    ax.text(0, -0.1, str(d5) + "mm",
            rotation=0, va='bottom', ha='center', color="k")

    ax.annotate("", xytext=(-d5 / 2, -0.1), xy=(d5 / 2, -0.1), arrowprops=dict(arrowstyle='<->', ))

    ax.set_ylim(-0.11, 1.02)
    ax.set_xlim(-x_pos.max() * 1.01, x_pos.max() * 1.01)
    ax.set_yticks([])
    ax.set_xticks([])
    # plt.ylim(0,1.05)
    plt.show()