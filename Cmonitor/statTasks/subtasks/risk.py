# -*- coding: utf-8 -*-

import datetime
import pandas as pd
from libfile.dbConfig import MAIN_CONFIG, LOCAL_CONFIG
from libfile.dbModel import dbc
from uniId import timeScale

def passRate():
	try:
		timeList = timeScale()
		db = dbc(LOCAL_CONFIG)
		db.connection()
		result = db.select('select distinct createDate from risk_RiskPassRate')
		tmwait = [str(item['createDate']) for item in result]

		for i in range(len(timeList)-1):

			db = dbc(MAIN_CONFIG)
			db.connection()

			stTime = timeList[i]
			edTime = timeList[i+1]

			if stTime in tmwait:
				continue

			print('用户通过率数据更新： ' + stTime + '~' + edTime)

			sql = """
		 		select status,count(*) 'num' 
		 		from ci_cash_apply_info 
		 		where create_time > '{}' and create_time < '{}'
		 		GROUP BY status
			""".format(stTime,edTime)
			result = db.select(sql)
			passNum = 0
			applyNum = 0
			for item in result:
				if item['status'] == 'SUCCESS':
					passNum = item['num']
				else:
					pass
				applyNum += item['num']
			passRate = passNum/applyNum*100 if applyNum else 0

			#数据插入
			result = [(applyNum,passNum,passRate,stTime)]
			db = dbc(LOCAL_CONFIG)
			db.connection()
			up_sql = """ insert into risk_RiskPassRate(applyNum,passNum,passRate,createDate) values (%s,%s,%s,%s) """
			db.update(up_sql, result)
		return 'SUCCESS', ''
	except Exception as e:
		return 'FAILURE', e
def overdueRate():
	try:
		db = dbc(MAIN_CONFIG)
		db.connection()
		sql = """
			SELECT termDate
				, round(100 - paidMoneyZero / termMoney * 100, 2) AS overdueRateTzero
				, round(100 - paidMoneyThree / termMoney * 100, 2) AS overdueRateTthree
				, round(100 - paidMoneySeven / termMoney * 100, 2) AS overdueRateTseven
				, round(100 - paidMoneyFourteen / termMoney * 100, 2) AS overdueRateTfourteen
				, round(100 - paidMoneyTwentyone / termMoney * 100, 2) AS overdueRateTtwentyone
				, round(100 - paidMoneyThreety / termMoney * 100, 2) AS overdueRateMone
				, round(100 - paidMoneySixty / termMoney * 100, 2) AS overdueRateMtwo
				, round(100 - paidMoneyNinety / termMoney * 100, 2) AS overdueRateMthree
				, CURDATE() AS createDate
			FROM (
			SELECT l1.termDate
				, SUM(l1.lendMoney) AS termMoney
				, SUM(CASE WHEN l1.overdueday <= 0 THEN l1.lendMoney ELSE 0 END) AS paidMoneyZero
				, SUM(CASE WHEN l1.overdueday <= 3 THEN l1.lendMoney ELSE 0 END) AS paidMoneyThree
				, SUM(CASE WHEN l1.overdueday <= 7 THEN l1.lendMoney ELSE 0 END) AS paidMoneySeven
				, SUM(CASE WHEN l1.overdueday <= 14 THEN l1.lendMoney ELSE 0 END) AS paidMoneyFourteen
				, SUM(CASE WHEN l1.overdueday <= 21 THEN l1.lendMoney ELSE 0 END) AS paidMoneyTwentyone
				, SUM(CASE WHEN l1.overdueday <= 30 THEN l1.lendMoney ELSE 0 END) AS paidMoneyThreety
				, SUM(CASE WHEN l1.overdueday <= 60 THEN l1.lendMoney ELSE 0 END) AS paidMoneySixty
				, SUM(CASE WHEN l1.overdueday <= 90 THEN l1.lendMoney ELSE 0 END) AS paidMoneyNinety
			FROM (
			SELECT lr.termDate
				, l.lendMoney
				, lr.repaidTime
				, IF(lr.repaidTime IS NULL, DATEDIFF(CURDATE(),lr.termDate), DATEDIFF(lr.repaidTime,lr.termDate)) AS overdueday
			FROM loan_repaying lr, loan l
				WHERE lr.loanId = l.id
					AND lr.compatibleStatus NOT IN ('CANCEL')
					AND l.status = 6
					AND lr.termDate < CURDATE()
			) l1
			GROUP BY l1.termDate
			) s1
		"""
		result = db.select(sql)
		result = [(item['overdueRateTzero'], item['overdueRateTthree'], item['overdueRateTseven'], item['overdueRateTfourteen'], item['overdueRateTtwentyone'], item['overdueRateMone'],
			item['overdueRateMtwo'], item['overdueRateMthree'], item['termDate'], item['createDate']) for item in result]
		db = dbc(LOCAL_CONFIG)
		db.connection()
		db.delete('delete from risk_RiskOverDueRate')
		up_sql = """
			insert into risk_RiskOverDueRate(delayRate0, delayRate3, delayRate7, delayRate14, delayRate21, delayRateM1, delayRateM2, delayRateM3, \
			termDate, createDate) \
			values (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
		"""
		db.update(up_sql, result)
		return 'SUCCESS', ''
	except Exception as e:
		print(e)
		return 'FAILURE', e
if __name__ == '__main__':
	#passRate()
	overdueRate()