from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.db.models import Max
from django.http import JsonResponse
from rest_framework import status

from apps.risk.models import RiskPassRate, RiskOverDueRate
from apps.risk.serializers import RiskPassRateSerializer, RiskOverDueRateSerializer

@login_required
def passRate_view(request):
	return render(request,'riskPassRate.html')

@login_required
def overdueRate_view(request):
	return render(request,'riskOverdueRate.html')

tableModel = {
	'passRate': {
			'models': RiskPassRate,
			'serializers': RiskPassRateSerializer,
	},
	'overdueRate': {
			'models': RiskOverDueRate,
			'serializers': RiskOverDueRateSerializer,
	}
}

@api_view(['POST'])
def searchRisk(request):
	if request.method == 'POST':
		tables = request.POST.get('table', None)
		if tables:
			objectModel = tableModel[tables]['models']
			objectSerializer = tableModel[tables]['serializers']
			expos = objectModel.objects.all()
			if expos:
				serializer = objectSerializer(expos, many=True)
				return Response({'code': 0, 'data': serializer.data})
			else:
				return Response({'code': 0, 'data': None}, status=200)
		else:
			return JsonResponse({'code': 1, 'info': 'input para error'}, status=status.HTTP_400_BAD_REQUEST)
	else:
		return JsonResponse({'code': 1, 'info': 'request method error'}, status=status.HTTP_400_BAD_REQUEST)
