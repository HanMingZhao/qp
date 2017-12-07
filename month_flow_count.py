import pymysql as db
import config
import xlwt

cf = config.product
src_con = db.connect(user=cf['user'], host=cf['host'], passwd=cf['pass'], port=cf['port'], charset=cf['charset'])
src_cur = src_con.cursor()

workbook = xlwt.Workbook()







src_cur.close()
src_con.close()
