from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.db.models import Max
from django.http import JsonResponse
from rest_framework import status

from apps.index.models import IndexHead, IndexHopper, IndexCity
from apps.index.serializers import IndexHeadSerializer, IndexHopperSerializer, IndexCitySerializer

@login_required
def index_view(request):
	return render(request,'index.html')

tableModel = {
	'indexhead': {
			'models': IndexHead,
			'serializers': IndexHeadSerializer,
	},
	'indexhopper': {
			'models': IndexHopper,
			'serializers': IndexHopperSerializer,
	},
	'indexcity': {
			'models': IndexCity,
			'serializers': IndexCitySerializer,
	}
}

@api_view(['POST'])
def searchDashboard(request):
	if request.method == 'POST':
		tables = request.POST.get('table', None)
		if tables:
			objectModel = tableModel[tables]['models']
			objectSerializer = tableModel[tables]['serializers']
			max_year = objectModel.objects.aggregate(Max('createDate'))['createDate__max']
			if max_year:
				expos = AvgIndex.objects.filter(createDate=max_year)
				serializer = AvgIndexSerializer(expos, many=True)
				return Response({'code': 0, 'data': serializer.data})
			else:
				return Response({'code': 0, 'data': None}, status=200)
		else:
			return JsonResponse({'code': 1, 'info': 'input para error'}, status=status.HTTP_400_BAD_REQUEST)
	else:
		return JsonResponse({'code': 1, 'info': 'request method error'}, status=status.HTTP_400_BAD_REQUEST)