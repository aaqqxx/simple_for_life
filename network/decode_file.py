#coding:utf-8
#!/usr/bin/env python

__author__ = 'SAF'

f = file(r"C:\Users\SAF\Documents\Tencent Files\506926059\FileRecv\ZA.c",'r')
x = f.readlines()
# print x
txt = x[8]
print txt.decode('utf-8',
                 #errors='ignore'
                 ).encode('gbk','replace')
# for i,each in enumerate(x):
#     each = each.decode('utf-8').encode('utf-8')
#     print i,each,