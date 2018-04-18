#coding:utf-8
#!/usr/env/bin python

'''
最初的目的：GoogleChrome的缓存图片会自动把文件名去掉，浏览的图片想查看不太方便，想要实现在其缓冲的文件夹下面找到可能是
图片的文件，为其添加后缀方便在Windows系统中使用图像浏览器浏览。
在所需文件夹下，查找相应的文件名，找到后，添加文件后缀。
'''
__author__ = 'aaqqxx'

import os
import re
import sys

path=""

def find_the_file(path=os.getcwd(),pattern="*"):
    file_names_reg=os.listdir(path)
    res=[]
    for each in file_names_reg:
        m=re.match(pattern,each)
        if m is not None:
            print m.group()
            res.append(os.path.join(path,each))
        else:
            print "Find no file! Check the pattern!"
    return res

def change_file_name(oldname,new_suffix):
    os.rename(oldname,oldname+new_suffix)

def find_and_rename_files(path,pattern,new_suffix):
    res=find_the_file(path,pattern)
    [change_file_name(each,new_suffix) for each in res]

if __name__=="__main__":
    if len(sys.argv)!=0:
        res=find_the_file(sys.argv[1],'f_\w\w\w\w\w\w')
    res=find_the_file(path=r'C:\Documents and Settings\SIOM\Local Settings\Application Data\Google\Chrome\User Data\Profile 1\Cache',pattern=r'f_\w\w\w\w\w\w')
    for each in res:
       print each