import pymysql
import csv

conn = pymysql.connect(host='localhost', user='root', password='1234', db='testdb', charset='utf8')
curs = conn.cursor()
conn.commit()

f = open('cinema.csv', 'r', encoding='cp949')
rd = csv.reader(f)

for line in rd:
    sql = "insert into Cine values("
    sql += "%s," * 14
    sql += "%s)"
    curs.execute(sql,line)
conn.commit()

f.close()
conn.close()