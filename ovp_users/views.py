from ovp_users import serializers
from ovp_users import models

from rest_framework import decorators
from rest_framework import mixins
from rest_framework import response
from rest_framework import viewsets
from rest_framework import permissions
from rest_framework import pagination

class UserCreateViewSet(mixins.CreateModelMixin, viewsets.GenericViewSet):
  """
  UserCreateViewset resource endpoint
  """
  serializer_class = serializers.UserCreateSerializer
  queryset = models.User.objects.all()


class CurrentUserViewSet(viewsets.GenericViewSet):
  """
  CurrentUserViewset resource endpoint
  """
  serializer_class = serializers.UserSearchSerializer
  queryset = models.User.objects.all()
  permission_classes = (permissions.IsAuthenticated,)
  pagination_class = pagination.BasePagination

  def list(self, request, *args, **kwargs):
      queryset = self.get_queryset().get(pk=request.user.pk)
      serializer = self.get_serializer(queryset)
      return response.Response(serializer.data)
