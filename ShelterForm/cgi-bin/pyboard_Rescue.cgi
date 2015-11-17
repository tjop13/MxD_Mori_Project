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
    <style>
        body{
          background-color: #FFEEDC;

        }

        .option{
          float:left;
          width:140px;
          background-color: #6699BB;
          height: 400px;
        }

        .main{
          float:left;
          overflow: scroll;
          width: 600px;
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
      <div class="option">

      '''

form = cgi.FieldStorage()
try:
    if form.has_key('Menu'):
        if form.getfirst('Menu','') == "Patient":
            print '''
                <form method="POST" action="http://192.168.42.1:8000/cgi-bin/pyboard_Patient.cgi" target="pyboard_Patient" >
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
              <form method="POST" action="http://192.168.42.1:8000/cgi-bin/pyboard_Patient.cgi" target="pyboard_Patient">
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
                <iframe name="pyboard_Patient" src="http://192.168.42.1:8000/cgi-bin/pyboard_Patient.cgi" width="100%" height="70%" frameborder="0" />
              </div>
            </div>
            '''
        elif form.getfirst('Menu','') == "Chronology":
            print '''
                  <form method="POST" action="http://192.168.42.1:8000/cgi-bin/pyboard_chronology.cgi" target="pyboard_chronology" id="Location">
                    <br>
                        記入者検索:<br>
                    <input type="text" name="name" size="13" value="">
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

                <form method="POST" action="http://192.168.42.1:8000/cgi-bin/pyboard_chronology.cgi" target="pyboard_chronology">
                  <table>
                    <tr>
                    <td><b>記入者の名前:</b></td>
                    <td><input type="text" name="Registrant" size="10"></td>
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
                <div class="main">
                  <iframe name="pyboard_chronology" src="http://192.168.42.1:8000/cgi-bin/pyboard_chronology.cgi" width="100%" height="70%" frameborder="0" />
                </div>
              </div>
              '''
        elif form.getfirst('Menu','') == "Instraction":
          print '''
                <form method="POST" action="http://192.168.42.1:8000/cgi-bin/pyboard_Instraction.cgi" target="pyboard_Instraction" >
                  <br>
                      記入者検索:<br>
                  <input type="text" name="name" size="13" value="">
                      <br>宛先検索:<br>
                  <input type="text" name="target" size="13" value="">

                  <button type="submit" style="margin-left: 5px; width: 90px; height: 30px;">変更</button>
                </form>
              </div>

              <form method="POST" action="http://192.168.42.1:8000/cgi-bin/pyboard_Instraction.cgi" target="pyboard_Instraction">
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
              <div class="main">
                <iframe name="pyboard_Instraction" src="http://192.168.42.1:8000/cgi-bin/pyboard_Instraction.cgi" width="100%" height="70%" frameborder="0" />
              </div>
            </div>
            '''
    else:
        print '''
            <form method="POST" action="http://192.168.42.1:8000/cgi-bin/pyboard_Patient.cgi" target="pyboard_Patient" >
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
          <form method="POST" action="http://192.168.42.1:8000/cgi-bin/pyboard_Patient.cgi" target="pyboard_Patient">
            <table>
              <tr>
              <td><b>記入者の名前:</b></td>
              <td><input type="text" name="Registrant" size="10"></td>
              </tr>
                </table>
                <table width="600px">
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
            <iframe name="pyboard_Patient" src="http://192.168.42.1:8000/cgi-bin/pyboard_Patient.cgi" width="100%" height="70%" frameborder="0" />
          </div>
        </div>
        '''
finally:
    print "</body></html>"
