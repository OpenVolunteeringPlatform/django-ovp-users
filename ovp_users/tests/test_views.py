from django.test import TestCase

from rest_framework.reverse import reverse
from rest_framework.test import APIClient

class UserCreateViewsetTestCase(TestCase):
  def create_user_req(self):
    data = {
      'name': 'Valid Name',
      'email': 'validemail@gmail.com',
      'password': 'validpassword'
    }

    client = APIClient()
    return client.post(reverse('user-list'), data, format="json")

  def test_can_create_user(self):
    """Assert that it's possible to create an user"""
    response = self.create_user_req()
    self.assertTrue(response.data['id'] > 0)

class RecoveryTokenViewsetTestCase(TestCase):
  def create_user_req(self):
    data = {
      'name': 'Valid Name',
      'email': 'validemail@gmail.com',
      'password': 'validpassword'
    }

    client = APIClient()
    return client.post(reverse('user-list'), data, format="json")

  def test_can_create_user(self):
    """Assert that it's possible to create an user"""
    response = self.create_user_req()
    self.assertTrue(response.data['id'] > 0)
