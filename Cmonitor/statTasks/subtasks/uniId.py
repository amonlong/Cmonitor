# -*- coding: utf-8 -*-

import datetime

from libfile.dbConfig import MAIN_CONFIG, LOCAL_CONFIG
from libfile.dbModel import dbc

def timeScale(startTime = "2018-01-01"):
	nowTime = datetime.date.today()
	i = 0
	timeList = []
	while True:
		endTime = str(nowTime-datetime.timedelta(days=i))
		timeList.insert(0,endTime)
		if endTime == startTime:
			break
		i = i + 1
	return timeList

def liveProduct():
	try:
		db = dbc(MAIN_CONFIG)
		db.connection()
		sql = """
			select lp.id as 'productId', lp.firmId from loan_product lp, loan_account_type lat
			where lp.accountType = lat.type and lat.parentType = 301
		"""
		result = db.select(sql)
		firmId = [str(item['firmId']) for item in result]
		productId = [str(item['productId']) for item in result]
		plist = "','".join(productId)
		flist = "','".join(firmId)
		return plist, flist
	except Exception as e:
		return None

def productFirm():
	try:
		db = dbc(MAIN_CONFIG)
		db.connection()
		sql = """
			select lp.id as 'productId', lp.firmId, lp.title from loan_product lp, loan_account_type lat
			where lp.accountType = lat.type and lat.parentType = 301
		"""
		result = db.select(sql)
		result = [(item['firmId'],item['productId'],item['title'],datetime.datetime.now().strftime('%Y-%m-%d')) for item in result]
		db = dbc(LOCAL_CONFIG)
		db.connection()
		db.delete('delete from product_ProductFirm')
		up_sql = """ insert into product_ProductFirm(firmId,productId,title,createDate) values (%s,%s,%s,%s) """
		db.update(up_sql, result)
		return 'SUCCESS', ''
	except Exception as e:
		return 'FAILURE', e

if __name__ == '__main__':
	productFirm()