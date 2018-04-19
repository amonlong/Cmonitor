# -*- coding: utf-8 -*-

import datetime
import pandas as pd
from libfile.dbConfig import MAIN_CONFIG, LOCAL_CONFIG
from libfile.dbModel import dbc
from uniId import timeScale, liveProduct

def flowLoanMoneyNO():
	try:
		timeList = timeScale()
		db = dbc(LOCAL_CONFIG)
		db.connection()
		result = db.select('select distinct createDate from business_FlowLoanMoneyNO')
		tmwait = [str(item['createDate']) for item in result]

		db = dbc(MAIN_CONFIG)
		db.connection()
		livepid, livefirm = liveProduct()

		for i in range(len(timeList)-1):

			db = dbc(MAIN_CONFIG)
			db.connection()

			stTime = timeList[i]
			edTime = timeList[i+1]

			if stTime in tmwait:
				continue

			#借贷金额
			print('借贷金额(新老)数据更新：' + stTime + '~' + edTime)
			#old
			sql = """
				select l.firmId
				, l.productId 
				, sum(l.payMoney) 'money'
				from loan_repaying lr,loan l
				where lr.loanId = l.id
				and lr.compatibleStatus <> 'CANCEL' and l.status = 6 
				and lr.createdTime >= '{}' and lr.createdTime < '{}'
				and lr.productId in ('{}')
				and lr.firmId in ('{}')
				and l.userSid in (select distinct userSid from loan_repaying where createdTime < '{}')
				group by l.firmId,l.productId
			""".format(stTime,edTime,livepid,livefirm,stTime)
			loanOld = db.select(sql)

			#new
			sql = """
				select l.firmId
				, l.productId 
				, sum(l.payMoney) 'money'
				from loan_repaying lr,loan l
				where lr.loanId = l.id
				and lr.compatibleStatus <> 'CANCEL' and l.status = 6 
				and lr.createdTime >= '{}' and lr.createdTime < '{}'
				and lr.productId in ('{}')
				and lr.firmId in ('{}')
				and l.userSid not in (select distinct userSid from loan_repaying where createdTime < '{}')
				group by l.firmId,l.productId
			""".format(stTime,edTime,livepid,livefirm,stTime)
			loanNew = db.select(sql)

			loan_dict = {}
			
			#数据插入
			for item in loanOld:
				temp = {'loanOld': 0, 'loanNew': 0, 'createDate': stTime}
				if not loan_dict.get(item['firmId']):
					temp['loanOld'] = item['money'] if item['money'] else 0
					loan_dict[item['firmId']] = temp
				else:
					loan_dict[item['firmId']]['loanOld'] = item['money'] if item['money'] else 0

			for item in loanNew:
				temp = {'loanOld': 0, 'loanNew': 0, 'createDate': stTime}
				if not loan_dict.get(item['firmId']):
					temp['loanNew'] = item['money'] if item['money'] else 0
					loan_dict[item['firmId']] = temp
				else:
					loan_dict[item['firmId']]['loanNew'] = item['money'] if item['money'] else 0

			result = []
			for key,values in loan_dict.items():
				result.append((key,values['loanOld'],values['loanNew'],values['createDate']))
			db = dbc(LOCAL_CONFIG)
			db.connection()
			up_sql = """ insert into business_FlowLoanMoneyNO(firmId,loanOld,loanNew,createDate) values (%s,%s,%s,%s) """
			db.update(up_sql, result)
		return 'SUCCESS', ''
	except Exception as e:
		return 'FAILURE', e

def flowRepayMoney():
	try:
		timeList = timeScale()
		db = dbc(LOCAL_CONFIG)
		db.connection()
		result = db.select('select distinct createDate from business_FlowRepayMoney')
		tmwait = [str(item['createDate']) for item in result]

		db = dbc(MAIN_CONFIG)
		db.connection()
		livepid, livefirm = liveProduct()

		for i in range(len(timeList)-1):

			db = dbc(MAIN_CONFIG)
			db.connection()

			stTime = timeList[i]
			edTime = timeList[i+1]

			if stTime in tmwait:
				continue

			print('应还实还数据更新：' + stTime)
			sql = """
				select firmId,productId,sum(repayMoney) 'money' from loan_repaying
				where termDate='{}' and compatibleStatus not in ('CANCEL')
				and productId in ('{}') and firmId in ('{}')
				group by firmId, productId
			""".format(stTime, livepid, livefirm)
			allRepayMoney = db.select(sql)

			sql = """
				select firmId,productId,sum(repayMoney) 'money' from loan_repaying
				where termDate='{}' and compatibleStatus not in ('CANCEL') 
				and repaidTime is not null and DATE_FORMAT(termDate,'%Y-%m-%d') >= DATE_FORMAT(repaidTime,'%Y-%m-%d')
				and productId in ('{}') and firmId in ('{}')
				group by firmId, productId
			""".format(stTime, livepid, livefirm)
			acRepayMoney = db.select(sql)

			loan_dict = {}
			
			#数据插入
			for item in allRepayMoney:
				temp = {'allRepayMoney': 0, 'acRepayMoney': 0, 'createDate': stTime}
				if not loan_dict.get(item['firmId']):
					temp['allRepayMoney'] = item['money'] if item['money'] else 0
					loan_dict[item['firmId']] = temp
				else:
					loan_dict[item['firmId']]['allRepayMoney'] = item['money'] if item['money'] else 0

			for item in acRepayMoney:
				temp = {'allRepayMoney': 0, 'acRepayMoney': 0, 'createDate': stTime}
				if not loan_dict.get(item['firmId']):
					temp['acRepayMoney'] = item['money'] if item['money'] else 0
					loan_dict[item['firmId']] = temp
				else:
					loan_dict[item['firmId']]['acRepayMoney'] = item['money'] if item['money'] else 0

			result = []
			for key,values in loan_dict.items():
				repayRate = 0 if values['allRepayMoney'] == 0 else int(values['acRepayMoney']/values['allRepayMoney']*100)
				result.append((key, values['allRepayMoney'], values['acRepayMoney'], repayRate, values['createDate']))

			db = dbc(LOCAL_CONFIG)
			db.connection()
			up_sql = """ insert into business_FlowRepayMoney(firmId,allRepayMoney,acRepayMoney,repayRate,createDate) values (%s,%s,%s,%s,%s) """
			db.update(up_sql, result)
		return 'SUCCESS', ''
	except Exception as e:
		return 'FAILURE', e

def flowDelayRate():
	try:
		db = dbc(MAIN_CONFIG)
		db.connection()
		livepid, livefirm = liveProduct()
		sql = """
			SELECT productId,firmId,termDate
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
			SELECT l1.productId,l1.firmId,l1.termDate
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
			SELECT l.productId
				, l.firmId
				, lr.termDate
				, l.lendMoney
				, lr.repaidTime
				, IF(lr.repaidTime IS NULL, DATEDIFF(CURDATE(),lr.termDate), DATEDIFF(lr.repaidTime,lr.termDate)) AS overdueday
			FROM loan_repaying lr, loan l
				WHERE lr.loanId = l.id
					AND lr.compatibleStatus NOT IN ('CANCEL')
					AND l.status = 6
					AND lr.termDate < CURDATE()
					AND l.productId in ('{}')
					AND l.firmId in ('{}')
			) l1
			GROUP BY l1.productId,l1.firmId,l1.termDate
			) s1
		"""
		result = db.select(sql.format(livepid, livefirm))
		result = [(item['firmId'], item['overdueRateTzero'], item['overdueRateTthree'], item['overdueRateTseven'], item['overdueRateTfourteen'], item['overdueRateTtwentyone'], item['overdueRateMone'],
			item['overdueRateMtwo'], item['overdueRateMthree'], item['termDate'], item['createDate']) for item in result]
		db = dbc(LOCAL_CONFIG)
		db.connection()
		db.delete('delete from business_FlowDelayRate')
		up_sql = """
			insert into business_FlowDelayRate(firmId, delayRate0, delayRate3, delayRate7, delayRate14, delayRate21, delayRateM1, delayRateM2, delayRateM3, \
			termDate, createDate) \
			values (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
		"""
		db.update(up_sql, result)
		return 'SUCCESS', ''
	except Exception as e:
		return 'FAILURE', e

if __name__ == '__main__':
	flowLoanMoneyNO()
	flowRepayMoney()
	flowDelayRate()