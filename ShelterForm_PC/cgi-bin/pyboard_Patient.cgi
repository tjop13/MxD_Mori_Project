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

        #Date{
          text-align: right;
        }
        #Edit{
            background-color: #0055AA;
        }

        #Solved{
          background-color: #666666;
        }
        #BLACK{
          background-color: #222222;
        }
        #RED{
          background-color: #FF3333;
        }
        #YELLOW{
          background-color: #F0E68C;
        }
        #GREEN{
          background-color: #90EE90
        }

    </style>
    　
    </head>
    <body>
    <form method="POST" action="http://localhost:8000/cgi-bin/pyboard_Patient.cgi" target="pyboard_Patient">
      <table>
        <tr>
        <td><b>記入者の名前:</b></td>
        <td><input type="text" name="Registrant" size="10" ></td>
        </tr>
        <tr>
        <td><b>傷病者名:</b><br>
        <textarea cols="10" rows="1" name="Patient_Name" ></textarea></td>
        <td><b>年齢:</b><br>
        <textarea cols="5" rows="1" name="Patient_Age" ></textarea></td>
        <td><b>性別:</b><br>
          <input type="radio" name="Patient_Gender" value="男" checked>男
          <input type="radio" name="Patient_Gender" value="女">女
        </td>
        <td><b>トリアージ区分:</b><br>
          <input type="radio" name="Patient_Triage" value="black" checked>黒
          <input type="radio" name="Patient_Triage" value="red">赤
          <input type="radio" name="Patient_Triage" value="yellow">黄
          <input type="radio" name="Patient_Triage" value="green">緑
        </td>
      </table>
      <table>
        <tr>
        <td><b>傷病名:</b>
        <textarea cols="20" rows="3" name="Patient_Injuries_Diseases" ></textarea></td>
        <td><b>行った処置:</b>
        <textarea cols="20" rows="3" name="Patient_Treatment" ></textarea></td>
        <td><b>搬送先病院:</b>
        <textarea cols="20" rows="3" name="Patient_Hospital" ></textarea></td>
        <td><b>備考:</b>
        <textarea cols="20" rows="3" name="comment" ></textarea></td>
        </tr>
        <tr>
        <td colspan="2"><input type="submit" name="send" value="Send"><input type="reset" value="Reset"></td>
        </tr>
      </table>
    </form>
    <div class="scr">
    '''

message = '''
    <dt id="Title"><hr />ID: %(ID)s, %(regdate)s 場所ID: %(LocationID)s 記入者: %(Registrant)s</dt><br>
    <dd id="Message">
    <table>
    <tr>
    <th>傷病者名</th>
    <th>性別</th>
    <th>年齢</th>
    <th>傷病名</th>
    <th>処置</th>
    <th>搬送先病院</th>
    <th>備考</th>
    </tr>
    <tr>
    <td>%(Patient_Name)s</td>
    <td>%(Patient_Gender)s</td>
    <td>%(Patient_Age)s</td>
    <td>%(Patient_Injuries_Diseases)s</td>
    <td>%(Patient_Treatment)s</td>
    <td>%(Patient_Hospital)s</td>
    <td>%(comment)s</td>
    </tr>
    </table>
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
    cur.executescript("""CREATE TABLE Patienttbl(UNIQUEID integer primary key autoincrement, ID integer, LocationID varchar(5), regdate timestamp, Registrant varchar(100), Patient_Name varchar(100), Patient_Age varchar(10), Patient_Gender varchar(10), Patient_Triage varchar(10), Patient_Injuries_Diseases varchar(1024), Patient_Treatment varchar(1024), Patient_Hospital varchar(1024), comment varchar(1024), SolvedFlag varchar(1), Send varchar(2));""")
    cur.close()
    cur = con.cursor()
    cur.executescript("""CREATE TABLE Chronologytbl(UNIQUEID integer primary key autoincrement, ID integer, LocationID varchar(5), regdate timestamp, Registrant varchar(100),  Message varchar(1024),Replyname varchar(100),Replycomment varchar(1024),Tag varchar(50), Send varchar(2));""")
    cur.close()
except:
    print
finally:
    # 入力データがあれば、DB登録
    form = cgi.FieldStorage()
    Key = form.keys()
    EditID = 0
    ESubmitFlag = 0

    if len(Key)!=0:
        if "Edit" in Key[0]:
            if "Fin" in Key[0]:
                EditID = 0
            else:
                EditID = int(Key[0].lstrip("Edit"))

        if len(Key)>8:
            for data in Key:
                if "ESubmit" in data:
                    print data
                    ESubmitID = int(data.lstrip("ESubmit_"))
                    ESubmitFlag = 1

            if ESubmitFlag == 1:
                print ESubmitID
                Registrant = unicode(form.getfirst('Registrant',''),'utf-8')
                Patient_Name = unicode(form.getfirst('Patient_Name',''),'utf-8')
                Patient_Age = unicode(form.getfirst('Patient_Age',''),'utf-8')
                Patient_Gender = unicode(form.getfirst('Patient_Gender',''),'utf-8')
                Patient_Triage = unicode(form.getfirst('Patient_Triage',''),'utf-8')
                Patient_Injuries_Diseases = unicode(form.getfirst('Patient_Injuries_Diseases',''),'utf-8')
                Patient_Treatment = unicode(form.getfirst('Patient_Treatment',''),'utf-8')
                Patient_Hospital = unicode(form.getfirst('Patient_Hospital',''),'utf-8')
                comment = unicode(form.getfirst('comment',''),'utf-8')
                Message = "項目：傷病者情報編集<br>傷病者名：" + Patient_Name + "<br>編集内容：" + unicode(form.getfirst('Message',''),'utf-8')
                cur = con.cursor()
                try:
                    cur.execute("UPDATE Patienttbl SET Registrant=:Registrant ,Patient_Name=:Patient_Name ,Patient_Age=:Patient_Age ,Patient_Gender=:Patient_Gender ,Patient_Triage=:Patient_Triage ,Patient_Injuries_Diseases=:Patient_Injuries_Diseases ,Patient_Treatment=:Patient_Treatment ,Patient_Hospital=:Patient_Hospital,comment=:comment, Send='1' WHERE ID=:ID",{"Registrant":Registrant ,"Patient_Name":Patient_Name ,"Patient_Age":Patient_Age ,"Patient_Gender":Patient_Gender ,"Patient_Triage":Patient_Triage ,"Patient_Triage":Patient_Triage ,"Patient_Injuries_Diseases":Patient_Injuries_Diseases ,"Patient_Treatment":Patient_Treatment ,"Patient_Hospital":Patient_Hospital ,"comment":comment, "ID":ESubmitID})
                    con.commit()
                except:
                    con.rollback()
                finally:
                    cur.close()
                    cur = con.cursor()
                    # print Registrant,Patient_Name,Patient_Age,Patient_Gender,Patient_Triage,Patient_Injuries_Diseases,Patient_Treatment,Patient_Hospital,comment
                    try:
                        cur.execute("SELECT count(*) FROM Chronologytbl WHERE LocationID='1' ")
                        IDnum = cur.fetchone()[0]
                        cur.execute("SELECT * FROM Chronologytbl WHERE ID=:id AND Registrant=:Registrant AND Message=:Message",{"id":IDnum,"Registrant":Registrant,"Message":Message})
                        if cur.fetchone() == None:
                            IDnum += 1
                            #cur.execute("INSERT INTO Chronologytbl(ID,LocationID,regdate,Registrant,Patient_Name,comment,SolvedFlag) values(?,'1',datetime('now','localtime'),?,?,?,'0')",(IDnum,Registrant,Patient_Name,comment))
                            cur.execute("INSERT INTO Chronologytbl(ID,LocationID,regdate,Registrant,Message,Tag,Send) values(?,'1',datetime('now','localtime'),?,?,'傷病者情報編集','1')",(IDnum,Registrant,Message))
                        con.commit()
                    except:
                        con.rollback()
                    finally:
                        cur.close()

    if form.getfirst('send') and form.has_key('send') and form.has_key('Registrant') and form.has_key('Patient_Name'):
        # nameが指定されていたらコメント登録
        Registrant = unicode(form.getfirst('Registrant',''),'utf-8')
        Patient_Name = unicode(form.getfirst('Patient_Name',''),'utf-8')
        Patient_Age = unicode(form.getfirst('Patient_Age',''),'utf-8')
        Patient_Gender = unicode(form.getfirst('Patient_Gender',''),'utf-8')
        Patient_Triage = unicode(form.getfirst('Patient_Triage',''),'utf-8')
        Patient_Injuries_Diseases = unicode(form.getfirst('Patient_Injuries_Diseases',''),'utf-8')
        Patient_Treatment = unicode(form.getfirst('Patient_Treatment',''),'utf-8')
        Patient_Hospital = unicode(form.getfirst('Patient_Hospital',''),'utf-8')
        comment = unicode(form.getfirst('comment',''),'utf-8')
        cur = con.cursor()
        # print Registrant,Patient_Name,Patient_Age,Patient_Gender,Patient_Triage,Patient_Injuries_Diseases,Patient_Treatment,Patient_Hospital,comment
        try:
            cur.execute("SELECT count(*) FROM Patienttbl WHERE LocationID='1' ")
            IDnum = cur.fetchone()[0]
            cur.execute("SELECT * FROM Patienttbl WHERE ID=:id AND Registrant=:Registrant AND Patient_Name=:Patient_Name",{"id":IDnum,"Registrant":Registrant,"Patient_Name":Patient_Name})

            if cur.fetchone() == None:
                IDnum += 1
                #cur.execute("INSERT INTO Patienttbl(ID,LocationID,regdate,Registrant,Patient_Name,comment,SolvedFlag) values(?,'1',datetime('now','localtime'),?,?,?,'0')",(IDnum,Registrant,Patient_Name,comment))
                cur.execute("INSERT INTO Patienttbl(ID,LocationID,regdate,Registrant,Patient_Name,Patient_Age,Patient_Gender,Patient_Triage,Patient_Injuries_Diseases,Patient_Treatment,Patient_Hospital,comment,SolvedFlag) values(?,'1',datetime('now','localtime'),?,?,?,?,?,?,?,?,?,'0')",(IDnum,Registrant,Patient_Name,Patient_Age,Patient_Gender,Patient_Triage,Patient_Injuries_Diseases,Patient_Treatment,Patient_Hospital,comment))

            con.commit()
        except:
            con.rollback()
        finally:
            cur.close()

    # 掲示板表示
    con.row_factory = sqlite3.Row
    cur = con.cursor()
    try:
        Tag=""
        Solve=""
        if form.has_key('TAGBlack'):
            Tag = "Patient_Triage='black' OR "
        if form.has_key('TAGRed'):
            Tag += "Patient_Triage='red' OR "
        if form.has_key('TAGYellow'):
            Tag += "Patient_Triage='yellow' OR "
        if form.has_key('TAGGreen'):
            Tag += "Patient_Triage='green' OR "
        if Tag != "":
            Tag = Tag.rstrip("OR ")
            Tag = "( " + Tag + " )"


        if form.getfirst('Resolve','') == "Resolve":
            Solve += "SolvedFlag = 1 OR "
        if form.getfirst('Unsolved','') == "Unsolved":
            Solve += "SolvedFlag = 0 OR "
        if Solve != "":
            Solve = Solve.rstrip("OR ")
            Solve = "( " + Solve + " )"

        show = ""
        if Tag != "":
            show = "WHERE " + Tag
            if Solve != "":
                show += " AND " + Solve
        elif Solve != "":
            show = "WHERE " + Solve

        print show

        cur.execute("SELECT * FROM Patienttbl %s ORDER BY regdate DESC" % show)
        print "<dl>"
        for each in cur.fetchall():
            COLOR = "<div id='Solved'>" if each['SolvedFlag'] == '1' else "TAG"
            if COLOR == "TAG":
                if each['UNIQUEID'] == EditID:
                    COLOR = "<div id='Edit'>"
                elif each['Patient_Triage'] == 'black':
                    COLOR = "<div id='BLACK'>"
                elif each['Patient_Triage'] == 'red':
                    COLOR = "<div id='RED'>"
                elif each['Patient_Triage'] == 'yellow':
                    COLOR = "<div id='YELLOW'>"
                elif each['Patient_Triage'] == 'green':
                    COLOR = "<div id='GREEN'>"
            print COLOR
            if each['UNIQUEID'] == EditID:
                # print message%{'ID':each['UNIQUEID'],'LocationID':each['LocationID'],'Registrant':each['Registrant'].encode('utf-8'),'regdate':each['regdate'].encode('utf-8'),'Patient_Name':each['Patient_Name'].encode('utf-8'),'Patient_Age':each['Patient_Age'].encode('utf-8'),'Patient_Gender':each['Patient_Gender'].encode('utf-8'),'Patient_Triage':each['Patient_Triage'].encode('utf-8'),'Patient_Injuries_Diseases':each['Patient_Injuries_Diseases'].encode('utf-8'),'Patient_Treatment':each['Patient_Treatment'].encode('utf-8'),'Patient_Hospital':each['Patient_Hospital'].encode('utf-8'),'comment':each['comment'].encode('utf-8'),'EditButton':"FinEdit"+str(each['UNIQUEID'])}
                print '''
                    <form method="POST" action="./pyboard_Patient.cgi" target="pyboard_Patient">
                    <table>
                    <tr>
                    <td><b>編集者の名前:</b></td>
                    <td><input type="text" name="Registrant" size="10" value="田中"></td>
                    </tr>
                    </table>
                    <table>
                    <tr>
                    <td><b>傷病者名:</b>
                    <textarea cols="10" rows="1" name="Patient_Name" >%(Patient_Name)s</textarea></td>
                    <td><b>年齢:</b>
                    <textarea cols="5" rows="1" name="Patient_Age" >%(Patient_Age)s</textarea></td>
                    '''%{'Patient_Name':each['Patient_Name'].encode('utf-8'),'Patient_Age':each['Patient_Age'].encode('utf-8')}
                if each['Patient_Gender']=="男":
                    print '''
                        <td><b>性別:</b>
                          <input type="radio" name="Patient_Gender" value="男" checked>男
                          <input type="radio" name="Patient_Gender" value="女">女
                        </td>
                    '''
                else:
                    print '''
                        <td><b>性別:</b>
                          <input type="radio" name="Patient_Gender" value="男">男
                          <input type="radio" name="Patient_Gender" value="女" checked>女
                        </td>
                    '''
                print "<td><b>トリアージ区分:</b>"
                if each['Patient_Triage']=="black":
                    print '''
                      <input type="radio" name="Patient_Triage" value="black" checked>黒
                      <input type="radio" name="Patient_Triage" value="red">赤
                      <input type="radio" name="Patient_Triage" value="yellow">黄
                      <input type="radio" name="Patient_Triage" value="green">緑
                      '''
                elif each['Patient_Triage']=="red":
                    print '''
                      <input type="radio" name="Patient_Triage" value="black">黒
                      <input type="radio" name="Patient_Triage" value="red" checked>赤
                      <input type="radio" name="Patient_Triage" value="yellow">黄
                      <input type="radio" name="Patient_Triage" value="green">緑
                      '''
                elif each['Patient_Triage']=="yellow":
                    print '''
                      <input type="radio" name="Patient_Triage" value="black">黒
                      <input type="radio" name="Patient_Triage" value="red">赤
                      <input type="radio" name="Patient_Triage" value="yellow" checked>黄
                      <input type="radio" name="Patient_Triage" value="green">緑
                      '''
                elif each['Patient_Triage']=="green":
                    print '''
                      <input type="radio" name="Patient_Triage" value="black">黒
                      <input type="radio" name="Patient_Triage" value="red">赤
                      <input type="radio" name="Patient_Triage" value="yellow">黄
                      <input type="radio" name="Patient_Triage" value="green" checked>緑
                      '''
                print '''
                    </td>
                    </table>
                    <table>
                    <tr>
                    <td><b>傷病名:</b>
                    <textarea cols="20" rows="3" name="Patient_Injuries_Diseases" >%(Patient_Injuries_Diseases)s</textarea></td>
                    <td><b>行った処置:</b>
                    <textarea cols="20" rows="3" name="Patient_Treatment" >%(Patient_Treatment)s</textarea></td>
                    <td><b>搬送先病院:</b>
                    <textarea cols="20" rows="3" name="Patient_Hospital" >%(Patient_Hospital)s</textarea></td>
                    <td><b>備考:</b>
                    <textarea cols="20" rows="3" name="comment" >%(comment)s</textarea></td>
                    </tr>
                    <tr>
                    <td><b>編集した内容:</b>
                    <textarea cols="20" rows="3" name="Message" placeholder="編集した内容を入力してください">トリアージ変更</textarea></td>
                    </tr>
                    <tr>
                    <td colspan="2"><input type="submit" name="ESubmit_%(EditID)s" value="Send"><input type="reset" value="Reset"></td>
                    <td><input type="submit" name=%(EditButton)s value="更新終了"></td>
                    </tr>
                    </table>
                    </form>
                '''%{'Patient_Injuries_Diseases':each['Patient_Injuries_Diseases'].encode('utf-8'),'Patient_Treatment':each['Patient_Treatment'].encode('utf-8'),'Patient_Hospital':each['Patient_Hospital'].encode('utf-8'),'comment':each['comment'].encode('utf-8'),'EditID':EditID,'EditButton':"FinEdit"+str(each['UNIQUEID'])}
            else:
                print message%{'ID':each['UNIQUEID'],'LocationID':each['LocationID'],'Registrant':each['Registrant'].encode('utf-8'),'regdate':each['regdate'].encode('utf-8'),'Patient_Name':each['Patient_Name'].encode('utf-8'),'Patient_Age':each['Patient_Age'].encode('utf-8'),'Patient_Gender':each['Patient_Gender'].encode('utf-8'),'Patient_Triage':each['Patient_Triage'].encode('utf-8'),'Patient_Injuries_Diseases':each['Patient_Injuries_Diseases'].encode('utf-8'),'Patient_Treatment':each['Patient_Treatment'].encode('utf-8'),'Patient_Hospital':each['Patient_Hospital'].encode('utf-8'),'comment':each['comment'].encode('utf-8'),'EditButton':"Edit"+str(each['UNIQUEID'])}
            print "</div>"
            print "</dl>"

    finally:
        cur.close()
        con.close()
        print "</div></body></html>"
