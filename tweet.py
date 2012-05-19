#!usr/bin/env python
#-*- coding:utf-8 -*-

# Taha Dogan Gunes
# tdgunes@gmail.com	

import sync #sync library example 

message = raw_input("Message: ")

sync.tweet = True
sync.api = sync.authorizeTwitter(sync.tckey,
                            sync.tcsecret,
                            sync.tatkey,
                            sync.tatsecret)
sync.printLog(message)
