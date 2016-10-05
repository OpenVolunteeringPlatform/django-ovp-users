import uuid

from ovp_users import emails

from django.contrib.auth.models import AbstractBaseUser
from django.contrib.auth.models import BaseUserManager

from django.db import models
from django.utils import timezone


class UserManager(BaseUserManager):
  def create_user(self, email, password=None, **extra_fields):
    now = timezone.now()
    if not email:
        raise ValueError('The given email address must be set')
    email = UserManager.normalize_email(email)
    user = self.model(email=email, is_staff=False,
                      is_active=True, last_login=now,
                      joined_date=now, **extra_fields)

    user.set_password(password)
    user.save()
    return user

  def create_superuser(self, email, password, **extra_fields):
    user = self.create_user(email, password, **extra_fields)
    user.is_staff = True
    user.is_active = True
    user.is_superuser = True
    user.save()
    return user

  class Meta:
    app_label = 'atados_core'

class User(AbstractBaseUser):
  email = models.EmailField('Email', max_length=254, unique=True)
  name = models.CharField('Name', max_length=200, null=False, blank=False)
  slug = models.SlugField('Slug', max_length=100, null=True, blank=True, unique=True)

  is_staff = models.BooleanField('Staff', default=False)
  is_active = models.BooleanField('Active', default=True)
  is_email_verified = models.BooleanField('Email verified', default=False)

  joined_date = models.DateTimeField(auto_now_add=True, null=True, blank=True)
  modified_date = models.DateTimeField(auto_now=True, null=True, blank=True)

  def mailing(self):
    return emails.UserMail(self)

  objects = UserManager()
  USERNAME_FIELD = 'email'

class PasswordRecoveryToken(models.Model):
  user = models.ForeignKey('User', blank=True, null=True)
  token = models.CharField('Token', max_length=128, null=False, blank=False)
  created_date = models.DateTimeField(auto_now_add=True, blank=True, null=True)
  used_date = models.DateTimeField(default=None, blank=True, null=True)

  def save(self, *args, **kwargs):
    if not self.pk:
      self.token = uuid.uuid4()

    super(PasswordRecoveryToken, self).save(*args, **kwargs)
