#coding:utf-8
#!/usr/bin/env python

__author__ = 'XingHua'

"""
1.最简单的办法是把文件读入一个大的列表中,然后统计列表的长度.如果文件的路径是以参数的形式filepath传递的,
那么只用一行代码就可以完成我们的需求了:

2.当外部系统提供统计行数的方法时,你可以使用它们(通过os.popen),如unix的wc - l.当然,通过自己的程序来完成会更简单
,快捷和通用.你可以假设大多数的文本文件都有合理的大小,所以把它们一次读入内存中处理是可行的.对于这样的情况,len方
法返回readlines的大小是最简单的.假如一个文件的大小大于内存(比如,有好几百M那么大),那个最简单的方法会变得难以忍
受的慢,因为操作系统要使用虚拟内存,并不停同过硬盘来换页.也可能出现失败的情况 ,就是虚拟内存不够大.一台有256M内存
的机器,当处理一个1G或2G大小的文件的时候,仍然可能出现严重的问题.在这种情况下,使用循环处理是比较好的方式,
enumerate保存了函数.
3.核心思想是统计缓存中回车换行字符的个数.这可能最不容易直接想到的方法,也是最不通用的方法,但它可能是最快的方法.

"""


def get_line_nums1(filepath):
    count = len(open(filepath,'rU').readlines())
    return count

def get_line_nums2(filepath):
    count = -1
    for count, line in enumerate(open(filepath, 'rU')):
        pass
    count += 1
    return count

def get_line_nums3(thefilepath):
    count = 0
    thefile = open(thefilepath, 'rb')
    while True:
        buffer = thefile.read(8192*1024)
        if not buffer:
            break
        count += buffer.count('\n')
    thefile.close()
    return count

if __name__=="__main__":
    get_line_nums1()
    get_line_nums2()
    get_line_nums3()