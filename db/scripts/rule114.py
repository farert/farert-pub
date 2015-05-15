#!python3.0.1
# -*- coding: utf-8 -*-

"""
114

指定路線、駅からの下りと上りの200km到達点を得る

ex.

1174 身延線 富士

"""
import sys
import os
import jrdb

sql_desc = """
-- 上り方向で200km到達地点
select l1.sales_km-l2.sales_km+{0} as sales_km, l1.station_id
from  t_lines l1 left join t_lines l2 
where l1.line_id=?1 and l2.line_id=?1 
and   l1.sales_km>l2.sales_km 
and   l2.station_id=?2 
and   (l1.sales_km-l2.sales_km)>{1} order by l1.sales_km limit(1);
""".format(int(sys.argv[1]), 2000 - int(sys.argv[1]))

sql_asc = """
-- 上り方向で200km到達地点
select l2.sales_km - l1.sales_km+{0} as sales_km, l1.station_id
from  t_lines l1 left join t_lines l2 
where l1.line_id=?1 and l2.line_id=?1 
and   l2.sales_km>l1.sales_km 
and   l2.station_id=?2 
and   (l2.sales_km-l1.sales_km)>{1} order by l1.sales_km desc limit(1)
""".format(int(sys.argv[1]), 2000 - int(sys.argv[1]))


# result list
for inf in jrdb.sqlexec(sql_desc, [ jrdb.line_id(sys.argv[2]), 
							   jrdb.station_id(sys.argv[3]) ] ):
	print("下り:", inf[0], jrdb.station_name(inf[1]))

for inf in jrdb.sqlexec(sql_asc, [ jrdb.line_id(sys.argv[2]), 
							   jrdb.station_id(sys.argv[3]) ] ):
	print("上り:", inf[0], jrdb.station_name(inf[1]))

