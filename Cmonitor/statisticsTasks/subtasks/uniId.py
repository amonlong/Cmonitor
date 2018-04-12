# -*- coding: utf-8 -*-

import datetime

def timeScale(startTime = "2018-01-01"):
	nowTime = datetime.date.today()
	i = 0
	timeList = []
	while True:
		endTime = str(nowTime-datetime.timedelta(days=i))
		timeList.insert(0,endTime)
		if endTime == startTime:
			break
		i = i + 1
	return timeList

if __name__ == '__main__':
	liveProduct()