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
				and user_id not in (select distinct user_id from ci_cash_apply_info where create_time < '{}');
			""".format(stTime,edTime,stTime)
			result = db.select(sql)
			newApplyNum = result[0]['num']

			sql = """
				select count(distinct user_id) 'num' from ci_cash_apply_info 
				where create_time > '{}' and create_time < '{}' 
				and user_id in (select distinct user_id from ci_cash_apply_info where create_time < '{}');
			""".format(stTime,edTime,stTime)
			result = db.select(sql)
			oldApplyNum = result[0]['num']

			#授信
			sql = """
		 		select count(distinct user_id) 'num' from ci_cash_apply_info where audit_date > '{}' and audit_date < '{}' and status in ('SUCCESS')
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

if __name__ == '__main__':
	userIncrease()