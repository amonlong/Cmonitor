#-*- coding: utf-8 -*-

from __future__ import absolute_import,unicode_literals
import uuid
import time
from celery import states

from apps.record.models import TaskState, TaskItem
from statTasks.celery import app

from statTasks.subtasks import index, userInfo, business, risk, uniId
 
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

#index mession
@app.task
def indexHead(taskname):
	stime = time.time()
	state, memo = index.indexHead()
	makeRecord(taskname, stime, state, memo)
	return state, memo

@app.task
def indexHopper(taskname):
	stime = time.time()
	state, memo = index.indexHopper()
	makeRecord(taskname, stime, state, memo)
	return state, memo

@app.task
def indexPlace(taskname):
	stime = time.time()
	state, memo = index.indexPlace()
	makeRecord(taskname, stime, state, memo)
	return state, memo

#userInfo mession
@app.task
def userIncrease(taskname):
	stime = time.time()
	state, memo = userInfo.userIncrease()
	makeRecord(taskname, stime, state, memo)
	return state, memo

@app.task
def userAge(taskname):
	stime = time.time()
	state, memo = userInfo.userAge()
	makeRecord(taskname, stime, state, memo)
	return state, memo

#business
@app.task
def flowLoanMoneyNO(taskname):
	stime = time.time()
	state, memo = business.flowLoanMoneyNO()
	makeRecord(taskname, stime, state, memo)
	return state, memo

@app.task
def flowRepayMoney(taskname):
	stime = time.time()
	state, memo = business.flowRepayMoney()
	makeRecord(taskname, stime, state, memo)
	return state, memo

@app.task
def flowDelayRate(taskname):
	stime = time.time()
	state, memo = business.flowDelayRate()
	makeRecord(taskname, stime, state, memo)
	return state, memo

#risk mession
@app.task
def passRate(taskname):
	stime = time.time()
	state, memo = risk.passRate()
	makeRecord(taskname, stime, state, memo)
	return state, memo

@app.task
def overdueRate(taskname):
	stime = time.time()
	state, memo = risk.overdueRate()
	makeRecord(taskname, stime, state, memo)
	return state, memo

#uniId
def productFirm(taskname):
	stime = time.time()
	state, memo = uniId.productFirm()
	makeRecord(taskname, stime, state, memo)
	return state, memo
