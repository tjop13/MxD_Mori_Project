#!/usr/bin/env python
# -*- coding: utf-8 -*-

import cgitb
import sqlite3

cgitb.enable()

print "Content-type: text/plain"
print

con = sqlite3.connect("board.db")

try:
    # DB作成
    cur = con.cursor()
    cur.executescript("""CREATE TABLE Patienttbl(UNIQUEID integer primary key autoincrement, ID integer, LocationID varchar(5), regdate timestamp,  Registrant varchar(100), Patient_Name varchar(100), Patient_Age varchar(10), Patient_Gender varchar(10), Patient_Triage varchar(10), Patient_Injuries_Diseases varchar(1024), Patient_Treatment varchar(1024), Patient_Hospital varchar(1024), comment varchar(1024), SolvedFlag varchar(1));""")
    cur.executescript("""CREATE TABLE Chronologytbl(UNIQUEID integer primary key autoincrement, ID integer, LocationID varchar(5), regdate timestamp,  Registrant varchar(100),  Message varchar(1024));""")
    cur.executescript("""CREATE TABLE Instractiontbl(UNIQUEID integer primary key autoincrement, ID integer, LocationID varchar(5), regdate timestamp, name varchar(100),comment varchar(1024),Replyname varchar(100),Replycomment varchar(1024),SolvedFlag varchar(1));""")
    cur.close()
except:
    print
finally:
    con.row_factory = sqlite3.Row
    cur = con.cursor()

    try:
        cur.execute("SELECT DISTINCT * FROM Patienttbl ORDER BY regdate DESC")
        for each in cur.fetchall():
            print each['UNIQUEID'],'$&',each['LocationID'],'$&',each['Registrant'].encode('utf-8'),'$&',each['regdate'].encode('utf-8'),'$&',each['Patient_Name'].encode('utf-8'),'$&',each['Patient_Age'].encode('utf-8'),'$&',each['Patient_Gender'].encode('utf-8'),'$&',each['Patient_Triage'].encode('utf-8'),'$&',each['Patient_Injuries_Diseases'].encode('utf-8'),'$&',each['Patient_Treatment'].encode('utf-8'),'$&',each['Patient_Hospital'].encode('utf-8'),'$&',each['comment'].encode('utf-8'),'$&',each['SolvedFlag'].encode('utf-8'),"$& "
        print "$#&"

        cur.execute("SELECT DISTINCT * FROM Chronologytbl ORDER BY regdate DESC")
        for each in cur.fetchall():
            print each['UNIQUEID'],'$&',each['LocationID'],'$&',each['Registrant'].encode('utf-8'),'$&',each['regdate'].encode('utf-8'),'$&',each['Message'].encode('utf-8'),"$& "
        print "$#&"

        cur.execute("SELECT DISTINCT * FROM Instractiontbl ORDER BY regdate DESC")
        for each in cur.fetchall():
            print each['UNIQUEID'],'$&',each['LocationID'],'$&',each['Registrant'].encode('utf-8'),'$&',each['Target'].encode('utf-8'),'$&',each['regdate'].encode('utf-8'),'$&',each['Message'].encode('utf-8'),'$& '

    finally:
        cur.close()
        con.close()
