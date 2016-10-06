from django.test import TestCase

from ovp_users.recover_password import RecoveryTokenFilter
from ovp_users.recover_password import RecoverPasswordFilter

def TestPasswordRecoveryFilters(TestCase):
  def test_filters():
    """Assert filters do not throw error when instantiated"""
    # Nothing to assert here, we just instantiate them and
    # make sure it throws no error
    RecoveryTokenFilter()
    RecoverPasswordFilter()
