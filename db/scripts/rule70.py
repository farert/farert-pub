#!python3.0.1
# -*- coding: utf-8 -*-

"""
route mark
"""
import sys
import os
import jrdb

sql = """
select	t1.line_id,
	65535&t1.station_id,
	65535&t2.station_id,
	(t1.lflg&65535),
	(t2.lflg&65535),
	t2.sales_km + t1.sales_km
 from	t_lines t1 left join t_lines t2
 on t1.line_id=t2.line_id and
	(t1.lflg&(1<<24))!=0 and
	(t2.lflg&(1<<24))!=0 and
	(t1.lflg&65535)<>(t2.lflg & 65535)
 where
	(t1.lflg&65535)=?1 and
	(t2.lflg&65535)=?2
"""


# result list
for inf in jrdb.sqlexec(sql, [ jrdb.line_id(sys.argv[1]), 
								jrdb.line_id(sys.argv[2]) ] ):
	print(inf[0], jrdb.station_name(inf[1]), jrdb.station_name(inf[2]),
		jrdb.line_name(inf[3]), jrdb.line_name(inf[4]), inf[5])


