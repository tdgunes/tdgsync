#!usr/bin/env python
#-*- coding:utf-8 -*-

# Taha Dogan Gunes
# tdgunes@gmail.com	
# My ultimate test server solution!
# Requirements: python-twitter
# tdgunes.org/sync
# needs lm_sensors!

#FIXME needs a object-oriented sync.py for reader api connection 
# and for behaving as a library

from ftplib import FTP
import functions
import os,time,getpass,random,traceback,sys,argparse
import datetime,httplib2,platform,reader,cStringIO

#import constants
try:
    import tweepy
except ImportError:
    print """\nWarning - If you want to post your server status to Twitter,\n
           please install "tweepy" package from your distro's package system!\n
           or "easy_install tweepy" is possible too.\n
           You may need to edit this script to add your twitter user name.\n
           It is best to follow instructions from where you have downloaded it."""
try:
    import psutil
except ImportError:
    pass
    #more detailed information here FIXME

class api:  #configfile path will be getted with argparse(not ready)
    def __init__(self, configfile):
        """
        readers configfile automaticly and defines the values
        
        Example:
        
        mySyncObject = sync.api("/example/configfile")


        it stores ip in /var/log/tdgsync.log
        
        """
        self.configfile = configfile
        self.hostname = reader.getHostName(configfile)
        self.login = reader.getFTPLoginName(configfile)
        self.password = reader.ftpPassword(configfile)
        self.filepath = reader.ftpFilePath(configfile)
        self.filename = reader.htmlPageName(configfile)
        #twitter api keys
        tckey = reader.twitterAppKeys(configfile)[0]
        tcsecret = reader.twitterAppKeys(configfile)[1]
        #these are from user
        tatkey = reader.twitterUserKeys(configfile)[0]
        tatsecret = reader.twitterUserKeys(configfile)[1]
        #boolean
        self.tweet = reader.twitter(configfile)
        #version
        self.version = "0.4-beta"#constants.version
        self.limitTime =  reader.getCallTimes(configfile) # how many times script called 
  
        if self.tweet: #If you don't want twitter support
            self.tweetApi = functions.authorizeTwitter(tckey,tcsecret,tatkey,tatsecret)

    def logIP(self, newip):
        #clean first
        runtime = 0
        if os.path.exists("/var/log/tdgsync.log"):
            runtime = int(reader.getCallTimes("/var/log/tdgsync.log"))
            reader.deleteFile("/var/log/tdgsync.log")
        else:
            runtime = 0

        draft = ""
        draft += "currentip=" + str(newip) +"\n"
        draft += "calltimes=" + str(runtime+1) 
        
        reader.writeEngine(draft, "/var/log/tdgsync.log")

    def getIP(self):
        return functions.getIP() #functions getIP


    def sendTweet(self, message):
        self.tweetApi.update_status(message)   

    def printLog(self, log): #logs and tweets messages if tweet = True
        log +=" ("+functions.getDate()+") "
        if self.tweet:
            try:
                self.sendTweet(log)
                return True
            except:
                print "Error - Unable to send message to the Twitter!"
                traceback.print_exc()
                return False
            finally:
                print log
    def sendIPviaFTP(self):
        
        #making output
        output = cStringIO.StringIO(functions.fillAStringWithValues(reader.getHTMLString(self.configfile)))

        try:
            ftp = FTP(self.hostname,self.login,self.password)
            functions.ftpBrowse(ftp, self.filepath)
            ftp.storbinary('STOR %s' % self.filename.split("/")[-1], output)
            ftp.close()
            output.close()
        except:
            self.printLog("Error - FTP connection problem to the %s" % self.hostname)
            traceback.print_exc()


    def isFirstStart(self):
        if os.path.exists("/var/log/tdgsync.log"): 
            return False
        else:
            return True


    def isIPChanged(self,newip):
       
        logip = reader.readEngine("currentip","/var/log/tdgsync.log",1)
        if newip != logip:
            return True
        else:
            return False
            
    def aRandomMessage(self):
        randomsentence = random.choice(reader.getSentencesLines(self.configfile))
        randomsentence = functions.fillAStringWithValues(randomsentence)
        return randomsentence

    def startAll(self):
        """
            1. sync.api gets this computers ip address (ipv4)
            2. checks if it is a first start of script (if there is not a /var/log/tdgsync.log)
            3. cron calls with its defined interval, sync.api and sync.api checks if its ip changed.
            4. - if changed, it sends current ip address to a defined ftp server and sends a tweet
            5. and stores new ip address to /var/log/tdgsync.log, waits for another cron call
           


        """
        myip = self.getIP()   
   
        if self.isFirstStart():#First start of the service checks whether there is a /var/log/tdgsync.log or not
            self.printLog("TDG Server is Online! sync: %s ip: %s" % (self.version,self.currentip))
            self.printLog(self.aRandomMessage())
            self.sendIPviaFTP()
        else:
            if self.isIPChanged(myip):
                self.sendIPviaFTP()
                self.printLog("I hate being dynamic! But it is my nature: %s " % myip)
            else:
                pass

            if reader.getCallTimes("/var/log/tdgsync.log")==self.limitTime: #this is for sending a random message 
                self.printLog(self.aRandomMessage())
                reader.replaceEngine("calltimes","0","/var/log/tdgsync.log")


        self.logIP(myip)


# ========================================================================================
# ========================================================================================




# ==== Service Start ====

# Service Start and Loop Process

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="tdgsync tracks your ip changes and informs you if anything changes")

    parser.add_argument("configfile", help="path of sync.config file",
                        type=str)
    args = parser.parse_args()

    mySync = api(args.configfile)
    mySync.startAll() #makes everything :)


# ==== Service End ====
