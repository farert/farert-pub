#!python3.0.1
# -*- coding: utf-8 -*-
import sqlite3
con = sqlite3.connect("jr.db", isolation_level=None)


cur = con.cursor()
s = '福島x県'
cur.execute("select rowid from t_prefect where name=?", [s])
if cur.fetchone():
	prefect_id = cur.fetchone()[0]
else:
	prefect_id = -1

print(prefect_id)


cur.execute('insert into test values(?, ?)', ['nfforiyuki', 92])
print(cur.lastrowid)

