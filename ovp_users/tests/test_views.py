from django.test import TestCase

from rest_framework.reverse import reverse
from rest_framework.test import APIClient

def create_user(email="validemail@gmail.com"):
  data = {
    'name': 'Valid Name',
    'email': email,
    'password': 'validpassword'
  }

  client = APIClient()
  return client.post(reverse('user-list'), data, format="json")

class UserCreateViewsetTestCase(TestCase):
  def test_can_create_user(self):
    """Assert that it's possible to create an user"""
    response = create_user()
    self.assertTrue(response.data['id'] > 0)

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
