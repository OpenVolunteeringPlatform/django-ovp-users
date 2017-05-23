from rest_framework import serializers
from ovp_users.validators import PasswordReuseInRecovery

class RecoveryTokenSerializer(serializers.Serializer):
  email = serializers.CharField(required=True)

  class Meta:
    fields = ['email']

class RecoverPasswordSerializer(serializers.Serializer):
  token = serializers.CharField(required=True)
  new_password = serializers.CharField(required=True, validators=[PasswordReuseInRecovery()])

  class Meta:
    fields = ['token', 'new_password']
