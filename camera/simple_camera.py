# coding:utf-8
#!/usr/bin/env python

__author__ = 'XingHua'

"""
此方案为朋友LSJ提出并实现的，转过来供学习用，由于在测试时没有架设WEB服务器，也没有做手机上的测试，仅通过PC测试了下，最完整解决方案请参考原出处《DIY手机监控系统》。

方法：

 1 下载并安装VideoCapture、PIL。

 2.编码，3s抓一个图片并保存
"""

from VideoCapture import Device
import time, string
interval = 2

cam = Device(devnum=0, showVideoWindow=0)

#cam.setResolution(648, 480)
cam.saveSnapshot('image.jpg', timestamp=3, boldfont=1, quality=75)

i = 0
quant = interval * .1
starttime = time.time()
while 1:
    lasttime = now = int((time.time() - starttime) / interval)
    print i
    cam.saveSnapshot('image.jpg', timestamp=3, boldfont=1)

    i += 1
    while now == lasttime:
        now = int((time.time() - starttime) / interval)
        time.sleep(quant)


"""
写个网页，3s刷新一次，如下：

[html]
<HTML>
<HEAD>
        <meta http-equiv="Content-Type" content="text/html; charset=gb2312" />
        <title>Web监视</title>
        <META  http-equiv="refresh"  content="3">
        <META  http-equiv="Expires"  content="0">
        <META  http-equiv="Pragma"   content="no-cache">
</HEAD>
    <body >
        <img src='image.jpg?mail=dyx1024@gmail.com' width="47%" height="381"/>
    </body>
</HTML>
"""