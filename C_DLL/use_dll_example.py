# coding:utf-8
#!/usr/bin/env python

__author__ = 'XingHua'

"""
首先在Python中继承Structure构造一个和C DLL中一致的数据结构StructTest，
然后设置函数GetStructInfo的参数类型和返回值类型，
最后创建一个StructTest对象，并将其转化为指针作为参数，
调用函数GetStrcutInfo，
最后通过输出数据结构的值来检查是否调用成功
"""

from ctypes import *

ARRAY_NUMBER = 20
STR_LEN = 20
# define type
INTARRAY20 = c_int * ARRAY_NUMBER
CHARARRAY20 = c_char * STR_LEN
# define struct
class StructTest(Structure):
    _fields_ = [
        ("number", c_int),
        ("pChar", c_char_p),
        ("str", CHARARRAY20),
        ("iArray", INTARRAY20)
    ]

#load dll and get the function object
dll = cdll.LoadLibrary('hello.dll')
GetStructInfo = dll.GetStructInfo
#set the return type
GetStructInfo.restype = c_char_p
#set the argtypes
GetStructInfo.argtypes = [POINTER(StructTest)]

objectStruct = StructTest()
#invoke api GetStructInfo
retStr = GetStructInfo(byref(objectStruct))

#check result
print "number: ", objectStruct.number
print "pChar: ", objectStruct.pChar
print "str: ", objectStruct.str
for i, val in enumerate(objectStruct.iArray):
    print 'Array[i]: ', val
print retStr

dll1 = cdll.LoadLibrary('pointer_test.dll')
GetPointerInfo = dll1.GetPointerInfo
GetPointerInfo.restype = c_char_p
GetPointerInfo.argtypes =[POINTER()]
