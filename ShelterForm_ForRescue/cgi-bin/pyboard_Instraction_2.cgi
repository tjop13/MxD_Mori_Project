#!/usr/bin/env python
# -*- coding: utf-8 -*-

import cgi
import cgitb
import json

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
          background-color: #5588FF;
        }

    </style>
    　
    </head>
    <body>

    '''

message = '''
    <dt id="Title"><hr />ID: %(ID)s, %(regdate)s 場所ID: %(LocationID)s 記入者: %(Registrant)s 宛先: %(Target)s</dt><br>
    <dd id="Message">
    %(Message)s
    </dd><br>
    <dd id="Date">
    <form>
    <input type="submit" name=%(EditButton)s value="Edit">
    </form>
    </dd>
    '''

# 入力データがあれば、DB登録
f1 = open(('date.json'),'r')
f2 = open(('Management.json'),'r')
Main_data = json.load(f)
Management_data = json.load(f2)
f1.close()
f2.close()

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
    Target = unicode(form.getfirst('Target',''),'utf-8')
    cur = con.cursor()
    # print Registrant,Patient_Name,Patient_Age,Patient_Gender,Patient_Triage,Patient_Injuries_Diseases,Patient_Treatment,Patient_Hospital,comment
    try:
        IDNum = Management_data['Instraction']
        if Main_data['Instraction_%(num)s'%IDNum][3] != Registrant and Main_data['Instraction_%(num)s'%IDNum][4] != Target and Main_data['Instraction_%(num)s'%IDNum][5] != Message):
            IDNum += 1
            Main_data['Instraction_%(num)s'%IDNum] = (IDnum,'1',datetime('now','localtime'),Registrant,Target,Message)
            Management_data['Instraction'] = IDNum

    finally:
        f1 = open(('date.json'),'w')
        f2 = open(('Management.json'),'w')
        f1.write(json.dumps(json_data))
        f2.write(json.dumps(Management_data)
        f1.close()
        f2.close()

try:
    json_data
    print "<div class='scr'>"
    print "<dl>"
    for each in cur.fetchall():
        print "<div id='MessageBgcolor'>"
        if each['UNIQUEID'] == EditID:
            print '''
                <form method="POST" action="./pyboard.cgi" target="pyboard">
                <table>
                <tr>
                <td><b>記入者の名前:</b></td>
                <td><input type="text" name=%(Registrant)s size="10"></td>
                <td><b>宛先:</b></td>
                <td><input type="text" name="Target" size="10" value=%(Target)s></td>
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
                '''%{'Registrant':each['Registrant'].encode('utf-8'),'Message':each['Message'].encode('utf-8'),'Target':each['Target'].encode('utf-8')}
        else:
            print message%{'ID':each['UNIQUEID'],'LocationID':each['LocationID'],'Registrant':each['Registrant'].encode('utf-8'),'Target':each['Target'].encode('utf-8'),'regdate':each['regdate'].encode('utf-8'),'Message':each['Message'].encode('utf-8'),'EditButton':"Edit"+str(each['UNIQUEID'])}
        print "</div>"
        print "</dl>"

finally:
    cur.close()
    con.close()
    print "</div></body></html>"
