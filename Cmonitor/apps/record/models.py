#-*- coding: utf-8 -*-

from django.db import models
from celery import states
# Create your models here.

TASK_TYPE = sorted(zip(['定时任务', '循环任务'], ['定时任务', '循环任务']))
class TaskItem(models.Model):
	id = models.AutoField(primary_key=True)
	taskname = models.CharField('任务名称', max_length=200, null=True, db_index=True)
	partment = models.CharField('部门', max_length=200, null=True, db_index=True)
	types = models.CharField('任务类型', max_length=64, choices=TASK_TYPE)
	taskfunc = models.CharField('任务函数', max_length=100)
	para =  models.CharField('时间参数', max_length=100, help_text='字典')
	memo = models.CharField('说明', max_length=400)
	is_active = models.IntegerField('是否停止')
	createDate = models.DateTimeField(auto_now_add=True)

	class Meta:
		ordering = ['-createDate']

	def __str__(self):
		return self.taskname

ALL_STATES = sorted(states.ALL_STATES)
TASK_STATE_CHOICES = sorted(zip(ALL_STATES, ALL_STATES))
class TaskState(models.Model):
	task_id = models.CharField('UUID', max_length=36, primary_key=True, db_index=True)
	taskname = models.ForeignKey(TaskItem, on_delete=models.CASCADE)
	state = models.CharField('状态', max_length=64, choices=TASK_STATE_CHOICES, db_index=True)
	memo = models.CharField('备注', max_length=400)
	runtime = models.FloatField('执行时间', null=True, help_text='时间秒')
	createDate = models.DateTimeField(auto_now_add=True)

	class Meta:
		ordering = ['-createDate']

	def __str__(self):
		return self.taskname.taskname

	def getTaskName(self):
		return self.taskname.taskname