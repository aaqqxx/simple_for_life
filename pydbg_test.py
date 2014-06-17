# coding:utf-8
#!/usr/bin/env python

__author__ = 'XingHua'

"""

"""

from pydbg import *


dbg=pydbg()

heap_free_count = 0

def heap_free_handler(dbg):
    global printf_count
    heap_free_count += 1
    print "enter heap free handler ", heap_free_count

    return DBG_CONTINUE


def entry_point_handler(dbg):
    print "enter the entry point"

    #resolve the function address
    func_addr = dbg.func_resolve("KERNEL32.dll",  "HeapFree")

    #test the different between set restore=True to set restore=False
    if func_addr:
        dbg.bp_set(func_addr, restore=True, handler=heap_free_handler)
    else:
        print "resolve printf failed"

    return DBG_CONTINUE

def main():
    target = r"F:\MYPROJECTS\Ex15\Debug\Ex15.exe"

    pe = pefile.PE(target)
    dbg = pydbg()

    #if it's a console program, so set create_new_console = True
    dbg.load(target, create_new_console=True)

    #set a break point at the entry point
    entry_point = pe.OPTIONAL_HEADER.AddressOfEntryPoint + pe.OPTIONAL_HEADER.ImageBase
    dbg.bp_set(entry_point, handler=entry_point_handler)

    dbg.run()

if __name__=="__main__":
    main()