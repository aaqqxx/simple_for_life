# coding:utf-8
__author__ = 'XingHua'
import os
import datetime
import time

if __name__ == "__main__":
    result_dir = r'c:'
    l = os.listdir(result_dir)
    print l
    st = l.sort(key=lambda fn: os.path.getmtime(result_dir + "\\" + fn) if not os.path.isdir(
        result_dir + "\\" + fn) else 0)  # 第二句
    d = datetime.datetime.fromtimestamp(os.path.getmtime(result_dir + "\\" + l[-1]))
    print ('last file is ' + l[-1])
    time_end = time.mktime(d.timetuple())
    print 'time_end:', time_end
