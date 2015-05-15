#!python3.0.1
# -*- coding: utf-8 -*-

"""

ƒf[ƒ^ƒx[ƒX“o˜^
–kŠC“¹	JR–kŠC“¹	”ŸŠÙü	”ŸŠÙ‰w	‚Í‚±‚¾‚Ä	0	0	 	

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

con = sqlite3.connect(dbname, isolation_level=None)
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
	line_id 	integer not null references t_line(rowid),
	station_id 	integer not null references t_station(rowid),
	
	primary key (line_id, station_id)
);
"""
con.execute(sql)
###########################################

items = [[], [], []]
h_items = [defaultdict(int), defaultdict(int), defaultdict(int)]

n_lin = 0
for lin in open(fn, 'r'):
	n_lin += 1
	if n_lin == 1:
		continue

	linitems = lin.split('\t')

	for i in [0, 1, 2]:
		key = linitems[i].strip();
		h_items[i][key] += 1
		if 1 == h_items[i][key]:
			items[i].append([key])

con.executemany('insert into t_prefect values(?)', items[0])
print("registerd t_prefect.")

con.executemany('insert into t_company values(?)', items[1])
print("registerd t_company.")

con.executemany('insert into t_line values(?)', items[2])
print("registerd t_line.")


print("complete success.")


