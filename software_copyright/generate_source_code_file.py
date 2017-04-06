# coding:utf-8
# !/usr/bin/env python

__author__ = 'XingHua'

"""
将文件中的空白行都去掉。
"""

from glob import glob

if __name__ == "__main__":
    # file_name = r"E:\aaqqxx\pupil20150110\20150110Afternoon1\pupil_20150110_145913_264"
    txt_file_name_list = glob(r"E:\aaqqxx\IL_project\server\data_analysis\GUI\IL_data_analysis\*.py")
    # txt_file_name_list = glob(r"pupil_*.txt")
    txt_file_name_list.sort()
    txt = ""
    for file_name in txt_file_name_list:
        #rc文件太大，不需要
        if "_rc" not in file_name:
            print file_name
            txt += "\n"*3 + file_name + "\n"*2
            f = open(file_name)
            lines = f.readlines()
            f.close()
            res= ( txt +line for line in lines if line.strip())
            for line in lines:
                if line.strip():
                    txt += line
    output_file = "source_code.txt"
    f = open(output_file,"w")
    f.write(txt)
    f.close()
    # print txt