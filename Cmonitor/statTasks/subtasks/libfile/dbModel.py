# -*- coding: utf-8 -*-

import pymysql.cursors


class dbc():
	'''
    数据库操作
    :param config:
    :return result:
    '''
	def __init__(self, param):
		self.config = {
			'host': param.get('host', None),
			'port': param.get('port', None),
			'user': param.get('user', None),
			'password': param.get('password', None),
			'db': param.get('db', None),
			'charset': 'utf8mb4',
			'cursorclass': pymysql.cursors.DictCursor,
		}

	def connection(self):
		self.connection = pymysql.connect(**self.config)

	def select(self, sql):
		result = None
		try:
			with self.connection.cursor() as cursor:
				cursor.execute(sql)
				result = cursor.fetchall()
				self.connection.commit()
		except Exception as e:  
			raise e
		return result

	def update(self, sql, values):
		result = None
		try:
			with self.connection.cursor() as cursor:
				result = cursor.executemany(sql,values)
				self.connection.commit()
		except Exception as e:
			raise e
		finally:
			self.connection.close()
		return result

	def delete(self, sql):
		state = None
		try:
			with self.connection.cursor() as cursor:
				state = cursor.execute(sql)
				self.connection.commit()
		except Exception as e:  
			raise e
		return state