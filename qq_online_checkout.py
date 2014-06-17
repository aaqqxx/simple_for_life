#coding:utf-8
#!/usr/env/bin python

__author__ = 'XingHua'


import time,datetime
import urllib2
def chk_qq(qqnum):
    chkurl = 'http://wpa.qq.com/pa?p=1:'+`qqnum`+':1'
    a = urllib2.urlopen(chkurl)
    length=a.headers.get("content-length")
    a.close()
    print datetime.datetime.now()
    if length=='2329':
        return 'Online'
    elif length=='2262':
        return 'Offline'
    else:
        print length
        return 'Unknown Status!'

qq = 506926059
stat = chk_qq(qq)
print `qq` + ' is ' + stat