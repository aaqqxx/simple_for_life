__author__ = 'XingHua'

import fudge

from MySQLdb_fun import Foo

mysqldb = fudge.Fake('MySQLdb')
conn = mysqldb.expects('connect').returns_fake()
curs = conn.provides('cursor').returns_fake()
curs = curs.expects('execute').returns(1)
curs = curs.provides('fetchone').returns((1, 'Nathan'))

@fudge.with_fakes
@fudge.with_patched_object('MySQLdb_fun', 'MySQLdb', mysqldb)
def Test():
    Foo() # prints: 1 Nathan

if __name__ == '__main__':
    Test()