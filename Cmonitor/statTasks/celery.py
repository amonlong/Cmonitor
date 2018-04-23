#-*- coding: utf-8 -*-

from __future__ import absolute_import,unicode_literals
from celery import Celery, platforms
from kombu import Exchange, Queue

platforms.C_FORCE_ROOT = True
 
app = Celery('statTasks',
             broker= 'amqp://guest:guest@localhost//',#消息代理
             include=['statTasks.tasks'])#添加tasks.py

# 定义一个交换机
monitor_exchange = Exchange('monitor', type='direct')

# 创建1个队列
app.conf.task_queues = (
    Queue('monitor', exchange=monitor_exchange, routing_key='monitor')
)
 
app.config_from_object('statTasks.config') #加载Celery配置到config.py文件
if __name__ == '__main__':
    app.start()