from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.http import JsonResponse
from rest_framework import status

from apps.record.models import TaskItem, TaskState
from apps.record.serializers import TaskItemSerializer, TaskStateSerializer

from statTasks import tasks 
# Create your views here.

def task_view(request):
	return render(request, 'task.html')

def taskRecord_view(request):
	return render(request, 'taskRecord.html')

@api_view(['GET'])
def runTaskfunc_view(request):
	if request.method == 'GET':
		func = request.GET.get('taskfunc', None)
		taskname = request.GET.get('taskname', None)
		if func and taskname:
			func = func + '("' + taskname + '")'
			#func = func + '("' + taskname + '").delay()'
			try:
				state, info = eval(func)
				info = 'RUN ' + str(state) + '!\n' + str(info)
			except Exception as e:
				info = str(e)
			return JsonResponse({'info': info}, status=200)
		else:	
			return JsonResponse({'info': 'parameter error'}, status=200)
	else:
		return JsonResponse({'info': 'request method error'}, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
def searchTaskItem(request):
	if request.method == 'GET':
		taskitem = TaskItem.objects.all()
		if taskitem:
			serializer = TaskItemSerializer(taskitem, many=True)
			return Response(serializer.data)
		else:
			return JsonResponse({'info': None}, status=200)

@api_view(['GET'])
def searchTaskState(request):
	if request.method == 'GET':
		taskstate = TaskState.objects.all()
		if taskstate:
			serializer = TaskStateSerializer(taskstate, many=True)
			return Response(serializer.data)
		else:
			return JsonResponse({'info': None}, status=200)

