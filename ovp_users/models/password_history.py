from django.db import models

class PasswordHistory(models.Model):
  hashed_password = models.CharField(max_length=300)
  user = models.ForeignKey('ovp_users.User')
  set_date = models.DateTimeField(auto_now_add=True, null=True, blank=True)
