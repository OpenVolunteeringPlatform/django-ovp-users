from ovp_users import serializers
from ovp_users import models
from ovp_users import permissions as ovp_permissions

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

  @decorators.list_route(methods=["GET"])
  def current_user(self, request, *args, **kwargs):
    queryset = self.get_queryset().get(pk=request.user.pk)
    serializer = self.get_serializer(queryset)
    return response.Response(serializer.data)

  @decorators.list_route(url_path="current_user", methods=["PUT"])
  def current_user_update(self, request, *args, **kwargs):
    # whatever
    return response.Response({})
    #partial = kwargs.pop('partial', False)
    #instance = self.get_object()
    #serializer = self.get_serializer(instance, data=request.data, partial=partial)
    #serializer.is_valid(raise_exception=True)
    #return response(serializer.data)

  @decorators.list_route(url_path="current_user", methods=["PATCH"])
  def current_user_partial_update(self, request, *args, **kwargs):
    kwargs['partial'] = True
    return self.current_user_update(request, *args, **kwargs)

  # We need to override get_permissions and get_serializer_class to work
  # with multiple serializers and permissions
  def get_permissions(self):
    if self.action == ['create']:
      self.permission_classes = []
    elif self.action in ['current_user']:
      self.permission_classes = [permissions.IsAuthenticated, ]
    elif self.action in ['current_user_update', 'current_user_partial_update']:
      self.permission_classes = [permissions.IsAuthenticated, ovp_permissions.IsOwnerOrReadOnly]

    return super(UserResourceViewSet, self).get_permissions()

  def get_serializer_class(self):
    if self.action == 'create':
      return serializers.UserCreateSerializer
    elif self.action in ['current_user']:
      return serializers.UserSearchSerializer
    elif self.action in ['current_user_update', 'current_user_partial_update']:
      return serializers.UserUpdateSerializer
