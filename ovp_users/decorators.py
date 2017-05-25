from functools import wraps

from dateutil.relativedelta import relativedelta

from django.utils import timezone

from ovp_users.helpers import get_settings
from ovp_users.models import PasswordHistory

def expired_password(function):

  @wraps(function)
  def wrapper(self, *args, **kwargs):
    representation = function(self, *args, **kwargs)
    expiry_time = get_settings().get("EXPIRE_PASSWORD_IN", False)

    if expiry_time:
      representation["expired_password"] = False
      request = self.context["request"]
      entry = PasswordHistory.objects.filter(user=request.user).order_by('-pk').first()

      if not entry:
        representation["expired_password"] = True
      else:
        delta = relativedelta(seconds=expiry_time)
        if timezone.now() - delta > entry.created_date:
          representation["expired_password"] = True

    return representation

  return wrapper
