from ovp_users import serializers
from ovp_users import emails

from rest_framework import decorators
from rest_framework import mixins
from rest_framework import response
from rest_framework import viewsets
from rest_framework import permissions
from rest_framework import pagination

class UserMessageViewSet(mixins.CreateModelMixin, viewsets.GenericViewSet):
  email = ''
  locale = ''

  def mailing(self, async_mail=None):
    return emails.UserMail(self, async_mail)

  def create(self, request, *args, **kwargs):
    self.email = request.data['emailTo']
    self.mailing().sendMessageToAnotherVolunteer(request.data)
    return response.Response(True)