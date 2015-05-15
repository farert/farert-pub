#!python3.0.1
# -*- coding: utf-8 -*-

"""
farest table ref.
2駅間にfarest内にマッチする駅があるか

"""
import sys
import os
import jrdb
import time

sql1 = """
select station_id1, station_id2, fare from t_farest where kind=0
"""

sql2 = """
select station_id1, station_id2, fare from t_farest f where kind=0
	and exists (
	select *
	from t_lines where
	line_id=?1
	and station_id=f.station_id1
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
			and (lflg&(1<<31))=0))

	and exists (
	select *
	from t_lines where
	line_id=?1
	and station_id=f.station_id2
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
			and (lflg&(1<<31))=0))

	order by fare desc

"""

for inf in jrdb.sqlexec(sql2, [ jrdb.line_id(sys.argv[1]), 
							   jrdb.station_id(sys.argv[2]), 
							   jrdb.station_id(sys.argv[3])]):
		print(jrdb.station_name(inf[0]), jrdb.station_name(inf[1]), inf[2])

"""

create table ta(id1, id2, f);
create table la(skm, id);

insert into la values(2, 101);
insert into la values(4, 102);
insert into la values(5, 103);
insert into la values(7, 104);
insert into la values(12, 105);
insert into la values(14, 106);
insert into la values(19, 107);
insert into la values(22, 108);
insert into la values(31, 109);
insert into la values(33, 110);
insert into ta values(3, 2, 50);
insert into ta values(107, 105, 100);
insert into ta values(130, 134, 200);
insert into ta values(109, 105, 220);


select * from ta left joi

"""

