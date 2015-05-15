#!python3.0.1
# -*- coding: utf-8 -*-

# Mar.17, 2012 created by Sutezo.
#
# JR最短ルートの検索
# python jroute.py <発駅> <着駅>
#
#
#

import os
import jrdb
import sys
import re
import time
from collections import defaultdict

"""
'Farert'
Copyright (C) 2014 Sutezo (sutezo666@gmail.com)

   'Farert' is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    'Farert' is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with 'Farert'.  If not, see <http://www.gnu.org/licenses/>.

このプログラムはフリーソフトウェアです。あなたはこれを、フリーソフトウェ
ア財団によって発行された GNU 一般公衆利用許諾契約書(バージョン3か、希
望によってはそれ以降のバージョンのうちどれか)の定める条件の下で再頒布
または改変することができます。

このプログラムは有用であることを願って頒布されますが、*全くの無保証* 
です。商業可能性の保証や特定の目的への適合性は、言外に示されたものも含
め全く存在しません。詳しくはGNU 一般公衆利用許諾契約書をご覧ください。
 
あなたはこのプログラムと共に、GNU 一般公衆利用許諾契約書の複製物を一部
受け取ったはずです。もし受け取っていなければ、フリーソフトウェア財団ま
で請求してください
"""

n = 0
items = []
for jct in jrdb.jct_list():
	for node in jrdb.node_next(jct):
		items.append([node[2], node[1], jct, node[0]]) # line, cost, jct, neer
		# print(jrdb.station_from_jctid(jct), jrdb.station_from_jctid(node[0]), node[1], jrdb.line_name(node[2]))
		n += 1
print(n, "affected.")

assert(n == len(items))

items.sort()

b_item = ""
items2 = []
for item in items:
	t_item = b_item.split('/')
	if t_item[0] == str(item[0]) and t_item[1] == str(item[1]) and \
	   t_item[3] == str(item[2]) and t_item[2] == str(item[3]):
		# 除外するもの
		#print(jrdb.station_from_jctid(item[2]), jrdb.station_from_jctid(item[3]), item[1], jrdb.line_name(item[0]))
		pass
	else:
		items2.append(item)
	b_item = '/'.join(map(str, item))

print("------------");
#for item in items2:
#	print(jrdb.station_from_jctid(item[2]), jrdb.station_from_jctid(item[3]), item[1], jrdb.line_name(item[0]))

###########################################
jrdb.con.execute("""
--if exists (select * from sqlite_master where type='table' and name='t_node')
drop table if exists t_node;
""")
###########################################
jrdb.con.execute("""
create table t_node (
	jct_id	integer not null references t_jct(id),
	neer_id	integer not null references t_jct(id),
	cost	integer not null,
	line_id	integer not null references t_line(rowid),
	
	primary key (jct_id, neer_id, line_id)
	);
""")
###########################################
items = list(map(lambda x:[x[2], x[3], x[1], x[0]], items2))
items.sort()
for item in items:
	print(jrdb.station_from_jctid(item[0]) + "\t" + 
		  jrdb.station_from_jctid(item[1]) + "\t" +
		  str(item[2]) + "\t" + jrdb.line_name(item[3]))

jrdb.con.executemany('insert into t_node values(?, ?, ?, ?)', items)
jrdb.con.commit()
print("registerd t_node {0} affected.".format(len(items)))
assert(len(items2) == len(items))
