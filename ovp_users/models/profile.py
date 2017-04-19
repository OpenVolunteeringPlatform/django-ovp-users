from django.db import models
from django.utils.translation import ugettext_lazy as _

from ovp_users.helpers import get_settings, import_from_string

gender_choices = (
  ("male", "Male"),
  ("female", "Female"),
)

class UserProfile(models.Model):
  user = models.OneToOneField("User", blank=True, null=True, related_name="%(app_label)s_%(class)s_profile")
  full_name = models.CharField(_("Full name"), max_length=300, null=True, blank=True)
  skills = models.ManyToManyField("ovp_core.Skill")
  causes = models.ManyToManyField("ovp_core.Cause")
  about = models.TextField(_("About me"), null=True, blank=True)
  gender = models.CharField(_("Gender"), max_length=10, choices=gender_choices, default=None, null=True, blank=True)

def get_profile_model():
  s = get_settings()
  class_path = s.get("PROFILE_MODEL", None)
  if class_path:
    return import_from_string(class_path)
  return UserProfile
