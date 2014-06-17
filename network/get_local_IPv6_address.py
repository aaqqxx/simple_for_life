#coding: utf-8
#/usr/bin/env python

"""
这个Python脚本用于登录北科大校园网，修改文件中的username和password后，将文件
放到启动项中，就可以实现开机自动登录校园网了。
Python版本：2.7.3
"""

import httplib
import subprocess
import re

def get_local_ipv6_address():
    """
    This function will return your local machine's ipv6 address if it exits.
    If the local machine doesn't have a ipv6 address,then this function return None.
    This function use subprocess to execute command "ipconfig", then get the output
    and use regex to parse it ,trying to  find ipv6 address.
    """
    getIPV6_process = subprocess.Popen("ipconfig", stdout = subprocess.PIPE)
    output = (getIPV6_process.stdout.read())
    ipv6_pattern='(([a-f0-9]{1,4}:){7}[a-f0-9]{1,4})'
    #    m = re.search(ipv6_pattern, str(output))
    # 找到所有匹配的ipv6地址
    m = re.findall(ipv6_pattern, str(output))
    if m != []:
    #        return m.group()[1]
        # 返回临时IPv6
        print type(m)
        return m[1][0]
    else:
        return None

if __name__ == '__main__':
    #请将username和password修改成自己真实的校园网账户和密码
    username = 's201212'
    password = 'ddfds'

    headers = {"Connection": "keep-alive",
               "Cookie": "myusername=%s; pwd=%s; username=%s; smartdot=%s" % (username, password, username, password)}
    body = "DDDDD=%s&upass=%s&0MKKey=123456789&v6ip=%s&savePWD=on" % (username, password, get_local_ipv6_address())
    conn = httplib.HTTPConnection("202.204.48.82")
    conn.request("POST", "/", body = body,headers = headers)
    response = conn.getresponse()
    print response.status, response.reason

