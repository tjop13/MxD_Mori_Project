//
//  ViewController.swift
//  ConnectionClasses003
//

import UIKit
import SystemConfiguration.CaptiveNetwork

let useClosures = false

class ViewController: UIViewController,NSURLSessionDelegate,NSURLSessionDataDelegate, UITextFieldDelegate{
    
    var myTextView: UITextView!
    var mySession:NSURLSession!
    var RecieveFlag:Bool = false
    var SendFlag:Bool = false
    var RecieveIPAddress = ""
    var SendIPAddress = ""
    var SendData = ""
    var SendCount:Int = 0
    
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
        
        // 通信用のConfigを生成.
        let myConfig:NSURLSessionConfiguration = NSURLSessionConfiguration.backgroundSessionConfigurationWithIdentifier("backgroundTask")
        
        // Sessionを生成.
        mySession = NSURLSession(configuration: myConfig, delegate: self, delegateQueue: nil)
        
        //connectR()
        
        let Recievebutton = UIButton(frame: CGRectMake(50, 430, 100, 30))
        Recievebutton.setTitle("本部受信", forState: .Normal)
        Recievebutton.setBackgroundImage(createImageFromUIColor(UIColor.blackColor()), forState: .Normal)
        Recievebutton.setBackgroundImage(createImageFromUIColor(UIColor.lightGrayColor()) , forState: .Highlighted)
        Recievebutton.addTarget(self, action: "Recievebutton:", forControlEvents: .TouchUpInside)
        Recievebutton.tag = 2
        self.view.addSubview(Recievebutton)

        let SendButton = UIButton(frame: CGRectMake(50, 470, 100, 30))
        SendButton.setTitle("本部送信", forState: .Normal)
        SendButton.setBackgroundImage(createImageFromUIColor(UIColor.blackColor()), forState: .Normal)
        SendButton.setBackgroundImage(createImageFromUIColor(UIColor.lightGrayColor()) , forState: .Highlighted)
        SendButton.addTarget(self, action: "SendButton:", forControlEvents: .TouchUpInside)
        SendButton.tag = 2
        self.view.addSubview(SendButton)
     
        let Recievebutton2 = UIButton(frame: CGRectMake(170, 430, 100, 30))
        Recievebutton2.setTitle("避難所受信", forState: .Normal)
        Recievebutton2.setBackgroundImage(createImageFromUIColor(UIColor.blackColor()), forState: .Normal)
        Recievebutton2.setBackgroundImage(createImageFromUIColor(UIColor.lightGrayColor()) , forState: .Highlighted)
        Recievebutton2.addTarget(self, action: "Recievebutton:", forControlEvents: .TouchUpInside)
        Recievebutton2.tag = 3
        self.view.addSubview(Recievebutton2)
        
        let SendButton2 = UIButton(frame: CGRectMake(170, 470, 100, 30))
        SendButton2.setTitle("避難所送信", forState: .Normal)
        SendButton2.setBackgroundImage(createImageFromUIColor(UIColor.blackColor()), forState: .Normal)
        SendButton2.setBackgroundImage(createImageFromUIColor(UIColor.lightGrayColor()) , forState: .Highlighted)
        SendButton2.addTarget(self, action: "SendButton:", forControlEvents: .TouchUpInside)
        SendButton2.tag = 3
        self.view.addSubview(SendButton2)
        
        let CheckButton = UIButton(frame: CGRectMake(self.view.frame.width/2-75 , 390, 150, 30))
        CheckButton.setTitle("ログデータ確認", forState: .Normal)
        CheckButton.setBackgroundImage(createImageFromUIColor(UIColor.blackColor()), forState: .Normal)
        CheckButton.setBackgroundImage(createImageFromUIColor(UIColor.lightGrayColor()) , forState: .Highlighted)
        CheckButton.addTarget(self, action: "CheckButton:", forControlEvents: .TouchUpInside)
        self.view.addSubview(CheckButton)
        
        let CancelButton = UIButton(frame: CGRectMake(self.view.frame.width/2-75 , 510, 150, 30))
        CancelButton.setTitle("送信中止", forState: .Normal)
        CancelButton.setBackgroundImage(createImageFromUIColor(UIColor.redColor()), forState: .Normal)
        CancelButton.setBackgroundImage(createImageFromUIColor(UIColor.lightGrayColor()) , forState: .Highlighted)
        CancelButton.addTarget(self, action: "CancelButton:", forControlEvents: .TouchUpInside)
        self.view.addSubview(CancelButton)
    }
    
    func textFieldShouldReturn(textField: UITextField) -> Bool {
        textField.resignFirstResponder()
        
        
        return true
    }
    
    func createImageFromUIColor(color:UIColor)->UIImage {
        let rect:CGRect = CGRectMake(0, 0, 1, 1)
        UIGraphicsBeginImageContext(rect.size);
        let contextRef:CGContextRef = UIGraphicsGetCurrentContext()!
        CGContextSetFillColorWithColor(contextRef, color.CGColor)
        CGContextFillRect(contextRef, rect);
        let img:UIImage = UIGraphicsGetImageFromCurrentImageContext()
        UIGraphicsEndImageContext();
        
        return img
    }
    
    
    
    func Recievebutton(sender:UIButton){
        print("ReciveButton")
        if sender.tag == 2{
            RecieveIPAddress = "169.254.215.88:8080/cgi-bin"
        }else if sender.tag == 3{
            RecieveIPAddress = "192.168.42.1:8000/cgi-bin"
        }
        connectR(RecieveIPAddress)
    }
    
    func SendButton(sender:UIButton){
        print("SendButton")
        if sender.tag == 2{
            SendIPAddress = "169.254.215.88:8080/cgi-bin"
        }else if sender.tag == 3{
            SendIPAddress = "192.168.42.1:8000/cgi-bin"
        }
        connectS(SendIPAddress)
    }
    
    func CancelButton(sender:UIButton){
        SVProgressHUD.showErrorWithStatus("転送中止しました")
    }
    
    func CheckButton(sender:UIButton){
        let paths1 = NSSearchPathForDirectoriesInDomains(.DocumentDirectory, .UserDomainMask, true)
        let _path = (paths1[0] as NSString).stringByAppendingPathComponent("Log.txt")
        var LogData:NSString? = ""
        do {
            LogData = try NSString(contentsOfFile: _path, encoding: NSUTF8StringEncoding)
        } catch {
            print("error")
        }
        myTextView.text = LogData! as String

    }
    

    
    /*
    通信が終了したときに呼び出されるデリゲート.
    */
    func URLSession(session: NSURLSession, dataTask: NSURLSessionDataTask, didReceiveData data: NSData) {
        
        // 帰ってきたデータを文字列に変換.
        let myData:NSString = NSString(data: data, encoding: NSUTF8StringEncoding)!
        let paths1 = NSSearchPathForDirectoriesInDomains(.DocumentDirectory, .UserDomainMask, true)
        
        let _path2 = (paths1[0] as NSString).stringByAppendingPathComponent("Log.txt")
        
        let now = NSDate()
        
        let formatter = NSDateFormatter()
        formatter.dateFormat = "yyyy/MM/dd HH:mm:ss"
        
        let nowtime = formatter.stringFromDate(now)
        var LogData : NSString? = ""
        
        do {
            LogData = try NSString(contentsOfFile: _path2, encoding: NSUTF8StringEncoding)
        } catch {
            print("error")
        }
        let inputData:NSString = (LogData as! String) + "Send:" + SendIPAddress + (nowtime as String) + "\n" + SendData
        do {
            try inputData.writeToFile(_path2, atomically: true, encoding: NSUTF8StringEncoding)
        } catch {
            print("error")
        }
        
        SendCount-=1
        
        print(myData)
        print(SendCount)
        
        if SendCount == 0{
            SVProgressHUD.showSuccessWithStatus("受信成功")
        }
        // バックグラウンドだとUIの処理が出来ないので、メインスレッドでUIの処理を行わせる.
        dispatch_async(dispatch_get_main_queue(), {
            self.myTextView.text = "OK"
            if self.RecieveFlag {
                self.RecieveFlag = false
            }
            if self.SendFlag{
                if self.SendCount == 0 {
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
        //print("URLSessionDidFinishEventsForBackgroundURLSession")
    }
    override func didReceiveMemoryWarning() {
        super.didReceiveMemoryWarning()
    }
    
    func connectR(RecieveIPAddress:String){
        RecieveFlag = true

        print("connectR")
        
        // 通信先のURLを生成.
        if RecieveIPAddress == "" {
            print("Not Input")
            return
        }
//        let Address = "localhost:8000/cgi-bin"
        
        let URL:String! = "http://" + RecieveIPAddress + "/SendDB.py"
//        let URL = "http://192.168.1.125:8000/cgi-bin/SendDB.py"
        
        print(URL)
        
        let myUrl:NSURL = NSURL(string: URL)!
        
//        // タスクの生成.
//        let myTask:NSURLSessionDataTask = mySession.dataTaskWithURL(myUrl)
//        // タスクの実行.
//        myTask.resume()
        // リクエストを生成.
        let myRequest:NSURLRequest  = NSURLRequest(URL: myUrl)
        SVProgressHUD.showWithStatus("受信中")
        // 送信処理を始める.
        NSURLConnection.sendAsynchronousRequest(myRequest, queue: NSOperationQueue.mainQueue(), completionHandler: self.getHttp)
    }
    
    func getHttp(res:NSURLResponse?,data:NSData?,error:NSError?){
        SVProgressHUD.showSuccessWithStatus("受信成功")
        // 帰ってきたデータを文字列に変換.
//        print(data)
        let paths1 = NSSearchPathForDirectoriesInDomains(.DocumentDirectory, .UserDomainMask, true)

        if (data != nil && RecieveFlag==true){
            let myData:NSString = NSString(data: data!, encoding: NSUTF8StringEncoding)!
            print(myData)
            
            let _path = (paths1[0] as NSString).stringByAppendingPathComponent("data.txt")
            
            do {
                try myData.writeToFile(_path, atomically: true, encoding: NSUTF8StringEncoding)
                print("受信OK")
            } catch {
                print("送信error")
            }
            RecieveFlag = false
        
            let _path2 = (paths1[0] as NSString).stringByAppendingPathComponent("Log.txt")
            
            let now = NSDate()
            
            let formatter = NSDateFormatter()
            formatter.dateFormat = "yyyy/MM/dd HH:mm:ss"
            
            let nowtime = formatter.stringFromDate(now)
            var LogData : NSString? = ""
            
            do {
                LogData = try NSString(contentsOfFile: _path2, encoding: NSUTF8StringEncoding)
            } catch {
                print("LogDataerror")
            }
            let inputData:NSString = (LogData as! String) +  "Recieve:" + RecieveIPAddress + (nowtime as String) + "\n" + (myData as String)
            do {
                try inputData.writeToFile(_path2, atomically: true, encoding: NSUTF8StringEncoding)
            } catch {
                print("LogDataerror")
            }
        }
        
    }
    
    func connectS(SendIPAddress:String){

        
        print("connectS")
        SendFlag = true
        SendData = ""
        SVProgressHUD.showWithStatus("送信中")
        
        // 通信先のURLを生成.
        if SendIPAddress == "" {
            print("Not Input")
            return
        }
        
        let URL:String = "http://" + SendIPAddress + "/ReceveDB.py"
//        URL = "http://localhost:8080/cgi-bin/ReceveDB.py"
        
        
        let myUrl:NSURL = NSURL(string: URL)!

        // POST用のリクエストを生成.
        let myRequest:NSMutableURLRequest = NSMutableURLRequest(URL: myUrl)

        // POSTのメソッドを指定.
        
        myRequest.HTTPMethod = "POST"
        
        
        let paths1 = NSSearchPathForDirectoriesInDomains(.DocumentDirectory, .UserDomainMask, true)
        let _path = (paths1[0]as NSString).stringByAppendingPathComponent("data.txt")
        
        let PostData: NSString?
        
        do {
            PostData = try NSString(contentsOfFile: _path, encoding: NSUTF8StringEncoding)
            print ("File OPEN")
            print(PostData)
        } catch {
            PostData = nil
            // failed to write file – bad permissions, bad filename, missing permissions, or more likely it can't be converted to the encoding
        }
        
        let tmpData = PostData!.componentsSeparatedByString("$#&")
        SendCount = tmpData.count - 1
        var SendDatacount = 0
        for data in tmpData{
            var FinData = data.componentsSeparatedByString(" $& ")
            if SendDatacount == 0{
                for i in 0..<(FinData.count/13){
                    var str = "ID=\(FinData[0+i*13])&LocationID=\(FinData[1+i*13])&Registrant=\(FinData[2+i*13])&Class=Patient&regdate=\(FinData[3+i*13])&Patient_Name=\(FinData[4+i*13])&Patient_Age=\(FinData[5+i*13])&Patient_Gender=\(FinData[6+i*13])"
                    
                    str += "&Patient_Triage=\(FinData[7+i*13])&Patient_Injuries_Diseases=\(FinData[8+i*13])&Patient_Treatment=\(FinData[9+i*13])&Patient_Hospital=\(FinData[10+i*13])&comment=\(FinData[11+i*13])&SolvedFlag=\(FinData[12+i*13])"
                    print(str)
                    SendData += (str as String) + "\n"

                    let myData:NSData = str.dataUsingEncoding(NSUTF8StringEncoding)!
                    myRequest.HTTPBody = myData
        
                    // タスクの生成.
                    let myTask:NSURLSessionDataTask = mySession.dataTaskWithRequest(myRequest)
                    // タスクの実行.
                    myTask.resume()
                }

            }else if SendDatacount == 1{
                for i in 0..<(FinData.count/6){
                    let str = "ID=\(FinData[0+i*6])&LocationID=\(FinData[1+i*6])&Registrant=\(FinData[2+i*6])&Class=Chronology&regdate=\(FinData[3+i*6])&Message=\(FinData[4+i*6])&Tag=\(FinData[5+i*6])" as NSString
                    print(str)
                    SendData += (str as String) + "\n"
                    
                    let myData:NSData = str.dataUsingEncoding(NSUTF8StringEncoding)!
                    myRequest.HTTPBody = myData
                    
                    // タスクの生成.
                    let myTask:NSURLSessionDataTask = mySession.dataTaskWithRequest(myRequest)
                    // タスクの実行.
                    myTask.resume()
                }
            }else if SendDatacount == 2{
                for i in 0..<(FinData.count/9){
                    var str = "ID=\(FinData[0+i*9])&LocationID=\(FinData[1+i*9])&Registrant=\(FinData[2+i*9])&Class=Instraction&Target=\(FinData[3+i*9])&regdate=\(FinData[4+i*9])"
                    str += "&Message=\(FinData[5+i*9])&SolvedFlag=\(FinData[6+i*9])&Replyname=\(FinData[7+i*9])&Replycomment=\(FinData[8+i*9])"
                    print(str)
                    SendData += (str as String) + "\n"
                    
                    let myData:NSData = str.dataUsingEncoding(NSUTF8StringEncoding)!
                    myRequest.HTTPBody = myData
                    
                    // タスクの生成.
                    let myTask:NSURLSessionDataTask = mySession.dataTaskWithRequest(myRequest)
                    // タスクの実行.
                    myTask.resume()
                }
            }else{
                for i in 0..<(FinData.count/9){
                    var str = "ID=\(FinData[0+i*9])&genre=\(FinData[1+i*9])&LocationID=\(FinData[2+i*9])&Class=Victor&name=\(FinData[3+i*9])&regdate=\(FinData[4+i*9])"
                    str += "&comment=\(FinData[5+i*9])&SolvedFlag=\(FinData[6+i*9])&Replyname=\(FinData[7+i*9])&Replycomment=\(FinData[8+i*9])"
                    print(str)
                    SendData += (str as String) + "\n"

                    
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

}