# -*- coding: shift-jis -*-

"""
路線一意下
JR北海道	函館本線	0		函館駅	はこだて	 
JR北海道	函館本線	3.4		五稜郭駅	ごりょうかく	■江差線
JR北海道	函館本線	8.3		桔梗駅	ききょう	 
 :

北海道	JR北海道	函館線	函館駅	はこだて	0	0	 	

各フィールドの最大文字数を取得(UTF-8バイト）


"""
import sys

if 1 < len(sys.argv):
  fn = sys.argv[1] 
else:
  fn = 'jr.txt'

ln = 0
max_width_company = 0
max_width_prefect = 0
max_width_line = 0
max_width_station = 0
max_width_station_kana = 0
max_width_jct = 0
max_width_jct_num = 0

for lin in open(fn, 'r'):
	ln += 1
	if ln == 1: continue
	linitems = lin.split('\t')

	width = len(linitems[1].strip().encode()) # company
	if max_width_company < width:
		max_width_company = width

	width = len(linitems[0].strip().encode()) # prefect
	if max_width_prefect < width:
		max_width_prefect = width

	width = len(linitems[2].strip().encode()) # 線
	if max_width_line < width:
		max_width_line = width

	width = len(linitems[3].strip().encode()) # 駅
	if max_width_station < width:
		max_width_station = width

	width = len(linitems[4].strip().encode()) # 駅kana
	if max_width_station_kana < width:
		max_width_station_kana = width

	width = len(linitems[7].strip().encode()) # jct
	if max_width_jct < width:
		max_width_jct = width

	train_lines = [y for y in linitems[7].split('/') if y.strip() != '']
	train_lines = list(map(lambda r:r.strip(), train_lines))

	if max_width_jct_num < len(train_lines):
		max_width_jct_num = len(train_lines)


print("company max width {0} bytes.".format(max_width_company))
print("prefect max width {0} bytes.".format(max_width_prefect))
print("line max width {0} bytes.".format(max_width_line))
print("station max width {0} bytes.".format(max_width_station))
print("station_kana max width {0} bytes.".format(max_width_station_kana))
print("jct max width {0} bytes.".format(max_width_jct))
print("jct_num max width {0}.".format(max_width_jct_num))


