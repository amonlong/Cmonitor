from rest_framework import serializers
from apps.userInfo.models import UserIncrease, UserAge

class UserIncreaseSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserIncrease
        fields = ('register', 'allow', 'newApply', 'oldApply', 'createDate')

class UserAgeSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserAge
        fields = ('age1', 'age2', 'age3', 'age4', 'age5', 'createDate')