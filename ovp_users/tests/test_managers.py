from django.test import TestCase

from ovp_users.models import User

class TestUserManager(TestCase):
  def test_create_user_without_email(self):
    """Assert that UserManager doesn't create users without email"""
    with self.assertRaises(ValueError) as context:
      User.objects.create_user(None, 'validpassword')

    self.assertTrue('The given email address must be set.' == str(context.exception))
    #self.assertTrue(user.id > 0)

  def test_create_user(self):
    """Assert that UserManager can create user"""
    user = User.objects.create_user('test_create_user@test.com', 'validpassword')
    self.assertTrue(user.id > 0)

  def test_create_superuser(self):
    """Assert that UserManager can create super user"""
    user = User.objects.create_superuser('test_create_superuser@test.com', 'validpassword')
    self.assertTrue(user.id > 0)
