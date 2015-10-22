#!/usr/bin/env python
# -*- coding: utf-8 -*-

import cgitb
import cgi
import os
import sqlite3
from datetime import datetime as dt
import pyboard

cgitb.enable()

print "Content-type: text/plane"
print

con = sqlite3.connect("board.db")

try:
    # DB作成
    cur = con.cursor()
    curm.executescript("""CREATE TABLE boardtbl(UNIQUEID integer primary key autoincrement, ID integer, LocationID varchar(5), Genre varchar(10), regdate timestamp,name varchar(100),comment varchar(1024),Replyname varchar(100),Replycomment varchar(1024),SolvedFlag varchar(1));""")
    cur.close()
except:
    print
finally:
    # 入力データがあれば、DB登録
    form = cgi.FieldStorage()
    if form["ID"].value == False:
        print "Flase"
    elif  form.has_key("ID") and form.has_key("genre") and form.has_key('LocationID') and form.has_key("name") and form.has_key("regdate") and form.has_key("comment") and form.has_key("SolvedFlag"):
        # nameが指定されていたらコメント登録
        ID = int(form["ID"].value)
        LocationID = form["LocationID"].value
        genre = form["genre"].value
        name = unicode(form.getfirst('name',''),'utf-8')
        regdate = form["regdate"].value
        time = dt.strptime(regdate, '%Y-%m-%d %H:%M:%S')
        comment = unicode(form.getfirst('comment',''),'utf-8')
        SolvedFlag = form["SolvedFlag"].value
        cur = con.cursor()
        try:
            cur.execute("SELECT * FROM boardtbl WHERE ID=:id AND LocationID=:locationid",{"id":ID, "locationid":LocationID})
            if cur.fetchone() != None:
                # cur.execute("UPDATE boardtbl SET SolvedFlag='1' WHERE SolvedFlag!=:solvedflag AND ID=:id",{"solvedflag":SolvedFlag, "id":ID})
                print "update"
            else:
                cur.execute("INSERT INTO boardtbl(ID,LocationID,Genre,regdate,name,comment,Replyname,Replycomment,SolvedFlag) values(?,?,?,?,?,?,'','',?)",(ID,LocationID,genre,time,name,comment,SolvedFlag))
                print "insert"
            con.commit()
        except:
            con.rollback()
        finally:
        	cur.close()


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
