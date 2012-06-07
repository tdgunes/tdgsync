#!/usr/bin/env python
#-*- coding:utf-8 -*-
#
# Author: Taha Doğan Güneş
# Licensed under the GNU General Public License, version 3.
# See the file http://www.gnu.org/copyleft/gpl.txt
#
# For increasing or decreasing photos exif create date to given difference time.
#
# Dependencies:
#     tweepy
#     psutil
#
# Usage:
#     python sync.py configfile
#
# Example:
#     python sync.py /home/example/sync.config
#

# Standart Library
 
from ftplib import FTP
import os
import random
import traceback
import sys
import argparse
import datetime
import httplib2
import platform
import cStringIO

# Sync Library

import functions
import reader
import constants

# 3rd Party Library

class api:  #configfile path will be getted with argparse(not ready)
    def __init__(self, configfile):
        """
        readers configfile automatically and defines the values
        
        Example:
        
        mySyncObject = sync.api("/example/configfile")


        it stores ip in /var/log/tdgsync.log
        
        """
        self.configfile = configfile #configuration file
        self.hostname = reader.getHostName(configfile) #ftp hostname
        self.login = reader.getFTPLoginName(configfile) #ftp login name
        self.password = reader.ftpPassword(configfile) #ftp password
        self.filepath = reader.ftpFilePath(configfile) #ftp upload path
        self.filename = reader.htmlPageName(configfile) #ftp upload file
        #twitter api keys for tdgserver
        tckey = reader.twitterAppKeys(configfile)[0] 
        tcsecret = reader.twitterAppKeys(configfile)[1]
        #these are from user
        tatkey = reader.twitterUserKeys(configfile)[0]
        tatsecret = reader.twitterUserKeys(configfile)[1]
        
        self.tweet = reader.twitter(configfile) #comes boolean
        
        self.version = constants.VERSION

        self.limitTime =  reader.getCallTimes(configfile) # how many run times left until utility message can be called 
  

        self.dynamicmessage = reader.getDynamicMessage(configfile)
        self.startmessage = reader.getStartMessage(configfile)


        if self.tweet: #If you don't want twitter support
            self.tweetApi = functions.authorizeTwitter(tckey,tcsecret,tatkey,tatsecret)

    def logIP(self, newip):
        #clean first
        runtime = 0
        if os.path.exists(constants.LOGFILE):
            runtime = int(reader.getCallTimes(constants.LOGFILE))
            reader.deleteFile(constants.LOGFILE)
        else:
            runtime = 0

        draft = ""
        draft += "currentip=" + str(newip) +"\n"
        draft += "calltimes=" + str(runtime+1) 
        
        reader.writeEngine(draft, constants.LOGFILE)

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
    def sendIPviaFTP(self, ip):
        
        #making output
        htmldraft =reader.getHTMLString(self.configfile)
        output = cStringIO.StringIO(functions.fillString(htmldraft,ip))

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
        if os.path.exists(constants.LOGFILE): 
            return False
        else:
            return True


    def isIPChanged(self,newip):
       
        logip = reader.readEngine("currentip",constants.LOGFILE,1)
        if newip != logip:
            return True
        else:
            return False
            
    def aRandomMessage(self,ip):
        randomsentence = random.choice(reader.getSentencesLines(self.configfile))
        randomsentence = functions.fillString(randomsentence,ip)
        return randomsentence

    def startAll(self):
        """
            1. sync.api gets this computers ip address (ipv4)
            2. checks if it is a first start of script (if there is not a /var/log/tdgsync.log)
            3. cron calls with its defined interval, sync.api and sync.api checks if its ip changed.
            4. - if changed, it sends current ip address to a defined ftp server and sends a tweet
            5. and stores new ip address to /var/log/tdgsync.log, waits for another cron call
           

            This makes just a one http request to get ip address to minimize internet activity
        """
        myip = self.getIP()   
   
        if self.isFirstStart():#First start of the service checks whether there is a /var/log/tdgsync.log or not
            self.printLog(functions.fillString(self.startmessage))
            self.printLog(self.aRandomMessage(myip))
            self.sendIPviaFTP(myip)
        else:
            if self.isIPChanged(myip):
                self.sendIPviaFTP(myip)
                self.printLog(functions.fillString(self.dynamicmessage))
            else:
                pass

            if reader.getCallTimes(constants.LOGFILE)==self.limitTime: #this is for sending a random message 
                self.printLog(self.aRandomMessage(myip))
                reader.replaceEngine("calltimes","0",constants.LOGFILE)


        self.logIP(myip)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="tdgsync tracks your ip changes and informs you if anything changes")

    parser.add_argument("configfile", help="path of sync.config file",
                        type=str)
    args = parser.parse_args()
    mySync = api(args.configfile)
    mySync.startAll() #makes everything :)


