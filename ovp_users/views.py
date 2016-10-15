from ovp_users import serializers
from ovp_users import models

from rest_framework import decorators
from rest_framework import mixins
from rest_framework import response
from rest_framework import viewsets
from rest_framework import permissions
from rest_framework import pagination

class UserResourceViewSet(mixins.CreateModelMixin, viewsets.GenericViewSet):
  """
  UserResourceViewSet resource endpoint
  """
  queryset = models.User.objects.all()
  lookup_field = 'email'
  lookup_value_regex = '[^/]+' # default is [^/.]+ - here we're allowing dots in the url slug field

  def current_user_get(self, request, *args, **kwargs):
    queryset = self.get_object()
    serializer = self.get_serializer(queryset)
    return response.Response(serializer.data)

  def current_user_put(self, request, *args, **kwargs):
    partial = kwargs.pop('partial', False)
    instance = self.get_object()
    serializer = self.get_serializer(instance, data=request.data, partial=partial)
    serializer.is_valid(raise_exception=True)
    serializer.save()
    return response.Response(serializer.data)

  def current_user_patch(self, request, *args, **kwargs):
    kwargs['partial'] = True
    return self.current_user_put(request, *args, **kwargs)

  @decorators.list_route(url_path="current-user", methods=['GET', 'PATCH', 'PUT'])
  def current_user(self, request, *args, **kwargs):
    if request.method == 'GET':
      return self.current_user_get(request, *args, **kwargs)
    if request.method == 'PUT':
      return self.current_user_put(request, *args, **kwargs)
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
        return serializers.UserSearchSerializer
      elif request.method in ["PUT", "PATCH"]:
        return serializers.UserUpdateSerializer
