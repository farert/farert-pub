#!python3.0.1
# -*- coding: utf-8 -*-

"""
指定路線、駅1から駅2までの営業キロ、計算キロを得る


2012-8-31 ＊＊＊＊ sql2の方が10倍以上速い！！！！

"""
import sys
import os
import jrdb
import time

sql1 = """
select l1.sales_km - l2.sales_km, l1.calc_km - l2.calc_km,
 case when (l1.calc_km-l2.calc_km)=0 then l1.sales_km - l2.sales_km else  l1.calc_km - l2.calc_km end
 from t_lines l1
 left join t_lines l2
 where l1.line_id=?1
 and l2.line_id=?1
 and l1.sales_km>l2.sales_km 
 and ((l1.station_id=?2 and l2.station_id=?3) 
 or (l1.station_id=?3 and l2.station_id=?2));
"""

sql2 = """
select max(sales_km)-min(sales_km), max(calc_km)-min(calc_km), 
 case when sum(calc_km)=0 then max(sales_km)-min(sales_km) else max(calc_km)-min(calc_km) end
 from t_lines
 where line_id=?1
 and	sales_km>=(select min(sales_km) from t_lines where line_id=?1 and (station_id=?2 or station_id=?3))
 and	sales_km<=(select max(sales_km) from t_lines where line_id=?1 and (station_id=?2 or station_id=?3))
"""

# result list
for inf in jrdb.sqlexec(sql1, [ jrdb.line_id(sys.argv[1]), 
							   jrdb.station_id(sys.argv[2]), jrdb.station_id(sys.argv[3]) ] ):
	print(inf[0], inf[1], inf[2])

for inf in jrdb.sqlexec(sql2, [ jrdb.line_id(sys.argv[1]), 
							   jrdb.station_id(sys.argv[2]), jrdb.station_id(sys.argv[3]) ] ):
	print(inf[0], inf[1], inf[2])


t0 = time.time()
for n in range(1000):
	for inf in jrdb.sqlexec(sql1, [ jrdb.line_id(sys.argv[1]), 
							   jrdb.station_id(sys.argv[2]), jrdb.station_id(sys.argv[3]) ] ):
		pass

print("lapse time", time.time() - t0)

t0 = time.time()
for n in range(1000):
	for inf in jrdb.sqlexec(sql2, [ jrdb.line_id(sys.argv[1]), 
							   jrdb.station_id(sys.argv[2]), jrdb.station_id(sys.argv[3]) ] ):
		pass

print("lapse time", time.time() - t0)
