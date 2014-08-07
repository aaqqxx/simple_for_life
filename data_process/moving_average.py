# coding:utf-8
#!/usr/bin/env python

__author__ = 'XingHua'

"""
移动平均
最大值 min
最小值 max
平均值 mean
标准偏差 std
"""

import numpy as np


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
    data_all = np.loadtxt("EDU_Ophir_BMU_energy_data", skiprows=0, delimiter="\t", usecols=(0, 1))

    res = moving_average(data_all, 3)
    print res, '\n', len(res)

