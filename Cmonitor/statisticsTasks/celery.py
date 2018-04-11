#-*- coding: utf-8 -*-

from __future__ import absolute_import,unicode_literals
from celery import Celery, platforms

platforms.C_FORCE_ROOT = True
 
app = Celery('statisticsTasks',
             broker= 'amqp://guest:guest@localhost//',#消息代理
             include=['statisticsTasks.tasks'])#添加tasks.py
 
app.config_from_object('statisticsTasks.config') #加载Celery配置到config.py文件
if __name__ == '__main__':
    app.start()