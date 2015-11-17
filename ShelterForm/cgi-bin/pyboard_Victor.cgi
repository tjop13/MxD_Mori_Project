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
          background-color: #90EE90;
        }
        #RESCUE{
          background-color: #FF3333;
        }
        #REFUGE{
          background-color: #87CEFA;
        }
        #ReplyComment{
          margin-left: 50px;
          width: 95%;
          background-color: #DDDDDD;
        }

    </style>
    　
    </head>
    <body>
    '''

message = '''
    <dt id="Title"><hr />ID:%(ID)s LocationID:%(LocationID)s Name:%(name)s</dt><br>
    <dd id="Message">%(comment)s</dd><br>
    <dt id="Date">%(Genre)s,%(regdate)s</dt>
    '''

con = sqlite3.connect("board.db")

try:
    # DB作成
    cur = con.cursor()
    cur.executescript("""CREATE TABLE Victortbl(UNIQUEID integer primary key autoincrement, ID integer, LocationID varchar(5), Genre varchar(10), regdate timestamp,name varchar(100),comment varchar(1024),Replyname varchar(100),Replycomment varchar(1024),SolvedFlag varchar(1), Send varchar(2));""")
    cur.close()
except:
    print
finally:
    # 入力データがあれば、DB登録
    form = cgi.FieldStorage()
    if form.getfirst('send') and form.has_key('send'):
        # nameが指定されていたらコメント登録
        name = unicode(form.getfirst('name',''),'utf-8')
        comment = unicode(form.getfirst('comment',''),'utf-8')
        genre = form.getfirst('Genre','')
        cur = con.cursor()
        try:
            cur.execute("SELECT count(*) FROM Victortbl WHERE LocationID='1' ")
            IDnum = cur.fetchone()[0]
            cur.execute("SELECT * FROM Victortbl WHERE ID=:id AND name=:Name AND comment=:Comment",{"id":IDnum,"Name":name,"Comment":comment})
            if cur.fetchone() == None:
                IDnum += 1
                cur.execute("INSERT INTO Victortbl(ID,LocationID,Genre,regdate,name,comment,Replyname,Replycomment,SolvedFlag,Send) values(?,'1',?,datetime('now','localtime'),?,?,'','','0','1')",(IDnum,cgi.escape(genre),name,comment))
            con.commit()
        except:
            con.rollback()
        finally:
            cur.close()

    # 掲示板表示
    con.row_factory = sqlite3.Row
    cur = con.cursor()
    try:
        cur.execute("SELECT * FROM Victortbl ORDER BY regdate DESC")
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
            print COLOR
            print message%{'ID':each['UNIQUEID'],'Genre':each['Genre'],'LocationID':each['LocationID'],'name':each['name'].encode('utf-8'),'regdate':each['regdate'].encode('utf-8'),'comment':each['comment'].encode('utf-8'),'SolvedFlag':each['SolvedFlag']}
            print "</div>"
            print "</dl>"
            if each['Replyname'] != '':
                print '''
                <div id='ReplyComment'>
                <dt id="Title"><hr />ReplyName:%(Replyname)s</dt><br>
                <dd id="Message">%(Replycomment)s</dd><br>
                </div>
                ''' % {'Replyname':each['Replyname'],'Replycomment':each['Replycomment']}

    finally:
        cur.close()
        con.close()
        print "</body></html>"
