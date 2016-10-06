from django.test import TestCase
from django.core import mail

from ovp_users.models import User, PasswordRecoveryToken

class TestEmailTriggers(TestCase):
  def test_user_creation_trigger_email(self):
    """Assert that email is triggered when creating an user"""
    user = User(email="a@b.c", password="validpassword", name="valid name")
    user.save()
    self.assertTrue(len(mail.outbox) > 0)

  def test_token_creation_trigger_email(self):
    """Assert that email is triggered when password recovery token is created"""
    user = User(email="d@e.f", password="validpassword", name="valid name")
    user.save()
    token = PasswordRecoveryToken(user=user)
    token.save()
    self.assertTrue(len(mail.outbox) >= 2)

  def test_async_email_works(self):
    """Assert that async emails are triggered by testing user creation"""
    user = User(email="a@b.c", password="validpassword", name="valid name")
    user.mailing(async_mail=True).sendWelcome().join()
    self.assertTrue(len(mail.outbox) > 0)
