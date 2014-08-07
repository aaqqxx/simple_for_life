# coding:utf-8
#!/usr/bin/env python
from __future__ import unicode_literals

__author__ = 'XingHua'

import numpy as np
import matplotlib

matplotlib.rcParams['font.sans-serif'] = ['SimHei']
from matplotlib import pyplot as plt
import random
from time import sleep
import sys

# plt.rcParams

"""

"""

font = {'family': 'serif',
        'color': 'darkred',
        'weight': 'normal',
        'size': 16,
}


def moving_average(data, steps):
    res = []
    if (steps > len(data)):
        print "steps nums too big"
        return None
    else:
        for each in xrange(len(data) - steps):
            data1 = data[each:each + steps].sum() / steps
            # print  data[each:each + steps].sum
            res.append(data1)
        return np.array(res)


if __name__ == "__main__":
    if len(sys.argv) == 2:
        filename = sys.argv[1]
    else:
        filename = r'..\data_process\EDU_Ophir_BMU_energy_data1'
    # print filename

    # x, y, z = np.loadtxt(filename, delimiter='\t', usecols=(0, 1, 2), skiprows=1, unpack=True)
    # x, y = np.loadtxt(filename, delimiter='\t', usecols=(0, 1), skiprows=1, unpack=True)

    Ophir, EDU, BMU = np.loadtxt(filename, delimiter='\t', usecols=(0, 1, 2), skiprows=1, unpack=True)

    OB = Ophir / BMU
    EB = EDU / BMU
    OE = Ophir / EDU

    OE_moving_avg = moving_average(OE, 7)

    Ophir_moving_avg = moving_average(Ophir, 7)
    EDU_moving_avg = moving_average(EDU, 7)
    BMU_moving_avg = moving_average(BMU, 7)

    # plt.text(0.2, 0.8, r"hello", fontdict=font)

    # 归一化
    Ophir = Ophir / Ophir.max()
    EDU = EDU / EDU.max()
    BMU = BMU / BMU.max()

    Ophir_moving_avg = Ophir_moving_avg / Ophir_moving_avg.max()
    EDU_moving_avg = EDU_moving_avg / EDU_moving_avg.max()
    BMU_moving_avg = BMU_moving_avg / BMU_moving_avg.max()

    # Ophir_line = plt.plot(Ophir, '-*',markersize=12 )
    # EDU_line = plt.plot(EDU, '-*', markersize=12)
    # BMU_line = plt.plot(BMU,'-*',markersize=12)

    Ophir_moving_avg_line = plt.plot(Ophir_moving_avg, '-*',markersize=12 )
    EDU_moving_avg_line = plt.plot(EDU_moving_avg, '-*', markersize=12)
    BMU_moving_avg_line = plt.plot(BMU_moving_avg,'-*',markersize=12)

    #OE_line = plt.plot(OE, '-*',markersize=12 )
    #OE_moving_avg_line = plt.plot(OE_moving_avg, '-*', markersize=12)

    #Ophir_line[0].set_label("Ophir")
    #EDU_line[0].set_label("EDU")
    #BMU_line[0].set_label("BMU")

    #Ophir_moving_avg_line[0].set_label("Ophir_moving_avg")
    #EDU_moving_avg_line[0].set_label("EDU_moving_avg")
    #BMU_moving_avg_line[0].set_label("BMU_moving_avg")


    plt.legend()

    #plt.ylim(0.2,0.35)

    #Ophir.min Ophir.max Ophir.mean Ophir.std Ophir_sigma=

    #note = "EDU: avg = %.4f, std = %.4f\n" % (Ophir.mean(), Ophir.std())
    #note += "BMU: avg = %.4f, std = %.4f\n" % (Ophir.mean(), Ophir.std())
    #note += "Ophir: avg = %.4f, std = %.4f\n" % (Ophir.mean(), Ophir.std())
    #plt.xlabel(note, fontdict=font)
    # plt.ylabel(note, rotation=0,verticalalignment="bottom")
    # plt.annotate('local max', xy=(2, 1), xytext=(3, 1.5),
    #              arrowprops=dict(facecolor='black', shrink=0.05),
    # )
    # plt.annotate('THE DAY I REALIZED\nI COULD COOK BACON\nWHENEVER I WANTED', (0, 0.13))
    print "ok"
    plt.title("Processed data")
    plt.show()

    # data1_plot=plt.plotfile(filename,(2,),delimiter='\t',subplots=False)