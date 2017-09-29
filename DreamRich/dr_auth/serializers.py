from rest_framework import serializers
from dr_auth.models import BaseUser


class BaseUserSerializer(serializers.ModelSerializer):

    class Meta:
        model = BaseUser
        fields = [
            'username',
            'permissions',
            'id',
        ]
