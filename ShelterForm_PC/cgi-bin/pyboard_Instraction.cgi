#!/usr/bin/env python
# -*- coding: utf-8 -*-

import cgi
import cgitb
import sqlite3

import unicodedata

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
          width: 590px;
          height: 1000px;
        }

        #Title{
            text-align: left;
        }
        #Message{
          text-align: left;
          margin-left: 20px;
        }

        #BLACK{
          background-color: #666666;
        }
        #Date{
          text-align: right;
        }
        #Edit{
            background-color: #0055AA;
        }

        #MessageBgcolor{
          background-color: #5588FF;
        }

    </style>
    　
    </head>
    <body>
    <form method="POST" action="http://localhost:8000/cgi-bin/pyboard_Instraction.cgi" target="pyboard_Instraction">
    <table>
      <tr>
      <td><b>記入者の名前:</b></td>
      <td><input type="text" name="Registrant" size="10" ></td>
      <td><b>宛先:</b></td>
      <td><input type="text" name="Target" size="10"></td>
      </tr>
    </table>
    <table>
    <tr>
    <td><b>内容:</b>
    <textarea cols="50" rows="5" name="Message" ></textarea></td>
    </tr>
    <tr>
    <td colspan="2"><input type="submit" name="send" value="Send"><input type="reset" value="Reset"></td>
    </tr>
    </table>
    </form>
    <div class="scr">
    '''

message = '''
    <dt id="Title"><hr />ID: %(ID)s, %(regdate)s 場所ID: %(LocationID)s 記入者: %(Registrant)s 宛先: %(Target)s</dt><br>
    <dd id="Message">
    %(Message)s
    </dd><br>
    <dd id="Date">
    <form>
    <input type="submit" name=%(ConfirmationButton)s value="確認完了">
    </form>
    </dd>
    '''

con = sqlite3.connect("board.db")

try:
    # DB作成
    cur = con.cursor()
    cur.executescript("""CREATE TABLE Instractiontbl(UNIQUEID integer primary key autoincrement, ID integer, LocationID varchar(5), regdate timestamp, Registrant varchar(100), Target varchar(100), Message varchar(1024),Replyname varchar(100),Replycomment varchar(1024), SolvedFlag varchar(1), Send varchar(2));""")
    cur.close()
except:
    print
finally:
    # 入力データがあれば、DB登録
    form = cgi.FieldStorage()
    Key = form.keys()
    EditID = 0
    Option = ""

    if len(Key)!=0:
        if "Confirmation" in Key[0]:
            ThisKey = int(Key[0].lstrip("Confirmation"))
            cur = con.cursor()
            try:
                cur.execute("UPDATE Instractiontbl SET SolvedFlag='1', Send='1' WHERE UNIQUEID=:uniqueid",{"uniqueid":ThisKey})
                con.commit()
            except:
                con.rollback()
            finally:
                cur.close()
        if "name" in Key:
            name = unicodedata.normalize('NFKC', unicode(form.getfirst('name',''),'utf-8'))
            target = unicodedata.normalize('NFKC', unicode(form.getfirst('target',''),'utf-8'))
            # name = unicodedata.normalize('NFKC', form.getfirst('name',''),'utf-8')
            Option = " WHERE Registrant like '%" + name + "%' "
            if "location" in Key:
                Option += "AND Target like '%" + target + "%' "
        elif "target" in Key:
            target = unicodedata.normalize('NFKC', unicode(form.getfirst('target',''),'utf-8'))
            Option = " WHERE Target like '%" + target + "%' "

    if form.getfirst('send') and form.has_key('send') and form.has_key('Registrant') and form.has_key('Message'):
        # nameが指定されていたらコメント登録
        Registrant = unicodedata.normalize('NFKC', unicode(form.getfirst('Registrant',''),'utf-8'))
        Message = unicode(form.getfirst('Message',''),'utf-8')
        Target = unicodedata.normalize('NFKC', unicode(form.getfirst('Target',''),'utf-8'))
        cur = con.cursor()
        # print Registrant,Patient_Name,Patient_Age,Patient_Gender,Patient_Triage,Patient_Injuries_Diseases,Patient_Treatment,Patient_Hospital,comment
        try:
            cur.execute("SELECT count(*) FROM Instractiontbl WHERE LocationID='1' ")
            IDnum = cur.fetchone()[0]
            cur.execute("SELECT * FROM Instractiontbl WHERE ID=:id AND Registrant=:Registrant AND Message=:Message",{"id":IDnum,"Registrant":Registrant,"Message":Message})

            if cur.fetchone() == None:
                IDnum += 1
                #cur.execute("INSERT INTO Instractiontbl(ID,LocationID,regdate,Registrant,Patient_Name,comment,SolvedFlag) values(?,'1',datetime('now','localtime'),?,?,?,'0')",(IDnum,Registrant,Patient_Name,comment))
                cur.execute("INSERT INTO Instractiontbl(ID,LocationID,regdate,Registrant,Target,Message,Replyname,Replycomment,SolvedFlag,Send) values(?,'1',datetime('now','localtime'),?,?,?,'','','0','1')",(IDnum,Registrant,Target,Message))
            con.commit()
        except:
            con.rollback()
        finally:
            cur.close()

    # 掲示板表示
    con.row_factory = sqlite3.Row
    cur = con.cursor()

    try:
        cur.execute("SELECT * FROM Instractiontbl %(Option)s ORDER BY regdate DESC"%{"Option":Option})
        print "<dl>"
        for each in cur.fetchall():
            print "<div id='BLACK'>" if each['SolvedFlag'] == '1' else "<div id='MessageBgcolor'>"
            # if each['UNIQUEID'] == EditID:
            #     print '''
            #         <form method="POST" action="./pyboard.cgi" target="pyboard">
            #         <table>
            #         <tr>
            #         <td><b>記入者の名前:</b></td>
            #         <td><input type="text" name=%(Registrant)s size="10"></td>
            #         <td><b>宛先:</b></td>
            #         <td><input type="text" name="Target" size="10" value=%(Target)s></td>
            #         </tr>
            #         </table>
            #         <table>
            #         <tr>
            #         <td><b>傷病者名:</b>
            #         <textarea cols="50" rows="5" name="Message" >救護所1設営完了</textarea></td>
            #         <tr>
            #         <td colspan="2"><input type="submit" name="send" value="Send"><input type="reset" value="Reset"></td>
            #         </tr>
            #         </table>
            #         </form>
            #         '''%{'Registrant':each['Registrant'].encode('utf-8'),'Message':each['Message'].encode('utf-8'),'Target':each['Target'].encode('utf-8')}
            # else:
            print message%{'ID':each['UNIQUEID'],'LocationID':each['LocationID'],'Registrant':each['Registrant'].encode('utf-8'),'Target':each['Target'].encode('utf-8'),'regdate':each['regdate'].encode('utf-8'),'Message':each['Message'].encode('utf-8'),'ConfirmationButton':"Confirmation"+str(each['UNIQUEID'])}
            print "</div>"
            print "</dl>"

    finally:
        cur.close()
        con.close()
        print "</div></body></html>"
