#!/usr/bin/env python
# coding: UTF-8
__author__ = 'XingHua'

'''
windows和linux采用了不同的编码，这让很多人伤透了脑经，
这里我采用了Python的chardet库获得代码的编码，然后修改编码
'''

import sys
import os
import chardet


def print_usage():
    print '''usage:
　　change_charset [file|directory] [charset] [output file]\n
　　for example:
　　  change 1.txt utf-8 n1.txt
　　  change 1.txt utf-8
　　  change . utf-8
　　  change 1.txt
'''
def get_charset(s):
    return chardet.detect(s)['encoding']


def remove(file_name):
    os.remove(file_name)


def change_file_charset(file_name, output_file_name, charset):
    f = open(file_name)
    s = f.read()
    f.close()

    if file_name == output_file_name or output_file_name == "":
        remove(file_name)

    old_charset = get_charset(s)
    u = s.decode(old_charset)

    if output_file_name == "":
        output_file_name = file_name
    f = open(output_file_name, 'w')
    s = u.encode(charset)
    f.write(s)
    f.close()


def do(file_name, output_file_name, charset):
    if os.path.isdir(file_name):
        for item in os.listdir(file_name):
            try:
                if os.path.isdir(file_name+"/"+item):
                    do(file_name+"/"+item, "", charset)
                else:
                    change_file_charset(file_name+"/"+item, "", charset)
            except OSError, e:
                print e
    else:
        change_file_charset(file_name, output_file_name, charset)


if __name__ == '__main__':
    length = len(sys.argv)

    if length == 1:
        print_usage()
    elif length == 2:
        do(sys.argv[1], "", "utf-8")
    elif length == 3:
        do(sys.argv[1], "", sys.argv[2])
    elif length == 4:
        do(sys.argv[1], sys.argv[3], sys.argv[2])
    else:
        print_usage()