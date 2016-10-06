from django.core.exceptions import ValidationError
from django.contrib.auth.password_validation import validate_password
from ovp_users import models
from rest_framework import serializers

class UserCreateSerializer(serializers.ModelSerializer):
  class Meta:
    model = models.User
    fields = ['id', 'name', 'email', 'password']
    extra_kwargs = {'password': {'write_only': True}}

  def validate(self, data):
      password = data.get('password')

      errors = dict()
      try:
        validate_password(password=password)
      except ValidationError as e:
        errors['password'] = list(e.messages)

      if errors:
        raise serializers.ValidationError(errors)

      return super(UserCreateSerializer, self).validate(data)


class UserSearchSerializer(serializers.ModelSerializer):
  class Meta:
    model = models.User
    fields = ['id', 'name', 'email']

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
