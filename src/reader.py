#!/usr/bin/env python
#-*- coding:utf-8 -*-
#
# Author: Taha Doğan Güneş
# Licensed under the GNU General Public License, version 3.
# See the file http://www.gnu.org/copyleft/gpl.txt
#
# A high level "a=b" config file reader
#

import traceback, os

def copyArray(source):
    returner = []
    for i in source:
        returner.append("%s" % i)
    return returner

def readFile(filepath):
    """
        reading file lines without losing their lines
    """
    myfile = open(filepath,"r")
    filelines = copyArray(myfile.readlines())
    myfile.close()
    #print filelines
    return filelines

def deleteFile(filepath):
    try:
        os.remove(filepath)
        return True
    except:
        traceback.print_exc()
        return False

def writeEngine(filestring,filepath):
    """
        writing a string to a file is now much easier :)
    """
    myfile = open(filepath,"w")
    myfile.write(filestring)
    myfile.close()

def writeLinesEngine(filelines, filepath):
    """
        writing a string list to a file is now much easier :)
    """
    myfile = open(filepath,"w")
    myfile.writelines(filelines)
    myfile.close()




def readEngineReverse(result,configfile):
    """
        This is for only strings category = 1
        
        NOTE: This may not work because of duplicate keyword values
    """

    for i in readFile(configfile):
        if result == i.split("=")[1].strip() and i[0] != "#":
            draft = i.split("=")[0].strip()
            return draft
    return None


def replaceEngine(keyword,value,configfile):
    x = 0 #item that needs to be changed
    newline = ""
    filelines = readFile(configfile)
    for i in filelines:
        if keyword == i.split("=")[0].strip() and i[0] != "#":
            newline= keyword+"="+value+"\n"
            break
        x+=1     
    filelines[x] = newline
    os.remove(configfile)
    writeLinesEngine(filelines,configfile)
    

def readEngine(keyword,configfile,category):
    """
        For reading sync.config files, usage:
        - 'keyword' is for getting which value 
          you want to get from config file
 
        - 'configfile' is the path that configuration
          file is located
 
        - 'category' is the value getting type
          This is really important, for example
          in sync.config:
          'utility=1'
          if you want get this as a boolean value you need to use
          category number 2, for getting as a string please use 1.

    """
    #category = 1 is for getting normal values string or integer etc.
    #category = 2 is for yes no returns boolean values
    #category = 3 is for getting array values (ready!)
    if category in [1,2,3]:
        pass
    else:
        raise TypeError

    for i in readFile(configfile): #bug solved now it should work
        if keyword == i.split("=")[0].strip() and i[0] != "#":
            draft = i.split("=")[1].strip()
            if category == 1:
                return draft
            elif category == 2:
                if draft == "1":
                    return True
                elif draft == "0":
                    return False
            elif category == 3:
                #Arrays will be splitted using comma in config file
                return draft.split(",")
    return None



def getStartMessage(configfile):
    return readEngine("startmessage",configfile,1)

def getDynamicMessage(configfile):
    return readEngine("dynamicmessage",configfile,1)

def getFTPLoginName(configfile):
    return readEngine("ftpuser",configfile,1)


def getFTPLoginName(configfile):
    return readEngine("ftpuser",configfile,1)

def getHostName(configfile):
    return readEngine("hostname",configfile,1)

def getCallTimes(configfile):
    return int(readEngine("calltimes",configfile,1))

def htmlPageName(configfile):
    return readEngine("html",configfile,1)

def ftpFilePath(configfile):
    return readEngine("filepath",configfile,1)

def ftpPassword(configfile):
    return readEngine("ftppass",configfile,1) 

def twitter(configfile):
    return readEngine("twitter",configfile,1)

def getSentencesPath(configfile):
    return readEngine("sentences",configfile,1)

def getSentencesLines(configfile):
    myfile = open(getSentencesPath(configfile),"r")
    return (copyArray(myfile.readlines()))


def getSentencesString(configfile):
    myfile = open(getSentencesPath(configfile),"r")
    return("%s" % myfile.read())

def getHTMLString(configfile):
    myfile = open(htmlPageName(configfile),"r")
    #sometimes .read() returns None, so
    return("%s" % myfile.read())



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



