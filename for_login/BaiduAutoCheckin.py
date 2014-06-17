#coding:utf-8
#!/usr/bin/env python

__author__ = 'SAF'

#   Author: 柠之漠然 <shiniv.ning@gmail.com>
#
# 使用说明:
#	   1.安装python 2.x
#	   2.在脚本当前目录下建立'config'文件
#		   config文件中,一行一个账号,格式为
#			   ID1,email1,cookie1
#		   不希望收到邮件提醒的email写'x'  (邮件提醒在网络不好时可能引起错误导致崩溃)
#			   ID2,x,cookie2
#		   cookie可以在贴吧页面ctrl+shift+k执行alert(document.cookie);得到
#			   *最好是手机版贴吧的cookie
#			   *如果要获得多个账号的cookie,切换账号时要直接'清除cookie'不能'注销'
#	   3.执行 python BaiduAutoCheckin.py
#
import os
import re
import urllib
import urllib2
import smtplib
import threading
from email.mime.text import MIMEText
# getBars
def getBars(cookie):
    req = urllib2.Request(
        url='http://wapp.baidu.com/m?tn=bdFBW&tab=favorite',
        headers={
            'cookie': cookie,
            'User-Agent': 'mozilla firefox'
        }
    )
    try:
        res = urllib2.urlopen(req, timeout=5).read()
    except:
        return None
    barList = re.findall(r'(?:\d+\.<a href="[^"]+">)([^<]+)(?:</a>)', res)
    if barList:
        return barList
    else:
        return None


# 签到函数
def sign(bar, cookie, again=20):
    req = urllib2.Request(
        url='http://wapp.baidu.com/f/?kw=' + urllib.quote(bar),
        headers={
            'cookie': cookie,
            'User-Agent': 'mozilla firefox'
        }
    )
    try:
        res = urllib2.urlopen(req, timeout=10).read()
    except:
        return sign(bar, cookie)
        # 得到地址
    addr = re.search(r'(?<=<a href=")[^"]+(?=">签到)', res)
    # 不能签到或者签到过
    if not addr:
        return '0'
        # 替换'amp;'
    addr = re.sub(r'amp;', '', addr.group())
    req = urllib2.Request(
        url='http://wapp.baidu.com' + addr,
        headers={
            'cookie': cookie,
            'User-Agetn': 'mozilla firefox'
        }
    )
    try:
        res = urllib2.urlopen(req, timeout=10).read()
    except:
        # 超时
        return sign(bar, cookie)
    success = re.search(r'(?<="light">)\d(?=<\/span>)', res)
    if not success:
        if again:
            return sign(bar, cookie, again - 1)
        return '-1'
    return success.group()

# sendmail
def sendMail(usr, email, text):
    if email == 'x':
        return
    msg = MIMEText(text, 'plain', 'utf-8')
    msg['Subject'] = usr + '百度贴吧签到结果'
    msg['From'] = 'shiniv'
    msg['To'] = email + ';'
    try:
        smtp = smtplib.SMTP_SSL('smtp.gmail.com', '25')
        smtp.login('邮箱地址', '密码')
        smtp.sendmail('发件人邮箱', email + ';', msg.as_string())
        print '发送成功'
    except Exception, e:
        print '发送失败'
        print e
    finally:
        smtp.quit()

# 每个ID的线程
class thread(threading.Thread):
    def __init__(self, usr, email, cookie):
        self.usr = usr
        self.email = email
        self.cookie = cookie
        self.logs = ""
        threading.Thread.__init__(self)

        # run

    def run(self):
        bars = getBars(self.cookie)
        if not bars:
            print '%s 获取贴吧列表失败!\n' % self.usr
            return
        print '%s 共有%d个吧需要签到\n' % (self.usr, len(bars))
        self.logs += '======>' + self.usr + ' 开始签到!\n'
        for bar in bars:
            res = sign(bar, self.cookie)
            if res == '0':
                self.logs += bar + '吧今天已经签到!\n'
            elif res == '-1':
                self.logs += bar + '吧\t###\t签到失败!请自己补签\n'
            else:
                self.logs += bar + '吧签到成功,经验+' + res + '\n'
        self.logs += '======>' + self.usr + ' 签到完成!\n\n'
        print self.logs
        return sendMail(self.usr, self.email, self.logs)

        # 启动,读配置文件


def init():
    if os.path.exists('./' + 'config'):
        f = open('config')
        # 开线程
        for line in f:
            args = line.split(',')
            thread(args[0], args[1], args[2]).start()
        f.close()
    else:
        print '%s没有配置文件!' % os.getcwd()
        os._exit(-1)


init()