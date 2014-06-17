#coding=utf-8
#!/usr/bin/env python

__author__ = 'XingHua'

import fudge

mock = fudge.Fake('mock')

mock.expects('method')\
    .with_arg_count(arg1=1, arg2='2').returns(True)

mock.method(arg1=1, arg2='2')

fudge.verify()

