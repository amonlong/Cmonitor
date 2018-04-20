# -*- coding: utf-8 -*-

import datetime
import pandas as pd
import json
import os

from libfile.dbConfig import MAIN_CONFIG, LOCAL_CONFIG
from libfile.dbModel import dbc
import config

def indexHead():
	try:
		db = dbc(MAIN_CONFIG)
		db.connection()

		sql = """select count(*) 'num' from user where date_created > '2018-01-01' """
		result = db.select(sql)
		registerNum = result[0]['num']

		sql = """select count(DISTINCT userSid) 'num' from loan where status=6 and createdTime > '2018-01-01' """
		result = db.select(sql)
		loanNum = result[0]['num']

		sql = """select count(*) 'num' from loan where status=6 and createdTime > '2018-01-01' """
		result = db.select(sql)
		tradeNum = result[0]['num']

		sql = """select sum(lendMoney) 'num' from loan where status=6 and createdTime > '2018-01-01' """
		result = db.select(sql)
		tradeMoney = result[0]['num']

		nowdate = datetime.datetime.now().strftime('%Y-%m-%d')
		result = [(registerNum,loanNum,tradeNum,tradeMoney,nowdate)]

		db = dbc(LOCAL_CONFIG)
		db.connection()
		db.delete('delete from index_IndexHead where createDate = "{}"'.format(nowdate))
		up_sql = """ insert into index_IndexHead(sumUser,activeUser,tradeNum,tradeMoney,createDate) values (%s,%s,%s,%s,%s) """
		db.update(up_sql, result)
		return 'SUCCESS', ''
	except Exception as e:
		return 'FAILURE', e

def indexHopper():
	try:
		db = dbc(MAIN_CONFIG)
		db.connection()

		sql = """select count(*) 'num' from user where date_created > '2018-01-01' """
		result = db.select(sql)
		registerNum = result[0]['num']

		sql = """
			select count(distinct cc.user_id) 'num' 
			from ci_cash_apply_info cc, user uu 
			where cc.user_id = uu.id 
			and uu.date_created > '2018-01-01'
		"""
		result = db.select(sql)
		applyNum = result[0]['num']

		sql = """
			select count(DISTINCT user_id) 'num' 
			from ci_cash_apply_info cc,user uu
			where cc.user_id = uu.id 
			and uu.date_created > '2018-01-01'
			and cc.status in ('FA_SUCCESS','SUCCESS')
			"""
		result = db.select(sql)
		passNum = result[0]['num']

		sql = """
			select count(DISTINCT userSid) 'num' 
			from loan l,user uu
			where l.userSid=uu.id and l.status=6 and uu.date_created > '2018-01-01'
		"""
		result = db.select(sql)
		loanNum = result[0]['num']

		sql = """
			select count(*) 'num' from ( 
				select userSid,count(1) 'num' 
				from loan ll,user uu
				where ll.userSid=uu.id and ll.status=6 and uu.date_created > '2018-01-01'
				group by ll.userSid ) l 
			where l.num > 1
		"""
		result = db.select(sql)
		reloanNum = result[0]['num']

		nowdate = datetime.datetime.now().strftime('%Y-%m-%d')
		result = [(registerNum,applyNum,passNum,loanNum,reloanNum,nowdate)]

		db = dbc(LOCAL_CONFIG)
		db.connection()
		db.delete('delete from index_IndexHopper where createDate = "{}"'.format(nowdate))
		up_sql = """ insert into index_IndexHopper(register,applys,passs,loan,reloan,createDate) values (%s,%s,%s,%s,%s,%s) """
		db.update(up_sql, result)
		return 'SUCCESS', ''
	except Exception as e:
		return 'FAILURE', e

def indexPlace():
	try:
		db = dbc(MAIN_CONFIG)
		db.connection()

		sql = """
			select aes_decrypt(a.id_num,'1zhida**') 'id_num' from _user a,loan b where a.id=b.userSid and a.id_num is not null and b.status=6 ;
		"""
		result = db.select(sql)
		result = [item['id_num'].decode('utf-8') for item in result]
		data = pd.DataFrame()
		data['id_num'] = result
		id_init = pd.read_csv(os.path.dirname(os.path.abspath(__file__)) + '/data/t_id_card_init.csv')
		id_init['code'] = id_init['code'].map(str)
		province = id_init[id_init['code'].map(lambda x:str(x)[-4:]=='0000')]
		province1 = province[province['name'].map(lambda x: '北京'in x or '上海' in x or '天津'in x or '重庆' in x)]   
		province2 = province[province['name'].map(lambda x: '市' not in x)] 
		province = pd.concat([province1,province2])
		city = id_init[id_init['code'].map(lambda x:str(x)[-2:]=='00')]
		data['province_t'] = data['id_num'].map(lambda x:str(x)[:2]+'0000')
		data['city_t'] = data['id_num'].map(lambda x:str(x)[:4]+'00')
		data['country_t'] = data['id_num'].map(lambda x:str(x)[:6])
		data = pd.merge(data,province,left_on='province_t',right_on='code',how='left')
		data['省'] = data['name']
		del data['code']
		del data['name']
		data = pd.merge(data,city,left_on='city_t',right_on='code',how='left')
		data['市'] = data['name']
		del data['code']
		del data['name']
		del data['province_t']
		del data['city_t']
		del data['country_t']
		data["人数"] = 1
		tp = pd.pivot_table(data,index=['省','市'],values=["人数"],aggfunc='count',fill_value=0)
		tp['省'] = tp.index.map(lambda x :x[0])
		tp['市'] = tp.index.map(lambda x :x[1])
		tp = tp.sort_values(by="人数",ascending=False)
		tp = tp.reset_index(drop=True)

		city = config.CITY
		cityName = []
		cityNum = []
		for i in range(50,-1,-1):
			item = tp.ix[i]
			key = item['省'] + item['市']
			if city.get(key,None) is not None:
				cityName.append(city.get(key))
				cityNum.append(int(item['人数']))

		nowdate = datetime.datetime.now().strftime('%Y-%m-%d')
		ctime = [nowdate]*len(cityName)

		db = dbc(LOCAL_CONFIG)
		db.connection()
		db.delete('delete from index_IndexCity where createDate = "{}"'.format(nowdate))
		up_sql = """ insert into index_IndexCity(cityName,numInCity,createDate) values (%s,%s,%s) """
		result = zip(cityName,cityNum,ctime)
		db.update(up_sql, result)
		return 'SUCCESS', ''
	except Exception as e:
		return 'FAILURE', e

if __name__ == '__main__':
	#indexHopper()
	#indexHead()
	indexPlace()