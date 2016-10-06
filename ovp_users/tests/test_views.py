from django.test import TestCase

from rest_framework.reverse import reverse
from rest_framework.test import APIClient

def create_user(email="validemail@gmail.com", password="validpassword"):
  data = {
    'name': 'Valid Name',
    'email': email,
    'password': password
  }

  client = APIClient()
  return client.post(reverse('user-list'), data, format="json")

class UserCreateViewsetTestCase(TestCase):
  def test_can_create_user(self):
    """Assert that it's possible to create an user"""
    response = create_user()
    self.assertTrue(response.data['id'] > 0)

  def test_cant_create_user_duplicated_email(self):
    """Assert that it's not possible to create an user with a repeated email"""
    response = create_user()
    self.assertTrue(response.data['id'] > 0)

  def test_doesnt_return_password_on_user_creation(self):
    """Assert that the serializer does not return user hashed password """
    response = create_user()
    self.assertTrue(response.data.get('password', None) == None)

class RecoveryTokenViewsetTestCase(TestCase):
  def create_token(self):
    data = {
      'email': 'test@recovery.token',
    }

    client = APIClient()
    return client.post(reverse('recovery-token-list'), data, format="json")

  def test_can_create_user(self):
    """Assert that it's possible to create an user"""
    user = create_user('test@recovery.token')
    response = self.create_token()
    self.assertTrue(response.data['success'] == True)

class JWTAuthTestCase(TestCase):
  def authenticate(self, email='test_can_login@test.com', password='validpassword'):
    data = {
      'email': email,
      'password': password
    }

    client = APIClient()
    return client.post('/api-token-auth/', data, format="json")

  def test_can_login(self):
    """Assert that it's possible to login"""
    user = create_user('test_can_login@test.com', 'validpassword')
    response = self.authenticate()
    self.assertTrue(response.data['token'] != None)

  def test_cant_login_wrong_password(self):
    """Assert that it's not possible to login with wrong password"""
    user = create_user('test_can_login@test.com', 'invalidpassword')
    response = self.authenticate()
    self.assertTrue(response.data['non_field_errors'][0] == 'Unable to login with provided credentials.')
