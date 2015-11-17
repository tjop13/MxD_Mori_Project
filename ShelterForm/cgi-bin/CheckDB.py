import cgi
import cgitb
import sqlite3

import sys
reload(sys)
sys.setdefaultencoding('utf-8')

cgitb.enable()

try:
    # DB作成
	cur = con.cursor()
	cur.executescript("""CREATE TABLE LogData(UNIQUEID integer primary key autoincrement, regdate timestamp, Type varchar(10), class varchar(10), ID integer, LocationID varchar(5));""")
	cur.close()
except:
    print "LogData error"
finally:
    con.row_factory = sqlite3.Row
    cur = con.cursor()

    try:
        cur.execute("SELECT * FROM LogData")
        for each in cur.fetchall():
            print each['UNIQUEID'],each['regdate'],each['Type'],each['class'],each['ID'],each['LocationID']
