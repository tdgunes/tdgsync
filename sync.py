#!usr/bin/env python
#-*- coding:utf-8 -*-

# Taha Dogan Gunes
# tdgunes@gmail.com	
# My ultimate test server solution!
# Requirements: python-twitter
# tdgunes.org/sync
# needs lm_sensors!
from ftplib import FTP
import os,time,getpass,random,traceback,sys
import datetime,httplib2,platform,reader
try:
    import tweepy
    tweet = True
except ImportError:
    tweet = False
    print """Warning - If you want to post your server status to Twitter,\n
           please install "tweepy" package from your distro's package system!\n
           or "easy_install tweepy" is possible too.\n
           You may need to edit this script to add your twitter user name.\n
           It is best to follow instructions from where you have downloaded it."""
try:
    import psutil
    utility = True
except ImportError:
    utility = False
    print """Warning - "utility = False"
              If you want to send, track your servers status,\n
             (like cpu usage, memory, disks etc.) You need to install\n
             psutil from "http://code.google.com/p/psutil/"""

configfile = "/home/tdgunes/scripts/tdgsyncv2/sync.config"


#reader api

hostname = reader.getHostName(configfile)
login = reader.getFTPLoginName(configfile)
password = reader.ftpPassword(configfile)
interval = reader.getIntervalValue(configfile)  #seconds
filepath = reader.ftpFilePath(configfile) #which directory your file will be stored
filename = reader.htmlPageName(configfile) #file that you want to store 
tckey = reader.twitterAppKeys(configfile)[0]
tcsecret = reader.twitterAppKeys(configfile)[1]
tatkey = reader.twitterUserKeys(configfile)[0] #secret
tatsecret = reader.twitterUserKeys(configfile)[1] # secret 
tweet = reader.twitter(configfile)

#DEFAULTS
version = "0.3.4"
#oldmessage ="" #in order to not send that same message again
currentip = "currentip"

def authorizeTwitter(ckey,csecret,atkey,atsecret):
    auth = tweepy.OAuthHandler(ckey,csecret)
    auth.set_access_token(atkey,atsecret)
    return tweepy.API(auth)

if tweet and len(sys.argv)>1: 
    api = authorizeTwitter(tckey,tcsecret,tatkey,tatsecret)

#TDG's Small Essential Library (TDG-SEL)
def printLog(log):
    log = log+" ("+getDate()+") "
    if tweet:
       try:
           sendTweet(log)
           return True
       except:
           print "Error - Unable to send message to the Twitter!"
           traceback.print_exc()
           return False
       finally:
           print log


def sendTweet(message):
    api.update_status(message)   


def getIP(): #TDG mini IP Service
    try:
        h = httplib2.Http('.cache')
        resp, content = h.request('http://tdgunes.org/getip/','GET')
        return content.strip()
    except:
        traceback.print_exc()
        printLog("Error - Unknown! Unable get IP adress!")
        return "Error - Unknown! Unable get IP adress!"
def getDate():
    return str(datetime.datetime.now())[:-3]

def generateHTML(ip,date):    
    html = """<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org /TR/xhtml1/DTD/xhtml1-transitional.dtd"> 
<html xmlns="http://www.w3.org/1999/xhtml"> 
    
    <html><title>TDG Home Server!</title>
    <body>
    <div class="centered">
    <h1>TDG Home Server Gateway!</h2>
    <p>TDG Home Server's IP is: <a href="http://%s/">%s</a></p>
    <p>This page updated at: %s</br>
    All of the current game servers will be listed here.</br>
    This page is planned to be updated for every %s  seconds!</p>
    <h2>Game Server List</h2>
      <table border="1">
    <tr>
      <th>Game</th>
      <th>IP+Port</th>
      <th>Port</th>
      <th>Password</th>
         
      </tr>
    <tr>
      <td>Minecraft</td>
      <td>%s:25565</td>
      <td>25565</td>
      <td>None</td>
    </tr>
    
    <tr>
     <td>Urban Terror</td>
      <td>%s:27960</td>
      <td>27960</td>
      <td>None</td>

    </tr>

    <tr>
     <td>VPN Server</td>
      <td>%s</td>
      <td>None</td>
      <td>...</td>


    </tr> 
 
    <tr>
     <td>Garry's Mod(VAC Enabled)</td>
      <td>%s:27015</td>
      <td>27015</td>
      <td>tdgtdgtdg</td>


    </tr> 
 

      <tr>
        <td>...</td>
        <td>...</td>
        <td>...</td>
      </tr>
    </table>
    <p><b>This page is not saying that these servers are running!
    </br> I will tell you if they are online or not :)</b></p>
    </br>
    </div> 
    <i>sync.py - %s</i></br>
    <i>%s</i></br>
    <i>Taha Dogan Gunes - <a href="http://tdgunes.org">tdgunes.org</a></i>
    </body></html>""" % (ip, ip, date, str(interval), ip, ip,ip,ip, version, platform.platform())
    return html

def ftpBrowse(ftpObject, path):
    paths = path.split("/")
    for i in paths:
        ftpObject.cwd(i)

def utilityMessage(): #My server's emotions
    if utility:
        x = random.randint(1,17)
        if x == 1:
            printLog("Am I overloaded ? I got %s cpu(s) and my cpu usage is %s percent" % (str(psutil.NUM_CPUS),str(psutil.cpu_percent(interval=1))))
        elif x == 2:
            printLog("%s percent of my memories caught me. I need upgrade!" % str(psutil.phymem_usage().percent))
        elif x == 3:
            printLog("My admin says if I stop working, I may find myself in trash can.")
        elif x == 4:
            printLog("I am an old wise server, yay!")
        elif x == 5:
            printLog("My root password is ... you think I am so stupid, don't you?")
        elif x == 6: 
            printLog("My body fat percent is %s" % str(psutil.disk_usage('/').percent))
        elif x == 7:
            printLog("I sit here everyday and show you my ip number, am I crazy ?")
        elif x == 8:
            a = os.popen("sensors")
            b = "%s" % a.read()
            b =b.split("temp1:")[1]
            b =b.strip().split(" ")
            printLog("Somebody help, I am melting here. My temperature is %s" % b[0])
        elif x == 9:
            printLog("I really wanted to show you my game server services someday!")
        elif x == 10:
            printLog("Connecting to SkyNet...///")
            printLog("Scared? Just joking :)")
        elif x == 11:
            printLog("If a message is duplicated serveral times, remember I am not a HUMAN")
        elif x == 12:
            printLog("I am capable of destroying the whole universe but I don't want to")
        elif x == 13:
            printLog("There is a cat on me, go away cat I am just a old-tech server")
        elif x == 14:
            printLog("I can do lots of things. %s -> I generated a random number!" % str(random.randint(23,124124)))
        elif x == 15:
            printLog("Not having a desktop environment is killing me!")
        elif x == 16:
            printLog("UrT ip: %s:27960" % getIP())
        elif x == 17:
            printLog("My firewall is undefeatable!")
            


def serviceLoop(): #Normal loop
   # print "- Looper OK"
    
    # Just print when ip changes
    ip = getIP()
    if currentip != ip:
       if printLog("I hate being dynamic! But it is my nature:%s " % ip):
           currentip = ip
    
    if random.randint(1,20000) == 89:
        utilityMessage()


    f = open('index.html','w')
    f.write(generateHTML(ip,getDate()))
    f.close()
    try:
        ftp = FTP(hostname,login,password)
        ftpBrowse(ftp, filepath)
        ftp.storbinary('STOR %s' % filename, open(filename,'rb'))
        ftp.close()
    except:
        printLog("Error - FTP connection problem to the %s" % hostname)
    time.sleep(interval)

if len(sys.argv)>1:
    currentip = getIP()
    printLog("TDG Server is Online! sync: %s ip: %s" % (version,currentip))
    printLog("Aaaah my head hurts!")
    while True:
        ip = getIP()
        if currentip != ip:
            if printLog("I hate being dynamic! But it is my nature:%s " % ip):
                currentip = ip

        if random.randint(1,20000) == 89:
            utilityMessage()


        f = open('index.html','w')
        f.write(generateHTML(ip,getDate()))
        f.close()
        try:
            ftp = FTP(hostname,login,password)
            ftpBrowse(ftp, filepath)
            ftp.storbinary('STOR %s' % filename, open(filename,'rb'))
            ftp.close()
        except:
            printLog("Error - FTP connection problem to the %s" % hostname)
        time.sleep(interval)
    
