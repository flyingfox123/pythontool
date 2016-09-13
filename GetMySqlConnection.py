# encoding:utf-8

import MySQLdb

def getMySqlConn(host,user,passwd,db):
    try:
        conn = MySQLdb.connect(
            host=host,
            port=3306,
            user=user,
            passwd=passwd,
            db=db,
            charset='utf8'
        )
        return conn
    except Exception, e:
        print "some exception dosomething"
        print e


if __name__ == "__main__":
    conn = getMySqlConn("10.186.116.213","root","root","manyidb")
    print conn