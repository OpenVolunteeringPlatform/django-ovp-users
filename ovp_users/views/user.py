from ovp_users import serializers
from ovp_users import models
from ovp_users import emails

from ovp_core.helpers import get_settings

from rest_framework import decorators
from rest_framework import mixins
from rest_framework import response
from rest_framework import viewsets
from rest_framework.views import APIView
from rest_framework import permissions
from rest_framework.decorators import detail_route

from rest_framework.test import APIRequestFactory

from rest_framework_jwt.views import obtain_jwt_token

import json

from django.utils import timezone
from dateutil.relativedelta import relativedelta

class UserResourceViewSet(mixins.CreateModelMixin, viewsets.GenericViewSet):
  """
  UserResourceViewSet resource endpoint
  """
  queryset = models.User.objects.all()
  lookup_field = 'slug'
  lookup_value_regex = '[^/]+' # default is [^/.]+ - here we're allowing dots in the url slug field

  def current_user_get(self, request, *args, **kwargs):
    queryset = self.get_object()
    serializer = self.get_serializer(queryset, context=self.get_serializer_context())
    return response.Response(serializer.data)

  def current_user_patch(self, request, *args, **kwargs):
    instance = self.get_object()
    serializer = self.get_serializer(instance, data=request.data, partial=True, context=self.get_serializer_context())
    serializer.is_valid(raise_exception=True)
    serializer.save()

    return response.Response(serializer.data)

  @decorators.list_route(url_path="current-user", methods=['GET', 'PATCH'])
  def current_user(self, request, *args, **kwargs):
    if request.method == 'GET':
      return self.current_user_get(request, *args, **kwargs)
    if request.method == 'PATCH':
      return self.current_user_patch(request, *args, **kwargs)

  def get_object(self):
    request = self.get_serializer_context()['request']
    if self.action == 'current_user':
      return self.get_queryset().get(pk=request.user.pk)

    # Shouldn't really be called for current implementation
    # but here as fail-safe for future updates
    return super(UserResourceViewSet, self).get_object() #pragma: no cover

  # We need to override get_permissions and get_serializer_class to work
  # with multiple serializers and permissions
  def get_permissions(self):
    request = self.get_serializer_context()['request']
    if self.action == 'create':
      self.permission_classes = []
    elif self.action in ['current_user']:
      self.permission_classes = [permissions.IsAuthenticated, ]

    return super(UserResourceViewSet, self).get_permissions()

  def get_serializer_class(self):
    request = self.get_serializer_context()['request']

    if self.action == 'create':
      return serializers.UserCreateSerializer

    if self.action == 'current_user':
      if request.method == "GET":
        return serializers.CurrentUserSerializer
      elif request.method in ["PUT", "PATCH"]:
        return serializers.UserUpdateSerializer


class PublicUserResourceViewSet(mixins.RetrieveModelMixin, viewsets.GenericViewSet):
  """
  PublicUserResourceViewSet resource endpoint
  """
  queryset = models.User.objects.filter(public=True)
  serializer_class = serializers.LongUserPublicRetrieveSerializer
  lookup_field = 'slug'
  lookup_value_regex = '[^/]+' # default is [^/.]+ - here we're allowing dots in the url slug field
  email = ''
  locale = ''

  def mailing(self, async_mail=None):
    return emails.UserMail(self, async_mail)

  @detail_route(methods=['post'], url_path='send-message')
  def send_message(self, request, slug, pk=None):
    self.email = self.queryset.get(slug=slug)
    context = {
                'message': request.data.get('message', None), 
                'from_name': request.user.name, 
                'from_email': request.user.email
              }

    self.mailing().sendMessageToAnotherVolunteer(context)
    return response.Response(True)


class UserAuthView(APIView):
  """
  UserAuthView resource endpoint
  """
  queryset = models.User.objects

  def post(self, request, format=None):
    s = get_settings('OVP_USERS')
    login_attempts_value = s.get('LOGIN_ATTEMPTS', None)
    data = request.data.copy()
    request_factory = APIRequestFactory()

    new_request = request_factory.post(request.path, data, format='json')
    token = obtain_jwt_token(new_request)

    if login_attempts_value is None:
      return token

    try:
      user = self.queryset.get(email=request.data.get('email', None))
    except:
      return token

    if token.status_code == 400:
      check_date = (timezone.now() - relativedelta(hours=1)).replace(tzinfo=timezone.utc)
      if user.exceeded_login_attempts:
        return response.Response({'error': True, 'detail': 'exceeded_login_attempts', 'message': 'Exceeded limit login attempts'}, 400)

      if user.last_login_attempt is None or check_date <= user.last_login_attempt:
        user.login_attempts = user.login_attempts + 1
      else:
        user.login_attempts = 1

      if user.login_attempts >= login_attempts_value:
        user.exceeded_login_attempts = True         
        user.last_login_attempt = timezone.now()
        user.save()

        token = models.PasswordRecoveryToken(user=user)
        token.save()
        return response.Response({'error': True, 'detail': 'exceeded_login_attempts', 'message': 'Exceeded limit login attempts'}, 400)

      user.last_login_attempt = timezone.now()
      user.save()
      return token

    if user.exceeded_login_attempts == 0:
      user.last_login_attempt = timezone.now()
      user.login_attempts = 0
      user.save()
      return token
    else:
      return response.Response({'error': True, 'detail': 'exceeded_login_attempts', 'message': 'Exceeded limit login attempts'}, 400)