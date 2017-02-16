from django.db import models

from django.utils.translation import ugettext_lazy as _

class UserProfile(models.Model):
  user = models.ForeignKey('User', blank=True, null=True)
  full_name = models.CharField(_('Full name'), max_length=300, null=True, blank=True)
  skills = models.ManyToManyField('ovp_core.Skill')
  about = models.TextField(_('About me'), null=True, blank=True)
