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
    <style type="text/css">
        body{
          background-color: #FFEEDC;

        }
        .scr {
          overflow: scroll;
          margin-left: 20px;
          width: 600px;
          height: 500px;
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
        #Edit{
            background-color: #0055AA;
        }

        #MessageBgcolor{
          background-color: #55FF88;
        }

    </style>
    　
    </head>
    <body>

    '''

message = '''
    <dt id="Title"><hr />ID: %(ID)s, %(regdate)s 場所ID: %(LocationID)s 記入者: %(Registrant)s</dt><br>
    <dd id="Message">
    %(Message)s
    </dd><br>
    <dd id="Date">
    <form>
    <input type="submit" name=%(EditButton)s value="Edit">
    </form>
    </dd>
    '''

con = sqlite3.connect("board.db")

try:
    # DB作成
    cur = con.cursor()
    cur.executescript("""CREATE TABLE Chronologytbl(UNIQUEID integer primary key autoincrement, ID integer, LocationID varchar(5), regdate timestamp, Registrant varchar(100),  Message varchar(1024));""")
    cur.close()
except:
    print
finally:
    # 入力データがあれば、DB登録
    form = cgi.FieldStorage()
    Key = form.keys()
    EditID = 0

    if len(Key)!=0:
        if "Edit" in Key[0]:
            if "Fin" in Key[0]:
                EditID = 0
            else:
                EditID = int(Key[0].lstrip("Edit"))

    if form.getfirst('send') and form.has_key('send') and form.has_key('Registrant') and form.has_key('Message'):
        # nameが指定されていたらコメント登録
        Registrant = unicode(form.getfirst('Registrant',''),'utf-8')
        Message = unicode(form.getfirst('Message',''),'utf-8')
        cur = con.cursor()
        # print Registrant,Patient_Name,Patient_Age,Patient_Gender,Patient_Triage,Patient_Injuries_Diseases,Patient_Treatment,Patient_Hospital,comment
        try:
            cur.execute("SELECT count(*) FROM Chronologytbl WHERE LocationID='1' ")
            IDnum = cur.fetchone()[0]
            cur.execute("SELECT * FROM Chronologytbl WHERE ID=:id AND Registrant=:Registrant AND Message=:Message",{"id":IDnum,"Registrant":Registrant,"Message":Message})

            if cur.fetchone() == None:
                IDnum += 1
                #cur.execute("INSERT INTO Chronologytbl(ID,LocationID,regdate,Registrant,Patient_Name,comment,SolvedFlag) values(?,'1',datetime('now','localtime'),?,?,?,'0')",(IDnum,Registrant,Patient_Name,comment))
                cur.execute("INSERT INTO Chronologytbl(ID,LocationID,regdate,Class,Registrant,Message) values(?,'1',datetime('now','localtime'),'Chronology',?,?)",(IDnum,Registrant,Message))
            con.commit()
        except:
            con.rollback()
        finally:
            cur.close()

    # 掲示板表示
    con.row_factory = sqlite3.Row
    cur = con.cursor()
    try:
        cur.execute("SELECT * FROM Chronologytbl ORDER BY regdate DESC")
        print "<div class='scr'>"
        print "<dl>"
        for each in cur.fetchall():
            print "<div id='MessageBgcolor'>"
            if each['UNIQUEID'] == EditID:
                # print message%{'ID':each['UNIQUEID'],'LocationID':each['LocationID'],'Registrant':each['Registrant'].encode('utf-8'),'regdate':each['regdate'].encode('utf-8'),'Patient_Name':each['Patient_Name'].encode('utf-8'),'Patient_Age':each['Patient_Age'].encode('utf-8'),'Patient_Gender':each['Patient_Gender'].encode('utf-8'),'Patient_Triage':each['Patient_Triage'].encode('utf-8'),'Patient_Injuries_Diseases':each['Patient_Injuries_Diseases'].encode('utf-8'),'Patient_Treatment':each['Patient_Treatment'].encode('utf-8'),'Patient_Hospital':each['Patient_Hospital'].encode('utf-8'),'comment':each['comment'].encode('utf-8'),'EditButton':"FinEdit"+str(each['UNIQUEID'])}
                print '''
                    <form method="POST" action="./pyboard.cgi" target="pyboard">
                    <table>
                    <tr>
                    <td><b>記入者の名前:</b></td>
                    <td><input type="text" name=%(Registrant)s size="10"></td>
                    </tr>
                    </table>
                    <table>
                    <tr>
                    <td><b>傷病者名:</b>
                    <textarea cols="50" rows="5" name="Message" >救護所1設営完了</textarea></td>
                    <tr>
                    <td colspan="2"><input type="submit" name="send" value="Send"><input type="reset" value="Reset"></td>
                    </tr>
                    </table>
                    </form>
                    '''%{'Registrant':each['Registrant'].encode('utf-8'),'Message':each['Message'].encode('utf-8')}
            else:
                print message%{'ID':each['UNIQUEID'],'LocationID':each['LocationID'],'Registrant':each['Registrant'].encode('utf-8'),'regdate':each['regdate'].encode('utf-8'),'Message':each['Message'].encode('utf-8'),'EditButton':"Edit"+str(each['UNIQUEID'])}
            print "</div>"
            print "</dl>"

    finally:
        cur.close()
        con.close()
        print "</div></body></html>"
