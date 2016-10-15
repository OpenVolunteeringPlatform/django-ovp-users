import re

from django.test import TestCase
from django.core import mail

from rest_framework.reverse import reverse
from rest_framework.test import APIClient

from ovp_users import models

def create_user(email="validemail@gmail.com", password="validpassword"):
  data = {
    'name': 'Valid Name',
    'email': email,
    'password': password
  }

  client = APIClient()
  return client.post(reverse('user-list'), data, format="json")

def authenticate(email='test_can_login@test.com', password='validpassword'):
  data = {
    'email': email,
    'password': password
  }

  client = APIClient()
  return client.post('/api-token-auth/', data, format="json")

def create_token(email='test@recovery.token'):
  data = {
    'email': email,
  }

  client = APIClient()
  return client.post(reverse('recovery-token-list'), data, format="json")

class UserResourceViewSetTestCase(TestCase):
  def test_can_create_user(self):
    """Assert that it's possible to create an user"""
    response = create_user()
    self.assertTrue(response.data['id'] > 0)

  def test_cant_create_user_duplicated_email(self):
    """Assert that it's not possible to create an user with a repeated email"""
    response = create_user()
    self.assertTrue(response.data['id'] > 0)

  def test_cant_create_user_invalid_password(self):
    """Assert that it's not possible to create an user with a repeated email"""
    response = create_user('test_cant_create_invalid_password@test.com', 'abc')
    self.assertTrue(len(response.data['password']) > 0)
    self.assertTrue(isinstance(response.data['password'], list))

  def test_doesnt_return_password_on_user_creation(self):
    """Assert that the serializer does not return user hashed password """
    response = create_user()
    self.assertTrue(response.data.get('password', None) == None)

  def test_can_patch_password(self):
    """Assert that it's possible to update user password"""
    response = create_user('test_can_patch_password@test.com', 'abcabcabc')
    u = models.User.objects.get(pk=response.data['id'])

    data = {'password': 'pwpw12341234'}
    client = APIClient()
    client.force_authenticate(user=u)
    response = client.patch(reverse('user-current-user'), data, format="json")
    self.assertTrue(response.status_code == 200)

    response = authenticate('test_can_patch_password@test.com', data['password'])
    self.assertTrue(response.data['token'] != None)

  def test_can_put_password(self):
    """Assert that it's possible to update user password"""
    response = create_user('test_can_put_password@test.com', 'abcabcabc')
    u = models.User.objects.get(pk=response.data['id'])

    data = {'password': 'pwpw12341234'}
    client = APIClient()
    client.force_authenticate(user=u)
    response = client.put(reverse('user-current-user'), data, format="json")
    self.assertTrue(response.status_code == 200)

    response = authenticate('test_can_put_password@test.com', data['password'])
    self.assertTrue(response.data['token'] != None)

  def test_can_get_current_user(self):
    """Assert that authenticated users can get associated info"""
    user = create_user('test_can_get_current_user@test.com', 'validpassword')

    client = APIClient()
    client.login(username='test_can_get_current_user@test.com', password='validpassword')
    response = client.get(reverse('user-current-user'), {}, format="json")
    self.assertTrue(response.data.get('id', None))
    self.assertTrue(response.data.get('email', None))
    self.assertTrue(response.data.get('name', None))

  def test_ask_for_credentials(self):
    """Assert that unauthenticated users can't get current user info"""
    client = APIClient()
    response = client.get(reverse('user-current-user'), {}, format="json")
    self.assertTrue(response.data['detail'] == 'Authentication credentials were not provided.')

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

