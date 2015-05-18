# coding:utf-8
# !/usr/bin/env python

__author__ = 'XingHua'

"""
在读取大文件的时候，有时只需要读取文件的最后一行，如果从头开始的读的话会浪费很多资源。
"""
import os


def get_last_line(inputfile):
    filesize = os.path.getsize(inputfile)
    print filesize
    blocksize = 1024
    dat_file = open(inputfile, 'rb')
    last_line = ""
    if filesize > blocksize:
        maxseekpoint = (filesize // blocksize)
        dat_file.seek((maxseekpoint - 1) * blocksize)
    elif filesize:
        # maxseekpoint = blocksize % filesize
        dat_file.seek(0, 0)
    lines = dat_file.readlines()
    if lines:
        last_line = lines[-1].strip()
    # print "last line : ", last_line
    dat_file.close()
    return last_line


if __name__ == "__main__":
    file_name = r"e:\data"
    print get_last_line(file_name)