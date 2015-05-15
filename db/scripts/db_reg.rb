#! ruby -Ku=beginデータベース登録=endrequire 'sqlite'db = SQLite3::Database.new("data.db")sql = <<SQL
create table 社員 (
  名前 varchar(10),
  年齢 integer,
  部署 varchar(200)
);
SQL
db.execute(sql)sql = "insert into 社員 values ('橋本', 26, '広報部')"
db.execute(sql)sql = "insert into 社員 values (?, ?, ?)"
db.execute(sql, '小泉', 35, '営業部')
db.execute(sql, '亀井', 40, '営業部')
db.execute('select * from 社員') do |row|
  #rowは結果の配列
  puts row.join("\t")
enddb.close