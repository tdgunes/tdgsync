#!/usr/bin/env python
#-*- coding:utf-8 -*-
#
# Author: Taha Doğan Güneş
# Licensed under the GNU General Public License, version 3.
# See the file http://www.gnu.org/copyleft/gpl.txt
#
# This is the example for using sync as a high level library


import sync 

message = raw_input("Message: ")
mysync = sync.api("/Users/tdgunes/Desktop/tdgconfigs/sync.config")
mysync.printLog(message)
