#!usr/bin/env python
#-*- coding:utf-8 -*-

# Taha Dogan Gunes
# tdgunes@gmail.com	
# My ultimate test server solution!
# Requirements: python-twitter
# tdgunes.org/sync
# Needs lm_sensors!
# GPLv3

from ftplib import FTP
import os,time,getpass,random,traceback
import datetime,httplib2,platform
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
    print """Warning - If you want to send, track your servers status,\n
             (like cpu usage, memory, disks etc.) You need to install\n
             psutil from "http://code.google.com/p/psutil/"""

hostname = 'ftp.tdgunes.org'
login = 'tdgunes'
password = getpass.getpass("FTP password: ")
version = "0.3"
interval = 75  #seconds
filepath = "/httpdocs/server/" #which directory your file will be stored
filename = "index.html" #file that you want to store 
currentip = "currentip" #dont edit this no need to
#twitter things
tckey = "xwJ9dBEZ1jUgRpnYCM7Xfg"
tcsecret = "IwZju6BuRJTPQLUuWhmSJ2atoc1EmIrSlUyLQfAGI"
tatkey = "" #secret you need authorize and get token key and secret 
tatsecret = ""  # secret 
#oldmessage ="" #in order to not send that same message again

if raw_input("Do you want to send service messages to Twitter(y/n): ") == "n":
    tweet= False

if tweet: #if you think it is secure to store your password in this script, go on! :-)
    #tweetpass = getpass.getpass("Twitter password: ") 
    auth = tweepy.OAuthHandler(tckey, tcsecret)
    auth.set_access_token(tatkey, tatsecret)
    api = tweepy.API(auth)


#TDG's Small Essential Library (TDG-SEL) :)
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
           #log = "("+getDate()+") "+log
           print log
def sendTweet(message):
    api.update_status(message)
 


def getIP(): #TDG mini IP Service
    try:
        h = httplib2.Http('.cache')
        resp, content = h.request('http://tdgunes.org/getip/','GET')
        return content.strip()
    except:
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
         
      </tr>
    <tr>
      <td>Minecraft</td>
      <td>%s:25565</td>
      <td>25565</td>
    </tr>
    
    <tr>
     <td>Urban Terror</td>
      <td>%s:27960</td>
      <td>27960</td>


    </tr>

    <tr>
     <td>VPN Server</td>
      <td>%s:1723</td>
      <td>1723</td>


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
    </body></html>""" % (ip, ip, date, str(interval), ip,ip,ip, version, platform.platform())
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
            
currentip = getIP()
printLog("TDG Server is Online! sync:%s ip:%s" % (version,currentip))
printLog("Hate being rebooted... :(")
while True: #Normal loop
   # print "- Looper OK"
    
    # Just print when ip changes
    ip = getIP()
    if currentip != ip:
       if printLog("I hate being dynamic! But it is my nature:%s " % ip):
           currentip = ip
    
    if random.randint(1,20) == 1:
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

