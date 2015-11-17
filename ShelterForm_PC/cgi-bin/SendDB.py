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
	cur.executescript("""CREATE TABLE LogData(UNIQUEID integer primary key autoincrement, regdate timestamp, Type varchar(10), class varchar(10), ID integer, LocationID varchar(5));""")
	cur.close()
# except:
#     print "LogData error"
finally:
	# cur = con.cursor()
	# cur.execute('select * from sqlite_master WHERE type="table"')
	#
	# for item in cur.fetchall():
	# 	if 'Patienttbl' not in item:
	# 		cur.executescript("""CREATE TABLE Patienttbl(UNIQUEID integer primary key autoincrement, ID integer, LocationID varchar(5), regdate timestamp, Registrant varchar(100), Patient_Name varchar(100), Patient_Age varchar(10), Patient_Gender varchar(10), Patient_Triage varchar(10), Patient_Injuries_Diseases varchar(1024), Patient_Treatment varchar(1024), Patient_Hospital varchar(1024), comment varchar(1024), SolvedFlag varchar(1), Send varchar(2));""")
	#
	# 	if 'Chronologytbl' not in item:
	# 		cur.executescript("""CREATE TABLE Chronologytbl(UNIQUEID integer primary key autoincrement, ID integer, LocationID varchar(5), regdate timestamp, Registrant varchar(100),  Message varchar(1024), Replyname varchar(100), Replycomment varchar(1024),Tag varchar(50), Send varchar(2);""")
	#
	# 	if 'Instractiontbl' not in item:
	# 		cur.executescript("""CREATE TABLE Instractiontbl(UNIQUEID integer primary key autoincrement, ID integer, LocationID varchar(5), regdate timestamp, Registrant varchar(100), Target varchar(100), Message varchar(1024),Replyname varchar(100),Replycomment varchar(1024), SolvedFlag varchar(1), Send varchar(2));""")
	#
	# 	if 'Victortbl' not in item:
	# 		cur.executescript("""CREATE TABLE Victortbl(UNIQUEID integer primary key autoincrement, ID integer, LocationID varchar(5), Genre varchar(10), regdate timestamp,name varchar(100),comment varchar(1024),Replyname varchar(100),Replycomment varchar(1024),SolvedFlag varchar(1), Send varchar(2));""")
	# cur.close()

	con.row_factory = sqlite3.Row
	cur = con.cursor()
	try:
		cur.execute("SELECT DISTINCT * FROM Patienttbl WHERE Send='1' ORDER BY regdate DESC")
		for each in cur.fetchall():
			IDnum = each['ID']
			print each['ID'],'$&',each['LocationID'],'$&',each['Registrant'].encode('utf-8'),'$&',each['regdate'].encode('utf-8'),'$&',each['Patient_Name'].encode('utf-8'),'$&',each['Patient_Age'].encode('utf-8'),'$&',each['Patient_Gender'].encode('utf-8'),'$&',each['Patient_Triage'].encode('utf-8'),'$&',each['Patient_Injuries_Diseases'].encode('utf-8'),'$&',each['Patient_Treatment'].encode('utf-8'),'$&',each['Patient_Hospital'].encode('utf-8'),'$&',each['comment'].encode('utf-8'),'$&',each['SolvedFlag'].encode('utf-8'),"$& "
			cur.execute("UPDATE Patienttbl SET Send='0' WHERE ID=:id",{"id":each['ID']})
			cur.execute("INSERT INTO LogData(regdate,type,class,ID,LocationID) values(datetime('now','localtime'),'Send','Patient',%d,'1')"% IDnum)
			con.commit()
		print "$#&"
	# except:
	# 	print "Patient Upadate error"
	finally:
	    cur.close()
	    con.close()

	# con.row_factory = sqlite3.Row
	cur = con.cursor()

	try:
	    cur.execute("SELECT DISTINCT * FROM Chronologytbl WHERE Send='1' ORDER BY regdate DESC")
	    for each in cur.fetchall():
	        IDnum = each['ID']
	        print each['ID'],'$&',each['LocationID'],'$&',each['Registrant'].encode('utf-8'),'$&',each['regdate'].encode('utf-8'),'$&',each['Message'].encode('utf-8'),'$&',each['Tag'].encode('utf-8'),"$& "
	        cur.execute("UPDATE Chronologytbl SET Send='0' WHERE ID=:id",{"id":each['ID']})
	        cur.execute("INSERT INTO LogData(regdate,type,class,ID,LocationID) values(datetime('now','localtime'),'Send','Chronology',%d,'1')"% IDnum)
	        con.commit()
	    print "$#&"
	# except:
	# 	print "Chronology Upadate error"
	finally:
	    cur.close()
	    con.close()

	# con.row_factory = sqlite3.Row
	cur = con.cursor()

	try:
	    cur.execute("SELECT DISTINCT * FROM Instractiontbl WHERE Send='1' ORDER BY regdate DESC")
	    for each in cur.fetchall():
	        IDnum = each['ID']
	        print each['ID'],'$&',each['LocationID'],'$&',each['Registrant'].encode('utf-8'),'$&',each['Target'].encode('utf-8'),'$&',each['regdate'].encode('utf-8'),'$&',each['Message'].encode('utf-8'),"$&",each['SolvedFlag'].encode('utf-8'),"$&",each['Replyname'].encode('utf-8'),"$&",each['Replycomment'].encode('utf-8'),'$& '
	        cur.execute("UPDATE Instractiontbl SET Send='0' WHERE ID=:id",{"id":each['ID']})
	        cur.execute("INSERT INTO LogData(regdate,type,class,ID,LocationID) values(datetime('now','localtime'),'Send','Instraction',%d,'1')"% IDnum)
	        con.commit()
	    print "$#&"
	# except:
	# 	print "Instraction Upadate error"
	finally:
	    cur.close()
	    con.close()


	# con.row_factory = sqlite3.Row
	cur = con.cursor()

	try:
	    cur.execute("SELECT DISTINCT * FROM Victortbl WHERE Send='1' ORDER BY regdate DESC")
	    for each in cur.fetchall():
	        IDnum = each['ID']
	        print each['ID'],"$&",each['Genre'],"$&",each['LocationID'],"$&",each['name'].encode('utf-8'),"$&",each['regdate'].encode('utf-8'),"$&",each['comment'].encode('utf-8'),"$&",each['SolvedFlag'].encode('utf-8'),"$&",each['Replyname'].encode('utf-8'),"$&",each['Replycomment'].encode('utf-8'),"$& "
	        cur.execute("UPDATE Victortbl SET Send='0' WHERE ID=:id",{"id":each['ID']})
	        cur.execute("INSERT INTO LogData(regdate,type,class,ID,LocationID) values(datetime('now','localtime'),'Send','Vitor',%d,'1')"% IDnum)
	        con.commit()
	# except:
	# 	print "Victor Upadate error"
	finally:
	    cur.close()
	    con.close()
