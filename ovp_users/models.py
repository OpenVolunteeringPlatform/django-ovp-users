import uuid

from ovp_users import emails

from django.contrib.auth.models import AbstractBaseUser
from django.contrib.auth.models import BaseUserManager
from django.contrib.auth.models import PermissionsMixin

from django.db import models
from django.utils import timezone

from django.utils.translation import ugettext_lazy as _

class UserManager(BaseUserManager):
  def create_user(self, email, password=None, **extra_fields):
    now = timezone.now()
    if not email:
      raise ValueError('The given email address must be set.')
    email = UserManager.normalize_email(email)
    user = self.model(email=email, is_staff=False,
                      is_active=True, last_login=now,
                      joined_date=now, **extra_fields)

    user.password = password
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
    app_label = 'ovp_user'

class User(AbstractBaseUser, PermissionsMixin):
  email = models.EmailField(_('Email'), max_length=254, unique=True)
  name = models.CharField(_('Name'), max_length=200, null=False, blank=False)
  slug = models.SlugField(_('Slug'), max_length=100, null=True, blank=True, unique=True)
  phone = models.CharField(_('Phone'), max_length=30, null=True, blank=True)
  avatar = models.ForeignKey('ovp_uploads.UploadedImage', blank=False, null=True, related_name='avatar_user', verbose_name=_('avatar'))

  is_staff = models.BooleanField(_('Staff'), default=False)
  is_superuser = models.BooleanField(_('Superuser'), default=False)
  is_active = models.BooleanField(_('Active'), default=True)
  is_email_verified = models.BooleanField(_('Email verified'), default=False)

  joined_date = models.DateTimeField(_('Joined date'), auto_now_add=True, null=True, blank=True)
  modified_date = models.DateTimeField(_('Modified date'), auto_now=True, null=True, blank=True)

  objects = UserManager()
  USERNAME_FIELD = 'email'

  def __init__(self, *args, **kwargs):
    super(User, self).__init__(*args, **kwargs)
    self.__original_password = self.password

  def mailing(self, async_mail=None):
    return emails.UserMail(self, async_mail)

  def save(self, *args, **kwargs):
    hash_password = False

    if not self.pk:
      hash_password = True
      self.mailing().sendWelcome()
    else:
      # checks if password has changed and if it was set by set_password
      if self.__original_password != self.password and not self.check_password(self._password):
        hash_password = True

    if hash_password:
      self.set_password(self.password) # hash it
      self.__original_password = self.password

    super(User, self).save(*args, **kwargs)

  def get_short_name(self):
    return self.name

  class Meta:
    app_label = 'ovp_users'


class PasswordRecoveryToken(models.Model):
  user = models.ForeignKey('User', blank=True, null=True)
  token = models.CharField(_('Token'), max_length=128, null=False, blank=False)
  created_date = models.DateTimeField(_('Created date'), auto_now_add=True, blank=True, null=True)
  used_date = models.DateTimeField(_('Used date'), default=None, blank=True, null=True)

  def save(self, *args, **kwargs):
    if not self.pk:
      self.token = uuid.uuid4()
      self.user.mailing().sendRecoveryToken({'token': self})

    super(PasswordRecoveryToken, self).save(*args, **kwargs)

  class Meta:
    app_label = 'ovp_users'
