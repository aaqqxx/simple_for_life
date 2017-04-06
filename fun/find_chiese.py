# coding:utf-8
#!/usr/bin/python

__author__ = 'XingHua'


import re

def find_chiese(txt):
    # pattern = u"([\x4E00-\x9FA5]+)"
    pattern = u"([\u4e00-\u9fa5]+)"
    res = re.findall(pattern,txt)
    if res:
        return res
    else:
        print "No found."
    pass


def main():
    txt = u"人啊打发aadfz"
    print find_chiese(txt)[0].encode("gbk")
    # print txt.encode("gbk")
    pass

if __name__ == '__main__':
    main()
    pass