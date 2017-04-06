#encoding:utf-8

__author__ = 'XingHua'

import urllib
import re


def remove_punctuation(text):
    return re.sub(ur"\p{P}+", "", text)


def find_most_long_chinese(txt):
    # a = re.findall(u"[\u4e00-\u9fa5]+\w+[\u3002]+",txt)
    a = re.findall(ur"[\u4e00-\u9fa5]+\w+[\w]+",txt)

    return a

if __name__ == '__main__':
    url = "http://www.yiibai.com/python/python3-webbug-series1.html"
    data = urllib.urlopen(url).read()
    data = data.decode('UTF-8')
    # print data
    # print "-"*100
    # data = ur"diaf人风机啊ii人漫长"
    for each in find_most_long_chinese(data):
        print each

