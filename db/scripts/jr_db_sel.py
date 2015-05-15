#!python3.0.1
# -*- coding: utf-8 -*-

import sqlite3

dbname = 'jr.db'con = sqlite3.connect(dbname, isolation_level=None)

c = con.cursor()
c.execute("select * from t_prefect")
for row in c: # rowはtuple
    print(row[0])
c.execute("select * from t_company")
for row in c: # rowはtuple
    print(row[0])

c.execute("select * from t_line")
for row in c: # rowはtuple
    print(row[0])
