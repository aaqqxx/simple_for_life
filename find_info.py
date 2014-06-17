#coding:utf-8
#!/usr/bin/env python

__author__ = 'SAF'

import re

if __name__=='__main__':
    txt = open(r'C:\Users\SAF\Desktop\fish_log.txt').read()
    #print txt
    #txt = 'Fish 7 ss'
    pattern1 = re.compile(r'Fish 7 attemps to attack \w+')
    m1=re.findall(pattern1,txt)
    #print m
    # for i,each in enumerate(m1):
    #     print i,each
    #     pattern = re.compile(r'Fish 7 attemps to attack \w+')

    pattern2 = re.compile(r'Fish \d+ attemps to attack Fish 8 at ')
    m2=re.findall(pattern2,txt)
    #print m
    for i,each in enumerate(m2):
        print i,each

