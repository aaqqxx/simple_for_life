# coding:utf-8
#!/usr/bin/env python

__author__ = 'XingHua'

"""

"""

import unittest


class Person:
    def age(self):
        return 34

    def name(self):
        return 'bob'


class TestSequenceFunctions(unittest.TestCase):
    def setUp(self):
        self.man = Person()
        print 'set up now'


    def test1(self):
        self.assertEqual(self.man.age(), 34)

    def test2(self):
        self.assertEqual(self.man.name(), 'bob')

    def test3(self):
        self.assertEqual(4 + 78, 82)


if __name__ == '__main__':
    unittest.main()