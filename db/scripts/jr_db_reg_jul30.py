#!python3.0.1
# -*- coding: utf-8 -*-

"""

データベース登録
北海道	JR北海道	函館線	函館駅	はこだて	0	0	 	

"""
import os
import sqlite3
import sys
import re
from collections import defaultdict


if 1 < len(sys.argv):
  fn = sys.argv[1] 
else:
  fn = 'jr.txt'


dbname = 'jr.db'

if os.access(dbname, os.F_OK):
	os.unlink(dbname)

con = sqlite3.connect(dbname)  # , isolation_level=None)
###########################################
sql = """
create table t_company (
	name char(11) not null primary key
);
"""
con.execute(sql)
###########################################
sql = """
create table t_prefect(
	name char(12) not null primary key
);
"""
con.execute(sql)
###########################################
sql = """
create table t_line(
	name text not null primary key
);
"""
con.execute(sql)
###########################################
sql = """
create table t_station(
	name text not null,
	kana text not null,
	company_id integer not null references t_company(rowid),
	prefect_id integer not null references t_prefect(rowid),
	jctflg  integer not null,
	sameflg integer not null default(0),
	cityflg integer not null,

	primary key(name, prefect_id)
);
"""
con.execute(sql)
###########################################
sql = """
create table t_lines (
	line_id 	integer not null references t_line(rowid),
	station_id 	integer not null references t_station(rowid),
	sales_km	integer not null,
	calc_km		integer not null,
	spe_route	integer not null default(0),

	primary key (line_id, station_id)
);
"""
con.execute(sql)
###########################################
sql = """
create table t_jct (
	id integer primary key autoincrement,
	station_id 	integer not null unique references t_station(rowid)
);
"""
con.execute(sql)
###########################################

items = [[], [], []]
h_items = [defaultdict(int), defaultdict(int), defaultdict(int)]

n_lin = 0
for lin in open(fn, 'r', encoding='shift-jis'):
	n_lin += 1
	if n_lin == 1:
		continue		# 1行目はヘッダなのでスキップ

	linitems = lin.split('\t')

	for i in [0, 1, 2]:		# 県、会社、線区
		key = linitems[i].strip();
		h_items[i][key] += 1
		if 1 == h_items[i][key]:
			items[i].append([key])

#県
con.executemany('insert into t_prefect values(?)', items[0])
print("registerd t_prefect {0} affected.".format(len(items[0])))
#会社
con.executemany('insert into t_company values(?)', items[1])
print("registerd t_company {0} affected.".format(len(items[1])))
#線区
con.executemany('insert into t_line values(?)', items[2])
print("registerd t_line {0} affected.".format(len(items[2])))

con.commit()

# 再読み込み - 2パス目
n_lin = 0
n_line = 0
n_station = 0
#try:
for lin in open(fn, 'r', encoding='shift-jis'):
	n_lin += 1
	if n_lin == 1:
		continue		# 1行目はヘッダなのでスキップ

	linitems = lin.split('\t')

	cur = con.cursor()
	cur.execute('select rowid from t_prefect where name=?', [linitems[0].strip()])	# 都道府県登録
	prefect_id = cur.fetchone()[0]
	
	cur.execute('select rowid from t_company where name=?', [linitems[1].strip()])	# 会社登録
	company_id = cur.fetchone()[0]

	cur.execute('select rowid from t_line where name=?', [linitems[2].strip()])		# 路線登録
	line_id = cur.fetchone()[0]

	cur.execute('select rowid from t_station where name=? and prefect_id=?', [linitems[3].strip(), prefect_id])
	row = cur.fetchone()
	if None != row:
		station_id = row[0]			# 登録済み
	else:
		jctflg = 0 if linitems[7].strip() == '' else 1
		#print("****name={0}, prefect_id={1}, company_id={2}, line_id={3}****".format(linitems[3].strip(), prefect_id, company_id, line_id))
		con.execute('insert into t_station values(?, ?, ?, ?, ?, ?, ?)', \
					[ linitems[3].strip(), linitems[4].strip(), company_id, prefect_id, \
					  jctflg, int(linitems[9]), int(linitems[10])])
		cur.execute('select rowid from t_station where name=? and prefect_id=?', \
					[ linitems[3].strip(), prefect_id])
		station_id = cur.fetchone()[0]
		n_station += 1

	sales_km = int(float(linitems[5]) * 10)
	calc_km = int(float(linitems[6]) * 10)
	con.execute('insert into t_lines values(?, ?, ?, ?, 0)', [line_id, station_id, sales_km, calc_km] )
	n_line += 1

con.execute('insert into t_jct(station_id) select rowid from t_station where jctflg!=0') # select id from t_jct j join t_station s on s.rowid=j.station_id where name='森';

con.execute('create view lines as select p.name as prefect, c.name as company, n.name as line, s.name as station, s.kana as station_kana, sales_km, calc_km, spe_route, jctflg, sameflg, cityflg from t_lines l join t_station s on s.rowid=l.station_id join t_line n on n.rowid=l.line_id join t_prefect p on p.rowid=s.prefect_id join t_company c on c.rowid=s.company_id')
con.execute('create view same_station as select name, count(*) as ''num'' from t_station where sameflg=1 group by name')
con.execute('create view junctions as select p.name as prefect, c.name as company, n.name as line, s.name as station, s.kana as station_kana, sales_km, calc_km, spe_route, jctflg, sameflg, cityflg from t_lines l join t_station s on s.rowid=l.station_id join t_line n on n.rowid=l.line_id join t_prefect p on p.rowid=s.prefect_id join t_company c on c.rowid=s.company_id where jctflg=1 order by line_id, sales_km')
con.execute('create view jct_station as select name, cityflg from t_station where jctflg=1')
"""
以下有効
 select station from junctions where line='東海道線' order by sales_km;
 東京駅の所属路線一覧
 select line from lines where station='東京';
 
 函館線の全駅
 select station from lines where line='函館線';

 函館線の分岐駅
 select station from lines where line='函館線' and jctflg=1;

 神奈川県の駅
 select e.name from t_station e join t_prefect p on p.rowid=e.prefect_id where p.name='神奈川県' order by kana;
 
 あ行の駅
 select name from t_station where kana like 'あ%' or kana like 'い%' or kana like 'う%' or kana like 'え%' or kana like 'お%'  order by kana;

 滋賀県の線
 select distinct(line) from lines where prefect='滋賀県';
 同上(駅数の多い順。但し、列2つ)
 select line, count(*) from lines where prefect='滋賀県' group by line order by count(*) desc;

 駅数の多い順に
 select line, count(*) from lines group by line order by count(*) desc;
 -> 東海道線 162駅

"""
con.commit()

cur.execute('select max(rowid) from t_station')
n_db_station = cur.fetchone()[0]
cur.execute('select count(*) from t_station')
assert(n_db_station == cur.fetchone()[0])
assert(n_db_station == n_station);

cur.execute('select max(rowid) from t_lines')
n_db_line = cur.fetchone()[0]
cur.execute('select count(*) from t_lines')
assert(n_db_line == cur.fetchone()[0])
assert(n_db_line == n_line)

#except sqlite3.IntegrityError:
#	print("Sqlite3 Integrity Error: current line={0}".format(n_lin))
#	exit(-1)
##########################################################

print("complete success. stations={0} affected, lines={1} affected.".format(n_station, n_line))


