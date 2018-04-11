# -*- coding: utf-8 -*-

import datetime

from libfile.dbConfig import MAIN_CONFIG, LOCAL_CONFIG
from libfile.dbModel import dbc
from sql import dashboard as sql
from uniId import liveProduct

def sumIndex():
	try:
		db = dbc(MAIN_CONFIG)
		db.connection()
		livepid, livefirm = liveProduct()
		result = db.select(sql.SUMINDEX.format(livepid, livefirm, livepid, livefirm, livepid, livefirm))
		result = [(str(item['firmId']), item['loanSumMoney'], item['loanSumPeopleNum'], item['unpaidSumMoney'], item['delaySumMoney'], item['createDate']) for item in result]
		db = dbc(LOCAL_CONFIG)
		db.connection()
		db.delete('delete from dashboard_SumIndex where createDate = "{}"'.format(datetime.datetime.now().strftime('%Y-%m-%d')))
		up_sql = """
			insert into dashboard_SumIndex(firmId, loanSumMoney, loanSumPeopleNum, unpaidSumMoney, delaySumMoney, createDate) values (%s,%s,%s,%s,%s,%s)
		"""
		db.update(up_sql, result)
		return 'SUCCESS', ''
	except Exception as e:
		return 'FAILURE', e

def avgIndex():
	try:
		db = dbc(MAIN_CONFIG)
		db.connection()
		livepid, livefirm = liveProduct()
		result = db.select(sql.AVGINDEX.format(livepid, livefirm, livepid, livefirm))
		result = [(str(item['firmId']), item['avgLoanMoney'], item['avgLoanTerm'], 
			item['avgRepayRate'], item['createDate']) for item in result]
		db = dbc(LOCAL_CONFIG)
		db.connection()
		state = db.delete('delete from dashboard_AvgIndex where createDate = "{}"'.format(datetime.datetime.now().strftime('%Y-%m-%d')))
		up_sql = """
			insert into dashboard_AvgIndex(firmId, avgLoanMoney, avgLoanTerm, avgRepayRate, createDate) values (%s,%s,%s,%s,%s)
		"""
		db.update(up_sql, result)
		return 'SUCCESS', ''
	except Exception as e:
		return 'FAILURE', e

def repaidMoney():
	try:
		db = dbc(MAIN_CONFIG)
		db.connection()
		livepid, livefirm = liveProduct()
		result = db.select(sql.REPAIDMONEY.format(livepid, livefirm, livepid, livefirm))
		result = [(str(item['firmId']), item['week'], item['weekdate'], item['paidSumMoney'],
			item['delaySumMoney'], item['paidRate'], item['createDate']) for item in result]
		db = dbc(LOCAL_CONFIG)
		db.connection()
		state = db.delete('delete from dashboard_RepaidMoney where createDate = "{}"'.format(datetime.datetime.now().strftime('%Y-%m-%d')))
		up_sql = """
			insert into dashboard_RepaidMoney(firmId, week, weekDate, paidSumMoney, delaySumMoney, paidRate, createDate) values (%s,%s,%s,%s,%s,%s,%s)
		"""
		db.update(up_sql, result)
		return 'SUCCESS', ''
	except Exception as e:
		return 'FAILURE', e

def overdueDay():
	try:
		db = dbc(MAIN_CONFIG)
		db.connection()
		livepid, livefirm = liveProduct()
		result = db.select(sql.OVERDUEDAY.format(livepid, livefirm))
		result = [(str(item['firmId']), item['overdueDayOnetoThree'], item['overdueDayFourtoTen'], item['overdueDayTentoTwoty'], 
			item['overdueDayTwotytoThreety'], item['overdueDayThreetytoSixty'], item['overdueDaySixtytoNinety'], item['createDate']) for item in result]
		db = dbc(LOCAL_CONFIG)
		db.connection()
		state = db.delete('delete from dashboard_OverdueDay where createDate = "{}"'.format(datetime.datetime.now().strftime('%Y-%m-%d')))
		up_sql = """
			insert into dashboard_OverdueDay(firmId, overdueDayT1, overdueDayT4, overdueDayT11, overdueDayT21, overdueDayT31, overdueDayT61, createDate) values (%s,%s,%s,%s,%s,%s,%s,%s)
		"""
		db.update(up_sql, result)
		return 'SUCCESS', ''
	except Exception as e:
		return 'FAILURE', e

def overdueRate():
	try:
		db = dbc(MAIN_CONFIG)
		db.connection()
		livepid, livefirm = liveProduct()
		result = db.select(sql.OVERDUERATE.format(livepid, livefirm))
		result = [(str(item['firmId']), item['week'], item['weekdate'], item['loanMoney'], item['overdueRateTzero'], item['overdueRateTthree'], 
			item['overdueRateTseven'], item['overdueRateTfourteen'], item['overdueRateTtwentyone'], item['overdueRateMone'], 
			item['overdueRateMtwo'], item['overdueRateMthree'], item['createDate']) for item in result]
		db = dbc(LOCAL_CONFIG)
		db.connection()
		state = db.delete('delete from dashboard_OverdueRate where createDate = "{}"'.format(datetime.datetime.now().strftime('%Y-%m-%d')))
		up_sql = """
			insert into dashboard_OverdueRate(firmId, week, weekDate, loanMoney, overdueRateT0, overdueRateT3, \
			overdueRateT7, overdueRateT14, overdueRateT21, overdueRateM1, overdueRateM2, overdueRateM3, createDate) \
			values (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
		"""
		db.update(up_sql, result)
		return 'SUCCESS', ''
	except Exception as e:
		return 'FAILURE', e

if __name__ == '__main__':
	sumIndex()
	# avgIndex()
	# repaidMoney()
	# overdueDay()
	# overdueRate()