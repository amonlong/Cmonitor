from django.db import models

# Create your models here.

class UserIncrease(models.Model):
	id = models.AutoField(primary_key=True)
	register = models.IntegerField(default=0)
	allow = models.IntegerField(default=0)
	newApply = models.IntegerField(default=0)
	oldApply = models.IntegerField(default=0)
	createDate = models.DateField(auto_now_add=True)

	class Meta:
		ordering = ('createDate',)

class UserAge(models.Model):
	id = models.AutoField(primary_key=True)
	age1 = models.IntegerField('18岁及以下', default=0)
	age2 = models.IntegerField('19-25岁', default=0)
	age3 = models.IntegerField('26-33岁', default=0)
	age4 = models.IntegerField('34-41岁', default=0)
	age5 = models.IntegerField('42岁及以上', default=0)
	createDate = models.DateField('日期', auto_now_add=True)

	class Meta:
		ordering = ('createDate',)