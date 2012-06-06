#!usr/bin/env python
#-*- coding:utf-8 -*-

# Taha Dogan Gunes
# tdgunes@gmail.com	

import sync #sync library example 

message = raw_input("Message: ")
mysync = sync.api("/Users/tdgunes/Desktop/tdgconfigs/sync.config")
mysync.printLog(message)
