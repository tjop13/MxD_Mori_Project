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

Tag = ""
Solve = ""

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
              width:750px;
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

            .menu{
              background-color: #32CD32;
              width:750px;
              height: 50px;
              margin: 0 auto;
            }
            .option{
            	float:left;
            	width:140px;
            	background-color: #FFE2B2;
            	height: 300px;
            }

            .main{
            	float:left;
            	width:600px;
                margin-left: 10px;
            	background-color: #D1F0FF;
            	height: 0px;
            }
            .clears{
              clear:both;
            }

        </style>

        </head>
        <body>
        <div class="option">


        '''

    form = cgi.FieldStorage()
    try:
        if form.has_key('Menu'):
            if form.getfirst('Menu','') == "Victim":
                print '''
                <form method="POST" action="pyboardMain.py" target="pyboardMain" >
                <br>
                    Tag:<br>
                <input type="radio" name="TAG" value="ALL" style-"margin-left: 5px;" id="TagALL" checked/>
                <label for="TagALL">ALL</label><br>
                <input type="radio" name="TAG" value="Rescue" style-"margin-left: 5px;" id="TagRescue"/>
                <label for="TagRescue">Rescue</label><br>
                <input type="radio" name="TAG" value="Goods" style-"margin-left: 5px;" id="TagGoods"/>
                <label for="TagGoods">Goods</label><br>
                    Soloved:<br>
                <input type="radio" name="SOLVE" value="ALL" style-"margin-left: 5px;" id="SolveALL" checked/>
                <label for="SolveALL">ALL</label><br>
                <input type="radio" name="SOLVE" value="Resolve" style-"margin-left: 5px;" id="SolveResolve"/>
                <label for="SolveResolve">Resolve</label><br>
                <input type="radio" name="SOLVE" value="Unsolved" style-"margin-left: 5px;" id="SolveUnsolved"/>
                <label for="SolveUnsolved">Unsolved</label><br><br>

                <button type="submit" style="margin-left: 5px; width: 90px; height: 30px;">変更</button>
                </form>
                </div>
                <div class="main">
                <iframe name="pyboardMain" width="100%" height="1000px" src="pyboardMain.py" frameborder="0" />
                '''
            if form.getfirst('Menu','') == "Patient":
                print '''
                <form method="POST" action="pyboard_Patient.py" target="pyboard_Patient" >
                <br>
                 トリアージ:<br>
                <input type="checkbox" name="TAGBlack" value="Black" style-"margin-left: 5px;" id="TagRescue"/>
                <label for="TagRescue">黒</label><br>
                <input type="checkbox" name="TAGRed" value="Red" style-"margin-left: 5px;" id="TagGoods"/>
                <label for="TagGoods">赤</label><br>
                <input type="checkbox" name="TAGYellow" value="Yellow" style-"margin-left: 5px;" id="TagGoods"/>
                <label for="TagGoods">黄</label><br>
                <input type="checkbox" name="TAGGreen" value="Green" style-"margin-left: 5px;" id="TagGoods"/>
                <label for="TagGoods">緑</label><br>
                 Soloved:<br>
                <input type="checkbox" name="Resolve" value="Resolve" style-"margin-left: 5px;" id="SolveResolve"/>
                <label for="SolveResolve">Resolve</label><br>
                <input type="checkbox" name="Unsolved" value="Unsolved" style-"margin-left: 5px;" id="SolveUnsolved"/>
                <label for="SolveUnsolved">Unsolved</label><br><br>

                <button type="submit" style="margin-left: 5px; width: 90px; height: 30px;">変更</button>
                </form>
                </div>
                <div class="main">
                <iframe name="pyboard_Patient" width="100%" height="1000px" src="pyboard_Patient.py" frameborder="0" />
                '''
            elif form.getfirst('Menu','') == "Chronology":
                print '''
                <form method="POST" action="pyboard_Chronology.py" target="pyboard_Chronology" id="Location">
                <br>
                    記入者検索:<br>
                <input type="text" name="name" size="13" value=""><br>
                    場所ID:<br>
                <select name="location" form="Location">
                <option value="1">1</option>
                <option value="2">2</option>
                <option value="3">3</option>
                </select><br>
                    タグ:<br>
                <input type="checkbox" name="TAGInfo_Shelter" value="Info_Shelter" style-"margin-left: 5px;" id="Info_Shelter"/>
                <label for="Info_Shelter">救護所情報</label><br>
                <input type="checkbox" name="TAGEdit_Patient" value="Edit_Patient" style-"margin-left: 5px;" id="Edit_Patient"/>
                <label for="Edit_Patient">傷病者情報編集</label><br>


                 <button type="submit" style="margin-left: 5px; width: 90px; height: 30px;">変更</button>
                </form>
                </div>
                <div class="main">
                <iframe name="pyboard_Chronology" width="100%" height="1000px" src="pyboard_Chronology.py" frameborder="0" />
                '''
            elif form.getfirst('Menu','') == "Instraction":
                print '''
                <form method="POST" action="pyboard_Instraction.py" target="pyboard_Instraction" id=Location>
                <br>
                    記入者検索:<br>
                <input type="text" name="name" size="13" value=""><br>
                    場所ID:<br>
                <select name="location" form="Location">
                <option value="1">1</option>
                <option value="2">2</option>
                <option value="3">3</option>
                </select><br>
                    宛先検索:<br>
                <input type="text" name="target" size="13" value="">

                <button type="submit" style="margin-left: 5px; width: 90px; height: 30px;">変更</button>
                </form>
                </div>
                <div class="main">
                <br>
                <form method="POST" action="http://localhost:8080/cgi-bin/pyboard_Instraction.py" target="pyboard_Instraction">
                  <table>
                    <tr>
                    <td><b>記入者の名前:</b></td>
                    <td><input type="text" name="Registrant" size="10" value="田中"></td>
                    <td><b>宛先:</b></td>
                    <td><input type="text" name="Target" size="10" value="救助隊A"></td>
                    </tr>
                  </table>
                <table>
                  <tr>
                  <td><b>内容:</b>
                  <textarea cols="50" rows="5" name="Message" >救助隊Aは救護所2へ移動</textarea></td>
                  </tr>
                  <tr>
                  <td colspan="2"><input type="submit" name="send" value="Send"><input type="reset" value="Reset"></td>
                  </tr>
                </table>
                </form>
                <iframe name="pyboard_Instraction" width="100%" height="500px" src="pyboard_Instraction.py" frameborder="0" />
                '''
        else:
            print '''
            <form method="POST" action="pyboard_Chronology.py" target="pyboard_Chronology" >
            <br>
                Location:<br>
            <input type="radio" name="Location" value="ALL" style-"margin-left: 5px;" id="TagALL" checked/>
            <label for="TagALL">ALL</label><br>
            <input type="radio" name="Location" value="Kyoto" style-"margin-left: 5px;" id="Kyoto"/>
            <label for="Kyoto">Kyoto</label><br>
            <input type="radio" name="Location" value="Osaka" style-"margin-left: 5px;" id="Osaka"/>
            <label for="Osaka">Osaka</label><br>
            <input type="radio" name="Location" value="Shiga" style-"margin-left: 5px;" id="Shiga"/>
            <label for="Shiga">Shiga</label><br>

            <button type="submit" style="margin-left: 5px; width: 90px; height: 30px;">変更</button>
            </form>
            </div>
            <div class="main">
            <iframe name="pyboard_Chronology" width="100%" height="1000px" src="pyboard_Chronology.py" frameborder="0" />
            '''

    finally:
        print "</body></html>"


if __name__=='__main__':
    PyBoard()
