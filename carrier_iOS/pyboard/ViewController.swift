//
//  ViewController.swift
//  ConnectionClasses003
//

import UIKit
import SystemConfiguration.CaptiveNetwork

let useClosures = false

class ViewController: UIViewController,NSURLSessionDelegate,NSURLSessionDataDelegate, UITextFieldDelegate{
    
    var myTextView: UITextView!
//    var SendIPAddress: UITextField!
//    var RecieveIPAddress: UITextField!
    var mySession:NSURLSession!
    var RecieveFlag:Bool = false
    var SendFlag:Bool = false
    var RecieveIPAddress = ""
    var SendCount:Int = 0
    
    let reachability = Reachability.reachabilityForLocalWiFi()
    let InternetConnection = Reachability.reachabilityForInternetConnection()
    //インターネットに接続した際は、サーバにそのままポストする
    //InternetConnectionでインターネットの有無をWifiChangeの時に確認する。
    //ネットワーク名は、jsonで保管
    
    override func viewDidLoad() {
        super.viewDidLoad()
        
        self.view.backgroundColor = UIColor.lightGrayColor()
        
        // 表示用のTextViewを用意.
        myTextView = UITextView(frame: CGRectMake(10, 30, self.view.frame.width - 20, 520))
        
        myTextView.backgroundColor = UIColor(red: 0.9, green: 0.9, blue: 1, alpha: 1.0)
        myTextView.layer.masksToBounds = true
        myTextView.layer.cornerRadius = 20.0
        myTextView.layer.borderWidth = 1
        myTextView.layer.borderColor = UIColor.blackColor().CGColor
        myTextView.font = UIFont.systemFontOfSize(CGFloat(20))
        myTextView.textColor = UIColor.blackColor()
        myTextView.textAlignment = NSTextAlignment.Left
        myTextView.dataDetectorTypes = UIDataDetectorTypes.All
        myTextView.layer.shadowOpacity = 0.5
        myTextView.layer.masksToBounds = false
        myTextView.editable = false
        
        self.view.addSubview(myTextView)
        
//        RecieveIPAddress = UITextField(frame: CGRectMake(10, 60, self.view.frame.width-100, 30))
//        RecieveIPAddress.delegate = self
//        RecieveIPAddress.borderStyle = .RoundedRect
//        self.view.addSubview(RecieveIPAddress)
//        
//        SendIPAddress = UITextField(frame: CGRectMake(10, 100, self.view.frame.width-100, 30))
//        SendIPAddress.delegate = self
//        SendIPAddress.borderStyle = .RoundedRect
//        self.view.addSubview(SendIPAddress)
        
        // 通信用のConfigを生成.
        let myConfig:NSURLSessionConfiguration = NSURLSessionConfiguration.backgroundSessionConfigurationWithIdentifier("backgroundTask")
        // Sessionを生成.
        mySession = NSURLSession(configuration: myConfig, delegate: self, delegateQueue: nil)
        
        //connectR()
        
        var Recievebutton = UIButton(frame: CGRectMake(50, 460, 100, 30))
        Recievebutton.setTitle("本部受信", forState: .Normal)
        Recievebutton.backgroundColor = UIColor.blackColor()
        Recievebutton.addTarget(self, action: "Recievebutton:", forControlEvents: .TouchUpInside)
        Recievebutton.tag = 2
        self.view.addSubview(Recievebutton)

        var SendButton = UIButton(frame: CGRectMake(50, 500, 100, 30))
        SendButton.setTitle("本部送信", forState: .Normal)
        SendButton.backgroundColor = UIColor.blackColor()
        SendButton.addTarget(self, action: "SendButton:", forControlEvents: .TouchUpInside)
        SendButton.tag = 2
        self.view.addSubview(SendButton)
     
        var Recievebutton2 = UIButton(frame: CGRectMake(170, 460, 100, 30))
        Recievebutton2.setTitle("避難所受信", forState: .Normal)
        Recievebutton2.backgroundColor = UIColor.blackColor()
        Recievebutton2.addTarget(self, action: "Recievebutton:", forControlEvents: .TouchUpInside)
        Recievebutton2.tag = 3
        self.view.addSubview(Recievebutton2)
        
        var SendButton2 = UIButton(frame: CGRectMake(170, 500, 100, 30))
        SendButton2.setTitle("避難所送信", forState: .Normal)
        SendButton2.backgroundColor = UIColor.blackColor()
        SendButton2.addTarget(self, action: "SendButton:", forControlEvents: .TouchUpInside)
        SendButton2.tag = 3
        self.view.addSubview(SendButton2)
        
        if (useClosures) {
            reachability.whenReachable = { reachability in
                self.Reachable(reachability)
            }
            reachability.whenUnreachable = { reachability in
                self.NotReachable(reachability)
            }
        } else {
            NSNotificationCenter.defaultCenter().addObserver(self, selector: "reachabilityChanged:", name: ReachabilityChangedNotification, object: reachability)
        }
        
        reachability.startNotifier()
        
        // Initial reachability check
        if reachability.isReachable() {
            Reachable(reachability)
        } else {
            NotReachable(reachability)
        }
        
//        DBfunction(myData)
    }
    
    deinit{
        reachability.stopNotifier()
        
        if (!useClosures) {
            NSNotificationCenter.defaultCenter().removeObserver(self, name: ReachabilityChangedNotification, object: nil)
        }
    }
    
    
    func textFieldShouldReturn(textField: UITextField) -> Bool {
        textField.resignFirstResponder()
        
        
        return true
    }
    
    func Recievebutton(sender:UIButton){
        println("ReciveButton")
        if sender.tag == 2{
            RecieveIPAddress = "localhost:8080/cgi-bin"
        }else if sender.tag == 3{
            RecieveIPAddress = "localhost:8000/cgi-bin"
        }
        connectR(RecieveIPAddress)
    }
    
    func SendButton(sender:UIButton){
        println("SendButton")
        var SendIPAddress = ""
        if sender.tag == 2{
            SendIPAddress = "localhost:8080/cgi-bin"
        }else if sender.tag == 3{
            SendIPAddress = "localhost:8000/cgi-bin"
        }
        connectS(SendIPAddress)
    }
    
    /*
    通信が終了したときに呼び出されるデリゲート.
    */
    func URLSession(session: NSURLSession, dataTask: NSURLSessionDataTask, didReceiveData data: NSData) {
        println("NSURLSessionDataTask")
        
        // 帰ってきたデータを文字列に変換.
        var myData:NSString = NSString(data: data, encoding: NSUTF8StringEncoding)!
        
        
//        var textData = myData as String
        if self.RecieveFlag {
            let paths1 = NSSearchPathForDirectoriesInDomains(.DocumentDirectory, .UserDomainMask, true)
            let _path = paths1[0].stringByAppendingPathComponent("data.txt")
            
            let success = myData.writeToFile(_path, atomically: true, encoding: NSUTF8StringEncoding, error: nil)
            if success {
                println("保存に成功")
            }
        }
        println(myData)
//            var tmpData = myData.componentsSeparatedByString(" $& ")
////            print(tmpData)
//            textData = ""
//            for i in 0..<(tmpData.count/9){
//                textData += (tmpData[0+i*9] as! String)+":"+(tmpData[3+i*9] as! String)+"\n Location:"
//                textData += (tmpData[2+i*9] as! String)+",Tag:"+(tmpData[1+i*9] as! String)+"\n"
//                textData += (tmpData[5+i*9] as! String)+"\n Date:"+(tmpData[4+i*9] as! String)+"\n\n"
//            }
//        }
        // バックグラウンドだとUIの処理が出来ないので、メインスレッドでUIの処理を行わせる.
        dispatch_async(dispatch_get_main_queue(), {
            self.myTextView.text = "OK"
//            println(self.SendFlag)
//            println(self.SendCount)
            if self.RecieveFlag {
                
//                self.DBfunction(myData)
                self.RecieveFlag = false
            }
            if self.SendFlag{
                if self.SendCount == 0 {
//                    self.connectR(self.RecieveIPAddress)
                    self.SendFlag = false
                }else{
                    self.SendCount -= 1
                }
            }
        })
        
    }
    /*
    バックグラウンドからフォアグラウンドの復帰時に呼び出されるデリゲート.
    */
    func URLSessionDidFinishEventsForBackgroundURLSession(session: NSURLSession) {
        //println("URLSessionDidFinishEventsForBackgroundURLSession")
    }
    override func didReceiveMemoryWarning() {
        super.didReceiveMemoryWarning()
    }
    
    func connectR(RecieveIPAddress:String){
        RecieveFlag = true

        println("connectR")
        
        // 通信先のURLを生成.
        if RecieveIPAddress == "" {
            println("Not Input")
            return
        }
//        let Address = "localhost:8000/cgi-bin"
        
        var URL:String! = "http://" + RecieveIPAddress + "/SendDB.py"
//        URL = "http://localhost:8080/cgi-bin/SendDB.py"
        
        var myUrl:NSURL = NSURL(string: URL)!
        
        // タスクの生成.
        var myTask:NSURLSessionDataTask = mySession.dataTaskWithURL(myUrl)
        // タスクの実行.
        myTask.resume()
    }
    
    func connectS(SendIPAddress:String){

        
        println("connectS")
        SendFlag = true
        
        // 通信先のURLを生成.
        if SendIPAddress == "" {
            println("Not Input")
            return
        }
        
//        let Address = "localhost:8000/cgi-bin"
        
        var URL:String = "http://" + SendIPAddress + "/ReceveDB.py"
//        URL = "http://localhost:8080/cgi-bin/ReceveDB.py"
        
//        println(URL)
        
        let myUrl:NSURL = NSURL(string: URL)!
        
        // POST用のリクエストを生成.
        let myRequest:NSMutableURLRequest = NSMutableURLRequest(URL: myUrl)
        // POSTのメソッドを指定.
        myRequest.HTTPMethod = "POST"
        
        let paths1 = NSSearchPathForDirectoriesInDomains(.DocumentDirectory, .UserDomainMask, true)
        let _path = paths1[0].stringByAppendingPathComponent("data.txt")
        
        let PostData = NSString(contentsOfFile: _path, encoding: NSUTF8StringEncoding, error: nil)!
        
        println(PostData)
        
        var tmpData = PostData.componentsSeparatedByString("$#&")

        var SendDatacount = 0
        for data in tmpData{
            var FinData = data.componentsSeparatedByString(" $& ")
            if SendDatacount == 0{
                for i in 0..<(FinData.count/13){
                    var str = "ID=\(FinData[0+i*13])&LocationID=\(FinData[1+i*13])&Registrant=\(FinData[2+i*13])&Class=Patient&regdate=\(FinData[3+i*13])&Patient_Name=\(FinData[4+i*13])&Patient_Age=\(FinData[5+i*13])&Patient_Gender=\(FinData[6+i*13])"
                    
                    str += "&Patient_Triage=\(FinData[7+i*13])&Patient_Injuries_Diseases=\(FinData[8+i*13])&Patient_Treatment=\(FinData[9+i*13])&Patient_Hospital=\(FinData[10+i*13])&comment=\(FinData[11+i*13])&SolvedFlag=\(FinData[12+i*13])"
                    println(str)

                    let myData:NSData = str.dataUsingEncoding(NSUTF8StringEncoding)!
                    myRequest.HTTPBody = myData
        
                    // タスクの生成.
                    let myTask:NSURLSessionDataTask = mySession.dataTaskWithRequest(myRequest)
                    // タスクの実行.
                    myTask.resume()
                }

            }else if SendDatacount == 1{
                for i in 0..<(FinData.count/6){
                    var str = "ID=\(FinData[0+i*6])&LocationID=\(FinData[1+i*6])&Registrant=\(FinData[2+i*6])&Class=Chronology&regdate=\(FinData[3+i*6])&Message=\(FinData[4+i*6])&Tag=\(FinData[5+i*6])" as NSString
                    println(str)
                    let myData:NSData = str.dataUsingEncoding(NSUTF8StringEncoding)!
                    myRequest.HTTPBody = myData
                    
                    // タスクの生成.
                    let myTask:NSURLSessionDataTask = mySession.dataTaskWithRequest(myRequest)
                    // タスクの実行.
                    myTask.resume()
                }
            }else if SendDatacount == 2{
                for i in 0..<(FinData.count/9){
                    var str = "ID=\(FinData[0+i*9])&LocationID=\(FinData[1+i*9])&Registrant=\(FinData[2+i*9])&Class=Instraction&Target=\(FinData[3+i*9])&regdate=\(FinData[4+i*9])&Message=\(FinData[5+i*9])&SolvedFlag=\(FinData[6+i*9])&Replyname=\(FinData[7+i*9])&Replycomment=\(FinData[8+i*9])" as NSString
                    println(str)
                    let myData:NSData = str.dataUsingEncoding(NSUTF8StringEncoding)!
                    myRequest.HTTPBody = myData
                    
                    // タスクの生成.
                    let myTask:NSURLSessionDataTask = mySession.dataTaskWithRequest(myRequest)
                    // タスクの実行.
                    myTask.resume()
                }
            }else{
                for i in 0..<(FinData.count/9){
                    var str = "ID=\(FinData[0+i*9])&genre=\(FinData[1+i*9])&LocationID=\(FinData[2+i*9])&Class=Victor&name=\(FinData[3+i*9])&regdate=\(FinData[4+i*9])&comment=\(FinData[5+i*9])&SolvedFlag=\(FinData[6+i*9])&Replyname=\(FinData[7+i*9])&Replycomment=\(FinData[8+i*9])" as NSString
                    println(str)
                    let myData:NSData = str.dataUsingEncoding(NSUTF8StringEncoding)!
                    myRequest.HTTPBody = myData
                    
                    // タスクの生成.
                    let myTask:NSURLSessionDataTask = mySession.dataTaskWithRequest(myRequest)
                    // タスクの実行.
                    myTask.resume()
                }
            }
            SendDatacount++
        }
    }
    
//        if DBData.count == 0{
//            println("DBData.count=0")
////            let str:NSString = "ID=False"
////            let myData:NSData = str.dataUsingEncoding(NSUTF8StringEncoding)!
////            myRequest.HTTPBody = myData
////            
////            // タスクの生成.
////            let myTask:NSURLSessionDataTask = mySession.dataTaskWithRequest(myRequest)
////            // タスクの実行.
////            myTask.resume()
//            SendFlag = false
//            self.connectR(self.RecieveIPAddress)
//            
//            return
//        }
//        
//        SendCount = Int(DBData.count/9)-1
//        println(SendCount)
        
//        // 送信するデータを生成・リクエストにセット.
//        for i in 0..<(DBData.count/9){
//            let str:NSString = "ID=\(DBData[0+i*9])&genre=\(DBData[1+i*9])&LocationID=\(DBData[2+i*9])&name=\(DBData[3+i*9])&regdate=\(DBData[4+i*9])&comment=\(DBData[5+i*9])&SolvedFlag=\(DBData[6+i*9])&Replyname=\(DBData[7+i*9])&Replycomment=\(DBData[8+i*9])"
//            println(str)
//            let myData:NSData = str.dataUsingEncoding(NSUTF8StringEncoding)!
//            myRequest.HTTPBody = myData
//        
//            // タスクの生成.
//            let myTask:NSURLSessionDataTask = mySession.dataTaskWithRequest(myRequest)
//            // タスクの実行.
//            myTask.resume()
//        }
//    }
    
//    func DBfunction(myData:NSString){
//        //table作成
////        println("FUNCTION")
//        DBCREATE()
//        DBINSERT(myData)
//
//        DBSELECT()
//    }
//    
//    func DBCREATE(){
//        self.isExistsDataBase()
//        if let err = SD.createTable("testTable", withColumnNamesAndTypes: ["LocalID": .StringVal, "genre": .StringVal, "LocationID": .StringVal, "name": .StringVal,"regdate": .DateVal, "comment": .StringVal, "SolvedFlag": .StringVal, "ReplyName": .StringVal, "ReplyMessage": .StringVal]){
//            println(SwiftData.errorMessageForCode(err))
//            return
//        }
////        println("create")
//    }
//    
//    func isExistsDataBase() -> Bool{
//        let (tb, err) = SwiftData.existingTables();
//        if(!contains(tb, "testTable")){
//            return false;
//        }
//        else{
//            SD.deleteTable("testTable")
//            return true;
//        }
//    }
//    
//    func DBINSERT(myData:NSString){
//        //代入処理
//        var separators = NSCharacterSet(charactersInString: "\n")
//        var words = myData.componentsSeparatedByCharactersInSet(separators)
//        
//        for i in 0..<(words.count-2){
//            var RData = words[i+1].componentsSeparatedByString(" $& ")
////            println(RData)
//
//            let formatter:NSDateFormatter = NSDateFormatter()
//            formatter.dateFormat = "yyyy-MM-dd HH:mm:ss"
//            var time : NSDate = formatter.dateFromString(RData[4] as! String)!
//            
//            let Insql = "INSERT INTO testTable(LocalID, Genre, LocationID, name, regdate, comment, SolvedFlag, ReplyName, ReplyMessage) VALUES(?,?,?,?,?,?,?,?,?)"
//            if let err = SD.executeChange(Insql, withArgs: [RData[0],RData[1],RData[2],RData[3],time,RData[5],RData[6],RData[7],RData[8]]){
//                println("IN")
//                println(SwiftData.errorMessageForCode(err))
//                return
//            }
//            else{
//                println("OK INSERT")
//            }
//
//        }
//    }
//    
//    func DBSELECT() -> NSMutableArray{
//        //出力処理
//        let Outsql = "SELECT DISTINCT * FROM testTable"
//        let (resultSet, err) = SD.executeQuery(Outsql)
//        var DBData:NSMutableArray = []
//        
//        if err != nil {
//            println("OUT")
//            println(SwiftData.errorMessageForCode(err!))
//            return []
//        }else{
//            for row in resultSet{
////                var LocationID = row["LocationID"]!.asString()
////                var name = row["name"]!.asString()
////                var title = row["title"]!.asString()
//                var regdate = row["regdate"]!.asDate()
//                var date_formatter = NSDateFormatter()
//                date_formatter.dateFormat = "yyyy-MM-dd HH:mm:ss"
//                var time = date_formatter.stringFromDate(regdate!)
////                var comment = row["comment"]!.asString()
//                
//                DBData.addObject(row["LocalID"]!.asString()!)
//                DBData.addObject(row["genre"]!.asString()!)
//                DBData.addObject(row["LocationID"]!.asString()!)
//                DBData.addObject(row["name"]!.asString()!)
//                DBData.addObject(time)
//                DBData.addObject(row["comment"]!.asString()!)
//                DBData.addObject(row["SolvedFlag"]!.asString()!)
//                DBData.addObject(row["ReplyName"]!.asString()!)
//                DBData.addObject(row["ReplyMessage"]!.asString()!)
//            }
//            return DBData
//        }
//    }
    
    
    func Reachable(reachability: Reachability) {
//        if reachability.isReachableViaWiFi() {
//            self.networkStatus.textColor = UIColor.greenColor()
//        } else {
//            self.networkStatus.textColor = UIColor.blueColor()
//        }
        
        var SendIPAddress = ""
//        var RecieveIPAddress = ""
        
//        println(reachability.currentReachabilityString)
        var WIFIID:String = getSSID()
        if (WIFIID == "TMori"){
            RecieveIPAddress = "169.254.143.4:8080/cgi-bin"
            SendIPAddress = "169.254.143.4:8080/cgi-bin"
        }
        else if(WIFIID == "Tmori-asus"){
            RecieveIPAddress = "192.168.43.1:9997"
            SendIPAddress = "192.168.43.1:9996"
        }
        else if(WIFIID == "Pi_AP"){
            RecieveIPAddress = "192.168.42.1:8000/cgi-bin"
            SendIPAddress = "192.168.42.1:8000/cgi-bin"
        }
        else{
            return
        }
        
        
        connectS(SendIPAddress)

        //self.myTextView.text = reachability.currentReachabilityString
    }
    
    func NotReachable(reachability: Reachability) {
//        self.networkStatus.textColor = UIColor.redColor()
        
       // self.myTextView.text = reachability.currentReachabilityString
        myTextView.text = "NO Connection"
//        println("NO Connection")
    }
    
    
    func reachabilityChanged(note: NSNotification) {
        let reachability = note.object as! Reachability
        
//        println(reachability)
//        println("OKWIFI")
        
        if reachability.isReachable() {
            Reachable(reachability)
        } else {
            NotReachable(reachability)
        }
    }
    
    
    func getSSID()->String{
        let interfaces:CFArray! = CNCopySupportedInterfaces()?.takeUnretainedValue()
        if interfaces == nil { return "Not" }
//        println(interfaces)
        let if0:UnsafePointer<Void>? = CFArrayGetValueAtIndex(interfaces, 0)
        if if0 == nil { return "Not"}
//        println(if0)
        let interfaceName:CFStringRef = unsafeBitCast(if0!, CFStringRef.self)
        let dicRef:NSDictionary! = CNCopyCurrentNetworkInfo(interfaceName)?.takeUnretainedValue() as! NSDictionary
        if dicRef == nil { return "Not"}
//        println(dicRef)
        let ssidObj:AnyObject? = dicRef[kCNNetworkInfoKeySSID as! String]
        if ssidObj == nil { return "Not"}
        println(ssidObj!)
        return ssidObj as! String
    }
}