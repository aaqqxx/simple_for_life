# coding:utf-8
# !/usr/bin/env python

__author__ = 'XingHua'

"""

"""

import serial
from time import sleep
from datetime import datetime


def cal_temp(temp, start_temp=-55., end_temp=150., min_dac=0., max_dac=65535.):
    k = (end_temp - start_temp) / (max_dac - min_dac)
    res = start_temp + k * temp
    return res
    pass


if __name__ == '__main__':
    print(cal_temp(37777, -55, 150))
