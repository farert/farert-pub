#!python3.0.1
# -*- coding: utf-8 -*-

import sys
import os
import jrdb

#####################################################################
#
#  start entry
#
if len(sys.argv) != 2:
	print("Usage python neer_node.py <start_station>")
	sys.exit(-1)

# 引数から開始駅、着駅を得る
for inf in jrdb.neer_node(jrdb.station_id(sys.argv[1])):
	print(jrdb.station_name(inf[0]), inf[1])


