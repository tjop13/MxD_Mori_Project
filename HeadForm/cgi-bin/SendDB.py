#!/usr/bin/env python
# -*- coding: utf-8 -*-

import cgitb
import sqlite3

cgitb.enable()

print "Content-type: text/plane"
print

con = sqlite3.connect("board.db")

try:
    # DB作成
        cur = con.cursor()
        cur.executescript("""CREATE TABLE boardtbl(UNIQUEID integer primary key autoincrement, ID integer, LocationID varchar(5), Genre varchar(10), regdate timestamp,name varchar(100),comment varchar(1024),Replyname varchar(100),Replycomment varchar(1024),SolvedFlag varchar(1));""")
        cur.close()
except:
    print
finally:
    con.row_factory = sqlite3.Row
    cur = con.cursor()

    try:
        cur.execute("SELECT DISTINCT * FROM boardtbl ORDER BY regdate DESC")
        for each in cur.fetchall():
            print each['ID'],"$&",each['Genre'],"$&",each['LocationID'],"$&",each['name'].encode('utf-8'),"$&",each['regdate'].encode('utf-8'),"$&",each['comment'].encode('utf-8'),"$&",each['SolvedFlag'].encode('utf-8'),"$&",each['Replyname'].encode('utf-8'),"$&",each['Replycomment'].encode('utf-8'),"$& "
    finally:
        cur.close()
        con.close()
