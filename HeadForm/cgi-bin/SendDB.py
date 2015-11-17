#!/usr/bin/env python
# -*- coding: utf-8 -*-

import cgitb
import sqlite3

cgitb.enable()

print "Content-type: text/plain"
print

con = sqlite3.connect("board.db")

try:
	cur = con.cursor()
	cur.executescript("""CREATE TABLE LogData(UNIQUEID integer primary key autoincrement, regdate timestamp, Type varchar(10), class varchar(10), ID integer, LocationID varchar(5));""")
 	cur.close()
except:
    print
finally:
    con.row_factory = sqlite3.Row
    cur = con.cursor()

    try:
        cur.execute("SELECT DISTINCT * FROM Patienttbl WHERE Send='1' ORDER BY regdate DESC")
        for each in cur.fetchall():
            print each['ID'],'$&',each['LocationID'],'$&',each['Registrant'].encode('utf-8'),'$&',each['regdate'].encode('utf-8'),'$&',each['Patient_Name'].encode('utf-8'),'$&',each['Patient_Age'].encode('utf-8'),'$&',each['Patient_Gender'].encode('utf-8'),'$&',each['Patient_Triage'].encode('utf-8'),'$&',each['Patient_Injuries_Diseases'].encode('utf-8'),'$&',each['Patient_Treatment'].encode('utf-8'),'$&',each['Patient_Hospital'].encode('utf-8'),'$&',each['comment'].encode('utf-8'),'$&',each['SolvedFlag'].encode('utf-8'),"$& "
            cur.execute("UPDATE Patienttbl SET Send='0' WHERE ID=:id",{"id":each['ID']})
            cur.execute("INSERT INTO LogData(regdate,type,class,ID,LocationID) values(datetime('now','localtime'),'Send','Patient',%d,'1')"% IDnum)
            con.commit()
        print "$#&"

        cur.execute("SELECT DISTINCT * FROM Chronologytbl WHERE Send='1' ORDER BY regdate DESC")
        for each in cur.fetchall():
            print each['ID'],'$&',each['LocationID'],'$&',each['Registrant'].encode('utf-8'),'$&',each['regdate'].encode('utf-8'),'$&',each['Message'].encode('utf-8'),"$& "
            cur.execute("UPDATE Chronologytbl SET Send='0' WHERE ID=:id",{"id":each['ID']})
            cur.execute("INSERT INTO LogData(regdate,type,class,ID,LocationID) values(datetime('now','localtime'),'Send','Chronology',%d,'1')"% IDnum)
            con.commit()
        print "$#&"

        cur.execute("SELECT DISTINCT * FROM Instractiontbl WHERE Send='1' ORDER BY regdate DESC")
        for each in cur.fetchall():
            print each['ID'],'$&',each['LocationID'],'$&',each['Registrant'].encode('utf-8'),'$&',each['Target'].encode('utf-8'),'$&',each['regdate'].encode('utf-8'),'$&',each['Message'].encode('utf-8'),'$& '
            cur.execute("UPDATE Instractiontbl SET Send='0' WHERE ID=:id",{"id":each['ID']})
            cur.execute("INSERT INTO LogData(regdate,type,class,ID,LocationID) values(datetime('now','localtime'),'Send','Instraction',%d,'1')"% IDnum)
            con.commit()
        print "$#&"

        cur.execute("SELECT DISTINCT * FROM Victortbl WHERE Send='1' ORDER BY regdate DESC")
        for each in cur.fetchall():
            print each['ID'],'$&',each['LocationID'],'$&',each['Genre'].encode('utf-8'),'$&',each['regdate'].encode('utf-8'),'$&',each['name'].encode('utf-8'),'$&',each['comment'].encode('utf-8'),'$&',each['Replyname'].encode('utf-8'),'$&',each['Replycomment'].encode('utf-8'),'$& '
            cur.execute("UPDATE Victortbl SET Send='0' WHERE ID=:id",{"id":each['ID']})
            cur.execute("INSERT INTO LogData(regdate,type,class,ID,LocationID) values(datetime('now','localtime'),'Send','Victor',%d,'1')"% IDnum)
            con.commit()

    finally:
        cur.close()
        con.close()
