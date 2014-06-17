#coding:utf-8
#!/usr/bin/env python

__author__ = 'SAF'
import urllib, urllib2, cookielib, sys

class Login_e10000:
    login_header = {'User-Agent':'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.4 (KHTML, like Gecko) Chrome/22.0.1229.79 Safari/537.4'}
    signin_header = {'User-Agent':'Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/32.0.1700.76 Safari/537.36', 'X-Requested-With':'XMLHttpRequest', 'Content-Length':0,
                     'Origin':'http://bbs.e10000.cn/', 'Referer':'http://bbs.e10000.cn/'}
    email = ''
    password = ''
    cookie = None
    cookieFile = './cookie.dat'

    def __init__(self, email, pwd):
        self.email = email
        self.password = pwd
        self.cookie = cookielib.LWPCookieJar()
        opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(self.cookie))
        urllib2.install_opener(opener)

    def login(self):
        postdata = {'email':self.email, 'password':self.password, 'done':'http://bbs.e10000.cn/User/login.asp', 'submitflag':'ddddls-%2B%2B%2B'}
        postdata = urllib.urlencode(postdata)
        print 'Logining...'
        req = urllib2.Request(url='http://bbs.e10000.cn/member/login.asp', data=postdata, headers=self.login_header)
        result = urllib2.urlopen(req).read()
        self.cookie.save(self.cookieFile)
        result = str(result).decode('utf-8').encode('utf-8')
        if 'Email 或者密码错误' in result:
            print 'Login failed due to Email or Password error...'
            sys.exit()
        else :
            print 'Login successfully!'

    def signIn(self):
        postdata = {}
        postdata = urllib.urlencode(postdata)
        print 'signing...'
        req = urllib2.Request(url='http://bbs.e10000.cn/plug-ins/signcenter/Default.asp?action=update', data=postdata, headers=self.signin_header)
        result = urllib2.urlopen(req).read()
        result = str(result).decode('utf-8').encode('utf-8')
        print "result is ",result
        self.cookie.save(self.cookieFile)
        try:
            result = int(result)
        except ValueError:
            print 'signing failed...'
            sys.exit()
        except:
            print 'signing failed due to unknown reasons ...'
            sys.exit()
        print 'signing successfully!'
        print self.email,'have signed', result, 'days continuously...'


if __name__ == '__main__':
    user = Login_e10000('aaqqxx1910', '53yFlTPK')
    user.login()
    user.signIn()