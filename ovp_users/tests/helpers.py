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


def create_user_with_profile(email="validemail@gmail.com", password="validpassword", profile={}):
  data = {
    'name': 'Valid Name',
    'email': email,
    'password': password,
    'profile': profile
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
