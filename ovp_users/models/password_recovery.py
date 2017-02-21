import uuid

from django.db import models

from django.utils.translation import ugettext_lazy as _

class PasswordRecoveryToken(models.Model):
  user = models.ForeignKey('User', blank=True, null=True)
  token = models.CharField(_('Token'), max_length=128, null=False, blank=False)
  created_date = models.DateTimeField(_('Created date'), auto_now_add=True, blank=True, null=True)
  used_date = models.DateTimeField(_('Used date'), default=None, blank=True, null=True)

  def save(self, *args, **kwargs):
    if not self.pk:
      self.token = uuid.uuid4()
      self.user.mailing().sendRecoveryToken({'token': self})

    super(PasswordRecoveryToken, self).save(*args, **kwargs)

  class Meta:
    app_label = 'ovp_users'
