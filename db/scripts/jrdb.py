#!python3.0.1
# -*- coding: utf-8 -*-

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

import sqlite3

	
# database
con = sqlite3.connect('jr.db')  # , isolation_level=None)

# sql
#
def sqlexec(sql, param):
  cur = con.cursor()
  cur.execute(sql, param)
  return list(cur)


# 路線IDは新幹線か？
#
# True|False = f(line_id)
#
def is_shinkansen(line_id):
	return 0 < line_id and line_id <= 6


#	並行在来線を得る
#
#	lineId = getHZLine(line_id, station_id)
#
#	line_idは新幹線であること
#	lineIdは並行在来線、0は並行在来線はないことを示す
#
def getHZline(line_id, station_id, station_id2 = -1):
	cur = con.cursor()
	try:
	 cur.execute("select line_id from t_hzline where rowid=(select (lflg>>19)&15 from t_lines where line_id=? and station_id=?)", [line_id, station_id])
	 lid = cur.fetchone()[0]
	 if 0 < lid and lid < 32768:
	  return lid
	 cur.execute("""
	 select line_id from t_hzline where line_id<32767 and rowid in (
		select ((lflg>>19)&15) from t_lines where ((lflg>>19)&15)!=0 and line_id=?1 and 
		case when (select sales_km from t_lines where line_id=?1 and station_id=?2)<
		          (select sales_km from t_lines where line_id=?1 and station_id=?3)
		then
		sales_km>(select sales_km from t_lines where line_id=?1 and station_id=?2)
		else
		sales_km<(select sales_km from t_lines where line_id=?1 and station_id=?2)
		end
	) limit(1);""", [line_id, station_id, station_id2]);
	 return cur.fetchone()[0]
	except:
	 return 0;


# 駅(station_id)の所属する路線IDを得る. 
# 駅は非分岐駅で, 路線は1つしかないと解っていることを前提とする.
#
# line_id = f(station_id)
#
def line_from_station_id(station_id):
  cur = con.cursor()
  cur.execute("""
  select line_id 
  from t_lines 
  where station_id=? 
  and 0<=sales_km 
  and 0=(lflg & ((1 << 31)|(1 << 17)))""", [station_id])
  return cur.fetchone()[0]

# 駅ID(分岐駅)の最寄りの分岐駅を得る(全路線）
#
# [neer_jct_id, calc_km, line_id][N] = f(jct_id)
#
def node_next(jct_id):
  nodes = []
  sql = """
select 	id, 
 (select case when calc_km>0 then calc_km else sales_km end 
  from t_jct j left join t_lines l on j.station_id=l.station_id 
  where line_id=?1 and id=?2 and 0<=sales_km and 0=(lflg&((1<<31)|(1<<17))))-case when calc_km>0 then calc_km else sales_km end as cost
from 	t_jct j left join t_lines l on j.station_id=l.station_id
where 	line_id=?1
and 	sales_km=(select max(sales_km) 
				  from t_jct j left join t_lines l on j.station_id=l.station_id  
				  where line_id=?1 and 0=(lflg&((1<<31)|(1<<17)))
				  and 0<=sales_km and sales_km<
				  (select sales_km from t_jct j left join t_lines l on 
				   j.station_id=l.station_id where line_id=?1 and id=?2 
				   and 0<=sales_km and 0=(lflg&((1<<31)|(1<<17)))))
union
select id, case when calc_km>0 then calc_km else sales_km end - 
 (select case when calc_km>0 then calc_km else sales_km end 
  from t_jct j left join t_lines l on j.station_id=l.station_id 
  where 0<=sales_km and line_id=?1 and id=?2 and 0=(lflg&((1<<31)|(1<<17)))) as cost
from 	t_lines l join t_jct j on j.station_id=l.station_id
where 	line_id=?1
and 	sales_km=(select min(sales_km) 
				  from t_jct j left join t_lines l on j.station_id=l.station_id  
				  where line_id=?1 and 0=(lflg&((1<<31)|(1<<17)))
				  and 0<=sales_km
				  and sales_km>(select sales_km 
						  		from t_jct j left join t_lines l on j.station_id=l.station_id 
						  		where line_id=?1 and 0=(lflg&((1<<31)|(1<<17)))
						  		and id=?2 and 0<=sales_km));
"""
  cur = con.cursor()
  cur2 = con.cursor()
  
  cur.execute("""
  select line_id 
  from t_lines l left join t_jct j on j.station_id=l.station_id 
  where id=?                and 0<=sales_km and 0=(lflg&((1<<31)|(1<<17)))""", [jct_id])
  for lin in cur:
    cur2.execute(sql, [lin[0], jct_id])
    for st in cur2:
      #if not is_shinkansen(lin[0]) or (0 == getHZline(lin[0], station_id_from_id(st[0])) and 0 == getHZline(lin[0], station_id_from_id(jct_id))):
      # if is_shinkansen(lin[0]):
      #   print("$", line_name(lin[0]), station_from_jctid(st[0]), station_from_jctid(jct_id))
       nodes.append([st[0], st[1], lin[0]]) # neer_jct, cost, line_id
  return nodes


# 駅ID(分岐駅)の最寄りの分岐駅を得る(全路線）
# 詳細はnode_list.py
# [jct_id, calc_km, line_id][N] = f(jct_id)
#
def node_next_db(jct_id):
  cur = con.cursor()
  cur.execute("""
	select case jct_id when ?1 then neer_id else jct_id end, cost, line_id
	from t_node
	where jct_id=?1 or neer_id=?1
	""", [jct_id])
  return list(cur)

# 駅ID(非分岐駅前提)から両隣の分岐駅とそこまでの計算キロを得る
#
#  [station_id, calc_km][2 or 1]
#
def neer_node(station_id):
	sql = """
select 	station_id , abs((
	select case when calc_km>0 then calc_km else sales_km end 
	from t_lines 
	where 0<=sales_km and 0=(lflg&((1<<31)|(1<<17))) 
	and line_id=(select line_id 
				 from	t_lines 
				 where	station_id=?1 
				 and	0<=sales_km 
				 and	0=(lflg&((1<<31)|(1<<17)))) 
	and station_id=?1)-case when calc_km>0 then calc_km else sales_km end) as cost
from 	t_lines 
where 	0<=sales_km and 0=(lflg&((1<<31)|(1<<17)))
 and	line_id=(select	line_id 
 				 from	t_lines 
 				 where	station_id=?1
 				 and	0<=sales_km
 				 and	0=(lflg&((1<<31)|(1<<17))))
 and	sales_km in ((select max(y.sales_km)
					  from	t_lines x left join t_lines y
					  on	x.line_id=y.line_id 
					  where	0<=x.sales_km and 0=(x.lflg&((1<<31)|(1<<17)))
					  and	0<=y.sales_km and (1<<15)=(y.lflg&((1<<31)|(1<<17)|(1<<15)))
					  and	x.station_id=?1
					  and	x.sales_km>y.sales_km
					 ),
					 (select min(y.sales_km)  
					  from	t_lines x left join t_lines y
					  on	x.line_id=y.line_id 
					  where 0<=x.sales_km and 0=(x.lflg&((1<<31)|(1<<17)))
					  and	0<=y.sales_km and (1<<15)=(y.lflg&((1<<31)|(1<<17)|(1<<15)))
					  and	x.station_id=?1
					  and	x.sales_km<y.sales_km));
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
  if 0 <= station_name.find('('):
    name = station_name[:station_name.find('(')]
    samename = station_name[station_name.find('('):]
  else:
  	name = station_name
  	samename = ''

  cur = con.cursor()
  cur.execute("select rowid from t_station where name=? and samename=?", [name, samename])
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

# 路線名より路線IDを返す
#
# line_id = f("路線名")
#
def line_id(line_name):
  cur = con.cursor()
  cur.execute("select rowid from t_line where name=?", [line_name])
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
  if 0 <= station.find('('):
    name = station[:station.find('(')]
    samename = station[station.find('('):]
  else:
  	name = station
  	samename = ''

  cur = con.cursor()
  cur.execute("""
  select id 
  from t_jct j join t_station t on t.rowid=j.station_id 
  where t.name=? 
  and t.samename=?""", [name, samename])
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


# 分岐ID一覧を返す
#
#
def jct_list():
  cur = con.cursor()
  cur.execute("select id from t_jct")
  return list(map(lambda x:x[0], cur))



if __name__ == "__main__":   # not module
	pass
