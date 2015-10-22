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
                #BLACK{
                  background-color: #666666;
                }
                #GOODS{
                  background-color: #E9967A;
                }
                #RESCUE{
                  background-color: #FF3333;
                }
                #Reply{
                  background-color: #1E90FF;
                }
                #ReplyComment{
                  background-color: #00FF7F;
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
            <h1>避難所情報</h1>
            <div class="main">
        '''


def PyBoardData():
    Tag = ""
    Solve = ""

    message = '''

        <dt id="Title"><hr />ID:%(ID)s LocationID:%(LocationID)s Name:%(name)s</dt><br>
        <dd id="Message">%(comment)s</dd><br>
        <dt id="Date">%(Genre)s,%(regdate)s</dt>
        <form method="POST" action="./pyboard_emis.py">
        <input type="submit" name=%(ResolButton)s value="Resolution">
        <input type="submit" name=%(ReplyButton)s value="Reply">
        </form>
        '''

    con = sqlite3.connect("board.db")

    try:
        # DB作成
        cur = con.cursor()
        cur.executescript("""CREATE TABLE boardtbl(UNIQUEID integer primary key autoincrement, ID integer, LocationID varchar(5), Genre varchar(10), regdate timestamp,name varchar(100),comment varchar(1024),Replyname varchar(100),Replycomment varchar(1024),SolvedFlag varchar(1));""")
        cur.close()
    except:
        print
    finally:
        # 入力データがあれば、DB登録
        form = cgi.FieldStorage()

        ReplyID = 0
        Key = form.keys()

        if len(Key)!=0:
            if "Resolution" in Key[0]:
                ThisKey = int(Key[0].lstrip("Resolution"))
                cur = con.cursor()
                try:
                    cur.execute("UPDATE boardtbl SET SolvedFlag='1' WHERE UNIQUEID=:uniqueid",{"uniqueid":ThisKey})
                    con.commit()
                except:
                    con.rollback()
                finally:
                    cur.close()
            elif "Reply" in Key[0]:
                if "Fin" in Key[0]:
                    ReplyID = 0
                else:
                    ReplyID = int(Key[0].lstrip("Reply"))
            print Key[0]
        # 掲示板表示
        con.row_factory = sqlite3.Row
        cur = con.cursor()

#------------------------------Reply Form--------------------------
        try:
            if form.has_key('Replyname') and form.has_key('Replycomment'):
                ReplyName =  unicode(form.getfirst('Replyname',''),'utf-8')
                ReplyComment = unicode(form.getfirst('Replycomment',''),'utf-8')
                ThisKey = int(Key[0].lstrip("send"))
                cur.execute("UPDATE boardtbl SET Replyname=:name, Replycomment=:comment WHERE UNIQUEID=:uniqueid",{'name':ReplyName, 'comment':ReplyComment, 'uniqueid':ThisKey})
                con.commit()
        except:
            con.rollback()

        try:
#------------------------------Tag button--------------------------
            if form.has_key('TAG'):
                if form.getfirst('TAG','') == "Rescue":
                    Tag = "Genre='Rescue'"
                elif form.getfirst('TAG','') == "Goods":
                    Tag = "Genre='Goods'"
                else:
                    Tag = ""

            if form.has_key('SOLVE'):
                if form.getfirst('SOLVE','') == "Resolve":
                    Solve = "SolvedFlag = 1"
                elif form.getfirst('SOLVE','') == "Unsolved":
                    Solve = "SolvedFlag = 0"
                else:
                    Solve = ""

            show = "WHERE Genre='Refuge' "
            if Tag != "":
                show = "AND " + Tag
                if Solve != "":
                    show += " AND " + Solve
            elif Solve != "":
                show = "AND " + Solve

            cur.execute("SELECT DISTINCT * FROM boardtbl %s ORDER BY regdate DESC" % show)

            print "<dl>"
            for each in cur.fetchall():
                COLOR = "<div id='BLACK'>" if each['SolvedFlag'] == '1' else "TAG"
                if COLOR == "TAG":
                    COLOR = "<div id='RESCUE'>" if each['Genre'] == 'Rescue' else "<div id='GOODS'>"
                print COLOR
                if each['UNIQUEID'] == ReplyID:
                    print message%{'UNIQUEID':each['UNIQUEID'],'ID':each['ID'],'Genre':each['Genre'], 'LocationID':each['LocationID'],'name':each['name'].encode('utf-8'),'regdate':each['regdate'].encode('utf-8'),'comment':each['comment'].encode('utf-8'),'ResolButton':"Resolution"+str(each['UNIQUEID']),'ReplyButton':"FinReply"+str(each['UNIQUEID'])}
                else:
                    print message%{'UNIQUEID':each['UNIQUEID'],'ID':each['ID'],'Genre':each['Genre'], 'LocationID':each['LocationID'],'name':each['name'].encode('utf-8'),'regdate':each['regdate'].encode('utf-8'),'comment':each['comment'].encode('utf-8'),'ResolButton':"Resolution"+str(each['UNIQUEID']),'ReplyButton':"Reply"+str(each['UNIQUEID'])}
                if each['Replyname'] != '':
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
                    <form method="POST" action="./pyboardMain.py">
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
