#coding:utf-8
#!/usr/bin/env python

__author__ = 'XingHua'

"""

"""


import os
import sys

reload(sys)
sys.setdefaultencoding('utf8')

def DelBlankLineInFile(infile, isOverwrite):
    '''delete blank lines of single file

    infile is source file'''
    isOverwrite = isOverwrite.upper()

    dir = os.path.dirname(infile)
    oldbasename = os.path.basename(infile)
    newbasename = oldbasename + '-new'
    extname = os.path.splitext(infile)[1]
    outfile = dir+'\\' + newbasename + extname

    infp = open(infile, "r")
    outfp = open(outfile, "w")
    lines = infp.readlines()
    for line in lines:
        #print type(line)
        if line.split():
            outfp.writelines(line)
    infp.close()
    outfp.close()

    if isOverwrite == 'Y':
        #print 'remove',infile
        os.remove(infile)
        os.rename(outfile, infile)
        outfile = infile

    #print 'read %s'%infile, 'and save as %s'%outfile
    print 'read %s and save as %s'%(infile, outfile)

def DelBlankLineInFolders():
    """delete blank lines of all files in target path

    XXXXXXXXXXXXXXXXX"""
    str = u'请输入目标文件夹路径====>'
    inpath = raw_input(str.encode('gbk'))
    str = u'您输入是：' + inpath
    print str

    str = u'是否覆盖源文件(Y/N)'
    isOverwrite = raw_input(str.encode('gbk'))
    isOverwrite = isOverwrite.upper()
    str = u'您的选择是：' + isOverwrite
    print str

    for (path,dirs,files) in os.walk(inpath):
        for file in files:
            infile = os.path.join(path, file)
            #print infile
            DelBlankLineInFile(infile, isOverwrite)

    if isOverwrite == 'Y':
        str = u'是否执行文件合并操作(Y/N)'
        isMerged = raw_input(str.encode('gbk'))
        isMerged = isMerged.upper()
        str = u'您选择的是：' + isMerged
        print str

        if isMerged == 'Y':
            mergedfile = os.path.join(inpath, 'MergedFile.txt')
            infiles = []
            for (path,dirs,files) in os.walk(path):
                for file in files:
                    infiles.append(os.path.join(path, file))

            MergeFiles(infiles, mergedfile)

def MergeFiles(infiles, outfile):
    """Merge infiles to one outfile

    infiles indicate input file list
    outfile is merged file"""
    outfp = open(outfile, 'a')

    for file in infiles:
        filename = os.path.split(file)[1]
        #print filename
        #print file
        outfp.write('***' + filename + '***\n')

        infp = open(file, 'r')
        for line in infp.readlines():
            outfp.write(line)
        infp.close()
        outfp.write('\n')

    outfp.close()

    print '***Merge file list***'
    no = 0
    for file in infiles:
        no += 1
        print 'No.%d'%no, file
    print 'Merged File:%s'%outfile
    print '*********************'




if __name__ == "__main__":
    str = u'1   删除指定目录下所有文件中的空行(包括子目录)'
    print str
    str = u'2   删除指定文件中的所有空行'
    print str
    str = u'请输入数字编号====>'
    index = int(raw_input(str.encode('gbk')))

    if index == 1:
        DelBlankLineInFolders()
    elif index ==2:
        str = u'请输入目标文件路径====>'
        infile = raw_input(str.encode('gbk'))
        str = u'您输入是：' + infile
        print str

        str = u'是否覆盖源文件(Y/N)'
        isOverwrite = raw_input(str.encode('gbk'))
        str = u'您的选择是：' + isOverwrite.upper()
        print str

        DelBlankLineInFile(infile, isOverwrite)
    else:
        str = u'编号输入错误,程序退出'
        print str
        sys.exit()

    raw_input("press Enter to exit")
    sys.exit()