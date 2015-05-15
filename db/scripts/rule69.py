#!python3.0.1
# -*- coding: utf-8 -*-

"""
route mark
"""
import sys
import os
import jrdb

sql = """
 select station_id, lflg
 from t_lines
 where line_id=?1
 and station_id
 in (select station_id
      from t_lines
      where line_id=?1
      and ((sales_km>=(select sales_km
                   from t_lines
                   where line_id=?1
                   and station_id=?2)
      and  (sales_km<=(select sales_km
                   from t_lines
                   where line_id=?1
                   and station_id=?3)))
      or  (sales_km<=(select sales_km
                  from t_lines
                  where line_id=?1
                  and station_id=?2)
      and (sales_km>=(select sales_km
                  from t_lines
                  where line_id=?1
                  and station_id=?3))))) and (lflg&(1<<29))!=0
 order by 
 case when 
 (select sales_km from t_lines where line_id=?1 and station_id=?3) <
 (select sales_km from t_lines where line_id=?1 and station_id=?2) then 
 sales_km  
 end desc,
 case when 
 (select sales_km from t_lines where line_id=?1 and station_id=?3) >
 (select sales_km from t_lines where line_id=?1 and station_id=?2) then 
 sales_km  
 end asc;
"""


# result list
for inf in jrdb.sqlexec(sql, [ jrdb.line_id(sys.argv[1]), 
								jrdb.station_id(sys.argv[2]), jrdb.station_id(sys.argv[3]) ] ):
	print(jrdb.station_name(inf[0]))


