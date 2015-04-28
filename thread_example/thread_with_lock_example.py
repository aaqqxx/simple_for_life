# coding:utf-8
#!/usr/bin/env python

__author__ = 'XingHua'

"""

"""
import time, thread

count = 0
lock = thread.allocate_lock()


def test():
    global count, lock
    lock.acquire()

    for i in range(0, 10000):
        count += 1

    lock.release()


for i in range(0, 10):
    thread.start_new_thread(test, ())
time.sleep(1)
print count