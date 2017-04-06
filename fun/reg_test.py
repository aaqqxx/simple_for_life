#coding:utf-8
#!/usr/bin/python

import cookielib, urllib2, urllib, sys, time
import httplib

__author__ = 'XingHua'

http = httplib.HTTP('你要连接的host')

# write header
http.putrequest("POST", '/phpwind/post.php?')
http.putheader("User-Agent", "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; .NET CLR 1.1.4322; InfoPath.2; MAXTHON 2.0)")
http.putheader("Referer", 'http://10.16.62.100/phpwind/post.php?fid=2')
http.putheader("Host", '10.16.62.100')
http.putheader("Cookie", cookie)
http.putheader("Content-Type", 'multipart/form-data; boundary=---------------------------7d91d42da0af0')
http.putheader("Content-Length", str(len(data)))
http.endheaders()

# write body
http.send(data)

# get response
errcode, errmsg, headers = http.getreply()

if errcode != 200:
    raise Error(errcode, errmsg, headers)
file = http.getfile()
print file.read()