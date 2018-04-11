#-*- coding: utf-8 -*-

from __future__ import absolute_import,unicode_literals
import uuid
import time
from celery import states

from record.models import TaskState, TaskItem
from statisticsTasks.celery import app

from statisticsTasks.subtasks import dashboard, performance, report
 
def makeRecord(taskname, stime, state, memo):
	task = TaskItem.objects.filter(taskname=taskname)
	if task:
		sname = taskname + str(time.time())																								
		ts = TaskState(
			task_id = uuid.uuid3(uuid.NAMESPACE_DNS, sname), 
			taskname = task[0], 
			state = state, 
			memo = memo, 
			runtime = time.time() - stime
		)
		ts.save()

#dashboard mession
@app.task
def sumIndex(taskname):
	stime = time.time()
	state, memo = dashboard.sumIndex()
	makeRecord(taskname, stime, state, memo)
	return state, memo

@app.task
def avgIndex(taskname):
	stime = time.time()
	state, memo = dashboard.avgIndex()
	makeRecord(taskname, stime, state, memo)
	return state, memo

@app.task
def repaidMoney(taskname):
	stime = time.time()
	state, memo = dashboard.repaidMoney()
	makeRecord(taskname, stime, state, memo)
	return state, memo

@app.task
def overdueDay(taskname):
	stime = time.time()
	state, memo = dashboard.overdueDay()
	makeRecord(taskname, stime, state, memo)
	return state, memo

@app.task
def overdueRate(taskname):
	stime = time.time()
	state, memo = dashboard.overdueRate()
	makeRecord(taskname, stime, state, memo)
	return state, memo

#performance mession
@app.task
def monthPerformance(taskname):
	stime = time.time()
	state, memo = performance.monthPerformance()
	makeRecord(taskname, stime, state, memo)
	return state, memo

#report mession
@app.task
def allLoan(taskname):
	stime = time.time()
	state, memo = report.allLoan()
	makeRecord(taskname, stime, state, memo)
	return state, memo

@app.task
def weekLoan(taskname):
	stime = time.time()
	state, memo = report.weekLoan()
	makeRecord(taskname, stime, state, memo)
	return state, memo

@app.task
def weekOverdue(taskname):
	stime = time.time()
	state, memo = report.weekOverdue()
	makeRecord(taskname, stime, state, memo)
	return state, memo