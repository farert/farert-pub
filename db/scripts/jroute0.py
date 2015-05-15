#!python3.0.1
# -*- coding: utf-8 -*-

# Mar.17, 2012 created by Sutezo.
#

import os
import sqlite3
import sys
import re
import time
from collections import defaultdict


con = sqlite3.connect('jr.db')  # , isolation_level=None)

# 
def node_next(station_id):
  nodes = []
  sql = """
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
  cur = con.cursor()
  cur2 = con.cursor()
  
  cur.execute("select line_id from t_lines where station_id=?", [station_id])
  for lin in cur:
    #print("lin={0}, st={1}".format(lin[0], station_id))
    cur2.execute(sql, [lin[0], station_id])
    for st in cur2:
      #print("st={0}".format(st[0]))
      nodes.append([st[0], st[1], lin[0]])

  return nodes


# 
def station_id(station_name):
  cur = con.cursor()
  cur.execute("select rowid from t_station where name=?", [station_name])
  try:
   return cur.fetchone()[0]
  except:
   return 0;

# 
def station_name(station_id):
  cur = con.cursor()
  cur.execute("select name from t_station where rowid=?", [station_id])
  try:
   return cur.fetchone()[0]
  except:
   return "";

# 
def line_name(line_id):
  cur = con.cursor()
  cur.execute("select name from t_line where rowid=?", [line_id])
  try:
   return cur.fetchone()[0]
  except:
   return "";


# 
def station_from_jctid(id):
  cur = con.cursor()
  cur.execute("select t.name from t_jct j join t_station t on j.station_id=t.rowid where j.id=?", [id])
  try:
   return cur.fetchone()[0]
  except:
   return "";


# 
def id_from_station_id(station_id):
  cur = con.cursor()
  cur.execute("select id from t_jct where station_id=?", [station_id])
  try:
   return cur.fetchone()[0]
  except:
   return 0;

# 
def id_from_station(station):
  cur = con.cursor()
  cur.execute("select id from t_jct j join t_station t on t.rowid=j.station_id where t.name=?", [station])
  try:
   return cur.fetchone()[0]
  except:
   return 0;

#
#
def station_id_from_id(id):
  cur = con.cursor()
  cur.execute("select station_id from t_jct where id=?", [id])
  try:
   return cur.fetchone()[0]
  except:
   return 0

#
def n_jct():
  cur = con.cursor()
  cur.execute("select count(*) from t_jct")
  try:
   return cur.fetchone()[0]
  except:
   return 0



minCost = []
fromNode = []
done_flg = []
line_id = []
for i in range(n_jct()):
	minCost.append(-1)
	fromNode.append(0)
	done_flg.append(False)
	line_id.append(0)
#
#
def dijkstra(begin_node_id, except_shinkansen):
	for i in range(len(minCost)):
		minCost[i] = -1
		done_flg[i] = False

	minCost[begin_node_id-1] = 0
	while True:
		doneNode = -1
		for i in range(len(minCost)):
			# ノードiが確定しているとき
			# ノードiまでの現時点での最小コストが不明のとき
			if done_flg[i] or (minCost[i]) < 0:
				continue;

			# 確定したノード番号が-1かノードiの現時点の最小コストが小さいとき
			# 確定ノード番号を更新する
			if ((doneNode < 0) or (minCost[i] < minCost[doneNode])):
				doneNode = i;

		if (doneNode == -1):
			break	# すべてのノードが確定したら終了

		done_flg[doneNode] = True		# Enter start node

		node_id = station_id_from_id(doneNode + 1)
		for node_item in node_next(node_id):
			id_next = id_from_station_id(node_item[0]) - 1
			cost = minCost[doneNode] + node_item[1]

			# ノードtoはまだ訪れていないノード
			# またはノードtoへより小さいコストの経路だったら
			# ノードtoの最小コストを更新
			#if ((minCost[id_next] < 0) or (cost < minCost[id_next])):
			if (not except_shinkansen or node_item[2] != 117) and \
			   ((minCost[id_next] < 0) or (cost < minCost[id_next])):
				minCost[id_next] = cost
				fromNode[id_next] = doneNode
				line_id[id_next] = node_item[2]

if len(sys.argv) != 3:
	print("Usage python jroute.py <start_station> <end_station>")
	sys.exit(-1)

t0 = time.time()

begin_station = sys.argv[1]
arrive_station = sys.argv[2]

startnode = id_from_station(begin_station)
lastnode = id_from_station(arrive_station)

#dijkstra(startnode, False)
dijkstra(startnode, True)
route = []
id = lastnode
lineid = 0
while id != startnode:
	if lineid != line_id[id - 1]:
		route.append(id - 1)
		lineid = line_id[id - 1]
	id = fromNode[id - 1] + 1

route.append(startnode - 1)
route.reverse()
for i in range(len(route)):
	print("{0:10s}\t[{1:10}]{2:10d}.{3}".format(line_name(line_id[route[i]]), \
	                                   station_from_jctid(route[i] + 1), \
	                                   minCost[route[i]] // 10, \
	                                   minCost[route[i]] % 10))

print(time.time() - t0)
