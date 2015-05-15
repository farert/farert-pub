#!python3.0.1
# -*- coding: utf-8 -*-

"""
route mark
"""
import sys
import os
import jrdb

sql = """
 select count(*) 
	from t_lines 
	where line_id=?1 
	and station_id=?4
	and sales_km>=
			(select min(sales_km)
			from t_lines 
			where line_id=?1
			and (station_id=?2 or 
				 station_id=?3)
			and (lflg&(1<<31))=0)
	and sales_km<=
			(select max(sales_km)
			from t_lines 
			where line_id=?1
			and (station_id=?2 or 
				 station_id=?3)
			and (lflg&(1<<31))=0)
"""

# select count(*) 
#	from t_lines 
#	where line_id=?1 
#	and station_id=?4
#	and ((sales_km>=(select sales_km 
#			from t_lines 
#			where line_id=?1 
#			and station_id=?2 
#			and (lflg&(1<<31))=0)
#		and (sales_km<=(select sales_km 
#			from t_lines 
#			where line_id=?1 
#			and station_id=?3 and (lflg&(1<<31))=0))) 
#	or (sales_km<=(select sales_km 
#			from t_lines 
#			where line_id=?1 
#			and station_id=?2 and (lflg&(1<<31))=0)
#	and (sales_km>=(select sales_km 
#			from t_lines 
#			where line_id=?1 
#			and station_id=?3 and (lflg&(1<<31))=0))))
#"""
#
#select count(*) from (
# select station_id
# from t_lines
# where line_id=?1
# and station_id
# in (select station_id 
#	from t_lines 
#	where line_id=?1 
#	and ((sales_km>=(select sales_km 
#			from t_lines 
#			where line_id=?1 
#			and station_id=?2 
#			and (lflg&(1<<31))=0)
#		and (sales_km<=(select sales_km 
#			from t_lines 
#			where line_id=?1 
#			and station_id=?3 and (lflg&(1<<31))=0))) 
#	or (sales_km<=(select sales_km 
#			from t_lines 
#			where line_id=?1 
#			and station_id=?2 and (lflg&(1<<31))=0)
#	and (sales_km>=(select sales_km 
#			from t_lines 
#			where line_id=?1 
#			and station_id=?3 and (lflg&(1<<31))=0)))))
#) where station_id=?4;
#"""

#x select count(*) from (
#x  select station_id
#x  from t_lines
#x  where line_id=?1
#x  and station_id
#x  in (select station_id 
#x       from t_lines 
#x       where line_id=?1
#x       and ((sales_km>=(select sales_km 
#x 				from t_lines 
#x 				where line_id=?1 
#x 				and station_id=?2
#x 				 and (lflg&(1<<31)|(1<<22))=0)
#x       and  (sales_km<=(select sales_km 
#x 				from t_lines 
#x 				where line_id=?1 
#x 				and station_id=?3
#x 				 and (lflg&(1<<31)|(1<<22))=0))) 
#x 	or  (sales_km<=(select sales_km 
#x 				from t_lines 
#x 				where line_id=?1 
#x 				and station_id=?2
#x 				 and (lflg&(1<<31)|(1<<22))=0)
#x 		and (sales_km>=(select sales_km 
#x 				from t_lines 
#x 				where line_id=?1 
#x 				and station_id=?3
#x 				 and (lflg&(1<<31)|(1<<22))=0)))
#x 		))
#x ) where station_id=?4
#x """


# result list
for inf in jrdb.sqlexec(sql, [ jrdb.line_id(sys.argv[1]), 
							   jrdb.station_id(sys.argv[2]), 
							   jrdb.station_id(sys.argv[3]),
							   jrdb.station_id(sys.argv[4])] ):
	#print(jrdb.station_from_jctid(inf[0]))
	print(inf[0])


