# coding:utf-8
#!/usr/bin/env python

__author__ = 'XingHua'

"""
com 调用示例(使用Windows Media Player 播放音乐)
貌似不管用，难道是路径问题或者是文件格式问题？需要wma？
"""

from win32com.client import Dispatch
mp = Dispatch("WMPlayer.OCX")
tune = mp.newMedia("e:/manmandeng.mp3")
mp.currentPlaylist.appendItem(tune)
mp.controls.play()