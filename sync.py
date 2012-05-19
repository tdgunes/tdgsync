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
import os,time,getpass,random,traceback,sys
import datetime,httplib2,platform,reader,cStringIO
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
              If you want to send, track your serers status,\n
             (like cpu usage, memory, disks etc.) You need to install\n
             psutil from "http://code.google.com/p/psutil/"""

configfile = "/home/tdgunes/scripts/tdgsyncv3/sync.config"


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


# ========================================================================================

#TDG's Small Essential Library (TDG-SEL) :_P
def printLog(log): #logs and tweets messages if tweet = True
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


def getIP(): #TDG mini IP Service - works
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


def ftpBrowse(ftpObject, path): #more easy way to browse in ftp 
    paths = path.split("/")
    for i in paths:
        ftpObject.cwd(i)

def getTemperature(): # getting temperature from hard way
     a = os.popen("sensors")
     b = "%s" % a.read()
     b =b.split("temp1:")[1]
     b =b.strip().split(" ")
     return b[0].strip()

def fillAStringWithValues(mystring):
    # =ip= for getIP()
    # =cpunumber= for str(psutil.NUM_CPUS)
    # =cpupercent= for str(psutil.cpu_percent(interval=1))
    # =memory= for str(psutil.phymem_usage().percent)
    # =diskusage= for str(psutil.disk_usage('/').percent)
    # =temp= for getTemperature()
    # =random= for str(random.randint(23,124124))
    # =ip= for getIP()
    # =version= for version
    # =date= for getDate()
    # =interval= for interval
    # =platform= for platform.platform()

    mystring = mystring.replace("=ip=", getIP())
    mystring = mystring.replace("=cpunumber=",str(psutil.NUM_CPUS))
    mystring = mystring.replace("=cpupercent=", str(psutil.cpu_percent(interval=1)))
    mystring = mystring.replace("=memory=",  str(psutil.phymem_usage().percent))
    mystring = mystring.replace("=diskusage=",  str(psutil.disk_usage('/').percent))
    mystring = mystring.replace("=temp=", getTemperature())
    mystring = mystring.replace("=random=", str(random.randint(23,124124)))
    mystring = mystring.replace("=version=", version)
    mystring = mystring.replace("=date=",getDate())
    mystring = mystring.replace("=interval",str(interval))
    mystring = mystring.replace("=platform=", platfrom.platform())

    return mystring

def authorizeTwitter(ckey,csecret,atkey,atsecret):
    auth = tweepy.OAuthHandler(ckey,csecret)
    auth.set_access_token(atkey,atsecret)
    return tweepy.API(auth)

# ========================================================================================




# ==== Service Start ====

# Service Start and Loop Process

if len(sys.argv)>1: 
    if tweet:
        api = authorizeTwitter(tckey,tcsecret,tatkey,tatsecret)



    currentip = getIP()
    printLog("TDG Server is Online! sync: %s ip: %s" % (version,currentip))
    printLog("Aaaah my head hurts!")
    while True:
        ip = getIP()
        if currentip != ip:
            if printLog("I hate being dynamic! But it is my nature:%s " % ip):
                currentip = ip

        if random.randint(1,2000) == 89:
            if utility:
                randomsentence = random.choice(getSentencesLines(configfile))
                printLog(fillAStringWithValues(randomsentence))


        output = cStringIO.StringIO()
        output.write(fillAStringWithValues(reader.getHTMLString(configfile)))

        try:
            ftp = FTP(hostname,login,password)
            ftpBrowse(ftp, filepath)
            ftp.storbinary('STOR %s' % filename, output)
            ftp.close()
            output.close()
        except:
            printLog("Error - FTP connection problem to the %s" % hostname)
            traceback.print_exc()
        time.sleep(interval)

# ==== Service End ====
