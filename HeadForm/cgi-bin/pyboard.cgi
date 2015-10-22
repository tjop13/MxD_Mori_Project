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
            	width:100px;
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
            if form.getfirst('Menu','') == "METHANE":
                print '''
                <form method="POST" action="pyboard_methane.py" target="pyboard_methane" >
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
                <iframe name="pyboard_methane" width="100%" height="1000px" src="pyboard_methane.py" frameborder="0" />
                '''
            elif form.getfirst('Menu','') == "EMIS":
                print '''
                <form method="POST" action="pyboard_emis.py" target="pyboard_emis" >
                <br>
                    Location:<br>
                <input type="radio" name="TAG" value="ALL" style-"margin-left: 5px;" id="TagALL" checked/>
                <label for="TagALL">ALL</label><br>
                <input type="radio" name="TAG" value="Rescue" style-"margin-left: 5px;" id="TagRescue"/>
                <label for="TagRescue">Rescue</label><br>
                <input type="radio" name="TAG" value="Goods" style-"margin-left: 5px;" id="TagGoods"/>
                <label for="TagGoods">Goods</label><br>

                <button type="submit" style="margin-left: 5px; width: 90px; height: 30px;">変更</button>
                </form>
                </div>
                <div class="main">
                <iframe name="pyboard_emis" width="100%" height="1000px" src="pyboard_emis.py" frameborder="0" />
                '''
        else:
            print '''
            <form method="POST" action="pyboard_methane.py" target="pyboard_methane" >
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
            <iframe name="pyboard_methane" width="100%" height="1000px" src="pyboard_methane.py" frameborder="0" />
            '''

    finally:
        print "</body></html>"


if __name__=='__main__':
    PyBoard()
