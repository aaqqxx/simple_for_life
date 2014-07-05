# coding:utf-8
#!/usr/bin/env python

__author__ = 'XingHua'

"""
thread模块已经不推荐使用了，考虑使用threading模块。
"""

import thread
import time


def run_thread(n):
    for i in range(n):
        print i


thread.start_new_thread(run_thread, (4,))  # 参数一定是元组，两个参数可以写成（a,b）
time.sleep(0.0001) #如果注释掉，则会出现Unhandled exception in thread started by sys.excepthook is missing lost sys.stderr
print "ok"
time.sleep(1)