#!python3.0.1
# -*- coding: utf-8 -*-

"""
会社線料金取得


"""
import sys
import os
import jrdb
import time

t0 = time.time()

sql = """
select fare from t_clinfar
 where 
 ((station_id1=?1 and station_id2=?2) or
  (station_id1=?2 and station_id2=?1))
"""


# result list
for inf in jrdb.sqlexec(sql, [ jrdb.station_id(sys.argv[1]), jrdb.station_id(sys.argv[2]) ] ):
		print(inf[0])

print("lapse ", time.time() - t0)


