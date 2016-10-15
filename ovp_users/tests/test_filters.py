from django.test import TestCase

from ovp_users.recover_password import RecoveryTokenFilter
from ovp_users.recover_password import RecoverPasswordFilter

def test_filter(c):
  obj = c()
  obj.filter_queryset('a', 'b', 'c')
  obj.get_fields('a')

class PasswordRecoveryFiltersTestCase(TestCase):
  def test_filters(self):
    """Assert filters do not throw error when instantiated"""
    # Nothing to assert here, we just instantiate them and
    # make sure it throws no error
    test_filter(RecoveryTokenFilter)
    test_filter(RecoverPasswordFilter)

