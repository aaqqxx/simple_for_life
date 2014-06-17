__author__ = 'XingHua'

import os


def Foo():
    print os.listdir('.')
    open('a.txt', 'w').write('HelloWorld')


if __name__ == '__main__':
    Foo()