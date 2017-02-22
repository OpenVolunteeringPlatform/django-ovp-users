from django.db import models

from django.utils.translation import ugettext_lazy as _

class UserProfile(models.Model):
  user = models.OneToOneField('User', blank=True, null=True, related_name='profile')
  full_name = models.CharField(_('Full name'), max_length=300, null=True, blank=True)
  skills = models.ManyToManyField('ovp_core.Skill')
  causes = models.ManyToManyField('ovp_core.Cause')
  about = models.TextField(_('About me'), null=True, blank=True)
  public = models.BooleanField(_('Public Profile'), default=True)

def get_profile_model():
  return UserProfile
