#!python3.0.1
# -*- coding: utf-8 -*-


import os
import sys


if 1 < len(sys.argv):
  fn = sys.argv[1] 
else:
  fn = 'tk70.txt'

items = []
for lin in open(fn, 'r', encoding='shift-jis'):
	items.append(lin)

wf = open('tk70_def.txt', 'w', encoding='shift-jis');
items_ = items
a = []
for item_ in items_:
	a.append(item_)
	for item in items:
		if item not in a:
			wf.write(item_.strip("\r\n ") + '\t' + item)

