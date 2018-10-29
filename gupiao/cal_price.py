# coding:utf-8
# !/usr/bin/env python

__author__ = 'XingHua'

"""

"""

# Example of Naive Bayes implemented from Scratch in Python
import numpy
import re
import math
import matplotlib.pyplot as plt
from matplotlib.ticker import MultipleLocator, FormatStrFormatter

txt = r"1990年1美元兑换4.783人民币元，1991年1美元兑换5.323人民币元，1992年1美元兑换5.516人民币元，1993年1美元兑换5.762人民币元，1994年1美元兑换8.619人民币元，1995年1美元兑换8.351人民币元，1996年1美元兑换8.314人民币元，1997年1美元兑换8.290人民币元，1998年1美元兑换8.279人民币元，1999年1美元兑换8.278人民币元。"

res = re.findall("\d.\d\d\d", txt)
years = re.findall("\d\d\d\d", txt)
print(res)
ax = plt.subplot()
ax.plot(years, res, "-o")
plt.grid()
plt.gca().xaxis.set_major_locator(MultipleLocator(1))
plt.show()


def cal_dia(awg):
    d = 0.127 * 92 ** ((36. - awg) / 39)
    return d


print((cal_dia(22)))
awg = list(range(0, 64))
zz = list(map(cal_dia, awg))
print(zz)
tmp=[]
for each in zz:
    tmp.append(each)
    print(each)
plt.plot(list(zz),"-o")
plt.grid()
plt.gca().xaxis.set_major_locator(MultipleLocator(4))
plt.title(u"AWG2mm")
plt.show()
