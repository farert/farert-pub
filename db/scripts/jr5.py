# -*- coding: shift-jis -*-

"""
路線一意下
JR北海道	函館本線	0		函館駅	はこだて	 
JR北海道	函館本線	3.4		五稜郭駅	ごりょうかく	■江差線
JR北海道	函館本線	8.3		桔梗駅	ききょう	 
 :

北海道	JR北海道	函館線	函館駅	はこだて	0	0	 	

駅名で、駅という文字が混じっている駅
重複駅名

を抽出

"""
import sys
import re
from collections import defaultdict


if 1 < len(sys.argv):
  fn = sys.argv[1] 
else:
  fn = 'jr.txt'

ln = 0
r1 = re.compile('駅.*駅')
r2 = re.compile('.+駅\Z')
e1 = []
e2 = []

branch = defaultdict(str)
h_eki = defaultdict(int)

for lin in open(fn, 'r'):
	ln += 1
	if ln == 1: continue
	linitems = lin.split('\t')
	eki = linitems[3]		# 駅
	h_eki[eki] += 1
	train_lines = []
	train_lines.append(linitems[2])    # 路線 
	if linitems[7].strip != "":
		train_lines.extend( linitems[7].split('/'))

	train_lines = [y for y in train_lines if y.strip() != '']
	train_lines = list(map(lambda r:r.strip(), train_lines))
	
	train_lines.sort()									 # 路線、分岐路線群の配列ソート
	if branch[eki] != "":
		branch[eki] += ","
  
	branch[eki] += "|".join(train_lines)   # 各駅毎に路線、分岐路線群を|区切りの文字列で保持

	if r1.match(eki):   # 駅を含む駅
		e1.append("{0}({1}): {2}".format(fn, ln, eki))

	if not (r2.match(eki)): # 駅で終わっていない駅
		e2.append("{0}({1}): {2}".format(fn, ln, eki) )

print("＊＊＊駅という文字が複数＊＊＊")
for e in e1:
   print(e)

#print("＊＊＊駅という文字で終わっていない＊＊＊")
#e2.each do |e|
#   print(e)
#end
print("＊＊＊重複駅名 or 分岐駅(所属路線が複数)＊＊＊")
# 江差線|函館線,江差線|函館線
# 函館線

# h_keys  各駅登場回数を保持
# branch  各駅所属路線を保持
#
for e in h_eki.keys():			# 各駅毎
	bra = branch[e].split(",")   # 駅が2回以上ある場合, braに個数分の所属路線の配列が入る
	bra = list(map(lambda r:r.split("|"), bra))  #bra.map! {|r| r.split("|") }
	
	if 1 < h_eki[e]: # 分岐駅 or 2度以上登場した駅 e
		if len(bra) != h_eki[e]:
			print("!!!!!!!!!bug!!!!! #{0}:#{1}".format(e, len(bra)))

		print("{0}({1})".format(e, h_eki[e]))   # 駅名(登場数)
		other_station_lines = False
		n_eki = 0
		
		for station_lines in bra:		# 同名駅毎
			n_eki += 1
			if False == other_station_lines:
				other_station_lines = station_lines
				if len(station_lines) <= 0:
					print("!!!!!bug!!!!!")
				elif len(station_lines)  == 1:
					print("  {0}駅{1}/{2}: 駅複数なのに分岐駅なし(同名駅)".format(e, n_eki, len(bra)))
				elif len(station_lines) != h_eki[e]:
					print("  {0}駅{1}/{2}: 分岐路線数の相違 {3}, {4}: {5}".format(e, n_eki, len(bra), len(station_lines), h_eki[e], '/'.join(station_lines)))

			if other_station_lines != station_lines and len(station_lines) != 1:
				print("  {0}駅{1}/{2}: 分岐路線不足: {3}, {4}".format(e, n_eki, len(bra), '/'.join(other_station_lines), '/'.join(station_lines)))
			elif len(station_lines) == 1:
				print("               {0}".format('/'.join(station_lines)))

	else: # 駅1個(分岐なし)
		if 1 < len(bra[0]):
			print("駅一個なのに分岐駅？ {0}:{1}->{2}".format(e, len(bra), bra[0]))


