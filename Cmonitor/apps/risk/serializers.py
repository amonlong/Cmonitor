from rest_framework import serializers

from apps.risk.models import RiskPassRate, RiskOverDueRate

class RiskPassRateSerializer(serializers.ModelSerializer):
    class Meta:
        model = RiskPassRate
        fields = ('applyNum', 'passNum', 'passRate', 'createDate')

class RiskOverDueRateSerializer(serializers.ModelSerializer):
    class Meta:
        model = RiskOverDueRate
        fields = ('delayRate0', 'delayRate3', 'delayRate7', 'delayRate14', 'delayRate21', 'delayRateM1', 'delayRateM2', 'delayRateM3', 'termDate')
