#coding:utf-8
#!/usr/bin/env python

__author__ = 'XingHua'

"""
最近需要将内存中的Flash Dump出来，找到一款软件 Flash吸血鬼，可以查找内存中的Flash，不过没有注册版本的不能直接
保存为Flash格式，于是自己摸索了半天，弄了一个Python版本的。

swf文件有两种，一种为未压缩的，另外一种为zlib压缩过的。

未压缩的：
1-3字节为：Hex: 46 57 53(ASCII: FWS)，
第4字节为：版本，
第5-8字节为swf文件大小，包含8字节文件头。
结尾4个字节为Hex:40 00 00 00

zlib压缩过的：
1-3字节为：Hex: 43 57 53(ASCII: CWS)，
第4字节为版本，
第5-8字节为swf未压缩前大小。
第9字节为Hex:78，
第10字节为zlib压缩方法，
从第9字节开始需要用zlib解压。

Flash版本现在常用的有 0x07,0x08,0x09,0x0A

Python版Flash吸血鬼需要解决2个问题

能把进程的内存dump到文件
遍历文件，把Flash都找出来
dump内存，这里使用了[winappdbg][1]，很好用的一个Python win32库。在Win7下使用，需要保证运行权限是管理员权限，
才能成功dump内存。

在文件里查找Flash，对于未压缩的直接提取即可，对于压缩过的，使用Python的zlib即可解压。


goolgechrome还有IE浏览器，貌似用这个脚本，得到的都不怎么对啊，临时文件很大，但是识别的flash一般只有50KB以内
感觉flash识别的算法不行啊。。。还要改进
"""

from winappdbg import Process, System, CrashDump
from winappdbg import win32
import zlib


class SwfDump(object):
    def __init__(self):
        self.num = 1

    def dump_byname(self, name):
        '''
        get Process pid by process name
        '''

        sy = System()
        sy.scan_processes()
        targets = set()
        pl = sy.find_processes_by_filename(name)

        if not pl:
            print "Process not found: %s,\nMake true your are logined on as administrator." % name
            exit()

        for p, n in pl:
            pid = p.get_pid()
            targets.add(pid)

        targets = list(targets)

        f = file('tmp', 'wb')
        for pid in targets:
            process = Process(pid)
            process.get_handle()

            #dump process content to tmp
            for mbi in process.take_memory_snapshot():
                if mbi.content:
                    f.write(mbi.content)

        print "dump memory ok"

    def save_swf(self, data):
        with open("%i.swf" % self.num, 'wb') as f:
            f.write(data)
            print "%s swf dump ok" % self.num
            self.num += 1

    def dump_swf(self):
        ''' dump swf file from dump file '''

        with open("tmp", "rb") as f:
            map = f.read()

            #dump CWS swf file
            l = len(map)
            index = map.rfind('CWS', 0, l)
            while index > -1:
                if map[index:index + 3] == "CWS" and map[index + 8] == "x" and ord(map[index + 3]) in [0x08, 0x09,
                                                                                                       0x0A]:
                    try:
                        data = zlib.decompress(map[index + 8:])
                        data = "FWS" + map[index + 3:index + 8] + data
                        self.save_swf(data)
                    except:
                        pass
                index = map.rfind('CWS', 0, index)

            #dump FWS swf file
            index = map.rfind("FWS", 0, l)
            while index > -1:
                #get swf length
                size = ord(map[index + 4]) + ord(map[index + 5]) * 256 + ord(map[index + 6]) * 256 * 256 + ord(
                    map[index + 7]) * 256 * 256 * 256
                #max file size 10M
                if size < 1000000 and ord(map[index + 3]) in [0x08, 0x09, 0x0A] and ord(map[index + size - 4]) == 0x40:
                    data = map[index:index + size]
                    self.save_swf(data)
                index = map.rfind("FWS", 0, index)

            print "dump done. Calum(http://sa3.org)"

    def dump_swf1(self):
        ''' dump swf file from dump file '''

        with open("tmp", "rb") as f:
            map = f.read()
            #dump CWS swf file
            l = len(map)
            index = map.find('CWS', 0, l)
            while index > -1:
                if map[index:index + 3] == "CWS" and map[index + 8] == "x" and ord(map[index + 3]) in [0x08, 0x09,
                                                                                                       0x0A]:
                    print "zz"
                    try:
                        data = zlib.decompress(map[index + 8:])
                        data = "FWS" + map[index + 3:index + 8] + data
                        self.save_swf(data)
                    except:
                        pass
                index = map.rfind('CWS', index, -1)
                print index
            print "dump CWS swf file over,begin dump FWS swf file."

            #dump FWS swf file
            index = map.find("FWS", 0, l)
            while index > -1:
                #get swf length
                size = ord(map[index + 4]) + ord(map[index + 5]) * 256 + ord(map[index + 6]) * 256 * 256 + ord(
                    map[index + 7]) * 256 * 256 * 256
                #max file size 10M
                if size < 1000000 and ord(map[index + 3]) in [0x08, 0x09, 0x0A] and ord(map[index + size - 4]) == 0x40:
                    data = map[index:index + size]
                    self.save_swf(data)
                index = map.find("FWS", index, -1)

            print "dump done. Calum(http://sa3.org)"

if __name__ == '__main__':
    import sys

    if len(sys.argv) < 2:
        print "Usage: python swfdump.py process name \n       python swfdump.py firefox.exe"
        exit()

    swfdump = SwfDump()
    swfdump.dump_byname(sys.argv[1])
    swfdump.dump_swf1()