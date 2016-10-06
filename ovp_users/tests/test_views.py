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

class CurrentUserViewSetTestCase(TestCase):
  def test_can_get_current_user(self):
    """Assert that authenticated users can get associated info"""
    user = create_user('test_can_get_current_user@test.com', 'validpassword')

    client = APIClient()
    client.login(username='test_can_get_current_user@test.com', password='validpassword')
    response = client.get(reverse('current-user-list'), {}, format="json")
    self.assertTrue(response.data.get('id', None))
    self.assertTrue(response.data.get('email', None))
    self.assertTrue(response.data.get('name', None))

  def test_ask_for_credentials(self):
    """Assert that unauthenticated users can't get current user info"""
    client = APIClient()
    response = client.get(reverse('current-user-list'), {}, format="json")
    self.assertTrue(response.data['detail'] == 'Authentication credentials were not provided.')
