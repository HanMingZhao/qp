import pymysql as db
import config
import xlwt
import time

cf = config.product
connect = db.connect(host=cf['host'], user=cf['user'], passwd=cf['pass'], db=cf['db'], port=cf['port'],
                     charset=cf['charset'])
cursor = connect.cursor()
workbook = xlwt.Workbook()

start_time = time.time()
print('start scanning...')
history_sql = '''
SELECT CONCAT(mmu.nick_name,mmu.user_limit),a.account_name,a.plat_name,IF(b.flow-a.flow>0,b.flow-a.flow,0),b.update_time 
FROM ( 
SELECT mpa.user_id,mfh.account_id,mfh.plat_id,mfh.account_name,mfh.plat_name,SUM(mfh.flow_count) `flow`,mfh.update_time 
FROM med_flow_history mfh 
LEFT JOIN med_plat_account mpa 
ON mpa.`account_id` = mfh.`account_id` 
WHERE mpa.`rank_id` IN (8,9,10,11,12,13,14,15,16,17,18,19) 
AND mfh.update_time >= '2017-12-{} 00:00:00' 
AND mfh.update_time <= '2017-12-{} 01:00:00' 
GROUP BY mfh.account_id,mfh.plat_id,mfh.update_time 
)a 
INNER JOIN (
SELECT mfh.account_id,mfh.plat_id,mfh.account_name,mfh.plat_name,SUM(mfh.flow_count) `flow`,mfh.update_time 
FROM med_flow_history mfh 
LEFT JOIN med_plat_account mpa 
ON mpa.`account_id` = mfh.`account_id` 
WHERE mpa.`rank_id` IN (8,9,10,11,12,13,14,15,16,17,18,19) 
AND mfh.update_time >= '2017-12-{} 00:00:00' 
AND mfh.update_time <= '2017-12-{} 01:00:00' 
GROUP BY mfh.account_id,mfh.plat_id,mfh.update_time 
)b 
ON a.account_id=b.account_id  
LEFT JOIN mng_manager_user mmu 
ON mmu.muid = a.user_id 
WHERE b.update_time > a.update_time 
AND (UNIX_TIMESTAMP(b.update_time)-UNIX_TIMESTAMP(a.update_time))/60/60 <5
'''
start = '01'
end = '08'
cursor.execute(history_sql.format(start, end, start, end))
result = cursor.fetchall()
print('scanning over...', time.time()-start_time)
sheet = workbook.add_sheet('sheet')
sheet.write(0, 0, '用户')
sheet.write(0, 1, '平台')
sheet.write(0, 2, '帐号')
sheet.write(0, 3, '流量增量')
sheet.write(0, 4, '时间')
for i, r in enumerate(result):
    sheet.write(i+1, 0, r[0])
    sheet.write(i+1, 1, r[2])
    sheet.write(i+1, 2, r[1])
    sheet.write(i+1, 3, r[3])
    sheet.write(i+1, 4, r[4].strftime('%Y-%m-%d %H:%M:%s'))
print('write over...', time.time()-start_time)
workbook.save('12{}history.xls'.format(start))
cursor.close()
connect.close()
