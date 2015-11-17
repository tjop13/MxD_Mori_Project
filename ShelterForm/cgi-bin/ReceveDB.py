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
	cur.executescript("""CREATE TABLE LogData(UNIQUEID integer primary key autoincrement, regdate timestamp, Type varchar(10), class varchar(10), ID integer, LocationID varchar(5));""")
	cur.close()
except:
    print "LogData error"
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

        cur.execute("INSERT INTO LogData(regdate,Type,class,ID,LocationID) values(datetime('now','localtime'),'Receve',?,?,?)",(form["Class"].value,ID,LocationID))

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
                    cur.execute("UPDATE Patienttbl SET SolvedFlag='1',Send='0' WHERE SolvedFlag!=:solvedflag AND ID=:id",{"solvedflag":SolvedFlag, "id":ID})
                    print "update"
                else:
                    cur.execute("INSERT INTO Patienttbl(ID,LocationID,regdate,Registrant,Patient_Name,Patient_Age,Patient_Gender,Patient_Triage,Patient_Injuries_Diseases,Patient_Treatment,Patient_Hospital,comment,SolvedFlag,Send) values(?,?,?,?,?,?,?,?,?,?,?,?,?,0)",(ID,LocationID,regdate,Registrant.decode('utf-8'),Patient_Name.decode('utf-8'),Patient_Age.decode('utf-8'),Patient_Gender.decode('utf-8'),Patient_Triage.decode('utf-8'),Patient_Injuries_Diseases.decode('utf-8'),Patient_Treatment.decode('utf-8'),Patient_Hospital.decode('utf-8'),comment.decode('utf-8'),SolvedFlag))
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
            Tag = form['Tag'].value
            try:
                cur.execute("SELECT * FROM Chronologytbl WHERE ID=:id AND LocationID=:locationid",{"id":ID, "locationid":LocationID})
                if cur.fetchone() != None:
                    cur.execute("UPDATE Chronologytbl SET SolvedFlag='1' WHERE SolvedFlag!=:solvedflag,Send='0' AND ID=:id",{"solvedflag":SolvedFlag, "id":ID})
                    print "update"
                else:
                    cur.execute("INSERT INTO Chronologytbl(ID,LocationID,regdate,Registrant,Message,Tag,Send) values(?,?,?,?,?,?,'0')",(ID,LocationID,regdate,Registrant.decode('utf-8'),Message.decode('utf-8'),Tag.decode('utf-8')))
                    print "insert"
                con.commit()
            except:
                con.rollback()
            finally:
            	cur.close()

        elif form["Class"].value == 'Instraction':
            print "Instraction"
            ReplyName = ''
            ReplyComment = ''

            Registrant = form['Registrant'].value
            Target = form['Target'].value
            Message = form['Message'].value
            SolvedFlag = form["SolvedFlag"].value
            if form.has_key('Replyname'):
                ReplyName = form['Replyname'].value
            if form.has_key('Replycomment'):
                ReplyComment = form['Replycomment'].value

            # print ID,LocationID,regdate,Registrant,Target,Message
            try:
                cur.execute("SELECT * FROM Instractiontbl WHERE ID=:id AND LocationID=:locationid",{"id":ID, "locationid":LocationID})
                if cur.fetchone() != None:
                    cur.execute("UPDATE Instractiontbl SET SolvedFlag='1',Send='0' WHERE SolvedFlag!=:solvedflag AND ID=:id",{"solvedflag":SolvedFlag, "id":ID})
                    print "update"
                else:
                    cur.execute("INSERT INTO Instractiontbl(ID,LocationID,regdate,Registrant,Target,Message,SolvedFlag,Replyname,Replycomment,Send) values(?,?,?,?,?,?,?,?,?,'0')",(ID,LocationID,regdate,Registrant.decode('utf-8'),Target.decode('utf-8'),Message.decode('utf-8'),SolvedFlag,ReplyName.decode('utf-8'),ReplyComment.decode('utf-8')))
                    # cur.execute("INSERT INTO Instractiontbl(ID,LocationID,regdate,Registrant,Target,Message) values(?,?,?,?,?,?)",(ID,LocationID,regdate,Registrant.decode('utf-8'),Target.decode('utf-8'),Message.decode('utf-8')))
                    print "insert"
                con.commit()
            except:
                con.rollback()
            finally:
            	cur.close()

        elif form["Class"].value == 'Victor':
            genre = form["genre"].value
            name = unicode(form.getfirst('name',''),'utf-8')
            comment = unicode(form.getfirst('comment',''),'utf-8')
            Replyname = unicode(form.getfirst('Replyname',''),'utf-8')
            Replycomment = unicode(form.getfirst('Replycomment',''),'utf-8')
            SolvedFlag = form["SolvedFlag"].value
            cur = con.cursor()
            try:
                cur.execute("SELECT * FROM Victortbl WHERE ID=:id AND LocationID=:locationid",{"id":ID, "locationid":LocationID})
                if cur.fetchone() != None:
                    cur.execute("UPDATE Victortbl SET SolvedFlag='1' WHERE SolvedFlag!=:solvedflag, Send='0' AND ID=:id AND LocationID=:LoactionID",{"solvedflag":SolvedFlag, "id":ID, "LocationID":LocationID})
                    cur.execute("UPDATE Victortbl SET Replyname=:Replyname, Replycomment=:Replycomment, Send='0' WHERE ID=:ID AND LocationID=:LoactionID",{"Replyname":Replyname, "Replycomment":Replycomment, "ID":ID, "LocationID":LocationID})
                    print "update"
                else:
                    cur.execute("INSERT INTO Victortbl(ID,LocationID,Genre,regdate,name,comment,Replyname,Replycomment,SolvedFlag,Send) values(?,?,?,?,?,?,?,?,?,'0')",(ID,LocationID,genre,regdate,name,comment,Replyname,Replycomment,SolvedFlag))
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
