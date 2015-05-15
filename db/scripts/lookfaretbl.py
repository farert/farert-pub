#!python3.0.1
# -*- coding: utf-8 -*-

"""
fare table ref.


"""
import sys
import os
import jrdb
import time

if len(sys.argv) == 2:
	sql = """
	select km from t_farem where km<=? order by km desc limit(1);
	"""

	for inf in jrdb.sqlexec(sql, [ sys.argv[1] ] ):
		print(inf[0])

else:
	# skm, dkm

	sql = """
select k,l from t_farels where dkm=?2 and (skm=-1 or skm=?1)
"""
	#                                  skm        dkm
	for inf in jrdb.sqlexec(sql, [ sys.argv[1], sys.argv[2] ] ):
		print(inf[0], inf[1])
	



