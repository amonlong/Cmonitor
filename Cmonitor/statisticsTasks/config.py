#-*- coding: utf-8 -*-
import django
django.setup()

from celery.schedules import crontab
from datetime import timedelta
from record.models import TaskItem 

CELERY_ENABLE_UTC = False # 不是用UTC
CELERY_TIMEZONE = 'Asia/Shanghai'
# CELERYD_LOG_FILE = BASE_DIR + "/log/celery/celery.log" # log路径
# CELERYBEAT_LOG_FILE = BASE_DIR + "/log/celery/beat.log" # beat log路径

def makeSchedule():
	tdict = {}
	taskitem = TaskItem.objects.filter(is_active=0)
	if taskitem:
		for item in taskitem:
			temp = {}
			hour, minute = eval(item.para).get('hour', 0), eval(item.para).get('minute', 0)
			temp['task'] = 'statisticsTasks.' + item.taskfunc
			#temp['schedule'] = timedelta(seconds=5)
			temp['schedule'] = crontab(hour=hour, minute=minute)
			temp['args'] = (item.taskname,)

			tdict[item.taskname] = temp
	return tdict
			
CELERYBEAT_SCHEDULE = makeSchedule()
# CELERYBEAT_SCHEDULE = {
#     'add-every-30-seconds': {
#         'task': 'statisticsTasks.tasks.test',#任务
#         'schedule': crontab(hour=14, minute=33),#timedelta(seconds=5),#时间
#         'args': ('任务1',)#参数
#     },
# }

