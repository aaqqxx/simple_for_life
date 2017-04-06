# -*- coding: utf-8 -*-
#!/usr/env/bin python

__author__ = 'XingHua'



import subprocess,os


def process_rc(filename):
    print r'pyrcc4 -o images.py %s'%filename
    # pipe = subprocess.Popen(r'pyrcc4 -o images.py %s'%filename, stdout = subprocess.PIPE, stdin = subprocess.PIPE, stderr = subprocess.PIPE, creationflags=0x08)
    pipe = os.system(r'F:\Anaconda2\Library\bin\pyrcc4 -o %s.py %s'%(filename[:-4],filename))
    pass



def main():
    filename = "IL_data_analysis_mainwindow.qrc"
    process_rc(filename)
    pass



if __name__ == '__main__':
    main()

    pass



