from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.db.models import Max
from django.http import JsonResponse
from rest_framework import status

from apps.business.models import FlowLoanMoneyNO, FlowPaidMoney, FlowDelayRate
from apps.business.serializers import FlowLoanMoneyNOSerializer, FlowDelayRateSerializer, FlowPaidMoneySerializer

@login_required
def flowLoan_view(request):
	return render(request,'flowLoan.html')

@login_required
def flowDelayRate_view(request):
	return render(request,'flowDelayRate.html')

tableModel = {
	'flowLoanMoneyNO': {
			'models': FlowLoanMoneyNO,
			'serializers': FlowLoanMoneyNOSerializer,
	},
	'flowPaidMoney': {
			'models': FlowPaidMoney,
			'serializers': FlowPaidMoneySerializer,
	},
	'flowDelayRate': {
			'models': FlowDelayRate,
			'serializers': FlowDelayRateSerializer,
	}
}

@api_view(['POST'])
def searchBussiness(request):
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