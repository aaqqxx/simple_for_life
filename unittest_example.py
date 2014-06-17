__author__ = 'XingHua'

import unittest


class MyTestCase(unittest.TestCase):
    def test1(self):
        """Run test 1"""
        print "test1"
        pass
    def test2(self):
        """Run test 2"""
        pass
if __name__ == '__main__':
    unittest.main()