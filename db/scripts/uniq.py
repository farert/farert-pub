# -*- coding: shift-jis -*-

"""
北海道	JR北海道	函館線	函館駅	はこだて	0	0	 	
"""


import sys
import re
from collections import defaultdict

if 1 < len(sys.argv):
  fn = sys.argv[1] 
else:
  fn = 'jr.txt'

h_prefect = {}
h_company = {}
h_trline = {}

for lin in open(fn, 'r'):
	linitems = lin.split('\t')
	h_prefect[linitems[0]] = '.'	# pref
	h_company[linitems[1]] = '.'	# company
	h_trline[linitems[2]] = '.'		# line

for pref in h_prefect:
	print(pref)


for company in h_company:
	print(company)

for trline in sorted(h_trline.keys()):
	print(trline)

