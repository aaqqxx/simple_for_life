__author__ = 'XingHua'

import MySQLdb


def Foo():
    conn = MySQLdb.connect(host='localhost',
                           user='root', passwd='abc123', db='test')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM people')
    id, name = cursor.fetchone()
    print id, name


if __name__ == '__main__':
    Foo()