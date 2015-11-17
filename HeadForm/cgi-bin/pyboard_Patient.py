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
                #SOLVED{
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
            <h1>傷病者情報</h1>
            <div class="main">
        '''


def PyBoardData():
    Tag = ""
    Solve = ""

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
        <form method="POST" action="./pyboard_Patient.py">
        <input type="submit" name=%(ResolButton)s value="Resolution">
        </form>
        </dd>
        '''

    con = sqlite3.connect("board.db")

    try:
        # DB作成
        cur = con.cursor()
        cur.executescript("""CREATE TABLE Patienttbl(UNIQUEID integer primary key autoincrement, ID integer, LocationID varchar(5), regdate timestamp, Registrant varchar(100), Patient_Name varchar(100), Patient_Age varchar(10), Patient_Gender varchar(10), Patient_Triage varchar(10), Patient_Injuries_Diseases varchar(1024), Patient_Treatment varchar(1024), Patient_Hospital varchar(1024), comment varchar(1024), SolvedFlag varchar(1), Send varchar(2));""")
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
                    cur.execute("UPDATE Patienttbl SET SolvedFlag='1', Send='1' WHERE UNIQUEID=:uniqueid",{"uniqueid":ThisKey})
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

            cur.execute("SELECT DISTINCT * FROM Patienttbl %s ORDER BY regdate DESC" % show)

            print "<dl>"
            for each in cur.fetchall():
                COLOR = "<div id='SOLVED'>" if each['SolvedFlag'] == '1' else "TAG"
                if COLOR == "TAG":
                    if each['Patient_Triage'] == 'black':
                        COLOR = "<div id='BLACK'>"
                    elif each['Patient_Triage'] == 'red':
                        COLOR = "<div id='RED'>"
                    elif each['Patient_Triage'] == 'yellow':
                        COLOR = "<div id='YELLOW'>"
                    elif each['Patient_Triage'] == 'green':
                        COLOR = "<div id='GREEN'>"
                print COLOR
                print message%{'ID':each['UNIQUEID'],'LocationID':each['LocationID'],'Registrant':each['Registrant'].encode('utf-8'),'regdate':each['regdate'].encode('utf-8'),'Patient_Name':each['Patient_Name'].encode('utf-8'),'Patient_Age':each['Patient_Age'].encode('utf-8'),'Patient_Gender':each['Patient_Gender'].encode('utf-8'),'Patient_Triage':each['Patient_Triage'].encode('utf-8'),'Patient_Injuries_Diseases':each['Patient_Injuries_Diseases'].encode('utf-8'),'Patient_Treatment':each['Patient_Treatment'].encode('utf-8'),'Patient_Hospital':each['Patient_Hospital'].encode('utf-8'),'comment':each['comment'].encode('utf-8'),'EditButton':"Edit"+str(each['UNIQUEID']),'ResolButton':"Resolution"+str(each['UNIQUEID'])}
                print "</div></dl>"
        finally:
            cur.close()
            con.close()
            print "</div>"


if __name__=='__main__':
    PyBoard()
    PyBoardData()
