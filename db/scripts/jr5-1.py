# -*- coding: shift-jis -*-

"""
路線一意下
JR北海道	函館本線	0		函館駅	はこだて	 
JR北海道	函館本線	3.4		五稜郭駅	ごりょうかく	■江差線
JR北海道	函館本線	8.3		桔梗駅	ききょう	 
 :

北海道	JR北海道	函館線	函館駅	はこだて	0	0	 	分岐路線	分岐路線フラグ	同名	都区市内

- 分岐路線フラグが合っているか
- 同名フラグが合っているか
- 都区市内別一覧表示

札幌市内	1
仙台市内	2
都区内	3
山手線内	4
横浜市内	5
名古屋市内	6
京都市内	7
大阪市内	8
神戸市内	9
広島市内	10
北九州市内	11
福岡市内	12

"""
import sys
import re
from collections import defaultdict


if 1 < len(sys.argv):
  fn = sys.argv[1] 
else:
  fn = 'jr.txt'

ln = 0
toku = ([], [], [], [], [], [], [], [], [], [], [], [] )
dupstations = []

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


	i = int(linitems[9])
	if i == 1:
		dupstations.append(eki + '(' + linitems[0] + ');' + linitems[2])
	elif i != 0:
		print("{0}({1}) 同名駅フラグ不正={2}".format(fn, ln, i))


	i = int(linitems[10])
	if len(toku) < i:
		print("{0}({1}) 都区市内コード不正={2}".format(fn, ln, i))
	elif 0 < i:
		toku[i - 1].append("{0}({1})".format(linitems[3], linitems[2]))


	if linitems[7].strip() != "":
		train_lines.extend( linitems[7].split('/'))
		if 1 != int(linitems[8]):
			print("{0}({1}) 分岐路線フラグ不正(1であるべきが{2})".format(fn, ln, int(linitems[8])))
	else:
		if 0 != int(linitems[8]):
			print("{0}({1}) 分岐路線フラグ不正(0であるべきが{2})".format(fn, ln, int(linitems[8])))

	train_lines = [y for y in train_lines if y.strip() != '']
	train_lines = list(map(lambda r:r.strip(), train_lines))
	
	train_lines.sort()									 # 路線、分岐路線群の配列ソート
	if branch[eki] != "":
		branch[eki] += ","
  
	branch[eki] += "|".join(train_lines)   # 各駅毎に路線、分岐路線群を|区切りの文字列で保持


print("＊＊＊都区市内一覧＊＊＊")
s = """
札幌市内
仙台市内
都区内
山手線内
横浜市内
名古屋市内
京都市内
大阪市内
神戸市内
広島市内
北九州市内
福岡市内
"""
stoku = s.split('\n')[1:-1]

for i in range(len(toku)):
	print("***{0}***".format(stoku[i]))
	for e in toku[i]:
		print(e)


# h_keys  各駅登場回数を保持
# branch  各駅所属路線を保持
#
dup_e = []
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
					dup_e.append(e)
				elif len(station_lines) != h_eki[e]:
					print("  {0}駅{1}/{2}: 分岐路線数の相違 {3}, {4}: {5}".format(e, n_eki, len(bra), len(station_lines), h_eki[e], '/'.join(station_lines)))

			if other_station_lines != station_lines and len(station_lines) != 1:
				print("  {0}駅{1}/{2}: 分岐路線不足: {3}, {4}".format(e, n_eki, len(bra), '/'.join(other_station_lines), '/'.join(station_lines)))
			elif len(station_lines) == 1:
				print("               {0}".format('/'.join(station_lines)))

	else: # 駅1個(分岐なし)
		if 1 < len(bra[0]):
			print("駅一個なのに分岐駅？ {0}:{1}->{2}".format(e, len(bra), bra[0]))


print("＊＊＊同名駅一覧＊＊＊")
dupstations.sort()
for el in dupstations:
	e = el[0:el.index('(')]
	if e in dup_e:
		print(el + '*')
		del dup_e[dup_e.index(e)]
	else:
		print(el)
		
print('=======')
for e in dup_e:
	print(e)
