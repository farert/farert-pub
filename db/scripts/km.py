#!python3.0.1
# -*- coding: utf-8 -*-

"""
route mark
"""
import sys
import os
import jrdb

sql = """
select l1.sales_km - l2.sales_km, l1.calc_km - l2.calc_km,
 case when l1.calc_km<>l2.calc_km then l1.sales_km - l2.sales_km else  l1.calc_km - l2.calc_km end
 from t_lines l1
 left join t_lines l2
 where l1.line_id=?1
 --and l2.line_id=?1
 and l1.sales_km>l2.sales_km 
 and ((l1.station_id=?2 and l2.station_id=?3)
 or (l1.station_id=?3 and l2.station_id=?2))
"""

# result list
for inf in jrdb.sqlexec(sql, [ jrdb.line_id(sys.argv[1]), 
								jrdb.station_id(sys.argv[2]), jrdb.station_id(sys.argv[3]) ] ):
	print(inf[0], inf[1])


