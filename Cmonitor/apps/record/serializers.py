from rest_framework import serializers
from apps.record.models import TaskItem, TaskState

class TaskItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = TaskItem
        fields = ('id', 'taskname', 'partment', 'types', 'taskfunc', 'para', 'memo', 'is_active', 'createDate')

class TaskStateSerializer(serializers.ModelSerializer):
    class Meta:
        model = TaskState
        fields = ('task_id', 'getTaskName', 'state', 'memo', 'runtime', 'createDate')
