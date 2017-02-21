from django.core.exceptions import ValidationError
from django.contrib.auth.password_validation import validate_password
from django.contrib.auth import authenticate

from ovp_users import models
from ovp_users.models.profile import get_profile_model
from ovp_users.serializers.profile import ProfileCreateUpdateSerializer
from ovp_users.serializers.profile import ProfileRetrieveSerializer
from ovp_users.serializers.profile import ProfileSearchSerializer
from ovp_uploads.serializers import UploadedImageSerializer

from rest_framework import serializers
from rest_framework import permissions
from rest_framework import fields

class UserCreateSerializer(serializers.ModelSerializer):
  profile = ProfileCreateUpdateSerializer(required=False)

  class Meta:
    model = models.User
    fields = ['id', 'name', 'email', 'password', 'phone', 'avatar', 'locale', 'profile']
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

  def create(self, validated_data):
    profile_data = validated_data.pop('profile', {})

    # Create user
    user = models.User.objects.create(**validated_data)

    # Profile
    profile_data['user'] = user
    profile_sr = ProfileCreateUpdateSerializer(data=profile_data)
    profile = profile_sr.create(profile_data)

    return user

class UserUpdateSerializer(UserCreateSerializer):
  current_password = fields.CharField(write_only=True)
  profile = ProfileCreateUpdateSerializer(required=False)

  class Meta:
    model = models.User
    permission_classes = (permissions.IsAuthenticated,)
    fields = ['name', 'phone', 'password', 'avatar', 'current_password', 'locale', 'profile']
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

  def update(self, instance, data):
    profile_data = data.pop('profile', None)
    if profile_data:

      if instance.profile:
        profile = instance.profile
      else:
        profile = get_profile_model()(user=instance)
        profile.save()

      profile_sr = ProfileCreateUpdateSerializer(profile, data=profile_data)
      profile_sr.is_valid(raise_exception=True)
      profile = profile_sr.update(profile, profile_sr.validated_data)

    return super(UserUpdateSerializer, self).update(instance, data)


class CurrentUserSerializer(serializers.ModelSerializer):
  avatar = UploadedImageSerializer()
  profile = ProfileRetrieveSerializer()

  class Meta:
    model = models.User
    fields = ['id', 'name', 'phone', 'avatar', 'email', 'locale', 'profile']

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

class UserSearchSerializer(serializers.ModelSerializer):
  avatar = UploadedImageSerializer()
  profile = ProfileSearchSerializer()

  class Meta:
    model = models.User
    fields = ['id', 'name', 'avatar', 'profile']

def get_user_search_serializer():
  return UserSearchSerializer
