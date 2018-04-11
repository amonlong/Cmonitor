# -*- coding: utf-8 -*-

from libfile.dbConfig import MAIN_CONFIG, LOCAL_CONFIG
from libfile.dbModel import dbc

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

if __name__ == '__main__':
	liveProduct()