#!python3.0.1
# -*- coding: utf-8 -*-

# Mar.17, 2012 created by sutezo.
# Mar.22, 2012 complete.
# May.10, 2012 update.
#
# JR最短ルートの検索
# python jroute.py <発駅> <着駅>
#

import jrdb
import sys
import time



# ダイクストラ実行
#
# void f(True|False)
#
# minCost[jrdb.n_jct()]
# fromNode[jrdb.n_jct()]
# done_flg[jrdb.n_jct()]
# line_id[jrdb.n_jct()]
#
def dijkstra():

	t_cnt = 0	# for profile
	t_cnt1 = 0	# for profile

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

		#for node_item in jrdb.node_next_db(doneNode + 1):
		for node_item in jrdb.node_next(doneNode + 1):
			id_next = node_item[0] - 1

			if 3 < len(sys.argv) and jrdb.is_shinkansen(node_item[2]):	### 新幹線除外の場合
			 continue								### 

			cost = minCost[doneNode] + node_item[1]

			# ノードtoはまだ訪れていないノード
			# またはノードtoへより小さいコストの経路だったら
			# ノードtoの最小コストを更新
			#if ((minCost[id_next] < 0) or (cost < minCost[id_next])):
			#if (not except_shinkansen or not is_shinkansen(node_item[2])) and \
#			if ((minCost[id_next] < 0) or (cost < minCost[id_next])):
#				minCost[id_next] = cost
#				fromNode[id_next] = doneNode
#				line_id[id_next] = node_item[2]
#<-以前の方法。並行在来線と新幹線が並んだら新幹線を採用する方法->
			if ((minCost[id_next] < 0) or (cost <= minCost[id_next])):
				if cost == minCost[id_next]:
				  if not jrdb.is_shinkansen(node_item[2]):
				    continue
				minCost[id_next] = cost
				fromNode[id_next] = doneNode
				line_id[id_next] = node_item[2]
#
			t_cnt += 1
		t_cnt1 += 1
		
	#print("cnt=", t_cnt, t_cnt1)

#####################################################################
#
#  start entry
#
if len(sys.argv) < 3:
	print("Usage python jroute.py <start_station> <end_station>")
	sys.exit(-1)

t0 = time.time()

# 引数から開始駅、着駅を得る
begin_station = sys.argv[1]
arrive_station = sys.argv[2]

# 開始駅、着駅の分岐IDを得る
startnode = jrdb.id_from_station(begin_station)
lastnode = jrdb.id_from_station(arrive_station)

begin_station_id = jrdb.station_id(begin_station)
arrive_station_id = jrdb.station_id(arrive_station)

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
for i in range(jrdb.n_jct()):
	minCost.append(-1)
	fromNode.append(0)
	done_flg.append(False)
	line_id.append(0)

if startnode == 0:	# 開始駅は非分岐駅?

	# 開始駅～着駅は同一路線？
	blid = jrdb.line_from_station_id(begin_station_id)
	if blid == jrdb.line_from_station_id(arrive_station_id):
							# 発駅～着駅までの距離を得る
		sales_km, calc_km = jrdb.distance_station_between(blid, begin_station_id, arrive_station_id)
		if calc_km == 0:
			calc_km = sales_km
		
		print("{0:10}\t[{1:10}]{2:10d}.{3}".format("", begin_station, 0, 0))
		print("+{0:10}\t[{1:10}]{2:10d}.{3}".format(jrdb.line_name(blid), arrive_station, calc_km // 10, calc_km % 10))
							# 渋谷-原宿
							# 渋谷-高田馬場
		sys.exit(0)			# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>

	# 駅の両隣の最寄分岐駅IDとその駅までの計算キロを得る
	neerNode = jrdb.neer_node(begin_station_id) 

	# 発駅～最初の分岐駅までの計算キロを最初の分岐駅までの初期コストとして初期化
	a = jrdb.id_from_station_id(neerNode[0][0])
	minCost[a - 1] = neerNode[0][1]
	fromNode[a - 1] = -1 # from駅を-1(分岐駅でないので存在しない分岐駅)として初期化
	line_id[a - 1] = blid

	if 2<=len(neerNode): # 盲腸線でなければもう一つの最初の分岐駅側も同様に初期化
		b = jrdb.id_from_station_id(neerNode[1][0])
		minCost[b - 1] = neerNode[1][1]
		fromNode[b - 1] = -1
		line_id[b - 1] = blid

else:				# 分岐駅
	minCost[startnode - 1] = 0	# 発駅の初期コストは0として初期化

#**************************************************************************
# ダイクストラ実行
#**************************************************************************
dijkstra()

# 終了駅は非分岐駅?
if lastnode == 0:
	# 駅の両隣の最寄分岐駅IDとその駅までの計算キロを得る
	neerNode = jrdb.neer_node(arrive_station_id) 
	
	# 最後の分岐駅の決定：
	# 2つの最後の分岐駅候補(終了駅(非分岐駅）の両隣の分岐駅)～終了駅(非分岐駅)までの
	# 計算キロ＋2つの最後の分岐駅候補までの計算キロは、
	# どちらが短いか？
	
	a = jrdb.id_from_station_id(neerNode[0][0])
	if 2 <= len(neerNode):
		b = jrdb.id_from_station_id(neerNode[1][0])
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
lineid = -1
# 発駅(=分岐駅)でなく最初の分岐駅(-1+1=0)でない間
# 最後の分岐駅からfromをトレース >> route[]
#jrdb.getHZline(lineid, jrdb.station_id_from_id(id))

while id != startnode and 0 < id:
	if lineid != line_id[id - 1]:
		print("o", jrdb.line_name(lineid), "[", jrdb.line_name(line_id[id - 1]), jrdb.station_from_jctid(id), "]")
		route.append(id - 1)
		lineid = line_id[id - 1]
	else:
		print("x", jrdb.line_name(lineid), jrdb.line_name(line_id[id - 1]), jrdb.station_from_jctid(id))
	
	id = fromNode[id - 1] + 1

if 0 < startnode:	# 発駅=分岐駅
	route.append(startnode - 1)
else:
	print("*{0:10}\t[{1:10}]{2:10d}.{3}".format("", begin_station, 0, 0))


#蟹田-天竜川
#富山-天竜川


route.reverse()
#############


####################
if lastnode_id != lastnode:	# 着駅は非分岐駅?
	llid = jrdb.line_from_station_id(arrive_station_id) # 着駅所属路線ID
	# 最終分岐駅～着駅までの営業キロ、運賃計算キロを取得
	d = jrdb.distance_station_between(llid, arrive_station_id, jrdb.station_id_from_id(lastnode_id))
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
	print("{0:10}\t[{1:10}]{2:10d}.{3}".format(jrdb.line_name(line_id[route[i]]), \
	                                   jrdb.station_from_jctid(route[i] + 1), \
	                                   minCost[route[i]] // 10, \
	                                   minCost[route[i]] % 10))
if 0 < di:
	assert(0 <llid)
	print("-{0:10}\t[{1:10}]{2:10d}.{3}".format(jrdb.line_name(llid), 
												jrdb.station_name(arrive_station_id), di // 10, di % 10))

print()
print("lapse time", time.time() - t0)


#
