# coding:utf-8
#!/usr/bin/env python

__author__ = 'XingHua'

"""

"""

import time, thread

count = 0


def test():
    global count

    for i in range(0, 10000):
        count += 1


for i in range(0, 10):
    thread.start_new_thread(test, ())
time.sleep(5)
print count