#!python3.0.1
# -*- coding: utf-8 -*-

"""

データベース登録

"""
import os
import sqlite3
import sys
import re
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

if 1 < len(sys.argv):
  fn = sys.argv[1] 
else:
  fn = 'jrdb.txt'


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
	samename text not null default(''),
	sflg integer not null,

	primary key(name, samename)
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
	lflg		integer not null default(0),

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
sql = """
create table t_clinfar (
	station_id1 integer not null,
	station_id2 intege not null,
	fare integer not null,
	-- line_id integer not null references t_line(rowid),
	primary key (station_id1, station_id2)
);
"""
con.execute(sql)
###########################################
con.execute("""
create table t_rule69 (
	id		integer primary key autoincrement,
	station_id1 integer not null references t_station(rowid),
	station_id2 integer not null references t_station(rowid),
	line_id integer not null references t_line(rowid),
	ord	integer not null default(0)
);
""")
###########################################
con.execute("""
create table t_rule86 (
	line_id1 integer not null references t_line(rowid),
	station_id integer not null references t_station(rowid),
	line_id2 integer not null references t_line(rowid),
	city_id integer not null,
	
	primary key (line_id1, city_id));
""")
###########################################
con.execute("""
create table t_farem (
	km	integer primary key,
	f	integer not null,
	g	integer not null,
	h	integer not null);
""")
###########################################
con.execute("""
create table t_farel (
	km	integer primary key,
	i	integer not null,
	j	integer not null);
""")
###########################################
con.execute("""
create table t_farels (
	dkm	integer primary key,
	skm	integer not null,
	k	integer not null,
	l	integer not null);
""")
###########################################
con.execute("""
create table t_fareopq (
	km	integer primary key,
	o	integer not null,
	p	integer not null,
	q	integer not null);
""")
###########################################
con.execute("""
create table t_farer (
	km	integer primary key,
	r	integer not null);
""")
###########################################
con.execute("""
create table t_farest (
	station_id1	integer not null references t_station(rowid),
	station_id2	integer not null references t_station(rowid),
	fare		integer not null,
	kind		integer not null,
	
	primary key (station_id1, station_id2)
);
""")
###########################################
con.execute("""
create table t_hzline(
	line_id	integer not null references t_line(rowid)
);
""")
###########################################



#県
prefects = [
['北海道'], ['青森県'], ['秋田県'], ['岩手県'], ['山形県'], ['宮城県'], ['福島県'], ['新潟県'], 
['栃木県'], ['群馬県'], ['茨城県'], ['千葉県'], ['埼玉県'], ['東京都'], ['神奈川県'], ['静岡県'], 
['山梨県'], ['長野県'], ['岐阜県'], ['富山県'], ['福井県'], ['石川県'], ['愛知県'], ['三重県'], 
['滋賀県'], ['京都府'], ['大阪府'], ['和歌山県'], ['奈良県'], ['兵庫県'], ['鳥取県'], ['島根県'], 
['岡山県'], ['広島県'], ['山口県'], ['香川県'], ['徳島県'], ['愛媛県'], ['高知県'], ['福岡県'], 
['佐賀県'], ['長崎県'], ['大分県'], ['熊本県'], ['宮崎県'], ['鹿児島県']]
con.executemany('insert into t_prefect values(?)', prefects)
print("registerd t_prefect {0} affected.".format(len(prefects)))

cur = con.cursor()

###########
# 1 pass
###########
items = [[], []]
h_items = [defaultdict(int), defaultdict(int)]
n_segment = 0

pre_items = []
post_items = []
for lin in open(fn, 'r', encoding='shift-jis'):
	if lin[0] == '#':
		continue		# コメントスキップ

	if lin.startswith('*line'):
		n_segment = 1
		continue
	elif lin.startswith('*'):
		break

	if not n_segment == 1:
		continue

	linitems = lin.split('\t')
	if linitems[0] not in list(map(lambda x:x[0], prefects)):	# 都道府県
		continue

	for i in range(2):				# 会社、線区
		key = linitems[i + 1].strip();
		h_items[i][key] += 1
		if 1 == h_items[i][key]:
			if i == 1 and key.endswith("新幹線"):
				pre_items.append([key])
			elif i == 1 and not linitems[1].startswith("JR"):
				post_items.append([key])
			else:
				items[i].append([key])

prefects = None
#会社
con.executemany('insert into t_company values(?)', items[0])
print("registerd t_company {0} affected.".format(len(items[0])))
#線区
con.executemany('insert into t_line values(?)', pre_items)
n_line_Index_of_Shinkansen = len(pre_items)
con.executemany('insert into t_line values(?)', items[1])
n_line_Index_of_CompanyLine = len(pre_items) + len(items[1])
con.executemany('insert into t_line values(?)', post_items)

print("registerd t_line {0} affected.".format(len(pre_items) + len(items[1]) + len(post_items)))

con.commit()

###########
# 2 pass
###########

n_station = 0
branch = []
id70 = 10000	# rule70適用t_linesのline_idの開始値
n_segment = 0
for lin in open(fn, 'r', encoding='shift-jis'):
	if lin[0] == '#':
		continue		# コメントスキップ

	if lin.startswith('*line'):
		n_segment = 1
		continue

	if lin.startswith('*t_clinfar'):
		n_segment = 2
		continue

	if lin.startswith('*t_rule69'):
		n_segment = 3
		continue

	if lin.startswith('*rule70'):
		n_segment = 4
		continue

	if lin.startswith('*rule86'):
		n_segment = 5
		continue

	if lin.startswith('*t_farem'):
		n_segment = 6
		continue

	if lin.startswith('*farel'):
		n_segment = 7
		continue

	if lin.startswith('*t_farels'):
		n_segment = 8
		continue

	if lin.startswith('*t_fareopq'):
		n_segment = 9
		continue

	if lin.startswith('*t_farer'):
		n_segment = 10
		continue

	if lin.startswith('*t_farest'):
		n_segment = 11
		continue

	linitems = lin.split('\t')

#------------------------------------------------------------------------------
	if n_segment == 1:	# 路線
		if 19 != len(linitems):
			raise ValueError

		if 0 <= linitems[1].find("branch"):
			branch.append([linitems[2].strip(), linitems[3].strip(), 
						   linitems[5].strip(), linitems[6].strip(), linitems[8].strip()])
			continue			# 分岐特例はあとで

		# BSRJCTFLG: 分岐フラグ
		flg = 0 if linitems[7].strip() == '' else (1 << 12)	# jctflg

		tmp = int(linitems[17])			# 規則69条 t_rule69.id
		if 0 < tmp and tmp < 0x10:		# BSR69NOMASK, BSR69TERM, BSR69CONT
			if 100 <= tmp:
				flg |= (1 << 28)		# BSR69CONT
				tmp -= 100
			flg |= (1 << 29)			# BSR69TERM
			flg |= (tmp << 17)			# BSR69NOMASK(20-17)


		# BSRBORDER: 本州3社、3島会社境界駅
		tmp = int(linitems[16])
		if 0 < tmp:
			flg |= (1 << 21)

		# BSRVIRJCT: 新幹線で新幹線の駅の無い在来線分岐駅
		tmp = int(linitems[18])
		if 0 < tmp:
			flg |= (1 << 22)

		# BSRHZLIN: 新幹線＜－＞並行在来線乗換
		tmp = linitems[15].strip()
		if tmp[0] != '!' and tmp != "":
			cur.execute('select rowid from t_hzline where line_id=(select rowid from t_line where name=?)', [tmp])
			row = cur.fetchone()
			if None == row:
				con.execute('insert into t_hzline values((select rowid from t_line where name=?))', [tmp])
				cur.execute('select rowid from t_hzline where line_id=(select rowid from t_line where name=?)', [tmp])
				row = cur.fetchone()
			
			tmp = row[0]
			tmp &= 0x0f
			flg |= (tmp << 13)		# bit16-13

		# BCRULE70:規則70条
		tmp = int(linitems[14])
		if 0 != tmp:
			flg |= (1 << 6)

		# BCYAMATE
		tmp = int(linitems[13])
		if 0 != tmp:
			flg |= (1 << 5)

		# BCOSMSP, BCTKMSP
		tmp = int(linitems[12])
		if 1 == tmp:
			flg |= (1 << 10)	# BCTKMSP: 東京電車特定区間
		elif 2 == tmp:
			flg |= (1 << 11)	# BCOSMSP: 大阪電車特定区間
		
		# BCSUBURB: 近郊区間
		tmp = int(linitems[11])
		tmp &= 0x07
		flg |= (tmp << 7)	# bit9-7

		# BSRSHINKTRSALW、BSRSHINKTRS: 新幹線、在来線乗換
		tmp = int(linitems[10])
		if 10 <= tmp and tmp <= 13:
			flg |= ((1 << 27) | ((tmp - 10) << 25))

		# BCCITYCT, BCCITYNO
		tmp = int(linitems[9])
		if 100 <= tmp:
			flg |= (tmp << 4)	# BCCITYCT
		
		tmp -= 100
		tmp &= 0x0f
		flg |= (tmp << 0)	# BCCITYNO: bit3-0

		# BSRCOMPANY
		if not linitems[1].strip().startswith("JR"):
			flg |= (1 << 23)

		cur.execute('select rowid from t_prefect where name=?', [linitems[0].strip()])	# retrive 都道府県id
		prefect_id = cur.fetchone()[0]

		cur.execute('select rowid from t_company where name=?', [linitems[1].strip()])	# retrive 会社id
		company_id = cur.fetchone()[0]

		cur.execute('select rowid from t_line where name=?', [linitems[2].strip()])		# retrive 路線id
		line_id = cur.fetchone()[0]

		station_name = linitems[3].strip()
		samename = linitems[8].strip()
		cur.execute('select rowid from t_station where name=? and samename=?', [station_name, samename])
		row = cur.fetchone()
		if None != row:
			station_id = row[0]			# 登録済み
		else:
			con.execute('insert into t_station values(?, ?, ?, ?, ?, ?)', \
						[ station_name, linitems[4].strip(), company_id, prefect_id, \
						  samename, flg])
			cur.execute('select rowid from t_station where name=? and samename=?', [station_name, samename])
			station_id = cur.fetchone()[0]
			n_station += 1

		sales_km = int(float(linitems[5]))
		if 0 < sales_km:
			sales_km *= 10

		calc_km = int(float(linitems[6]))
		if 0 < calc_km:
			calc_km *= 10

		con.execute('insert into t_lines values(?, ?, ?, ?, ?)', [line_id, station_id, sales_km, calc_km, flg] )

#------------------------------------------------------------------------------
	elif n_segment == 2:	# 料金表 各路線(N-1)*N/2 N=駅数
		tmp = linitems[0].strip()
		if 0 <= tmp.find('('):
			station1 = tmp[:tmp.find('(')]
			station1_s = tmp[tmp.find('('):]
		else:
			station1 = tmp
			station1_s = ''

		tmp = linitems[1].strip()
		if 0 <= tmp.find('('):
			station2 = tmp[:tmp.find('(')]
			station2_s = tmp[tmp.find('('):]
		else:
			station2 = tmp
			station2_s = ''

		con.execute("""insert into t_clinfar values(
 (select rowid from t_station where name=? and samename=?),
 (select rowid from t_station where name=? and samename=?), ?);
""", [station1, station1_s, station2, station2_s, int(linitems[2])])

#------------------------------------------------------------------------------
	elif n_segment == 3:		# t_rule69
		tmp = linitems[1].strip()
		if 0 <= tmp.find('('):
			station1 = tmp[:tmp.find('(')]
			station1_s = tmp[tmp.find('('):]
		else:
			station1 = tmp
			station1_s = ''

		tmp = linitems[2].strip()
		if 0 <= tmp.find('('):
			station2 = tmp[:tmp.find('(')]
			station2_s = tmp[tmp.find('('):]
		else:
			station2 = tmp
			station2_s = ''

		con.execute("""
insert into t_rule69(station_id1, station_id2, line_id, ord) values(
 (select rowid from t_station where name=? and samename=?),
 (select rowid from t_station where name=? and samename=?),
 (select rowid from t_line where name=?), ?)""",
			 [station1, station1_s, station2, station2_s, linitems[3], int(linitems[4])])

#------------------------------------------------------------------------------
	elif n_segment == 4:	# rule70
		sql = """
insert into t_lines values(?,
 (select rowid from t_station where name=? and samename=?),
 ?, 0, ((1 << 24) | (select rowid from t_line where name=?)));
"""
		# b24=special_t_lines
		# BSR70=(1 << 24)
		tmp = linitems[1].strip()
		if 0 <= tmp.find('('):
			station1 = tmp[:tmp.find('(')]
			station1_s = tmp[tmp.find('('):]
		else:
			station1 = tmp
			station1_s = ''

		tmp = linitems[3].strip()
		if 0 <= tmp.find('('):
			station2 = tmp[:tmp.find('(')]
			station2_s = tmp[tmp.find('('):]
		else:
			station2 = tmp
			station2_s = ''

		id70 += 1
		#print(id70, end='|')
		con.execute(sql, [id70, station1, station1_s, 0, linitems[0].strip()])
		if station1 == station2 and station1_s == station2_s:
			id70 += 1
		#print(id70, lin, end='')
		con.execute(sql, [id70, station2, station2_s, int(linitems[4]), linitems[2].strip()])

#------------------------------------------------------------------------------
	elif n_segment == 5:	# rule86
		tmp = linitems[1].strip()
		if 0 <= tmp.find('('):
			station = tmp[:tmp.find('(')]
			station_s = tmp[tmp.find('('):]
		else:
			station = tmp
			station_s = ''

		#print(lin, end='')
		con.execute("""
insert into t_rule86 values(
 (select rowid from t_line where name=?),
 (select rowid from t_station where name=? and samename=?),
 (select rowid from t_line where name=?), ?);""",
		[linitems[0].strip(), station, station_s, linitems[2].strip(), int(linitems[3])])

#------------------------------------------------------------------------------
	elif n_segment == 6:	# farem
		con.execute("""
insert into t_farem values(?, ?, ?, ?)""",
		[int(linitems[0].replace(',', '')), int(linitems[1].replace(',', '')), int(linitems[2].replace(',', '')), int(linitems[3].replace(',', ''))])
					# km, f, g, h

	elif n_segment == 7:	# farel
		con.execute("""
insert into t_farel values(?, ?, ?)""",
		[int(linitems[0].replace(',', '')), int(linitems[1].replace(',', '')), int(linitems[2].replace(',', ''))])
					# km, i, j

#------------------------------------------------------------------------------
	elif n_segment == 8:	# farels
		if linitems[1].replace(',', '').isdigit():
			skm = int(linitems[1].replace(',', ''))
		else:
			skm = -1
		
		if linitems[2].replace(',', '').isdigit():
			k = int(linitems[2].replace(',', ''))
		else:
			k = -1

		con.execute("""
insert into t_farels values(?, ?, ?, ?)""",
		[int(linitems[0].replace(',', '')), skm, k, int(linitems[3].replace(',', ''))])
		# dkm, skm, k, l

#------------------------------------------------------------------------------
	elif n_segment == 9:	# fareopq

		con.execute("""
insert into t_fareopq values(?, ?, ?, ?)""",
		[int(linitems[0].replace(',', '')), int(linitems[1].replace(',', '')), int(linitems[2].replace(',', '')), int(linitems[3].replace(',', ''))])
		# km, o, p, q

#------------------------------------------------------------------------------
	elif n_segment == 10:	# farer

		con.execute("""
insert into t_farer values(?, ?)""",
					[int(linitems[0].replace(',', '')), int(linitems[1].replace(',', ''))])
					# km, r

#------------------------------------------------------------------------------
	elif n_segment == 11:		# farest

		tmp = linitems[0].strip()
		if 0 <= tmp.find('('):
			station1 = tmp[:tmp.find('(')]
			station1_s = tmp[tmp.find('('):]
		else:
			station1 = tmp
			station1_s = ''

		tmp = linitems[1].strip()
		if 0 <= tmp.find('('):
			station2 = tmp[:tmp.find('(')]
			station2_s = tmp[tmp.find('('):]
		else:
			station2 = tmp
			station2_s = ''

		#print(lin, end='')
		con.execute("""
insert into t_farest values(
 (select rowid from t_station where name=? and samename=?),
 (select rowid from t_station where name=? and samename=?),
 ?, ?)""",
		[station1, station1_s, station2, station2_s, int(linitems[2].replace(',', '')), int(linitems[3].replace(',', ''))])
		# station_id1, station_id2, fare, kind
#------------------------------------------------------------------------------


for bitem in branch:
	if 0 <= bitem[2].find('('):
		bstation = bitem[2][:bitem[2].find('(')]
		bstation_same = bitem[2][bitem[2].find('('):]
	else:
		bstation = bitem[2]
		bstation_same = ''

	#print(bitem[0], bitem[1], bitem[4], bstation, bstation_same, bitem[3], end='|')
	con.execute("""insert into t_lines values(
	(select rowid from t_line where name=?), 
	(select rowid from t_station where name=? and samename=?), 
	(select rowid from t_station where name=? and samename=?), 
	(select rowid from t_line where name=?), ? | (select sflg from t_station where name=? and samename=?))""", 
	[bitem[0], bitem[1], bitem[4], bstation, bstation_same, bitem[3], 1 << 31, bitem[1], bitem[4]])
	# b31=special_t_lines

# make t_jct
con.execute("""
insert into t_jct(station_id) select rowid from t_station 
where (sflg & (1 << 12))!=0
""")
# select id from t_jct j join t_station s on s.rowid=j.station_id where name='森';

##con.execute('create view lines as select p.name as prefect, c.name as company, n.name as line, s.name as station, s.kana as station_kana, sales_km, calc_km, spe_route, jctflg, sameflg, cityflg from t_lines l join t_station s on s.rowid=l.station_id join t_line n on n.rowid=l.line_id join t_prefect p on p.rowid=s.prefect_id join t_company c on c.rowid=s.company_id')
##con.execute('create view same_station as select name, count(*) as ''num'' from t_station where sameflg=1 group by name')
##con.execute('create view junctions as select p.name as prefect, c.name as company, n.name as line, s.name as station, s.kana as station_kana, sales_km, calc_km, spe_route, jctflg, sameflg, cityflg from t_lines l join t_station s on s.rowid=l.station_id join t_line n on n.rowid=l.line_id join t_prefect p on p.rowid=s.prefect_id join t_company c on c.rowid=s.company_id where jctflg=1 order by line_id, sales_km')
##con.execute('create view jct_station as select name, cityflg from t_station where jctflg=1')

con.commit()

cur.execute('select max(rowid) from t_station')
n_db_station = cur.fetchone()[0]
cur.execute('select count(*) from t_station')
assert(n_db_station == cur.fetchone()[0])
assert(n_db_station == n_station);

cur.execute('select count(*) from t_line')
n_line = cur.fetchone()[0]

cur.execute('select count(*) from t_lines where line_id in (select rowid from t_line)')
n_lines = cur.fetchone()[0]

cur.execute('select count(*) from t_lines')
n_dblines = cur.fetchone()[0]

#except sqlite3.IntegrityError:
#	print("Sqlite3 Integrity Error: current line={0}".format(n_lin))
#	exit(-1)
##########################################################

print("complete success. line={0}, stations={1} affected, lines={2}({3}) affected.".format(n_line, n_station, n_lines, n_dblines))

print()
print("/* --------------------------------------- */")
print("#define MAX_STATION	{0}".format(n_station))
print("#define MAX_LINE	{0}".format(n_line))

#cur.execute("select max(rowid) from t_line where name like '%新幹線'")
#n = cur.fetchone()[0]
print("#define IS_SHINKANSEN_LINE(id)	((id)<={0})".format(n_line_Index_of_Shinkansen))
print("#define IS_COMPANY_LINE(id)	({0}<(id))".format(n_line_Index_of_CompanyLine))

# 以下のクエリー文でも会社線路線かどうか判定可(0でJR、非0で会社線)
# select count(*) from t_lines where line_id=? and (lflg & (1 << 23))!=0;

# 以下のクエリー文で会社線路線一覧を得られる
# select * from t_line where rowid in (select line_id from t_lines where (lflg & (1 << 23))!=0);
# または以下でも同様の結果が得られる
# select * from t_line n where exists (select * from t_lines l where l.line_id=n.rowid and (lflg & (1 << 23))!=0);

cur.execute("select count(*) from t_jct")
n = cur.fetchone()[0]
print("#define MAX_JCT	{0}".format(n))

cur.execute("select max(length(name)) from t_station");
n = cur.fetchone()[0]
print("#define MAX_STATION_CHR	{0}".format((n+1)*2))

cur.execute("select max(length(name)) from t_line");
n = cur.fetchone()[0]
print("#define MAX_LINE_CHR	{0}".format((n+1)*2))

 
"""
select t.name from t_station where company_id in (select rowid from t_company name not like 'JR%')

"""

