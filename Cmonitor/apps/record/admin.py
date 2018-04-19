from django.contrib import admin
from apps.record.models import TaskItem, TaskState

# Register your models here.

admin.site.register(TaskItem)
admin.site.register(TaskState)

