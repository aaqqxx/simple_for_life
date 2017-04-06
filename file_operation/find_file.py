#encoding:utf-8
__author__ = 'XingHua'

import glob
import fnmatch
import os

def find_file(file_name_pattern="f:/py/*.exe"):
    for filename in glob.glob(file_name_pattern):
        print filename




def iterfindfiles(path, fnexp):
    for root, dirs, files in os.walk(path):
        for filename in fnmatch.filter(files, fnexp):
            yield os.path.join(root, filename)

for filename in iterfindfiles(r"f:/py", "*.exe"):
    print filename