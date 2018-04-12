from django.db import models

# Create your models here.

class FlowLoanMoneyNO(models.Model):
	id = models.AutoField(primary_key=True)
	loanOld = models.IntegerField(default=0)
	loanNew = models.IntegerField(default=0)
	createDate = models.DateField(auto_now_add=True)

	class Meta:
		ordering = ('createDate',)

class FlowPaidMoney(models.Model):
	id = models.AutoField(primary_key=True)
	paidMoney = models.IntegerField(default=0)
	createDate = models.DateField(auto_now_add=True)

	class Meta:
		ordering = ('createDate',)

class FlowDelayRate(models.Model):
	id = models.AutoField(primary_key=True)
	delayRate0 = models.FloatField(default=0.0)
	delayRate3 = models.FloatField(default=0.0)
	delayRate7 = models.FloatField(default=0.0)
	delayRate14 = models.FloatField(default=0.0)
	delayRate21 = models.FloatField(default=0.0)
	delayRateM1 = models.FloatField(default=0.0)
	delayRateM2 = models.FloatField(default=0.0)
	delayRateM3 = models.FloatField(default=0.0)
	createDate = models.DateField(auto_now_add=True)

	class Meta:
		ordering = ('createDate',)