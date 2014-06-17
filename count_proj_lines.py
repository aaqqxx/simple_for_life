#coding:utf-8
#!/usr/bin/env python

__author__ = 'XingHua'

"""

"""

import os

totalfile = {}
# print os.getcwd()
for root, dirs, files in os.walk(os.getcwd(), True):
    flst = [os.path.join(root, f) for f in files if f.endswith(('.php', '.js', '.css', '.txt', '.py'))]

    print flst
    for fname in flst:
        ft = open(fname)
        totalfile[fname] = len([t for t in ft if len(t.strip())])
        ft.close()
        print "%s %d line code" % (fname, totalfile[fname])
        
print "line:%d,file:%d" % (sum(totalfile.values()), len(totalfile))

# os.system('pause')
