#!python3.0.1
# -*- coding: utf-8 -*-

"""

データベース登録

Copyright sutezo9@me . com Allrightreserve. Jun.2011 - 2012,2013.

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

def same_staion(station_name):
	if 0 <= station_name.find('('):
		name = station_name[:station_name.find('(')]		# 同名駅がある駅の場合
		same = station_name[station_name.find('('):]
	else:
		name = station_name								# 同名駅でない場合
		same = ''
	return (name, same)


if 1 < len(sys.argv):
  fn = sys.argv[1] 
else:
  fn = 'jrdb.txt'


class Dbreg:

	def __init__(self, dbname):
		if os.access(dbname, os.F_OK):
			os.unlink(dbname)

		self.con = sqlite3.connect(dbname)  # , isolation_level=None)
		self.cur = self.con.cursor()

		self.n_station = 0
		self.branch = []
		self.num_of_line = 0


	def create_table(self):
		###########################################
		sql = """
		create table t_company (
			name char(11) not null primary key
		);
		"""
		self.con.execute(sql)
		###########################################
		sql = """
		create table t_prefect(
			name char(12) not null primary key
		);
		"""
		self.con.execute(sql)
		###########################################
		sql = """
		create table t_line(
			name text not null primary key
		);
		"""
		self.con.execute(sql)
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
		self.con.execute(sql)
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
		self.con.execute(sql)
		###########################################
		sql = """
		create table t_jct (
			id integer primary key autoincrement,
			station_id 	integer not null unique references t_station(rowid)
		);
		"""
		self.con.execute(sql)
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
		self.con.execute(sql)
		###########################################
		sql = """
		create table t_clinfar5p (
			station_id1 integer not null,
			station_id2 intege not null,
			fare integer not null,
			-- line_id integer not null references t_line(rowid),
			primary key (station_id1, station_id2)
		);
		"""
		self.con.execute(sql)
		###########################################
		self.con.execute("""
		create table t_rule69 (
			id		integer not null,
			station_id1 integer not null references t_station(rowid),
			station_id2 integer not null references t_station(rowid),
			line_id integer not null references t_line(rowid),
			ord	integer not null default(0),
			
			primary key (id, station_id1)
		);
		""")
		###########################################
		self.con.execute("""
		create table t_rule70 (
			station_id1 integer not null references t_station(rowid),
			station_id2 integer not null references t_station(rowid),
			sales_km integer not null,

			primary key (station_id1, station_id2)
		);
		""")
		###########################################
		self.con.execute("""
		create table t_rule86 (
			line_id1 integer not null references t_line(rowid),
			station_id integer not null references t_station(rowid),
			line_id2 integer not null references t_line(rowid),
			city_id integer not null,
			
			primary key (line_id1, city_id));
		""")
		###########################################
		self.con.execute("""
		create table t_farebspekm (
			km	integer primary key,
			h8	integer not null,
			s8	integer not null,
			k8	integer not null,
			h5	integer not null,
			s5	integer not null,
			k5	integer not null);
		""")
		###########################################
		self.con.execute("""
		create table t_farelspekm (
			km	integer primary key,
			ckm	integer not null,
			e8	integer not null,
			h8	integer not null,
			e5	integer not null,
			h5	integer not null);
		""")
		###########################################
		self.con.execute("""
		create table t_farels (
			dkm	integer primary key,
			skm	integer not null,
			s8	integer not null,
			k8	integer not null,
			s5	integer not null,
			k5	integer not null);
		""")
		###########################################
		self.con.execute("""
		create table t_fareadd (
			km	integer primary key,
			ha	integer not null,
			sa	integer not null,
			ka	integer not null);
		""")
		###########################################
		self.con.execute("""
		create table t_fareadd5p (
			km	integer primary key,
			ha	integer not null,
			sa	integer not null,
			ka	integer not null);
		""")
		###########################################
		self.con.execute("""
		create table t_farehla (
			km	integer primary key,
			ha	integer not null)
		""")
		###########################################
		self.con.execute("""
		create table t_farehla5p (
			km	integer primary key,
			ha	integer not null)
		""")
		###########################################
		self.con.execute("""
		create table t_farespp (
			station_id1	integer not null references t_station(rowid),
			station_id2	integer not null references t_station(rowid),
			fare8p		integer not null,
			fare5p		integer not null,
			kind		integer not null,
			
			primary key (station_id1, station_id2, kind)
		);
		""")
		###########################################
		self.con.execute("""
		create table t_hzline(
			line_id	integer not null references t_line(rowid)
		);
		""")
		###########################################
		self.con.execute("""
		create table t_jctspcl(
			id integer primary key autoincrement,
			type integer not null,
			jctsp_line_id1 integer not null,
			jctsp_station_id1 integer not null,
			jctsp_line_id2 integer not null default(0),
			jctsp_station_id2 integer not null default(0)
		);
		""")
		###########################################

	n_line_Index_of_CompanyLine = 0
	n_line_Index_of_Shinkansen = 0


	def first_regist(self):
		#県
		prefects = [
		['北海道'], ['青森県'], ['秋田県'], ['岩手県'], ['山形県'], ['宮城県'], ['福島県'], ['新潟県'], 
		['栃木県'], ['群馬県'], ['茨城県'], ['千葉県'], ['埼玉県'], ['東京都'], ['神奈川県'], ['静岡県'], 
		['山梨県'], ['長野県'], ['岐阜県'], ['富山県'], ['福井県'], ['石川県'], ['愛知県'], ['三重県'], 
		['滋賀県'], ['京都府'], ['大阪府'], ['和歌山県'], ['奈良県'], ['兵庫県'], ['鳥取県'], ['島根県'], 
		['岡山県'], ['広島県'], ['山口県'], ['香川県'], ['徳島県'], ['愛媛県'], ['高知県'], ['福岡県'], 
		['佐賀県'], ['長崎県'], ['大分県'], ['熊本県'], ['宮崎県'], ['鹿児島県']]
		self.con.executemany('insert into t_prefect values(?)', prefects)
		print("registered t_prefect {0} affected.".format(len(prefects)))


		###########
		# 1 pass
		###########
		items = [[], []]
		h_items = [defaultdict(int), defaultdict(int)]
		n_segment = 0

		pre_items = []
		post_items = []
		self.num_of_line = 0
		for lin in open(fn, 'r', encoding='shift-jis'):
			self.num_of_line += 1
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
		self.con.executemany('insert into t_company values(?)', items[0])
		print("registered t_company {0} affected.".format(len(items[0])))
		#線区
		self.con.executemany('insert into t_line values(?)', pre_items)
		self.n_line_Index_of_Shinkansen = len(pre_items)
		self.con.executemany('insert into t_line values(?)', items[1])
		self.n_line_Index_of_CompanyLine = len(pre_items) + len(items[1])
		self.con.executemany('insert into t_line values(?)', post_items)

		print("registered t_line {0} affected.".format(len(pre_items) + len(items[1]) + len(post_items)))

		self.con.commit()

	def second_regist(self):
		###########
		# 2 pass
		###########


		dispatch = {
			'line'			: self.reg_line,
			't_clinfar'		: self.reg_t_clinfar,
			't_clinfar5p'	: self.reg_t_clinfar,
			't_rule69'		: self.reg_t_rule69,
			'rule70'		: self.reg_rule70,
			'rule86'		: self.reg_rule86,
			't_farebspekm'	: self.reg_t_farebspekm,
			't_farelspekm'	: self.reg_t_farelspekm,
			't_farels'		: self.reg_t_farels,
			't_fareadd'		: self.reg_t_fareadd,
			't_fareadd5p'	: self.reg_t_fareadd,
			't_farespp'		: self.reg_t_farespp,
			't_farehla'		: self.reg_t_farehla,
			't_farehla5p'	: self.reg_t_farehla,
		}

		self.num_of_line = 0
		proc_stage = ''
		for lin in open(fn, 'r', encoding='shift-jis'):
			self.num_of_line += 1
			if lin[0] == '#':
				continue		# コメントスキップ

			if lin.strip() == '':
				continue		# コメントスキップ

			linitems = lin.split('\t')

			if lin.startswith('*'):
				proc_stage = re.match(r'\w+', linitems[0][1:]).group(0)
			
			elif proc_stage in dispatch:
				dispatch[proc_stage](proc_stage, linitems, lin)




	def reg_line(self, label, linitems, lin):
	# 路線
		if 0 <= linitems[1].find("branch"):
			self.branch.append([linitems[2].strip(), linitems[3].strip(), linitems[4].strip(), 
						   linitems[5].strip(), linitems[6].strip(), linitems[8].strip(), 
						   linitems[7].strip(), 0 if linitems[7].strip() == '' else (1 << 15)])
			return			# 分岐特例はあとで

		if linitems[3].strip().startswith("-"):
			return

		if 20 != len(linitems):
			print(self.num_of_line, lin)
			raise ValueError

		# BSRJCTFLG: 分岐フラグ
		sflg = 0 if linitems[7].strip() == '' else (1 << 12)	# jctflg
		lflg = 0 if linitems[7].strip() == '' else (1 << 15)	# jctflg

		# 規則69条 t_rule69.id
		# BSR69NOMASK, BSR69TERM, BSR69CONT
		tmp = int(linitems[17])
		if 0 < tmp:
			if 100 <= tmp:
				lflg |= (1 << 23)		# BSR69CONT
				tmp -= 100
			lflg |= (1 << 24)			# BSR69TERM
			lflg |= ((0x0f & tmp) << 0)	# BSR69NOMASK(20-17)


		# BSRBORDER: 本州3社、3島会社境界駅
		tmp = int(linitems[16])
		if 0 < tmp:
			lflg |= (1 << 16)

		# BSRVIRJCT: 新幹線で新幹線の駅の無い在来線分岐駅
		tmp = int(linitems[18])
		if 0 < tmp:
			lflg |= (1 << 17)

		# BSRHZLIN: 新幹線＜－＞並行在来線乗換
		tmp = linitems[15].strip()
		if tmp[0] != '!' and tmp != "":
			if tmp.startswith('-'):
				# bit16-13	境界駅=高崎
				self.cur.execute('select rowid from t_hzline where line_id=65535')
				row = self.cur.fetchone()
				if None == row:
					self.con.execute('insert into t_hzline values(65535)')
					self.cur.execute('select rowid from t_hzline where line_id=65535')
					row = self.cur.fetchone()
			else:
				self.cur.execute('select rowid from t_hzline where line_id=(select rowid from t_line where name=?)', [tmp])
				row = self.cur.fetchone()
				if None == row:
					self.con.execute('insert into t_hzline values((select rowid from t_line where name=?))', [tmp])
					self.cur.execute('select rowid from t_hzline where line_id=(select rowid from t_line where name=?)', [tmp])
					row = self.cur.fetchone()
				
			tmp = row[0]
			tmp &= 0x0f
			lflg |= (tmp << 19)		# BSRHZLIN: bit16-13 -> 22-19

		# BCRULE70:規則70条
		tmp = int(linitems[14])
		if 0 != tmp:
			sflg |= (1 << 6)

		# BCYAMATE
		tmp = int(linitems[13])
		if 0 != tmp:
			sflg |= (1 << 5)

		# BCOSMSP, BCTKMSP
		tmp = int(linitems[12])
		if 1 == tmp:
			sflg |= (1 << 10)	# BCTKMSP: 東京電車特定区間
		elif 2 == tmp:
			sflg |= (1 << 11)	# BCOSMSP: 大阪電車特定区間
		
		# BCSUBURB: 近郊区間
		tmp = int(linitems[11])
		tmp &= 0x07
		sflg |= (tmp << 7)	# bit9-7

		# BSRSHINKTRSALW: 新幹線、在来線乗換
		# (新幹線のみ)
		tmp = int(linitems[10])
		if 10 <= tmp and tmp <= 13:
#140516			if 0 != int(linitems[16]):			###!!!なんの意味があったのか？
#				print(self.num_of_line, lin)
#				raise ValueError
			#lflg |= ((1 << 27) | ((tmp - 10) << 25))
			lflg |= ((tmp - 10) << 19)

		# BCCITYCT, BCCITYNO
		tmp = int(linitems[9])
		if 100 <= tmp:
			sflg |= (1 << 4)	# BCCITYCT
			tmp -= 100

		tmp &= 0x0f
		sflg |= (tmp << 0)	# BCCITYNO: bit3-0

		# BSRCOMPANY
		# (会社線)
		if not linitems[1].strip().startswith("JR"):
			lflg |= (1 << 18)

		# BSRJCTSP_B: 分岐特例
		tmp = linitems[19].strip()
		if tmp[0] != '!' and tmp != "":
			tmps = tmp.split('/')
			while len(tmps) < 5:
				tmps.append('')

			if int(tmps[0]) < 1 or 5 < int(tmps[0]):  # あえてisdigit()を使わず例外スローさせる
				print(self.num_of_line, lin)
				raise ValueError

			self.con.execute("""
			insert into t_jctspcl(type, jctsp_line_id1, jctsp_station_id1, jctsp_line_id2, jctsp_station_id2) values(
			?1, 
			(select case when (select rowid from t_line where name=?2) is null then 0 
			else              (select rowid from t_line where name=?2) end),
			(select case when (select rowid from t_station where name=?3 and samename=?4) is null then 0
			else              (select rowid from t_station where name=?3 and samename=?4) end),
			(select case when (select rowid from t_line where name=?5) is null then 0
			else              (select rowid from t_line where name=?5) end),
			(select case when (select rowid from t_station where name=?6 and samename=?7) is null then 0
			else              (select rowid from t_station where name=?6 and samename=?7) end))
			""", 
			[tmps[0], tmps[1], same_staion(tmps[2])[0], same_staion(tmps[2])[1], 
			 tmps[3], same_staion(tmps[4])[0], same_staion(tmps[4])[1]])

			self.cur.execute('select seq from sqlite_sequence where name=\'t_jctspcl\'')
			lflg &= 0xffffff00
			lflg |= (0xff & self.cur.fetchone()[0])
			lflg |= (1 << 29)

		self.cur.execute('select rowid from t_prefect where name=?', [linitems[0].strip()])	# retrive 都道府県id
		prefect_id = self.cur.fetchone()[0]

		self.cur.execute('select rowid from t_company where name=?', [linitems[1].strip()])	# retrive 会社id
		company_id = self.cur.fetchone()[0]

		self.cur.execute('select rowid from t_line where name=?', [linitems[2].strip()])		# retrive 路線id
		line_id = self.cur.fetchone()[0]

		station_name = linitems[3].strip()
		samename = linitems[8].strip()
		self.cur.execute('select rowid from t_station where name=? and samename=?', [station_name, samename])
		row = self.cur.fetchone()
		if None != row:
			station_id = row[0]			# 登録済み
		else:
			self.con.execute('insert into t_station values(?, ?, ?, ?, ?, ?)', \
						[ station_name, linitems[4].strip(), company_id, prefect_id, \
						  samename, sflg])
			self.cur.execute('select rowid from t_station where name=? and samename=?', [station_name, samename])
			station_id = self.cur.fetchone()[0]
			self.n_station += 1

		sales_km = int(float(linitems[5]) * 10)
		calc_km = int(float(linitems[6]) * 10)

		self.con.execute('insert into t_lines values(?, ?, ?, ?, ?)', [line_id, station_id, sales_km, calc_km, lflg] )

#------------------------------------------------------------------------------
	def reg_t_clinfar(self, label, linitems, lin):
# 料金表 各路線(N-1)*N/2 N=駅数
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

		sql = "insert into " + label + """
 values((select rowid from t_station where name=? and samename=?),
 		(select rowid from t_station where name=? and samename=?), ?);
"""
		self.con.execute(sql, [station1, station1_s, station2, station2_s, int(linitems[2])])

#------------------------------------------------------------------------------
	def reg_t_rule69(self, label, linitems, lin):
		# t_rule69
		ident = int(linitems[0])

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

		self.con.execute("""
insert into t_rule69(id, station_id1, station_id2, line_id, ord) values(
 ?,
 (select rowid from t_station where name=? and samename=?),
 (select rowid from t_station where name=? and samename=?),
 (select rowid from t_line where name=?), ?)""",
			 [ident, station1, station1_s, station2, station2_s, linitems[3], int(linitems[4])])

#------------------------------------------------------------------------------
	def reg_rule70(self, label, linitems, lin):
	# rule70

		tmp = linitems[0].strip()		# station_id1
		if 0 <= tmp.find('('):
			station1 = tmp[:tmp.find('(')]
			station1_s = tmp[tmp.find('('):]
		else:
			station1 = tmp
			station1_s = ''

		tmp = linitems[1].strip()		# station_id2
		if 0 <= tmp.find('('):
			station2 = tmp[:tmp.find('(')]
			station2_s = tmp[tmp.find('('):]
		else:
			station2 = tmp
			station2_s = ''

		self.con.execute("""
insert into t_rule70 values(
 (select rowid from t_station where name=? and samename=?),
 (select rowid from t_station where name=? and samename=?),
 ?);""",
		[station1, station1_s, station2, station2_s, int(linitems[2])])

#------------------------------------------------------------------------------

	def reg_rule86(self, label, linitems, lin):
	# rule86
		tmp = linitems[1].strip()
		if 0 <= tmp.find('('):
			station = tmp[:tmp.find('(')]
			station_s = tmp[tmp.find('('):]
		else:
			station = tmp
			station_s = ''

		#print(lin, end='')
		self.con.execute("""
insert into t_rule86 values(
 (select rowid from t_line where name=?),
 (select rowid from t_station where name=? and samename=?),
 (select rowid from t_line where name=?), ?);""",
		[linitems[0].strip(), station, station_s, linitems[2].strip(), int(linitems[3])])

#------------------------------------------------------------------------------
	def reg_t_farebspekm(self, label, linitems, lin):
	# t_farebspekm: 3島会社幹線例外
		self.con.execute("""
insert into t_farebspekm values(?, ?, ?, ?, ?, ?, ?)""",
		[int(linitems[0].replace(',', '')), int(linitems[1].replace(',', '')), 
		 int(linitems[2].replace(',', '')), int(linitems[3].replace(',', '')),
		 int(linitems[4].replace(',', '')), int(linitems[5].replace(',', '')),
		 int(linitems[6].replace(',', ''))])
#------------------------------------------------------------------------------
	def reg_t_farelspekm(self, label, linitems, lin):
	# t_farelspekm:地方交通線例外
		self.con.execute("""
insert into t_farelspekm values(?, ?, ?, ?, ?, ?)""",
		[int(linitems[0].replace(',', '')), int(linitems[1].replace(',', '')), 
		 int(linitems[2].replace(',', '')), int(linitems[3].replace(',', '')),
		 int(linitems[4].replace(',', '')), int(linitems[5].replace(',', ''))])
#------------------------------------------------------------------------------
	def reg_t_farels(self, label, linitems, lin):
	# t_farels: 2島会社地方交通線
		if linitems[1].replace(',', '').isdigit():
			skm = int(linitems[1].replace(',', ''))
		else:
			skm = -1
		
		if linitems[2].replace(',', '').isdigit():
			k = int(linitems[2].replace(',', ''))
		else:
			k = -1

		if linitems[3].replace(',', '').isdigit():
			l = int(linitems[3].replace(',', ''))
		else:
			l = -1

		if linitems[4].replace(',', '').isdigit():
			m = int(linitems[4].replace(',', ''))
		else:
			m = -1

		if linitems[5].replace(',', '').isdigit():
			n = int(linitems[5].replace(',', ''))
		else:
			n = -1

		self.con.execute("""
insert into t_farels values(?, ?, ?, ?, ?, ?)""",
		[int(linitems[0].replace(',', '')), skm, k, l, m, n])

#------------------------------------------------------------------------------
	def reg_t_fareadd(self, label, linitems, lin):
	# t_fareadd: 本州3社+3島加算
	
		self.con.execute("insert into " + label + " values(?, ?, ?, ?)",
		[int(linitems[0].replace(',', '')), int(linitems[1].replace(',', '')), 
		 int(linitems[2].replace(',', '')), int(linitems[3].replace(',', ''))])
		# km, ha, sa, ka

#------------------------------------------------------------------------------
	def reg_t_farespp(self, label, linitems, lin):
		# t_farespp: 特定区間通過加算

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
		self.con.execute("""
insert into t_farespp values(
 (select rowid from t_station where name=? and samename=?),
 (select rowid from t_station where name=? and samename=?),
 ?, ?, ?)""",
			[station1, station1_s, station2, station2_s, 
			 int(linitems[2].replace(',', '')), int(linitems[3].replace(',', '')), 
			 int(linitems[4].replace(',', ''))])
		# station_id1, station_id2, fare, kind
#------------------------------------------------------------------------------
	def reg_t_farehla(self, label, linitems, lin):
		# t_farehla : 本州3社+JR北地方交通線会社加算
		# t_farehla5p : 本州3社+JR北地方交通線会社加算(消費税5%版)
		
		self.con.execute("insert into " + label + " values(?, ?)",
		[int(linitems[0].replace(',', '')), int(linitems[1].replace(',', ''))])
		# km, ha
#------------------------------------------------------------------------------

	def last_regist(self):
		for bitem in self.branch:
			#		self.branch.append([linitems[2].strip(), linitems[3].strip(), linitems[4].strip(), 
			#					   linitems[5].strip(), linitems[6].strip(), linitems[8].strip(), linitems[7].strip(), lflg])
			# 0:路線、1:駅、2:分岐駅、3:営業キロ、4:分岐路線、5:同名駅, 6:分岐路線2/分岐駅2, 7:lflg

			if 0 <= bitem[2].find('('):
				bstation = bitem[2][:bitem[2].find('(')]
				bstation_same = bitem[2][bitem[2].find('('):]
			else:
				bstation = bitem[2]
				bstation_same = ''

			if bitem[6]:
				bline2 = bitem[6][:bitem[6].find('/')]					### 分岐駅まで2路線以上(日田彦山線‐小倉の例)
				bstation2t = bitem[6][bitem[6].find('/') + 1:]
				if 0 <= bstation2t.find('('):
					bstation2 = bstation2t[:bstation2t.find('(')]		# 同名駅がある駅の場合
					bstation2_same = bstation2t[bstation2t.find('('):]
				else:
					bstation2 = bstation2t								# 同名駅でない場合
					bstation2_same = ''

				self.con.execute("""
				insert into t_jctspcl(type, jctsp_line_id1, jctsp_station_id1, jctsp_line_id2, jctsp_station_id2) values(
				2,
				(select rowid from t_line where name=?), 
				(select rowid from t_station where name=? and samename=?), 
				(select rowid from t_line where name=?), 
				(select rowid from t_station where name=? and samename=?)) 
				""", 
				[bitem[4], bstation, bstation_same, bline2, bstation2, bstation2_same])
			else:
				self.con.execute("""
				insert into t_jctspcl(type, jctsp_line_id1, jctsp_station_id1) values(
				1,
				(select rowid from t_line where name=?), 
				(select rowid from t_station where name=? and samename=?)) 
				""", 
				[bitem[4], bstation, bstation_same])

			self.con.execute("""insert into t_lines values(
			(select rowid from t_line where name=?), 
			(select rowid from t_station where name=? and samename=?), 
			?,
			(select seq from sqlite_sequence where name='t_jctspcl'), 
			((1 << 31) | (4294967040 & ?) | (255 & (select seq from sqlite_sequence where name='t_jctspcl'))))""", 
			[bitem[0], bitem[1], bitem[5], bitem[3], bitem[7]])
			# b31=special_t_lines ※ lflgはb31=1なのと、b31=1の場合はb15のみ使用される
			# 0xffffff00=4294967040
		# make t_jct
		self.con.execute("""
		insert into t_jct(station_id) select rowid from t_station 
		where (sflg & (1 << 12))!=0
		""")
		# select id from t_jct j join t_station s on s.rowid=j.station_id where name='森';

		##self.con.execute('create view lines as select p.name as prefect, c.name as company, n.name as line, s.name as station, s.kana as station_kana, sales_km, calc_km, spe_route, jctflg, sameflg, cityflg from t_lines l join t_station s on s.rowid=l.station_id join t_line n on n.rowid=l.line_id join t_prefect p on p.rowid=s.prefect_id join t_company c on c.rowid=s.company_id')
		##self.con.execute('create view same_station as select name, count(*) as ''num'' from t_station where sameflg=1 group by name')
		##self.con.execute('create view junctions as select p.name as prefect, c.name as company, n.name as line, s.name as station, s.kana as station_kana, sales_km, calc_km, spe_route, jctflg, sameflg, cityflg from t_lines l join t_station s on s.rowid=l.station_id join t_line n on n.rowid=l.line_id join t_prefect p on p.rowid=s.prefect_id join t_company c on c.rowid=s.company_id where jctflg=1 order by line_id, sales_km')
		##self.con.execute('create view jct_station as select name, cityflg from t_station where jctflg=1')

		self.con.commit()

		self.cur.execute('select max(rowid) from t_station')
		n_db_station = self.cur.fetchone()[0]
		self.cur.execute('select count(*) from t_station')
		assert(n_db_station == self.cur.fetchone()[0])
		assert(n_db_station == self.n_station);

		self.cur.execute('select count(*) from t_line')
		n_line = self.cur.fetchone()[0]

		self.cur.execute('select count(*) from t_lines where line_id in (select rowid from t_line)')
		n_lines = self.cur.fetchone()[0]

		self.cur.execute('select count(*) from t_lines')
		n_dblines = self.cur.fetchone()[0]

		#except sqlite3.IntegrityError:
		#	print("Sqlite3 Integrity Error: current line={0}".format(n_lin))
		#	exit(-1)
		##########################################################

		print("complete success. line={0}, stations={1} affected, lines={2}({3}) affected.".format(n_line, self.n_station, n_lines, n_dblines))

		print()
		print("/* --------------------------------------- */")
		print("#define MAX_STATION	{0}".format(self.n_station))
		print("#define MAX_LINE	{0}".format(n_line))

		#self.cur.execute("select max(rowid) from t_line where name like '%新幹線'")
		#n = self.cur.fetchone()[0]
		print("#define IS_SHINKANSEN_LINE(id)	((0<(id))&&((id)<={0}))".format(self.n_line_Index_of_Shinkansen))
		print("#define IS_COMPANY_LINE(id)	({0}<(id))".format(self.n_line_Index_of_CompanyLine))

		# 以下のクエリー文でも会社線路線かどうか判定可(0でJR、非0で会社線)
		# select count(*) from t_lines where line_id=? and (lflg & (1 << 18))!=0;

		# 以下のクエリー文で会社線路線一覧を得られる
		# select * from t_line where rowid in (select line_id from t_lines where (lflg & (1 << 18))!=0);
		# または以下でも同様の結果が得られる
		# select * from t_line n where exists (select * from t_lines l where l.line_id=n.rowid and (lflg & (1 << 18))!=0);

		self.cur.execute("select count(*) from t_jct")
		n = self.cur.fetchone()[0]
		print("#define MAX_JCT	{0}".format(n))

		self.cur.execute("select max(length(name)) from t_station");
		n = self.cur.fetchone()[0]
		print("#define MAX_STATION_CHR	{0}".format((n+1)*2))

		self.cur.execute("select max(length(name)) from t_line");
		n = self.cur.fetchone()[0]
		print("#define MAX_LINE_CHR	{0}".format((n+1)*2))

		 
		"""
		select t.name from t_station where company_id in (select rowid from t_company name not like 'JR%')

		"""

dbreg = Dbreg('jr.db')
dbreg.create_table()
dbreg.first_regist()
dbreg.second_regist()
dbreg.last_regist()

