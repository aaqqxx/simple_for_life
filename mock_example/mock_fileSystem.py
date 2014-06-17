__author__ = 'XingHua'

import fudge
from cStringIO import StringIO
from fileSystem import Foo

listdir = fudge.Fake(callable=True).returns(['a.txt', 'b.jpg'])
buf = StringIO()
myopen = lambda filename, mode: buf


@fudge.with_fakes
@fudge.with_patched_object('os', 'listdir', listdir)
@fudge.with_patched_object('__builtin__', 'open', myopen)
def Test():
    Foo()  # prints: ['a.txt', 'b.jpg']
    print buf.getvalue()  # prints: HelloWorld


if __name__ == '__main__':
    Test()