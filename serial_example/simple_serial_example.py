# coding:utf-8
# !/usr/bin/env python

__author__ = 'XingHua'

"""

"""

import serial
from time import sleep

ser = serial.Serial('COM1', 9600, timeout=5)

cmd_list = ["cmd13\r\ncmd14\r\n", "cmd2", "cmd3", "cmd4"]
res_length_list = [4, 4, 4, 4]

while True:
    for cmd, res_length in zip(cmd_list, res_length_list):
        ser.write(cmd)
        sleep(0.1)
        data = ser.read_all()
        print data
        sleep(1)
