#!python3.0.1
# -*- coding: utf-8 -*-

"""
並行在来線を得る

東海道新幹線 小田原

"""
import sys
import os
import jrdb

sql = """
select line_id from t_hzline where rowid=(select (lflg>>13)&15 from t_lines where line_id=?1 and station_id=?2)
"""

# result list
for inf in jrdb.sqlexec(sql, [ jrdb.line_id(sys.argv[1]), 
							   jrdb.station_id(sys.argv[2]) ] ):
	print("", jrdb.line_name(inf[0]))


