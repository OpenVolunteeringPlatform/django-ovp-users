from django.utils import timezone
from django.core.exceptions import ValidationError
from django.contrib.auth.password_validation import validate_password

from dateutil.relativedelta import relativedelta

from ovp_users import serializers
from ovp_users import models

from rest_framework import decorators
from rest_framework import response
from rest_framework import mixins
from rest_framework import status
from rest_framework import viewsets
from rest_framework import filters



class RecoveryTokenFilter(filters.BaseFilterBackend):
  def filter_queryset(self, request, queryset, view):
    return queryset

  def get_fields(self, view):
    return ['email']


class RecoveryTokenViewSet(viewsets.GenericViewSet):
  """
  RecoveryToken resource endpoint
  """
  queryset = models.User.objects.all()
  filter_backends = (RecoveryTokenFilter,)
  serializer_class = serializers.RecoveryTokenSerializer

  def create(self, request, *args, **kwargs):
    email = request.data.get('email', None)

    try:
      user = self.get_queryset().get(email=email)
    except:
      user = None

    if user:
      # Allow only 5 requests per hour
      limit = 5
      now = timezone.now()
      to_check = (now - relativedelta(hours=1)).replace(tzinfo=timezone.utc)
      tokens = models.PasswordRecoveryToken.objects.filter(user=user, created_date__gte=to_check)

      if tokens.count() >= limit:
        will_release = tokens.order_by('-created_date')[limit-1].created_date + relativedelta(hours=1)
        seconds = abs((will_release - now).seconds)
        return response.Response({'success': False, 'message': 'Five tokens generated last hour.', 'try_again_in': seconds}, status=status.HTTP_429_TOO_MANY_REQUESTS)

      token = models.PasswordRecoveryToken(user=user)
      token.save()

    return response.Response({'success': True, 'message': 'Token requested successfully(if user exists).'})


class RecoverPasswordFilter(filters.BaseFilterBackend):
  def filter_queryset(self, request, queryset, view):
    return queryset

  def get_fields(self, view):
    return ['email']


class RecoverPasswordViewSet(viewsets.GenericViewSet):
  """
  RecoverPassword resource endpoint
  """
  queryset = models.PasswordRecoveryToken.objects.all()
  filter_backends = (RecoverPasswordFilter,)
  serializer_class = serializers.RecoverPasswordSerializer

  def create(self, request, *args, **kwargs):
    email = request.data.get('email', None)
    token = request.data.get('token', None)
    new_password = request.data.get('new_password', None)
    day_ago = (timezone.now() - relativedelta(hours=24)).replace(tzinfo=timezone.utc)

    try:
      rt = self.get_queryset().get(user__email=email, token=token)
    except:
      rt = None

    if (not rt) or rt.used_date or rt.created_date < day_ago:
      return response.Response({'message': 'Invalid email or token.'}, status=status.HTTP_401_UNAUTHORIZED)
    if not new_password:
      return response.Response({'message': 'Empty password not allowed.'}, status=status.HTTP_400_BAD_REQUEST)

    try:
      validate_password(new_password, user=rt.user)
    except ValidationError as e:
      return response.Response({'message': 'Invalid password.', 'errors': e}, status=status.HTTP_400_BAD_REQUEST)

    rt.used_date=timezone.now()
    rt.save()

    rt.user.password = new_password
    rt.user.save()

    return response.Response({'message': 'Password updated.'})
