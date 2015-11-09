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
                #Instraction{
                  background-color: #5588FF;
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
            <h1>活動指示</h1>
            <div class="main">
        '''


def PyBoardData():
    Tag = ""
    Solve = ""

    message = '''
        <dt id="Title"><hr />ID: %(ID)s, %(regdate)s 場所ID: %(LocationID)s 記入者: %(Registrant)s 宛先: %(Target)s</dt><br>
        <dd id="Message">
        %(Message)s
        </dd><br>
        <dd id="Date">
        <form method="POST" action="./pyboard_Chronology.py">
        <input type="submit" name=%(SolveButton)s value="Solved">
        </form>
        </dd>
        '''

    con = sqlite3.connect("board.db")

    try:
        # DB作成
        cur = con.cursor()
        cur.executescript("""CREATE TABLE Instractiontbl(UNIQUEID integer primary key autoincrement, ID integer, LocationID varchar(5), regdate timestamp, Registrant varchar(100), Target varchar(100), Message varchar(1024), SolvedFlag varchar(1), Send varchar(2));""")
        cur.close()
    except:
        print
    finally:
        # 入力データがあれば、DB登録
        form = cgi.FieldStorage()

        ReplyID = 0
        Key = form.keys()
        Option = ""

        if len(Key)!=0:
            if "Resolution" in Key[0]:
                ThisKey = int(Key[0].lstrip("Resolution"))
                cur = con.cursor()
                try:
                    cur.execute("UPDATE Instractiontbl SET SolvedFlag='1' WHERE UNIQUEID=:uniqueid",{"uniqueid":ThisKey})
                    con.commit()
                except:
                    con.rollback()
                finally:
                    cur.close()
            if "name" in Key:
                Option = " WHERE Registrant='" + unicode(form.getfirst('name',''),'utf-8') + "' "
                if "location" in Key:
                    Option += "AND Target='" + unicode(form.getfirst('target',''),'utf-8') + "' "
                    if "location" in Key:
                        Option += "AND LocationID=" + unicode(form.getfirst('location',''),'utf-8') + " "
            elif "target" in Key:
                Option = " WHERE Target='" + unicode(form.getfirst('target',''),'utf-8') + "' "
                if "location" in Key:
                    Option += "AND LocationID=" + unicode(form.getfirst('location',''),'utf-8') + " "
            elif "location" in Key:
                Option = " WHERE LocationID=" + unicode(form.getfirst('location',''),'utf-8') + " "


        if form.getfirst('send') and form.has_key('send') and form.has_key('Registrant') and form.has_key('Message'):
            # nameが指定されていたらコメント登録
            Registrant = unicode(form.getfirst('Registrant',''),'utf-8')
            Message = unicode(form.getfirst('Message',''),'utf-8')
            Target = unicode(form.getfirst('Target',''),'utf-8')
            cur = con.cursor()
            try:
                cur.execute("SELECT count(*) FROM Instractiontbl WHERE LocationID='1' ")
                IDnum = cur.fetchone()[0]
                cur.execute("SELECT * FROM Instractiontbl WHERE ID=:id AND Registrant=:Registrant AND Message=:Message",{"id":IDnum,"Registrant":Registrant,"Message":Message})

                if cur.fetchone() == None:
                    IDnum += 1
                    #cur.execute("INSERT INTO Instractiontbl(ID,LocationID,regdate,Registrant,Patient_Name,comment,SolvedFlag) values(?,'1',datetime('now','localtime'),?,?,?,'0')",(IDnum,Registrant,Patient_Name,comment))
                    cur.execute("INSERT INTO Instractiontbl(ID,LocationID,regdate,Registrant,Target,Message,SolvedFlag) values(?,'H',datetime('now','localtime'),?,?,?,'0')",(IDnum,Registrant,Target,Message))
                con.commit()
            except:
                con.rollback()
            finally:
                cur.close()

        # 掲示板表示
        con.row_factory = sqlite3.Row
        cur = con.cursor()

#------------------------------Tag button--------------------------
        try:
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

            show = ""
            if Tag != "":
                show = "AND " + Tag
                if Solve != "":
                    show += " AND " + Solve
            elif Solve != "":
                show = "AND " + Solve

            cur.execute("SELECT DISTINCT * FROM Instractiontbl %s ORDER BY regdate DESC" % Option)

            print "<dl>"
            for each in cur.fetchall():
                # COLOR = "<div id='BLACK'>" if each['SolvedFlag'] == '1' else "TAG"
                # if COLOR == "TAG":
                #     COLOR = "<div id='RESCUE'>" if each['Genre'] == 'Rescue' else "<div id='GOODS'>"
                COLOR = "<div id='Instraction'>"
                print COLOR
                # if each['UNIQUEID'] == ReplyID:
                print message%{'ID':each['UNIQUEID'],'LocationID':each['LocationID'],'Registrant':each['Registrant'].encode('utf-8'),'Target':each['Target'].encode('utf-8'),'regdate':each['regdate'].encode('utf-8'),'Message':each['Message'].encode('utf-8'),'SolveButton':"Resolution"+str(each['UNIQUEID'])}
                # else:
                #     print message%{'ID':each['UNIQUEID'],'LocationID':each['LocationID'],'Registrant':each['Registrant'].encode('utf-8'),'Target':each['Target'].encode('utf-8'),'regdate':each['regdate'].encode('utf-8'),'Message':each['Message'].encode('utf-8'),'ReplyButton':"Reply"+str(each['UNIQUEID'])}
                # if each['Replyname'] != '':
                #     print '''
                #     <div id='ReplyComment'>
                #     <dt id="Title"><hr />ReplyName:%(Replyname)s</dt><br>
                #     <dd id="Message">%(Replycomment)s</dd><br>
                #     </div>
                #     ''' % {'Replyname':each['Replyname'],'Replycomment':each['Replycomment']}
                print "</div>"
                print "</dl>"
                # if each['UNIQUEID'] == ReplyID:
                #     print '''
                #     <div id='Reply'>
                #     <form method="POST" action="./pyboardMain.py">
                #         <table>
                #         <tr>
                #         <td><b>Name:</b></td>
                #         <td><input type="text" name="Replyname" size="10" value=""></td>
                #         </tr>
                #         <tr>
                #         <td><b>Message:</b></td>
                #         <td><textarea cols="30" rows="5" name="Replycomment"></textarea></td>
                #         </tr>
                #         <tr>
                #         <td colspan="2"><input type="submit" name="send%(ReplyID)s" value="Send"><input type="reset" value="Reset"></td>
                #         </tr>
                #         </table>
                #     </form>
                #     </div>
                #     '''%{'ReplyID':ReplyID}
        finally:
            cur.close()
            con.close()
            print "</div>"


if __name__=='__main__':
    PyBoard()
    PyBoardData()
