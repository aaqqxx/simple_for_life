#coding:utf-8
#!/usr/env/bin python

__author__ = 'XingHua'

from PIL import ImageGrab

def main():
    im = ImageGrab.grab()
    im.save("zz.jpeg",'jpeg')

if __name__=="__main__":
    main()