#!python3.0.1
# -*- coding: utf-8 -*-
import sqlite3
con = sqlite3.connect("data.db")


sql = """
create table t_emp (
  名前 varchar(10),
  年齢 integer,
  部署 varchar(200)
);
"""

con.execute(sql)


sql = "insert into t_emp values ('橋本', 26, '広報部')"
con.execute(sql)


sql = "insert into t_emp values (?, ?, ?)"
con.execute(sql, ("小泉", 35, "営業部"))
con.execute(sql, ("亀井", 40, "営業部"))

con.executemany("insert into t_emp values (?, ?, ?)",
                [("小泉", 35, "営業部"),
                 ("亀井", 40, "営業部")])
                 
c = con.cursor()
c.execute("select * from t_emp")
for row in c: # rowはtuple
    print(row[0], row[1], row[2])

