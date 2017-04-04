from django.test import TestCase

from ovp_users.models import User

from shortuuid.main import encode as encode_uuid

class TestUserManager(TestCase):
  def test_create_user_without_email(self):
    """ Assert that UserManager doesn't create users without email"""
    with self.assertRaises(ValueError) as context:
      User.objects.create_user(None, 'validpassword')

    self.assertTrue('The given email address must be set.' == str(context.exception))
    #self.assertTrue(user.id > 0)

  def test_create_user(self):
    """ Assert that UserManager can create user"""
    user = User.objects.create_user('test_create_user@test.com', 'validpassword')
    self.assertTrue(user.id > 0)

  def test_create_superuser(self):
    """ Assert that UserManager can create super user"""
    user = User.objects.create_superuser('test_create_superuser@test.com', 'validpassword')
    self.assertTrue(user.id > 0)

class TestUserModel(TestCase):
  def test_short_name(self):
    """ Assert that get_short_name returns name"""
    user = User.objects.create_user('test_short_name@test.com', 'validpassword')
    user.name="Abc def"
    user.save()

    self.assertTrue(user.get_short_name() == user.name)

  def test_password_hashing(self):
    """ Assert password is not rehashed during saves """
    user = User.objects.create_user('user@email.com', 'validpassword')
    user.save()
    self.assertTrue(user.check_password('validpassword'))
    user.set_password('anotherpassword')
    self.assertTrue(user.check_password('anotherpassword'))
    user.save()
    self.assertTrue(user.check_password('anotherpassword'))

  def test_slug(self):
    """ Assert that during user creation slug matches the uuid """
    user = User.objects.create_user('user@email.com', 'validpassword')
    user.save()
    self.assertTrue(encode_uuid(user.uuid) == user.slug)
