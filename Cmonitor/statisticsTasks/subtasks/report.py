# -*- coding: utf-8 -*-

import datetime

from libfile.dbConfig import MAIN_CONFIG, LOCAL_CONFIG
from libfile.dbModel import dbc
from sql import report as sql

from uniId import liveProduct

def allLoan():
	try:
		db = dbc(MAIN_CONFIG)
		db.connection()
		livepid, livefirm = liveProduct()
		result = db.select(sql.ALLLOAN.format(livepid, livefirm, livepid, livefirm, livepid, livefirm))
		result = [(item['firmId'], item['week'], item['weekDate'], item['allLoanCount'], item['allLoanMoney'], item['allPayMoney'], 
			item['allPaidCount'], item['allPaidMoney'], item['allNoPaidCount'], item['allNoPaidMoney'], item['createDate']) for item in result]
		db = dbc(LOCAL_CONFIG)
		db.connection()
		db.delete('delete from report_AllLoan where createDate = "{}"'.format(datetime.datetime.now().strftime('%Y-%m-%d')))
		for item in result:
			db.delete('delete from report_AllLoan where firmId="{}" and week="{}"'.format(item[0], item[1]))
		up_sql = """
			insert into report_AllLoan(firmId, week, weekDate, allLoanCount, allLoanMoney, allPayMoney, allPaidCount, allPaidMoney, allNoPaidCount, allNoPaidMoney, createDate) \
			values (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
		"""
		db.update(up_sql, result)
		return 'SUCCESS', ''
	except Exception as e:
		return 'FAILURE', e

def weekLoan():
	try:
		db = dbc(MAIN_CONFIG)
		db.connection()
		livepid, livefirm = liveProduct()
		result = db.select(sql.WEEKLOAN.format(livepid, livefirm, livepid, livefirm))
		result = [(item['firmId'], item['week'], item['weekdate'], item['weekLoanCount'], item['weekLoanMoney'],
			item['weekPayMoney'], item['weekPaidCount'], item['weekPaidMoney'], item['createDate']) for item in result]
		db = dbc(LOCAL_CONFIG)
		db.connection()
		db.delete('delete from report_WeekLoan where createDate = "{}"'.format(datetime.datetime.now().strftime('%Y-%m-%d')))
		up_sql = """
			insert into report_WeekLoan(firmId, week, weekDate, weekLoanCount, weekLoanMoney, weekPayMoney, weekPaidCount, weekPaidMoney, createDate) \
			values (%s,%s,%s,%s,%s,%s,%s,%s,%s)
		"""
		db.update(up_sql, result)
		return 'SUCCESS', ''
	except Exception as e:
		return 'FAILURE', e

def weekOverdue():
	try:
		db = dbc(MAIN_CONFIG)
		db.connection()
		livepid, livefirm = liveProduct()
		result = db.select(sql.WEEKOVERDUE.format(livepid, livefirm))
		result = [(item['firmId'], item['week'], item['weekdate'], item['termMoney'], item['overdueMoneyTseven'],
			item['overdueMoneyTfourteen'], item['overdueMoneyTtwentyone'], item['overdueMoneyMone'], item['overdueMoneyMtwo'],
			item['overdueMoneyMthree'], item['overdueRateTseven'], item['overdueRateTfourteen'], item['overdueRateTtwentyone'],
			item['overdueRateMone'], item['overdueRateMtwo'], item['overdueRateMthree'], item['createDate']) for item in result]
		db = dbc(LOCAL_CONFIG)
		db.connection()
		db.delete('delete from report_WeekOverDue where createDate = "{}"'.format(datetime.datetime.now().strftime('%Y-%m-%d')))
		up_sql = """
			insert into report_WeekOverDue(firmId, week, weekDate, termMoney, overdueMoneyT7, overdueMoneyT14, overdueMoneyT21, overdueMoneyM1, \
			overdueMoneyM2, overdueMoneyM3, overdueRateT7, overdueRateT14, overdueRateT21, overdueRateM1, overdueRateM2, overdueRateM3, createDate) \
			values (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
		"""
		db.update(up_sql, result)
		return 'SUCCESS', ''
	except Exception as e:
		return 'FAILURE', e

if __name__ == '__main__':
	allLoan()
	#weekLoan()
	#weekOverdue()