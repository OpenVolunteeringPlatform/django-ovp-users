import re

from django.test import TestCase
from django.core import mail

from rest_framework.reverse import reverse
from rest_framework.test import APIClient

from ovp_users.tests.helpers import authenticate
from ovp_users.tests.helpers import create_user
from ovp_users.tests.helpers import create_token


class RecoveryTokenViewSetTestCase(TestCase):
  def test_can_create_token(self):
    """Assert that it's possible to create an recovery token"""
    user = create_user('test@recovery.token')
    response = create_token()
    self.assertTrue(response.data['success'] == True)

  def test_cant_create_6_tokens(self):
    """Assert that it's impossible to create more than 5 tokens in less than 60 minutes"""
    user = create_user('test2@recovery.token')
    response = None
    for i in range(6):
      response = create_token('test2@recovery.token')

    self.assertFalse(response.data.get('success', False) == True)

  def test_token_for_invalid_user(self):
    """Assert the server hides the fact user don't exist when requesting token"""
    response = create_token('invaliduser@invalid.com')
    self.assertTrue(response.data['success'] == True)
    self.assertTrue(response.data['success'] == True)
    self.assertTrue(len(mail.outbox) == 0)

class RecoverPasswordViewSetTestCase(TestCase):
  def test_can_recover_password(self):
    """Assert the user can recover his password with a valid token"""
    # Request token
    user = create_user('test_can_recover@password.com')
    response = create_token('test_can_recover@password.com')

    # Get Token from mailbox
    email_content = mail.outbox[1].alternatives[0][0]
    token = re.search('[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}', email_content).group(0)

    # Recover Password
    data = {
      'email': 'test_can_recover@password.com',
      'token': token,
      'new_password': 'newpwvalidpw*'
    }

    client = APIClient()
    response = client.post(reverse('recover-password-list'), data, format="json")
    self.assertTrue(response.data['message'] == 'Password updated.')

    # Test authentication new password
    auth = authenticate('test_can_recover@password.com', 'newpwvalidpw*')
    self.assertTrue(auth.data['token'] != None)

  def test_cant_recover_with_empty_password(self):
    """Assert that it's impossible to update password through recovery to an empty password"""
    # Request token
    user = create_user('test_cant_recover_empty@password.com')
    response = create_token('test_cant_recover_empty@password.com')

    # Get Token from mailbox
    email_content = mail.outbox[1].alternatives[0][0]
    token = re.search('[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}', email_content).group(0)

    # Recover Password
    data = {
      'email': 'test_cant_recover_empty@password.com',
      'token': token,
      'new_password': ''
    }

    client = APIClient()
    response = client.post(reverse('recover-password-list'), data, format="json")
    self.assertTrue(response.data['message'] == 'Empty password not allowed.')
    self.assertTrue(response.status_code == 400)

  def test_cant_recover_invalid_token(self):
    """Assert that it's impossible to update password through recovery with an invalid user token"""
    # Request token
    user = create_user('test_cant_recover_invalid@password.com')
    response = create_token('test_cant_recover_invalid@password.com')

    # Recover Password
    data = {
      'email': 'test_cant_recover_invalid@password.com',
      'token': 'invalid_token',
      'new_password': 'newpassword'
    }

    client = APIClient()
    response = client.post(reverse('recover-password-list'), data, format="json")
    self.assertTrue(response.data['message'] == 'Invalid email or token.')
    self.assertTrue(response.status_code == 401)

  def test_cant_recover_invalid_password(self):
    """Assert that it's impossible to update password through recovery with an invalid user token"""
    # Request token
    user = create_user('test_cant_recover_invalid_pw@password.com')
    response = create_token('test_cant_recover_invalid_pw@password.com')

    # Get Token from mailbox
    email_content = mail.outbox[1].alternatives[0][0]
    token = re.search('[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}', email_content).group(0)

    # Recover Password
    data = {
      'email': 'test_cant_recover_invalid_pw@password.com',
      'token': token,
      'new_password': 'ab'
    }

    client = APIClient()
    response = client.post(reverse('recover-password-list'), data, format="json")
    self.assertTrue(response.data['message'] == 'Invalid password.')
    self.assertTrue(response.status_code == 400)
