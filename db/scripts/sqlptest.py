#!python3.0.1
# -*- coding: utf-8 -*-

import os
import sqlite3
import sys
import re
import time
from collections import defaultdict

sql1 = """
select	station_id, (select case when calc_km>0 then calc_km else sales_km end from t_lines where line_id=?1 and station_id=?2)-case when calc_km>0 then calc_km else sales_km end as cost 
from	t_lines 
where	line_id=?1 
and		sales_km in ((select max(y.sales_km)  
					  from t_lines x, t_lines y, t_station t 
					  where x.line_id=y.line_id 
					  and x.line_id=?1 
					  and x.station_id=?2 
					  and t.rowid=y.station_id 
					  and t.jctflg<>0 
					  and x.sales_km>y.sales_km) ,
					 (select min(y.sales_km)  
					  from t_lines x, t_lines y, t_station t 
					  where x.line_id=y.line_id and x.line_id=?1 
					  and x.station_id=?2 
					  and t.rowid=y.station_id 
					  and t.jctflg<>0 
					  and x.sales_km<y.sales_km)
);
"""
sql2 = """
select 	station_id, (select case when calc_km>0 then calc_km else sales_km end from t_lines where line_id=?1 and station_id=?2)-case when calc_km>0 then calc_km else sales_km end as cost
from 	t_lines 
where 	line_id=?1 
and 	sales_km=(select max(sales_km) 
		  from t_lines l 
		  join t_station t 
		  on t.rowid=l.station_id 
		  where line_id=?1 
		  and jctflg<>0 
		  and sales_km<(select 	sales_km 
		  		from 	t_station t, t_lines l 
		  		where 	t.rowid=l.station_id 
		  		and 	jctflg<>0 
		  		and 	line_id=?1 
		  		and 	station_id=?2))
union
select 	station_id, case when calc_km>0 then calc_km else sales_km end - (select case when calc_km>0 then calc_km else sales_km end from t_lines where line_id=?1 and station_id=?2) as cost
from 	t_lines 
where 	line_id=?1 
and 	sales_km=(select min(sales_km) 
		  from t_lines l 
		  join t_station t 
		  on t.rowid=l.station_id 
		  where line_id=?1 
		  and jctflg<>0 
		  and sales_km>(select sales_km 
		  		from t_station t, t_lines l 
		  		where t.rowid=l.station_id 
		  		and jctflg<>0 
		  		and line_id=?1 
		  		and station_id=?2))
"""

sql3 = """
select	id, (select case when calc_km>0 then calc_km else sales_km end from t_lines l join t_jct j on j.station_id=l.station_id where line_id=?1 and id=?2)-case when calc_km>0 then calc_km else sales_km end as cost 
from 	t_lines l join t_jct j on j.station_id=l.station_id
where	line_id=?1 
and		sales_km in ((select max(y.sales_km)  
					  from t_lines x, t_lines y, t_jct j 
					  where x.line_id=y.line_id 
					  and x.line_id=?1 
					  and j.id=?2 
					  and j.station_id=y.station_id 
					  and x.sales_km>y.sales_km) ,
					 (select min(y.sales_km)  
					  from t_lines x, t_lines y, t_jct j 
					  where x.line_id=y.line_id and x.line_id=?1 
					  and j.id=?2 
					  and j.station_id=y.station_id 
					  and x.sales_km<y.sales_km)
);
"""

sql4 = """
select 	id, (select case when calc_km>0 then calc_km else sales_km end from t_lines l join t_jct j on j.station_id=l.station_id where line_id=?1 and id=?2) - case when calc_km>0 then calc_km else sales_km end as cost
from 	t_lines l join t_jct j on j.station_id=l.station_id
where 	line_id=?1 
and 	sales_km=(select max(sales_km) 
				  from t_lines l 
				  join t_jct j 
				  on j.station_id=l.station_id 
				  where line_id=?1 
				  and sales_km<(select 	sales_km 
						  		from 	t_jct j, t_lines l 
						  		where 	j.station_id=l.station_id 
						  		and 	line_id=?1 
						  		and 	id=?2))
union
select 	id, case when calc_km>0 then calc_km else sales_km end - (select case when calc_km>0 then calc_km else sales_km end from t_lines l join t_jct j on j.station_id=l.station_id where line_id=?1 and id=?2) as cost
from 	t_lines l join t_jct j on j.station_id=l.station_id
where 	line_id=?1 
and 	sales_km=(select min(sales_km) 
				  from t_lines l 
				  join t_jct j 
				  on j.station_id=l.station_id 
				  where line_id=?1 
				  and sales_km>(select	sales_km 
						  		from	t_jct j, t_lines l 
						  		where	j.station_id=l.station_id 
						  		and		line_id=?1 
						  		and		id=?2))
"""


con = sqlite3.connect('jr.db')  # , isolation_level=None)



# 
def node_next(station_id, sql):
  nodes = []
  cur = con.cursor()
  cur2 = con.cursor()
  
  cur.execute("select line_id from t_lines where station_id=?", [station_id])
  for lin in cur:
    cur2.execute(sql, [lin[0], station_id])
    for st in cur2:
      nodes.append(st[0])

  return nodes

# 
def node_next2(id, sql):
  nodes = []
  cur = con.cursor()
  cur2 = con.cursor()
  
  cur.execute("select line_id from t_lines l join t_jct j on l.station_id=j.station_id where id=?", [id])
  for lin in cur:
    cur2.execute(sql, [lin[0], id])
    for st in cur2:
      nodes.append(st[0])

  return nodes


for j in range(10):
	t0 = time.time()
	for i in range(1000):
	  a = node_next(535, sql1)
	print("sql1", a, time.time()-t0)

	t0 = time.time()
	for i in range(1000):
	  a = node_next(535, sql2)
	print("sql2", a, time.time()-t0)

	t0 = time.time()
	for i in range(1000):
	  a = node_next2(38, sql3)
	print("sql3", a, time.time()-t0)

	t0 = time.time()
	for i in range(1000):
	  a = node_next2(38, sql4)
	print("sql4", a, time.time()-t0)

# 意外や、意外に sql2の方が早いことが。sql1=1.8x, sql2=1.06xxでした
# SQL3や4は問題外(4sもかかる）、SQL3は結果もNGどっかまだ間違っている
