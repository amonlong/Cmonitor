from rest_framework import serializers

from apps.business.models import FlowLoanMoneyNO, FlowRepayMoney, FlowDelayRate

class FlowLoanMoneyNOSerializer(serializers.ModelSerializer):
    class Meta:
        model = FlowLoanMoneyNO
        fields = ('loanOld', 'loanNew', 'createDate')

class FlowDelayRateSerializer(serializers.ModelSerializer):
    class Meta:
        model = FlowDelayRate
        fields = ('delayRate0', 'delayRate3', 'delayRate7', 'delayRate14', 'delayRate21', 'delayRateM1', 'delayRateM2', 'delayRateM3', 'termDate')

class FlowRepayMoneySerializer(serializers.ModelSerializer):
    class Meta:
        model = FlowRepayMoney
        fields = ('allRepayMoney', 'acRepayMoney', 'repayRate', 'createDate')