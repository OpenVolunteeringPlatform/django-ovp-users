from django.test import TestCase

from rest_framework.reverse import reverse
from rest_framework.test import APIClient

from ovp_users import models
from ovp_users.tests.helpers import authenticate
from ovp_users.tests.helpers import create_user


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

  def test_cant_patch_password_without_current_password(self):
    """Assert that it's not possible to update user password without the current password"""
    response = create_user('test_can_patch_password@test.com', 'abcabcabc')
    u = models.User.objects.get(pk=response.data['id'])

    data = {'password': 'pwpw12341234'}
    client = APIClient()
    client.force_authenticate(user=u)
    response = client.patch(reverse('user-current-user'), data, format="json")
    self.assertTrue(response.status_code == 400)
    self.assertTrue(response.data["current_password"] == ["Invalid password."])

  def test_can_patch_password(self):
    """Assert that it's possible to update user password"""
    response = create_user('test_can_patch_password@test.com', 'abcabcabc')
    u = models.User.objects.get(pk=response.data['id'])

    data = {'password': 'pwpw12341234', 'current_password': 'abcabcabc'}
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

    data = {'name': 'abc', 'password': 'pwpw12341234', 'current_password': 'abcabcabc'}
    client = APIClient()
    client.force_authenticate(user=u)
    response = client.put(reverse('user-current-user'), data, format="json")
    self.assertTrue(response.status_code == 200)

    response = authenticate('test_can_put_password@test.com', data['password'])
    self.assertTrue(response.data['token'] != None)

  def test_cant_update_invalid_password(self):
    """Assert that it's impossible to update user password to a invalid password"""
    response = create_user('test_can_put_password@test.com', 'abcabcabc')
    u = models.User.objects.get(pk=response.data['id'])

    data = {'name': 'abc', 'password': 'abc', 'current_password': 'abcabcabc'}
    client = APIClient()
    client.force_authenticate(user=u)
    response = client.put(reverse('user-current-user'), data, format="json")
    self.assertTrue(response.status_code == 400)
    self.assertTrue(len(response.data['password']) > 0)
    self.assertTrue(isinstance(response.data['password'], list))

  def test_can_get_current_user(self):
    """Assert that authenticated users can get associated info"""
    user = create_user('test_can_get_current_user@test.com', 'validpassword')

    client = APIClient()
    client.login(username='test_can_get_current_user@test.com', password='validpassword')
    response = client.get(reverse('user-current-user'), {}, format="json")
    self.assertTrue(response.data.get('email', None))
    self.assertTrue(response.data.get('name', None))

  def test_ask_for_credentials(self):
    """Assert that unauthenticated users can't get current user info"""
    client = APIClient()
    response = client.get(reverse('user-current-user'), {}, format="json")
    self.assertTrue(response.data['detail'] == 'Authentication credentials were not provided.')
