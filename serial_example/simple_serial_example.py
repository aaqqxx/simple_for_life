# coding:utf-8
#!/usr/bin/env python

__author__ = 'XingHua'

"""

"""

import serial
ser = serial.Serial()
ser.baudrate = 38400
ser.port = 0
ser.open()
# ser.read(5)
# ser.write("hello")
print ser.read(5)