__author__ = 'XingHua'

import fudge
from cStringIO import StringIO
from network import Foo

urlopen = fudge.Fake('urlopen', callable=True) \
    .returns(StringIO('HelloWorld'))


@fudge.with_fakes
@fudge.with_patched_object('urllib2', 'urlopen', urlopen)
def Test():
    Foo()  # prints: HelloWorld


if __name__ == '__main__':
    Test()