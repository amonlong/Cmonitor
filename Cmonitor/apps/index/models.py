from django.db import models

# Create your models here.

class IndexHead(models.Model):
	id = models.AutoField(primary_key=True)
	tradeMoney = models.IntegerField(default=0)
	tradeNum = models.IntegerField(default=0)
	activeUser = models.IntegerField(default=0)
	sumUser = models.IntegerField(default=0)
	createDate = models.DateField(auto_now_add=True)

	class Meta:
		ordering = ('createDate',)


class IndexHopper(models.Model):
	id = models.AutoField(primary_key=True)
	register = models.IntegerField(default=0)
	applys = models.IntegerField(default=0)
	passs = models.IntegerField(default=0)
	loan = models.IntegerField(default=0)
	reloan = models.IntegerField(default=0)
	createDate = models.DateField(auto_now_add=True)

	class Meta:
		ordering = ('createDate',)

class IndexCity(models.Model):
	id = models.AutoField(primary_key=True)
	cityName = models.CharField(max_length=32,default='china')
	numInCity = models.IntegerField(default=0)
	createDate = models.DateField(auto_now_add=True)

	class Meta:
		ordering = ('createDate',)
