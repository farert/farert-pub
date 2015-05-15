#!python3.0.1
# -*- coding: utf-8 -*-

#	—LŒø“ú”

import sys


# ‰c‹ÆƒLƒ‚©‚ç—LŒø“ú”‚ğ“¾‚é

def days_ticket(km):
	if k < 1001:
		return 1

	d = (km + 1999) // 2000 + 1
	return d


db = 0
for k in range(1, 100000):
	d = days_ticket(k)
	if db != d:
		print((k + 9)//10, d)
		db = d
