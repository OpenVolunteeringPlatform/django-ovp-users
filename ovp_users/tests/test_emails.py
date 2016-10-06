from django.test import TestCase
from django.core import mail

from ovp_users.models import User

class TestEmailTriggers(TestCase):
  def test_user_creation_trigger_email(self):
    """Assert that email is triggered when creating an user"""
    user = User(email="validemail", password="validpassword", name="valid name")
    user.save()
    self.assertTrue(len(mail.outbox) > 0)
