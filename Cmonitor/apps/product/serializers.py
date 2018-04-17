from rest_framework import serializers

from apps.product.models import ProductFirm

class ProductFirmSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductFirm
        fields = ('firmId', 'productId', 'title')