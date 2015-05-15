#!python3.0.1
# -*- coding: utf-8 -*-

"""
route mark
"""
import sys
import os
import jrdb

sql = """
select id from t_lines l join t_jct j on j.station_id=l.station_id where
	line_id=?1 and (lflg&(1<<12))!=0 and (lflg&(1<<31))=0
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



"""
select id from t_lines l join t_jct j on j.station_id=l.station_id where
 line_id=?1 and (lflg&(1<<12))!=0 and (lflg&(1<<31))=0 and
 case when
 (select sales_km from t_lines where line_id=?1 and station_id=?3) <
 (select sales_km from t_lines where line_id=?1 and station_id=?2) then 
 (((sales_km>=(select sales_km from t_lines where line_id=?1 and station_id=?3)) and
 (sales_km<=(select sales_km from t_lines where line_id=?1 and station_id=?2))) ) else
 (((sales_km<=(select sales_km from t_lines where line_id=?1 and station_id=?3)) and
 (sales_km>=(select sales_km from t_lines where line_id=?1 and station_id=?2))) ) end
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

"""
select id from t_lines l join t_jct j on j.station_id=l.station_id where 
line_id=?1 and (lflg&(1<<12))!=0 and  (lflg&(1<<31))=0 and 
case when 
(select sales_km from t_lines where line_id=?1 and station_id=?3) <
(select sales_km from t_lines where line_id=?1 and station_id=?2) then 
(((sales_km>=(select sales_km from t_lines where line_id=?1 and station_id=?3)) and 
 (sales_km<=(select sales_km from t_lines where line_id=?1 and station_id=?2))) ) else 
(((sales_km<=(select sales_km from t_lines where line_id=?1 and station_id=?3)) and 
 (sales_km>=(select sales_km from t_lines where line_id=?1 and station_id=?2))) ) end
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
#
# 中央東線 八王子 松本
# としたらダメ。松本は中央東線ではないから。分岐特例は正式ルートに変換してからかけること。
#

# result list
for inf in jrdb.sqlexec(sql, [ jrdb.line_id(sys.argv[1]), jrdb.station_id(sys.argv[2]), jrdb.station_id(sys.argv[3]) ] ):
	print(jrdb.station_from_jctid(inf[0]))


