from rest_framework import serializers
from apps.index.models import IndexHead, IndexHopper, IndexCity

class IndexHeadSerializer(serializers.ModelSerializer):
    class Meta:
        model = IndexHead
        fields = ('tradeMoney', 'tradeNum', 'activeUser', 'sumUser')

class IndexHopperSerializer(serializers.ModelSerializer):
    class Meta:
        model = IndexHopper
        fields = ('register', 'applys', 'passs', 'loan', 'reloan')

class IndexCitySerializer(serializers.ModelSerializer):
    class Meta:
        model = IndexCity
        fields = ('cityName', 'numInCity')