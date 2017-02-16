from django.test import TestCase

from ovp_users.tests.helpers import authenticate
from ovp_users.tests.helpers import create_user
from ovp_users.tests.helpers import create_token


class JWTAuthTestCase(TestCase):
  def test_can_login(self):
    """Assert that it's possible to login"""
    user = create_user('test_can_login@test.com', 'validpassword')
    response = authenticate()
    self.assertTrue(response.data['token'] != None)

  def test_cant_login_wrong_password(self):
    """Assert that it's not possible to login with wrong password"""
    user = create_user('test_can_login@test.com', 'invalidpassword')
    response = authenticate()
    self.assertTrue(response.data['non_field_errors'][0] == 'Unable to login with provided credentials.')
