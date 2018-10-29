#!/usr/bin/env python
# -*- coding: utf-8 -*-

import win32com, os, sys, re
from win32com.client import Dispatch, constants


target_path = r"d:\daizhuan"
save_path = r"d:\wancheng"
# 打开新的文件
suoyou = os.listdir(target_path)
# print suoyou
for i in suoyou:
    wenjian_name = os.path.join(target_path, i)
    # print wenjian_name
    if os.path.isfile(wenjian_name):
        w = win32com.client.Dispatch('Word.Application')
        w.Visible = 0
        w.DisplayAlerts = 0
        daizhuan = 'd:\\daizhuan\\%s' % i  # 准备替换的文件夹
        wancheng = 'd:\\wancheng\\%s' % i  # 替换完成后输出的目录
        doc = w.Documents.Open('d:\\biaozhun\\biaozhun.doc')
        w.ActiveDocument.Sections[0].Headers[0].Range.Copy()
        wc = win32com.client.constants
        doc.Close()

        doc2 = w.Documents.Open(daizhuan)
        w.ActiveDocument.Sections[0].Headers[0].Range.Paste()
        w.ActiveDocument.SaveAs(wancheng)
        doc2.Close()

        doc3 = w.Documents.Open('d:\\biaozhun\\biaozhun.doc')
        w.ActiveDocument.Sections[0].Footers[0].Range.Copy()
        doc3.Close()

        doc4 = w.Documents.Open(daizhuan)
        w.ActiveDocument.Sections[0].Footers[0].Range.Paste()
        doc4.Close()
        try:
            w.Documents.Close()
            w.Quit()
        except Exception, e:
            print str(e)