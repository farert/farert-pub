#!python3.0.1
# -*- coding: utf-8 -*-

"""
指定路線、駅1から駅2までの営業キロ、計算キロを得る


"""
import sys
import os
import jrdb
import time

t0 = time.time()

sql = """
select 
	(select max(sales_km) from t_lines where line_id=?1 and (station_id=?2 or station_id=?3))-
	(select min(sales_km) from t_lines where line_id=?1 and (station_id=?2 or station_id=?3)),

	(select max(calc_km) from t_lines where line_id=?1 and (station_id=?2 or station_id=?3))-
	(select min(calc_km) from t_lines where line_id=?1 and (station_id=?2 or station_id=?3)),

	case when exists (select * from t_lines
	where line_id=?1 and (lflg&(1<<21)!=0) and station_id=?2)
	then -1 else
	abs((select sales_km from t_lines
	where line_id=?1 and  (lflg&(1<<21)!=0)
	and	sales_km>(select min(sales_km) from t_lines where line_id=?1 and (station_id=?2 or station_id=?3))
	and	sales_km<(select max(sales_km) from t_lines where line_id=?1 and (station_id=?2 or station_id=?3)))-
	(select sales_km from t_lines where line_id=?1 and station_id=?2)) end,

	case when exists (select * from t_lines
	where line_id=?1 and (lflg&(1<<21)!=0) and station_id=?3)
	then -1 else
	abs((select calc_km from t_lines
	where line_id=?1 and  (lflg&(1<<21)!=0) 
	and	sales_km>(select min(sales_km) from t_lines where line_id=?1 and (station_id=?2 or station_id=?3))
	and	sales_km<(select max(sales_km) from t_lines where line_id=?1 and (station_id=?2 or station_id=?3)))-
	(select calc_km from t_lines where line_id=?1 and station_id=?2)) end,

	((select company_id from t_station where rowid=?2) + (65536 * (select company_id from t_station where rowid=?3))),

	((select 2147483648*(1&(lflg>>23)) from t_lines where line_id=?1) + 
	 (select sflg&8191 from t_station where rowid=?2) + (select sflg&8191 from t_station where rowid=?3) * 65536)

"""

# s1 or s2が

# result list
for n in range(100):
	for inf in jrdb.sqlexec(sql, [ jrdb.line_id(sys.argv[1]), 
							   jrdb.station_id(sys.argv[2]), jrdb.station_id(sys.argv[3]) ] ):
		if n == 0: print(inf[0], inf[1], inf[2], inf[3], inf[4], inf[5])
		pass


print("lapse ", time.time() - t0)

# col1 : ?1の?2～?3の営業キロ
# col2 : ?1の?2～?3の計算キロ
# col3 : ?2～境界駅の営業キロ(?2が境界駅なら-1を返す, 境界駅が?2～?3間になければ、Noneを返す
# col4 : ?2～境界駅の計算キロ(?3が境界駅なら-1を返す, 境界駅が?2～?3間になければ、Noneを返す


# 2012-9-2
# 2012-12-21 上のを使用

print("----------------------------------------------------------------------------")

t0 = time.time()
sql = """
select	(select max(sales_km) from t_lines where line_id=?1 and (station_id=?2 or station_id=?3))-
		(select min(sales_km) from t_lines where line_id=?1 and (station_id=?2 or station_id=?3)),
		(select max(calc_km) from t_lines where line_id=?1 and (station_id=?2 or station_id=?3))-
		(select min(calc_km) from t_lines where line_id=?1 and (station_id=?2 or station_id=?3)),
		abs((select sales_km from t_lines where line_id=?1 and (lflg&(1<<21))!=0)-
			(select sales_km from t_lines where line_id=?1 and station_id=?2)),
		abs((select calc_km  from t_lines where line_id=?1 and (lflg&(1<<21))!=0)-
			 (select calc_km from t_lines where line_id=?1 and station_id=?2)),
		((select company_id	from t_station where rowid=?2) + (65536 * (select company_id from t_station where rowid=?3))),
		((select 2147483648*(1&(lflg>>23)) from t_lines where line_id=?1) + 
		 (select sflg&8191 from t_station where rowid=?2) + (select sflg&8191 from t_station where rowid=?3) * 65536)
"""

# sales_km, calc_km, sales_km(station1の会社区間), calc_km(station1の会社区間), station1のcompany_id, station2のcompany_id

# bit31: 会社線か否か


# result list
for n in range(500):
	for inf in jrdb.sqlexec(sql, [ jrdb.line_id(sys.argv[1]), 
							   jrdb.station_id(sys.argv[2]), jrdb.station_id(sys.argv[3]) ] ):
		if n == 0: print(inf[0], inf[1], inf[2], inf[3], inf[4], inf[5])
		pass



print("lapse ", time.time() - t0)











"""
3167	新山口
3180	門司      -> sales_km: 752  下関まで689

141	山陽線


12 2
15 2
19 2
22 2
29 2
32 2
40 3
48 3   36 = (40-12) + (48-40)


create table lin(km, cid, f);
insert into lin values(12, 2, 0);
insert into lin values(15, 2, 0);
insert into lin values(19, 2, 0);
insert into lin values(22, 2, 0);
insert into lin values(29, 2, 0);
insert into lin values(32, 2, 0);
insert into lin values(40, 3, 1);
insert into lin values(48, 3, 0);

"""


