#coding:utf-8
#!/usr/bin/env python

__author__ = 'SAF'

"""
金山快盘自动签到
"""
import urllib
import urllib2
import cookielib
import json
import re


class Login_kp:
    def __init__(self):
        cj = cookielib.CookieJar()
        self.opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))
        urllib2.install_opener(self.opener)
        self.opener.addheaders = [('User-agent', 'IE')]

    def login(self, username, password):
        url = 'http://1.1.1.2/ac_portal/default/pc.html?tabs=pwd'
        # data = urllib.urlencode({'username': username, 'userpwd': password})
        data = urllib.urlencode({'password_name': username, 'password_pwd': password})
        print data
        req = urllib2.Request(url, data)
        print req.headers
        try:
            fd = self.opener.open(req)
        except Exception, e:
            print(u'网络连接错误！')
            return False
        if fd.url != "http://www.kuaipan.cn/home.htm":
            print(u"用户名跟密码不匹配！")
            return False
        print(u'%s 登陆成功，准备签到..   ' % username),
        return True

    def logout(self):
        url = 'http://www.kuaipan.cn/index.php?ac=account&op=logout'
        req = urllib2.Request(url)
        fd = self.opener.open(req)
        fd.close()

    def sign(self):
        url = 'http://www.kuaipan.cn/index.php?ac=common&op=usersign'
        req = urllib2.Request(url)
        fd = self.opener.open(req)
        sign_js = json.loads(fd.read())
        if sign_js['state'] == -102:
            print(u"今天已签到了!")
        elif sign_js['state'] == 1:
            print(u"签到成功! 获得积分：%d，总积分：%d；获得空间：%dM\n" % (
            sign_js['increase'], sign_js['status']['points'], sign_js['rewardsize']))
        else:
            print(u"签到失败！")
        fd.close()


if __name__ == '__main__':
    l = Login_kp()
    if l.login('maxinghua', 'abcd1234') == False:
        exit(1)
    l.sign()