#!/usr/bin/python
# -*- coding:utf-8 -*-
import re
import sys
import urllib
import urllib2
import datetime


class CFlvcd(object):
    def __init__(self):
        self.url = ""
        # self.pattern = re.compile(r"<a href *= *\"(http://f\.youku\.com/player/getFlvPath/[^\"]+)")
        self.pattern = re.compile(r"(http://data\.vod\.itc\.cn/\?.+\.mp4[^\"]+)")
        self.headers = {"Accept": "*/*", "Accept-Language": "zh-CN", "": "",
                        "User-Agent": "Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.1)",
                        # "Accept-Encoding":"gzip, deflate",
                        "Connection": "Keep-Alive"}

    def parse(self, url):
        self.url = "http://www.flvcd.com/parse.php?kw=" + url + "&format=super"
        req = urllib2.Request(url=self.url, headers=self.headers)
        res = urllib2.urlopen(req)
        data = res.read()
        print data
        re_res = self.pattern.findall(data)
        if re_res != None:
            filename = datetime.datetime.now().strftime("%Y%m%d-%H%M%S.lst")
            fhandle = open(filename, "w")
            for url in re_res:
                # 注意是\r\n还是\n
                fhandle.write(url + "\r\n")
            fhandle.close()
            print("Parse URL Done!")
        else:
            print("URL Not Found")


if __name__ == "__main__":
    flvcd = CFlvcd()
    flvcd.parse(sys.argv[1])