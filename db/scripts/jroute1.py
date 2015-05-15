#!python3.0.1
# -*- coding: utf-8 -*-

# Mar.17, 2012 created by Sutezo.
# Mar.22, 2012 complete.
#
# JR最短ルートの検索
# python jroute.py <発駅> <着駅>
#

import sqlite3
import sys
import time

# database
con = sqlite3.connect('jr.db')  # , isolation_level=None)

# 駅(station_id)の所属する路線IDを得る. 
# 駅は非分岐駅で, 路線は1つしかないと解っていることを前提とする.
#
# line_id = f(station_id)
#
def line_from_station_id(station_id):
  cur = con.cursor()
  cur.execute("select line_id from t_lines where station_id=?", [station_id])
  return cur.fetchone()[0]

# 駅ID(分岐駅)の最寄りの分岐駅を得る(全路線）
#
# [station_id, calc_km, line_id][N] = f(station_id)
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
    cur2.execute(sql, [lin[0], station_id])
    for st in cur2:
      nodes.append([st[0], st[1], lin[0]])

  return nodes

# 駅ID(非分岐駅前提)から両隣の分岐駅とそこまでの計算キロを得る
#
#  [station_id, calc_kn][2 or 1]
#
def neer_node(station_id):
	sql = """
select 	station_id , abs((select case when calc_km>0 then calc_km else sales_km end from t_lines where line_id=(select line_id from t_lines where station_id=?1) and station_id=?1)-case when calc_km>0 then calc_km else sales_km end) as cost
from 	t_lines 
where 	line_id=(select line_id from t_lines where station_id=?1)
and 	sales_km in ((select max(y.sales_km)  
		      from t_lines x, t_lines y, t_station t 
		      where x.line_id=y.line_id 
		      -- and x.line_id=(select line_id from t_lines where station_id=?1)
		      and x.station_id=?1
		      and t.rowid=y.station_id 
		      and t.jctflg<>0 
		      and x.sales_km>y.sales_km) ,
		     (select min(y.sales_km)  
		      from t_lines x, t_lines y, t_station t 
		      where x.line_id=y.line_id 
		      -- and x.line_id=(select line_id from t_lines where station_id=?1)
		      and x.station_id=?1
		      and t.rowid=y.station_id 
		      and t.jctflg<>0 
		      and x.sales_km<y.sales_km));
"""
	result = []
	cur = con.cursor()
	cur.execute(sql, [station_id])
	for st in cur:
		result.append([st[0], st[1]])

	return result

#

# 路線IDの駅1から駅2の営業キロ、計算キロを得る
# 駅1、駅2は路線にあること
#
# [sales_km, calc_km] = f(line_id, station_id1, station_id2)
#
def distance_station_between(line_id, station_id1, station_id2):
  sql = """
select l1.sales_km - l2.sales_km, l1.calc_km - l2.calc_km 
from t_lines l1 
join t_lines l2 
where l1.line_id=?1 and l2.line_id=l1.line_id
and l1.sales_km>l2.sales_km 
and ((l1.station_id=?2 and l2.station_id=?3) 
or (l1.station_id=?3 and l2.station_id=?2))
"""
  cur = con.cursor()
  cur.execute(sql, [line_id, station_id1, station_id2])
  try:
   return cur.fetchone()
  except:
   return [];


# 駅名より駅IDを返す
#
# station_id = f("駅名")
#
def station_id(station_name):
  cur = con.cursor()
  cur.execute("select rowid from t_station where name=?", [station_name])
  try:
   return cur.fetchone()[0]
  except:
   return 0;

# 駅IDより駅名を返す
#
# "駅名" = f(station_id)
#
def station_name(station_id):
  cur = con.cursor()
  cur.execute("select name from t_station where rowid=?", [station_id])
  try:
   return cur.fetchone()[0]
  except:
   return "";

# 路線IDより路線名を返す
#
# "路線名" = f(line_id)
#
def line_name(line_id):
  cur = con.cursor()
  cur.execute("select name from t_line where rowid=?", [line_id])
  try:
   return cur.fetchone()[0]
  except:
   return "";


# 分岐IDより駅名を返す
#
# "駅名" = f(jct_id)
#
def station_from_jctid(id):
  cur = con.cursor()
  cur.execute("select t.name from t_jct j join t_station t on j.station_id=t.rowid where j.id=?", [id])
  try:
   return cur.fetchone()[0]
  except:
   return "";


# 駅IDより分岐ID(1 to 30x)を返す(駅が非分岐駅なら0を返す)
#
# jct_id = f(station_id)
#
def id_from_station_id(station_id):
  cur = con.cursor()
  cur.execute("select id from t_jct where station_id=?", [station_id])
  try:
   return cur.fetchone()[0]
  except:
   return 0;

# 駅名から分岐駅ID(1 to 30x)を返す(駅が非分岐駅なら0を返す)
#
# jct_id = f("駅名")
# 
def id_from_station(station):
  cur = con.cursor()
  cur.execute("select id from t_jct j join t_station t on t.rowid=j.station_id where t.name=?", [station])
  try:
   return cur.fetchone()[0]
  except:
   return 0;

# 分岐駅IDから駅IDを得る
#
# station_id = f(jct_id)
#
def station_id_from_id(id):
  cur = con.cursor()
  cur.execute("select station_id from t_jct where id=?", [id])
  return cur.fetchone()[0]
  # throw fatal error


# 分岐駅の総数を返す
#
# n = f()
#
def n_jct():
  cur = con.cursor()
  cur.execute("select count(*) from t_jct")
  return cur.fetchone()[0]


# 路線IDは新幹線か？
#
# True|False = f(line_id)
#
def is_shinkansen(lname):
# 103	東北新幹線
# 104	上越新幹線
# 105	北陸長野新幹線
# 117	東海道新幹線
# 166	山陽新幹線
# 201	九州新幹線
	return lname in [104, 117, 166]
	#return lname in [103, 104, 105, 117, 166, 201]


# ダイクストラ実行
#
# void f(True|False)
#
# minCost[n_jct()]
# fromNode[n_jct()]
# done_flg[n_jct()]
# line_id[n_jct()]
#
def dijkstra(except_shinkansen):

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

		for node_item in node_next(station_id_from_id(doneNode + 1)):
			id_next = id_from_station_id(node_item[0]) - 1
			cost = minCost[doneNode] + node_item[1]

			# ノードtoはまだ訪れていないノード
			# またはノードtoへより小さいコストの経路だったら
			# ノードtoの最小コストを更新
			#if ((minCost[id_next] < 0) or (cost < minCost[id_next])):
			if (not except_shinkansen or not is_shinkansen(node_item[2])) and \
			   ((minCost[id_next] < 0) or (cost < minCost[id_next])):
				minCost[id_next] = cost
				fromNode[id_next] = doneNode
				line_id[id_next] = node_item[2]

#####################################################################
#
#  start entry
#
if len(sys.argv) != 3:
	print("Usage python jroute.py <start_station> <end_station>")
	sys.exit(-1)

t0 = time.time()

# 引数から開始駅、着駅を得る
begin_station = sys.argv[1]
arrive_station = sys.argv[2]

# 開始駅、着駅の分岐IDを得る
startnode = id_from_station(begin_station)
lastnode = id_from_station(arrive_station)

begin_station_id = station_id(begin_station)
arrive_station_id = station_id(arrive_station)

if begin_station_id <= 0:
	print("発駅：駅名無効")
	sys.exit(0)			# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>

if arrive_station_id <= 0:
	print("着駅：駅名無効")
	sys.exit(0)			# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>

# ダイクストラの変数を初期化
minCost = []
fromNode = []
done_flg = []
line_id = []
for i in range(n_jct()):
	minCost.append(-1)
	fromNode.append(0)
	done_flg.append(False)
	line_id.append(0)

if startnode == 0:	# 開始駅は非分岐駅?

	# 開始駅～着駅は同一路線？
	blid = line_from_station_id(begin_station_id)
	if blid == line_from_station_id(arrive_station_id):
							# 発駅～着駅までの距離を得る
		sales_km, calc_km = distance_station_between(blid, begin_station_id, arrive_station_id)
		if calc_km == 0:
			calc_km = sales_km
		
		print("{0:10}\t[{1:10}]{2:10d}.{3}".format("", begin_station, 0, 0))
		print("+{0:10}\t[{1:10}]{2:10d}.{3}".format(line_name(blid), arrive_station, calc_km // 10, calc_km % 10))
							# 渋谷-原宿
							# 渋谷-高田馬場
		sys.exit(0)			# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>

	# 駅の両隣の最寄分岐駅IDとその駅までの計算キロを得る
	neerNode = neer_node(begin_station_id) 

	# 発駅～最初の分岐駅までの計算キロを最初の分岐駅までの初期コストとして初期化
	a = id_from_station_id(neerNode[0][0])
	minCost[a - 1] = neerNode[0][1]
	fromNode[a - 1] = -1 # from駅を-1(分岐駅でないので存在しない分岐駅)として初期化
	line_id[a - 1] = blid

	if 2<=len(neerNode): # 盲腸線でなければもう一つの最初の分岐駅側も同様に初期化
		b = id_from_station_id(neerNode[1][0])
		minCost[b - 1] = neerNode[1][1]
		fromNode[b - 1] = -1
		line_id[b - 1] = blid

else:				# 分岐駅
	minCost[startnode - 1] = 0	# 発駅の初期コストは0として初期化

#**************************************************************************
# ダイクストラ実行
#**************************************************************************
dijkstra(True)

# 終了駅は非分岐駅?
if lastnode == 0:
	# 駅の両隣の最寄分岐駅IDとその駅までの計算キロを得る
	neerNode = neer_node(arrive_station_id) 
	
	# 最後の分岐駅の決定：
	# 2つの最後の分岐駅候補(終了駅(非分岐駅）の両隣の分岐駅)～終了駅(非分岐駅)までの
	# 計算キロ＋2つの最後の分岐駅候補までの計算キロは、
	# どちらが短いか？
	
	a = id_from_station_id(neerNode[0][0])
	if 2 <= len(neerNode):
		b = id_from_station_id(neerNode[1][0])
		if (minCost[a - 1] + neerNode[0][1]) < (minCost[b - 1] + neerNode[1][1]):
			id = a		# 短い方を最後の分岐駅とする
		else:
			id = b		# 短い方を最後の分岐駅とする
	else:
		id = a			# 1つの場合その1つを最後の分岐駅とする(盲腸線)
	lastnode_id = id
else:
	lastnode_id = lastnode
	id = lastnode

route = []
lineid = 0
# 発駅(=分岐駅)でなく最初の分岐駅(-1+1=0)でない間
# 最後の分岐駅からfromをトレース >> route[]
while id != startnode and 0 < id:
	if lineid != line_id[id - 1]:
		route.append(id - 1)
		lineid = line_id[id - 1]
	id = fromNode[id - 1] + 1

if 0 < startnode:	# 発駅=分岐駅
	route.append(startnode - 1)
else:
	print("*{0:10}\t[{1:10}]{2:10d}.{3}".format("", begin_station, 0, 0))

route.reverse()


if lastnode_id != lastnode:	# 着駅は非分岐駅?
	llid = line_from_station_id(arrive_station_id) # 着駅所属路線ID
	# 最終分岐駅～着駅までの営業キロ、運賃計算キロを取得
	d = distance_station_between(llid, arrive_station_id, station_id_from_id(lastnode_id))
	if d[1] != 0:	# 営業キロか運賃計算キロか?
		di = d[1]
	else:
		di = d[0]

	di += minCost[route[-1]]	# 最後の分岐駅までの累積計算キロを更新

	if llid == line_id[route[-1]]: # 着駅の最寄分岐駅の路線=最後の分岐駅?
		print("+", end="")
		route.pop()			# if   渋谷-新宿-西国分寺-国立
							# else 渋谷-新宿-三鷹
else:
	di =0

for i in range(len(route)):
	print("{0:10}\t[{1:10}]{2:10d}.{3}".format(line_name(line_id[route[i]]), \
	                                   station_from_jctid(route[i] + 1), \
	                                   minCost[route[i]] // 10, \
	                                   minCost[route[i]] % 10))
if 0 < di:
	assert(0 <llid)
	print("-{0:10}\t[{1:10}]{2:10d}.{3}".format(line_name(llid), 
												station_name(arrive_station_id), di // 10, di % 10))

print()
print("lapse time", time.time() - t0)


#
