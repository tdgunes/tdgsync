#usr/bin/env python
#-*- coding:utf-8 -*-

# Taha Dogan Gunes
# tdgunes@gmail.com	
# My ultimate test server solution!
# Requirements: python-twitter
# tdgunes.org/sync
# needs lm_sensors!
# config file reader for sync.py!


def copyArray(source):
    returner = []
    for i in source:
        returner.append("%s" % i)
    return returner

def readFile(filepath):
    myfile = open(filepath,"r")
    filelines = copyArray(myfile.readlines())
    myfile.close()
    #print filelines
    return filelines

def readEngine(keyword,configfile,category):
    #category = 1 is for getting normal values string or integer etc.
    #category = 2 is for yes no returns boolean values
    #category = 3 is for getting array values (not ready!)
    if category in [1,2,3]:
        pass
    else:
        raise TypeError

    for i in readFile(configfile):
        if keyword in i and i[0] != "#":
            draft = i.split("=")[1].strip()
            if category == 1:
                return draft
            elif category == 2:
                if draft == "1":
                    return True
                elif draft == "0":
                    return False
    return None

def getFTPLoginName(configfile):
    return readEngine("ftpuser",configfile,1)

def getHostName(configfile):
    return readEngine("hostname",configfile,1)

def getIntervalValue(configfile):
    return int(readEngine("interval",configfile,1))

def htmlPageName(configfile):
    return readEngine("html",configfile,1)

def ftpFilePath(configfile):
    return readEngine("filepath",configfile,1)

def ftpPassword(configfile):
    return readEngine("ftppass",configfile,1) 


def twitter(configfile):
    return readEngine("twitter",configfile,1)

def twitterAppKeys(configfile):
    #api key 1 tckey 2 tcsecret
    returnlist = []
    returnlist.append(readEngine("tckey",configfile,1))
    returnlist.append(readEngine("tcsecret",configfile,1))
    return returnlist
    #apikeys

def twitterUserKeys(configfile):
    #1 tatkey 2 tatsecret    tokens
    returnlist = []
    returnlist.append(readEngine("tatkey",configfile,1))
    returnlist.append(readEngine("tatsecret",configfile,1))
    return returnlist
    #apikeys

