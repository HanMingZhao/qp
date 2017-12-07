import pymysql as db
import config
import xlwt
import time

cf = config.product
src_con = db.connect(user=cf['user'], host=cf['host'], passwd=cf['pass'], port=cf['port'], charset=cf['charset'],
                     db=cf['db'])
src_cur = src_con.cursor()

workbook = xlwt.Workbook()

start = time.time()

count_sql = '''
SELECT t.account_name,t.plat_name,COUNT(1) FROM 
(
SELECT mfh.account_name,mfh.account_id,mfh.plat_name,mfh.plat_id,mfh.title_name 
FROM med_flow_history mfh
LEFT JOIN med_plat_account mpa
ON mpa.`account_id` = mfh.`account_id`
WHERE mpa.`rank_id` IN (8,9,10,11,12,13,14,15,16,17,18,19) 
AND add_time >='2017-11-1' 
AND add_time < '2017-11-3' 
GROUP BY title_name
)t
GROUP BY t.account_id,t.plat_id
'''
src_cur.execute(count_sql)
print(time.time()-start)
result = src_cur.fetchall()
for r in result:
    print(r)

src_cur.close()
src_con.close()
