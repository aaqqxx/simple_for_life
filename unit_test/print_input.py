# coding:utf-8
# !/usr/bin/env python

__author__ = 'XingHua'

"""

"""


def print_input():
    print "please input your word:"
    txt = raw_input()
    cnt = len(txt)
    index = 0
    while index < cnt:
        print txt[index],
        index += 1
    pass


# test()
if __name__ == "__main__":
    print_input()
    pass