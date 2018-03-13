#coding = utf-8
#!/usr/bin/env python
import os
import time
def create_file_size(size):
    size *= 1024 * 1024*1024
    print size
    local_time = time.strftime("%Y%m%d%H%M%S", time.localtime())
    file_name = "g:\\tmp\\"+str(local_time) + ".txt"
    with open(file_name, 'w') as f:
        note = 'Test File Contents: '
        i = 0
        fsize = 0
        while True:
            i += 1
            text = note + str(i) + "\n"
            f.write(text)
            fsize += len(text)
            if fsize >= size:
                break
    print "ALL down!"
if __name__ == '__main__':
    size = input("input file's size(G):")
    create_file_size(size)