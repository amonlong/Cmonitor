# -*- coding: utf-8 -*-

import datetime

from libfile.dbConfig import MAIN_CONFIG, C2C_CONFIG, LOCAL_CONFIG
from libfile.dbModel import dbc
from sql import performance as sql
from uniId import liveProduct

def monthPerformance():
	try:
		db = dbc(C2C_CONFIG)
		db.connection()
		lender = db.select(" select id,username,firmId from lender ")
		lenderdict = {}
		firmdict = {}
		for item in lender:
			lenderdict[item['id']] = item['username']
			firmdict[item['id']] = item['firmId']

		db = dbc(MAIN_CONFIG)
		db.connection()
		livepid, livefirm = liveProduct()
		result = db.select(sql.MONTHPERFORMANCE.format(livepid, livefirm, livepid, livefirm))
		result = [(item['lenderId'], firmdict.get(item['lenderId'], None), lenderdict.get(item['lenderId'], None), item['month'], item['sumPayMoney'], 
			item['sumPaidMoney'], item['reward'], item['createDate']) for item in result if lenderdict.get(item['lenderId'], None)]
		db = dbc(LOCAL_CONFIG)
		db.connection()
		db.delete('delete from performance_MonthPerformance where createDate = "{}"'.format(datetime.datetime.now().strftime('%Y-%m-%d')))
		up_sql = """
			insert into performance_MonthPerformance(lenderId, firmId, lenderName, month, sumPayMoney, sumPaidMoney, reward, createDate) \
			values (%s,%s,%s,%s,%s,%s,%s,%s)
		"""
		db.update(up_sql, result)
		return 'SUCCESS', ''
	except Exception as e:
		return 'FAILURE', e

if __name__ == '__main__':
	monthPerformance()