#!/usr/bin/env python
# -*- coding: utf-8 -*-

import cgi
import cgitb
import sqlite3

import sys
reload(sys)
sys.setdefaultencoding('utf-8')

cgitb.enable()

print "Content-type: text/html; charset=utf-8"
print "Pragma: no-cache"
print "Cache-Control: no-cache"
print
print '''
    <!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01 Transitional//EN">
    <html lang="ja">
    <head>
    <META HTTP-EQUIV="Content-type" CONTENT="text/html; charset=UTF-8">
    <META HTTP-EQUIV="Pragma" CONTENT="no-cache">
    <META HTTP-EQUIV="Cache-Control" CONTENT="no-cache">
    <title>Sample</title>
    <style>
        body{
          background-color: #FFDECA;
        }

        #Title{
            text-align: left;
        }

        #Message{
          text-align: left;
          margin-left: 20px;
        }

        #Date{
          text-align: right;
        }

        #BLACK{
          background-color: #666666;
        }
        #GOODS{
          background-color: #E9967A;
        }
        #RESCUE{
          background-color: #FF3333;
        }
        #REFUGE{
          background-color: #87CEFA
        }
        #METHANE{
          background-color: #90EE90
        }

    </style>
    　
    </head>
    <body>
    '''

message = '''
    <dt id="Title"><hr />ID:%(ID)s LocationID:%(LocationID)s Name:%(Regisstrant)s</dt><br>
    <dd id="Message"></dd><br>
    <dt id="Date">%(Genre)s,%(regdate)s</dt>
    %(Patient_Name)s,%(Patient_Age)s,%(Patient_Gender)s,%(Patient_Triage)s,%(Patient_Injuries_Diseases)s,%(Patient_Treatment)s,%(Patient_Hospital)s
    '''

con = sqlite3.connect("board.db")

try:
    # DB作成
    cur = con.cursor()
    cur.executescript("""CREATE TABLE Patienttbl(UNIQUEID integer primary key autoincrement, ID integer, LocationID varchar(5), regdate timestamp, Regisstrant varchar(100), Patient_Name varchar(100), Patient_Age varchar(10), Patient_Gender varchar(10), Patient_Triage varchar(10), Patient_Injuries_Diseases varchar(1024), Patient_Treatment varchar(1024), Patient_Hospital varchar(1024), comment varchar(1024), SolvedFlag varchar(1));""")
    cur.close()
except:
    print
finally:
    # 入力データがあれば、DB登録
    form = cgi.FieldStorage()
    print form.keys()

    if form.getfirst('send') and form.has_key('send'):
        # nameが指定されていたらコメント登録
        Regisstrant = unicode(form.getfirst('Registrant',''),'utf-8')
        Patient_Name = unicode(form.getfirst('Patient_name',''),'utf-8')
        Patient_Age = unicode(form.getfirst('Patient_age',''),'utf-8')
        Patient_Gender = unicode(form.getfirst('Patient_Gender',''),'utf-8')
        Patient_Triage = unicode(form.getfirst('Patient_triage',''),'utf-8')
        Patient_Injuries_Diseases = unicode(form.getfirst('Patient_injuries_diseases',''),'utf-8')
        Patient_Treatment = unicode(form.getfirst('Patient_Treatment',''),'utf-8')
        Patient_Hospital = unicode(form.getfirst('Patient_Hospital',''),'utf-8')
        comment = unicode(form.getfirst('comment',''),'utf-8')
        cur = con.cursor()
        try:
            cur.execute("SELECT count(*) FROM Patienttbl WHERE LocationID='1' ")
            IDnum = cur.fetchone()[0]
            cur.execute("SELECT * FROM Patienttbl WHERE ID=:id AND name=:Name AND comment=:Comment",{"id":IDnum,"Regisstrant":Regisstrant})
            if cur.fetchone() == None:
                IDnum += 1
                cur.execute("INSERT INTO Patienttbl(ID,LocationID,regdate,Regisstrant,Patient_Name,Patient_Age,Patient_Gender,Patient_Triage,Patient_Injuries_Diseases,Patient_Treatment,Patient_Treatment,Patient_Hospital,comment,SolvedFlag) values(?,'1',datetime('now','localtime'),?,?,?,?,?,?,?,?,?,'0')",(IDnum,Regisstrant,Patient_Name,Patient_Age,Patient_Gender,Patient_Triage,Patient_Injuries_Diseases,Patient_Treatment,Patient_Hospital,commet))
            con.commit()
        except:
            con.rollback()
        finally:
            cur.close()

    # 掲示板表示
    con.row_factory = sqlite3.Row
    cur = con.cursor()
    try:
        cur.execute("SELECT * FROM Patienttbl ORDER BY regdate DESC")
        print "<dl>"
        for each in cur.fetchall():
            COLOR = "<div id='BLACK'>" if each['SolvedFlag'] == '1' else "TAG"
            if COLOR == "TAG":
                if each['Genre'] == 'Rescue':
                    COLOR = "<div id='RESCUE'>"
                elif each['Genre'] == 'Goods':
                    COLOR = "<div id='GOODS'>"
                elif each['Genre'] == 'Refuge':
                    COLOR = "<div id='REFUGE'>"
                elif each['Genre'] == 'METHANE':
                    COLOR = "<div id='METHANE'>"
            print COLOR
            print message%{'ID':each['UNIQUEID'],'LocationID':each['LocationID'],'Regisstrant':each['Regisstrant'].encode('utf-8'),'regdate':each['regdate'].encode('utf-8'),'Patient_Name':each['Patient_Name'].encode('utf-8'),'Patient_Age':each['Patient_Age'].encode('utf-8'),'Patient_Gender':each['Patient_Gender'].encode('utf-8'),'Patient_Triage':each['Patient_Triage'].encode('utf-8'),'Patient_Injuries_Diseases':each['Patient_Injuries_Diseases'].encode('utf-8'),'Patient_Treatment':each['Patient_Treatment'].encode('utf-8'),'Patient_Hospital':each['Patient_Hospital'].encode('utf-8')}
            print "</div>"
            print "</dl>"
    finally:
        cur.close()
        con.close()
        print "</body></html>"
