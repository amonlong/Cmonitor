from rest_framework import serializers
from apps.userInfo.models import UserIncrease

class UserIncreaseSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserIncrease
        fields = ('register', 'allow', 'newApply', 'oldApply', 'createDate')