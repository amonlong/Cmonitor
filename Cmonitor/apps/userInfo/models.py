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