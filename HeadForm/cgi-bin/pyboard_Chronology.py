#!/usr/bin/env python
# -*- coding: utf-8 -*-

import cgi
import cgitb
import sqlite3
import sqlitebck
import threading
import CheckDB

import sys
reload(sys)
sys.setdefaultencoding('utf-8')

cgitb.enable()

def PyBoard():
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
            <style type="text/css">
                body{
                  background-color: #E0FFFF;
                  width:600px;
                  margin:0 auto 0 auto;
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

                #resolution{
                  text-align: left;
                }
                #Chronology{
                  background-color: #55FF88;
                }
                #Reply{
                  background-color: #1E90FF;
                }
                #ReplyComment{
                  background-color: #00FF7F;
                }
                #Shelter_Bgcolor{
                  background-color: #FFCC66;
                }
                #Patient_Bgcolor{
                  background-color: #55FF88;
                }

                .main
                    {
                    float:left;
                    width:600px;
                    margin-left: 0px;
                    background-color: #D1F0FF;
                    height: 0px;
                    }
                .clears{
                  clear:both;
                  }

            </style>

            </head>
            <body>
            <h1>クロノロジー</h1>
            <div class="main">
        '''


def PyBoardData():
    Tag = ""
    Solve = ""

    message = '''
        <dt id="Title"><hr />ID: %(ID)s, %(regdate)s 場所ID: %(LocationID)s 記入者: %(Registrant)s タグ: %(Tag)s</dt><br>
        <dd id="Message">
        %(Message)s
        </dd><br>
        <dd id="Date">
        <form method="POST" action="./pyboard_Chronology.py">
        <input type="submit" name=%(ReplyButton)s value="Reply">
        </form>
        </dd>
        '''

    con = sqlite3.connect("board.db")

    try:
        # DB作成
        cur = con.cursor()
        cur.executescript("""CREATE TABLE Chronologytbl(UNIQUEID integer primary key autoincrement, ID integer, LocationID varchar(5), regdate timestamp, Registrant varchar(100), Message varchar(1024), Replyname varchar(100), Replycomment varchar(1024), Tag varchar(50), Send varchar(2));""")
        cur.close()
    except:
        print
    finally:
        # 入力データがあれば、DB登録
        form = cgi.FieldStorage()

        ReplyID = 0
        Key = form.keys()
        Option = ""
        Tag = ""

        if len(Key)!=0:
            if "Reply" in Key[0]:
                if "Fin" in Key[0]:
                    ReplyID = 0
                else:
                    ReplyID = int(Key[0].lstrip("Reply"))
            if "name" in Key:
                Option = " WHERE Registrant='" + unicode(form.getfirst('name',''),'utf-8') + "' "
                if "location" in Key:
                    Option += "AND LocationID=" + unicode(form.getfirst('location',''),'utf-8') + " "
            elif "location" in Key:
                Option = " WHERE LocationID=" + unicode(form.getfirst('location',''),'utf-8') + " "

        if form.has_key('TAGInfo_Shelter'):
            Tag = " Tag = '救護所情報' OR "
        if form.has_key('TAGEdit_Patient'):
            Tag = " Tag = '傷病者情報編集' OR "
        if Tag != "":
            Tag = Tag.rstrip("OR ")
            Tag = "( " + Tag + " ) "

            if Option != "":
                Option += " AND " + Tag
            else:
                Option = " WHERE" + Tag

        # 掲示板表示
        con.row_factory = sqlite3.Row
        cur = con.cursor()

#------------------------------Reply Form--------------------------
        try:
            if form.has_key('Replyname') and form.has_key('Replycomment'):
                ReplyName =  unicode(form.getfirst('Replyname',''),'utf-8')
                ReplyComment = unicode(form.getfirst('Replycomment',''),'utf-8')
                ThisKey = int(Key[0].lstrip("send"))
                cur.execute("UPDATE Chronologytbl SET Replyname=:name, Replycomment=:comment WHERE UNIQUEID=:uniqueid",{'name':ReplyName, 'comment':ReplyComment, 'uniqueid':ThisKey})
                con.commit()

            cur.execute("SELECT DISTINCT * FROM Chronologytbl %s ORDER BY regdate DESC" % Option)

            print "<dl>"
            for each in cur.fetchall():
                print "<div id='Shelter_Bgcolor'>" if each['Tag'] == '救護所情報' else "<div id='Patient_Bgcolor'>"

                # COLOR = "<div id='BLACK'>" if each['SolvedFlag'] == '1' else "TAG"
                # if COLOR == "TAG":
                #     COLOR = "<div id='RESCUE'>" if each['Genre'] == 'Rescue' else "<div id='GOODS'>"
                # COLOR = "<div id='Chronology'>"
                # print COLOR
                if each['UNIQUEID'] == ReplyID:
                    print message%{'ID':each['UNIQUEID'],'LocationID':each['LocationID'],'Registrant':each['Registrant'].encode('utf-8'),'regdate':each['regdate'].encode('utf-8'),'Message':each['Message'].encode('utf-8'),'Tag':each['Tag'].encode('utf-8'),'ReplyButton':"FinReply"+str(each['UNIQUEID'])}
                else:
                    print message%{'ID':each['UNIQUEID'],'LocationID':each['LocationID'],'Registrant':each['Registrant'].encode('utf-8'),'regdate':each['regdate'].encode('utf-8'),'Message':each['Message'].encode('utf-8'),'Tag':each['Tag'].encode('utf-8'),'ReplyButton':"Reply"+str(each['UNIQUEID'])}
                if each['Replyname'] != None:
                    print '''
                    <div id='ReplyComment'>
                    <dt id="Title"><hr />ReplyName:%(Replyname)s</dt><br>
                    <dd id="Message">%(Replycomment)s</dd><br>
                    </div>
                    ''' % {'Replyname':each['Replyname'],'Replycomment':each['Replycomment']}
                print "</div>"
                print "</dl>"
                if each['UNIQUEID'] == ReplyID:
                    print '''
                    <div id='Reply'>
                    <form method="POST" action="./pyboard_Chronology.py">
                        <table>
                        <tr>
                        <td><b>Name:</b></td>
                        <td><input type="text" name="Replyname" size="10" value=""></td>
                        </tr>
                        <tr>
                        <td><b>Message:</b></td>
                        <td><textarea cols="30" rows="5" name="Replycomment"></textarea></td>
                        </tr>
                        <tr>
                        <td colspan="2"><input type="submit" name="send%(ReplyID)s" value="Send"><input type="reset" value="Reset"></td>
                        </tr>
                        </table>
                    </form>
                    </div>
                    '''%{'ReplyID':ReplyID}
        finally:
            cur.close()
            con.close()
            print "</div>"


if __name__=='__main__':
    PyBoard()
    PyBoardData()
