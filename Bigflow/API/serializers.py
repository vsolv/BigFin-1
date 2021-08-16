from rest_framework import serializers
from Bigflow.Master.Model import mMasters
from rest_framework import exceptions

from rest_framework.serializers import (
    CharField,
    EmailField,
    HyperlinkedIdentityField,
    ModelSerializer,
    SerializerMethodField,
    ValidationError
    )

class loginSerializer(serializers.Serializer):


    user_name = serializers.CharField(required=False)
    user_password = serializers.CharField(required=False)


    class Meta:
        model = mMasters
        fields = [
            "user_name",
            "user_password"
        ]

    def validate(self, data):
            user_name = data.get('username')
            raise exceptions.ValidationError('TEST DONE')