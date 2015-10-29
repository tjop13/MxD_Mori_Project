#!/usr/bin/env python
# -*- coding: utf-8 -*-

import cgitb
import cgi
import os
import sqlite3
from datetime import datetime as dt

cgitb.enable()

print "Content-type: text/plain"
print

con = sqlite3.connect("board.db")

try:
    # DB作成
    cur = con.cursor()
    cur.executescript("""CREATE TABLE Patienttbl(UNIQUEID integer primary key autoincrement, ID integer, LocationID varchar(5), regdate timestamp, Registrant varchar(100), Patient_Name varchar(100), Patient_Age varchar(10), Patient_Gender varchar(10), Patient_Triage varchar(10), Patient_Injuries_Diseases varchar(1024), Patient_Treatment varchar(1024), Patient_Hospital varchar(1024), comment varchar(1024), SolvedFlag varchar(1));""")
    cur.executescript("""CREATE TABLE Chronologytbl(UNIQUEID integer primary key autoincrement, ID integer, LocationID varchar(5), regdate timestamp, Registrant varchar(100), Message varchar(1024));""")
    cur.executescript("""CREATE TABLE Instractiontbl(UNIQUEID integer primary key autoincrement, ID integer, LocationID varchar(5), regdate timestamp, Registrant varchar(100), Target varchar(100), Message varchar(1024));""")
    cur.close()
except:
    print
finally:
    # 入力データがあれば、DB登録
    form = cgi.FieldStorage()
    print form.keys()

    if  form.has_key("ID") and form.has_key('LocationID') and form.has_key("Class"):
        ID = int(form["ID"].value)
        LocationID = form["LocationID"].value
        Class = form["Class"].value
        regdate = form["regdate"].value
        # time = dt.strptime(regdate, '%Y-%m-%d %H:%M:%S')
        cur = con.cursor()

        if form["Class"].value == 'Patient':
            Registrant = form['Registrant'].value
            Patient_Name = form['Patient_Name'].value
            Patient_Age = form['Patient_Age'].value
            Patient_Gender = form['Patient_Gender'].value
            Patient_Triage = form['Patient_Triage'].value
            Patient_Injuries_Diseases = form['Patient_Injuries_Diseases'].value
            Patient_Treatment = form['Patient_Treatment'].value
            Patient_Hospital = form['Patient_Hospital'].value
            SolvedFlag = form['SolvedFlag'].value
            comment = form['comment'].value

            try:
                cur.execute("SELECT * FROM Patienttbl WHERE ID=:id AND LocationID=:locationid",{"id":ID, "locationid":LocationID})
                if cur.fetchone() != None:
                    cur.execute("UPDATE Patienttbl SET SolvedFlag='1' WHERE SolvedFlag!=:solvedflag AND ID=:id",{"solvedflag":SolvedFlag, "id":ID})
                    print "update"
                else:
                    cur.execute("INSERT INTO Patienttbl(ID,LocationID,regdate,Registrant,Patient_Name,Patient_Age,Patient_Gender,Patient_Triage,Patient_Injuries_Diseases,Patient_Treatment,Patient_Hospital,comment,SolvedFlag) values(?,?,?,?,?,?,?,?,?,?,?,?,?)",(ID,LocationID,regdate,Registrant.decode('utf-8'),Patient_Name.decode('utf-8'),Patient_Age.decode('utf-8'),Patient_Gender.decode('utf-8'),Patient_Triage.decode('utf-8'),Patient_Injuries_Diseases.decode('utf-8'),Patient_Treatment.decode('utf-8'),Patient_Hospital.decode('utf-8'),comment.decode('utf-8'),SolvedFlag))
                    print "insert"
                con.commit()
            except:
                con.rollback()
            finally:
            	cur.close()

        elif form["Class"].value == 'Chronology':
            print "Chronology"
            Registrant = form['Registrant'].value
            Message = form['Message'].value
            try:
                cur.execute("SELECT * FROM Chronologytbl WHERE ID=:id AND LocationID=:locationid",{"id":ID, "locationid":LocationID})
                if cur.fetchone() != None:
                    cur.execute("UPDATE Chronologytbl SET SolvedFlag='1' WHERE SolvedFlag!=:solvedflag AND ID=:id",{"solvedflag":SolvedFlag, "id":ID})
                    print "update"
                else:
                    cur.execute("INSERT INTO Chronologytbl(ID,LocationID,regdate,Registrant,Message) values(?,?,?,?,?)",(ID,LocationID,regdate,Registrant.decode('utf-8'),Message.decode('utf-8')))
                    print "insert"
                con.commit()
            except:
                con.rollback()
            finally:
            	cur.close()

        elif form["Class"].value == 'Instraction':
            print "Instraction"
            Registrant = form['Registrant'].value
            Target = form['Target'].value
            Message = form['Message'].value
            # print ID,LocationID,regdate,Registrant,Target,Message
            try:
                cur.execute("SELECT * FROM Instractiontbl WHERE ID=:id AND LocationID=:locationid",{"id":ID, "locationid":LocationID})
                if cur.fetchone() != None:
                    cur.execute("UPDATE Instractiontbl SET SolvedFlag='1' WHERE SolvedFlag!=:solvedflag AND ID=:id",{"solvedflag":SolvedFlag, "id":ID})
                    print "update"
                else:
                    cur.execute("INSERT INTO Instractiontbl(ID,LocationID,regdate,Registrant,Target,Message) values(?,?,?,?,?,?)",(ID,LocationID,regdate,Registrant.decode('utf-8'),Target.decode('utf-8'),Message.decode('utf-8')))
                    # cur.execute("INSERT INTO Instractiontbl(ID,LocationID,regdate,Registrant,Target,Message) values(?,?,?,?,?,?)",(ID,LocationID,regdate,Registrant.decode('utf-8'),Target.decode('utf-8'),Message.decode('utf-8')))
                    print "insert"
                con.commit()
            except:
                con.rollback()
            finally:
            	cur.close()
                
        else:
            print "error"
# if os.environ['REQUEST_METHOD'] == "POST":
#     form = cgi.FieldStorage()
#     if form.has_key("LocationID"):
#     	print form["LocationID"].value
#     if form.has_key("name"):
#     	print form["name"].value
#     if form.has_key("title"):
#     	print form["title"].value
#     if form.has_key("regdate"):
#     	print form["regdate"].value
#     if form.has_key("comment"):
#     	print form["comment"].value

print "OK"
