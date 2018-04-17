# -*- coding: utf-8 -*-

import datetime
import pandas as pd
from libfile.dbConfig import MAIN_CONFIG, LOCAL_CONFIG
from libfile.dbModel import dbc
from uniId import timeScale

def userIncrease():
	try:
		timeList = timeScale()
		db = dbc(LOCAL_CONFIG)
		db.connection()
		result = db.select('select distinct createDate from userInfo_UserIncrease')
		tmwait = [str(item['createDate']) for item in result]

		for i in range(len(timeList)-1):

			db = dbc(MAIN_CONFIG)
			db.connection()

			stTime = timeList[i]
			edTime = timeList[i+1]

			if stTime in tmwait:
				continue

			print('用户增长数据更新： ' + stTime + '~' + edTime)

			#注册
			sql = """
				select count(1) 'num' from user where date_created > '{}' and date_created < '{}'
			""".format(stTime,edTime)
			result = db.select(sql)
			registerNum = result[0]['num']

			#申请（新老）
			sql = """
				select count(distinct user_id) 'num' from ci_cash_apply_info 
				where create_time > '{}' and create_time < '{}' 
			""".format(stTime,edTime)
			result = db.select(sql)
			allApplyNum = result[0]['num']

			sql = """
				select count(distinct user_id) 'num' from ci_cash_apply_info 
				where create_time > '{}' and create_time < '{}' 
				and user_id in (select distinct user_id from ci_cash_apply_info where create_time < '{}');
			""".format(stTime,edTime,stTime)
			result = db.select(sql)
			oldApplyNum = result[0]['num']

			newApplyNum = allApplyNum - oldApplyNum

			#授信
			sql = """
		 		select count(distinct user_id) 'num' from ci_cash_apply_info where create_time > '{}' and create_time < '{}' and status in ('SUCCESS')
			""".format(stTime,edTime)
			result = db.select(sql)
			allowNum = result[0]['num']

			#数据插入
			result = [(registerNum,allowNum,newApplyNum,oldApplyNum,stTime)]
			db = dbc(LOCAL_CONFIG)
			db.connection()
			up_sql = """ insert into userInfo_UserIncrease(register,allow,newApply,oldApply,createDate) values (%s,%s,%s,%s,%s) """
			db.update(up_sql, result)
		return 'SUCCESS', ''
	except Exception as e:
		return 'FAILURE', e

def userAge():
	try:
		timeList = timeScale()
		db = dbc(LOCAL_CONFIG)
		db.connection()
		result = db.select('select distinct createDate from userInfo_UserAge')
		tmwait = [str(item['createDate']) for item in result]

		for i in range(len(timeList)-1):

			db = dbc(MAIN_CONFIG)
			db.connection()

			stTime = timeList[i]
			edTime = timeList[i+1]

			if stTime in tmwait:
				continue

			print('用户年龄数据更新： ' + stTime + '~' + edTime)

			sql = """
				select SUM(case when age <= 18 then 1 else 0 end) 'age1'
				, SUM(case when age > 18 and age <= 25  then 1 else 0 end) 'age2' 
				, SUM(case when age > 25 and age <= 33 then 1 else 0 end) 'age3'
				, SUM(case when age > 33 and age <= 42 then 1 else 0 end) 'age4'
				, SUM(case when age > 42 then 1 else 0 end) 'age5'
				from user 
				where date_created > '{}' and date_created < '{}' and age is not null
			""".format(stTime,edTime)
			result = db.select(sql)
			age1 = result[0]['age1'] if result[0]['age1'] else 0
			age2 = result[0]['age2'] if result[0]['age2'] else 0
			age3 = result[0]['age3'] if result[0]['age3'] else 0
			age4 = result[0]['age4'] if result[0]['age4'] else 0
			age5 = result[0]['age5'] if result[0]['age5'] else 0
			#数据插入
			result = [(age1,age2,age3,age4,age5,stTime)]
			db = dbc(LOCAL_CONFIG)
			db.connection()
			up_sql = """ insert into userInfo_UserAge(age1,age2,age3,age4,age5,createDate) values (%s,%s,%s,%s,%s,%s) """
			db.update(up_sql, result)
		return 'SUCCESS', ''
	except Exception as e:
		return 'FAILURE', e

if __name__ == '__main__':
	userIncrease()
	userAge()