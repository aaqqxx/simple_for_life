__author__ = 'XingHua'

import urllib2


def Foo():
     print urllib2.urlopen('http://www.google.com/').read()
if __name__ == '__main__':
    Foo()