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
SELECT date(t.add_time),t.name,t.account_name,t.plat_name,COUNT(1) FROM 
(
SELECT concat(mmu.nick_name,mmu.user_limit) `name`,mfh.account_name,mfh.account_id,mfh.plat_name,mfh.plat_id,
mfh.title_name,mfh.add_time 
FROM med_flow mfh
LEFT JOIN med_plat_account mpa
ON mpa.`account_id` = mfh.`account_id`
left join mng_manager_user mmu
on mpa.user_id = mmu.muid
WHERE mpa.`rank_id` IN (8,9,10,11,12,13,14,15,16,17,18,19) 
AND mfh.add_time >='2017-11-1' 
AND mfh.add_time < '2017-12-1' 
GROUP BY mfh.title_name
)t
GROUP BY t.account_id,t.plat_id,date(t.add_time)
'''
src_cur.execute(count_sql)
print(time.time()-start)
result = src_cur.fetchall()
sheet = workbook.add_sheet('发文数量')
sheet.write(0, 0, '日期')
sheet.write(0, 1, '用户')
sheet.write(0, 2, '账号')
sheet.write(0, 3, '平台')
sheet.write(0, 4, '数量')
sheet.write(0, 5, '日均发文')
for i, r in enumerate(result):
    sheet.write(i+1, 0, r[0].strftime(config.date_format))
    sheet.write(i+1, 1, r[1])
    sheet.write(i+1, 2, r[2])
    sheet.write(i+1, 3, r[3])
    sheet.write(i+1, 4, r[4])

sum_sql = '''
select t.time,t.name,t.account_name,t.plat_name,sum(t.flow) from
(
SELECT date(mfh.add_time) `time`,concat(mmu.nick_name,mmu.user_limit) `name`, mfh.account_name,mfh.account_id,mfh.plat_name,mfh.plat_id,
mfh.title_name,max(mfh.`flow_count`) flow
FROM med_flow mfh
LEFT JOIN med_plat_account mpa
ON mpa.`account_id` = mfh.`account_id`
left join mng_manager_user mmu
on mpa.user_id = mmu.muid
WHERE mpa.`rank_id` IN (8,9,10,11,12,13,14,15,16,17,18,19) 
AND mfh.add_time >='2017-11-1' 
AND mfh.add_time < '2017-12-1' 
GROUP BY mfh.title_name
)t
group by t.account_id,t.plat_id,t.time
'''
src_cur.execute(sum_sql)
print(time.time()-start)
result = src_cur.fetchall()
sheet = workbook.add_sheet('流量')
sheet.write(0, 0, '日期')
sheet.write(0, 1, '用户')
sheet.write(0, 2, '账号')
sheet.write(0, 3, '平台')
sheet.write(0, 4, '流量')
sheet.write(0, 5, '日均流量')
for i, r in enumerate(result):
    sheet.write(i+1, 0, r[0].strftime(config.date_format))
    sheet.write(i+1, 1, r[1])
    sheet.write(i+1, 2, r[2])
    sheet.write(i+1, 3, r[3])
    sheet.write(i+1, 4, r[4])

workbook.save('month_flow.xls')
src_cur.close()
src_con.close()
