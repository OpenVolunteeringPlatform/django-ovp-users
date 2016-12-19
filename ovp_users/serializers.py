from django.core.exceptions import ValidationError
from django.contrib.auth.password_validation import validate_password
from django.contrib.auth import authenticate

from ovp_users import models
from ovp_uploads.serializers import UploadedImageSerializer

from rest_framework import serializers
from rest_framework import permissions
from rest_framework import fields

class UserCreateSerializer(serializers.ModelSerializer):
  class Meta:
    model = models.User
    fields = ['id', 'name', 'email', 'password', 'phone', 'avatar']
    extra_kwargs = {'password': {'write_only': True}}

  def validate(self, data):
    errors = dict()

    if data.get('password'):
      password = data.get('password', '')
      try:
        validate_password(password=password)
      except ValidationError as e:
        errors['password'] = list(e.messages)

    if errors:
      raise serializers.ValidationError(errors)

    return super(UserCreateSerializer, self).validate(data)

class UserUpdateSerializer(UserCreateSerializer):
  current_password = fields.CharField(write_only=True)

  class Meta:
    model = models.User
    permission_classes = (permissions.IsAuthenticated,)
    fields = ['name', 'phone', 'password', 'avatar', 'current_password']
    extra_kwargs = {'password': {'write_only': True}}


  def validate(self, data):
    errors = dict()

    if data.get('password') or data.get('current_password'):
      current_password = data.pop('current_password', '')
      password = data.get('password', '')

      try:
        validate_password(password=password)
      except ValidationError as e:
        errors['password'] = list(e.messages)

      if not authenticate(email=self.context['request'].user.email, password=current_password):
        errors['current_password'] = ["Invalid password."]

    if errors:
      raise serializers.ValidationError(errors)

    return super(UserCreateSerializer, self).validate(data)


class CurrentUserSerializer(serializers.ModelSerializer):
  avatar = UploadedImageSerializer()

  class Meta:
    model = models.User
    fields = ['id', 'name', 'phone', 'avatar', 'email']

class UserPublicRetrieveSerializer(serializers.ModelSerializer):
  avatar = UploadedImageSerializer()

  class Meta:
    model = models.User
    fields = ['id', 'name', 'avatar']

class UserProjectRetrieveSerializer(serializers.ModelSerializer):
  avatar = UploadedImageSerializer()

  class Meta:
    model = models.User
    fields = ['id', 'name', 'avatar', 'email', 'phone']

class UserApplyRetrieveSerializer(serializers.ModelSerializer):
  avatar = UploadedImageSerializer()

  class Meta:
    model = models.User
    fields = ['id', 'name', 'avatar', 'phone', 'email']

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
