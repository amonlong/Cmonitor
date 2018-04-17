from django.db import models

# Create your models here.

class ProductFirm(models.Model):
	id = models.AutoField(primary_key=True)
	firmId = models.IntegerField(default=0)
	productId = models.IntegerField(default=0)
	title = models.CharField(max_length=100)
	createDate = models.DateField(auto_now_add=True)

	class Meta:
		ordering = ('createDate',)