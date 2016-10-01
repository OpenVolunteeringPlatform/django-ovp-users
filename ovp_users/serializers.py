from users import models
from rest_framework import serializers

class UserCreateSerializer(serializers.ModelSerializer):
  class Meta:
    model = models.User
    fields = ['name', 'email', 'password']

class RecoveryTokenSerializer(serializers.Serializer):
  email = serializers.CharField(required=True)

  class Meta:
    fields = ['email']

class RecoverPasswordSerializer(serializers.Serializer):
  email = serializers.CharField(required=True)
  token = serializers.CharField(required=True)
  new_password = serializers.CharField(required=True)

  class Meta:
    fields = ['email', 'token', 'new_password']
