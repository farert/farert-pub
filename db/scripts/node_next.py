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
	print("Usage python node_next.py <start_station>")
	sys.exit(-1)

# ˆø”‚©‚çŠJn‰wA’…‰w‚ğ“¾‚é
jctid = jrdb.id_from_station(sys.argv[1])
if jctid <= 0:
  print("Station is no junction error\n")
  exit(-1)

#for inf in jrdb.node_next(jctid):
for inf in jrdb.node_next(jctid):
	print(jrdb.station_from_jctid(inf[0]), inf[1], jrdb.line_name(inf[2]))


