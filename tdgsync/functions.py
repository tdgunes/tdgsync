#!/usr/bin/env python
#-*- coding:utf-8 -*-
#
# Author: Taha Doğan Güneş
# Licensed under the GNU General Public License, version 3.
# See the file http://www.gnu.org/copyleft/gpl.txt




from ftplib import FTP
import os
import random
import traceback
import sys
import datetime 
import httplib2
import platform


import reader
import constants

try:
    import tweepy
except ImportError:
    print "(ImportError) - tweepy library is not found!"
    sys.exit(1) 
    pass
    #more detailed information here FIXME
try:
    import psutil
except ImportError:
    print "(ImportError) - psutil library is not found!"
    sys.exit(1) 
    pass
    #more detailed information here FIXME


def getIP(): #TDG mini IP Service - it works
    websites = ["http://tdgunes.org/getip/"] #if this is unreachable trys other web sites to getIP
               # "http://ifconfig.me",  # for your privacy it is disabled, you can enable if you want
               #"http://automation.whatismyip.com/n09230945.asp"]
    gotIP = ""
    trynumber = 0
    while gotIP == "":
        try:
            h = httplib2.Http()
            resp, content = h.request(websites[trynumber],'GET')
            gotIP = content.strip()
            break
        except:
            traceback.print_exc()
            
        trynumber += 1
        if trynumber == len(websites):
            print "Error - Unknown! Unable get IP adress from %s" % websites[trynumber-1]
            return "Unknown!"
    return gotIP

def getDate():
    return str(datetime.datetime.now())[:-3]


def ftpBrowse(ftpObject, path): #more easy way to browse in ftp 
    paths = path.split("/")
    for i in paths:
        ftpObject.cwd(i)

def fillString(mystring,ip): 
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

    mystring = mystring.replace("=ip=", ip)
    mystring = mystring.replace("=cpunumber=",str(psutil.NUM_CPUS))
    mystring = mystring.replace("=cpupercent=", str(psutil.cpu_percent(interval=1)))
    mystring = mystring.replace("=memory=",  str(psutil.phymem_usage().percent))
    mystring = mystring.replace("=diskusage=",  str(psutil.disk_usage('/').percent))
    mystring = mystring.replace("=random=", str(random.randint(23,124124)))
    mystring = mystring.replace("=version=", constants.VERSION)
    mystring = mystring.replace("=date=",getDate())
    mystring = mystring.replace("=platform=", platform.platform())

    return mystring

def authorizeTwitter(ckey,csecret,atkey,atsecret):
    auth = tweepy.OAuthHandler(ckey,csecret)
    auth.set_access_token(atkey,atsecret)
    return tweepy.API(auth)


