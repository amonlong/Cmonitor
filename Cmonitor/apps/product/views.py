from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.http import JsonResponse
from rest_framework import status

from apps.product.models import ProductFirm
from apps.product.serializers import ProductFirmSerializer

@api_view(['POST'])
def searchProduct(request):
	if request.method == 'POST':
		expos = ProductFirm.objects.all()
		if expos:
			serializer = ProductFirmSerializer(expos, many=True)
			return Response({'code': 0, 'data': serializer.data})
		else:
			return Response({'code': 0, 'data': None}, status=200)
	else:
		return JsonResponse({'code': 1, 'info': 'request method error'}, status=status.HTTP_400_BAD_REQUEST)
