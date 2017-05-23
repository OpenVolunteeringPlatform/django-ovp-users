from ovp_users import emails
from ovp_users.models.profile import get_profile_model
from ovp_users.models.password_history import PasswordHistory

from django.contrib.auth.models import AbstractBaseUser
from django.contrib.auth.models import BaseUserManager
from django.contrib.auth.models import PermissionsMixin

from django.db.models.signals import post_save
from django.dispatch import receiver

from django.db import models
from django.utils import timezone
from django.utils.text import slugify

from django.utils.translation import ugettext_lazy as _

import uuid
from shortuuid.main import encode as encode_uuid

from random import randint


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
  uuid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
  email = models.EmailField(_('Email'), max_length=190, unique=True)
  name = models.CharField(_('Name'), max_length=200, null=False, blank=False)
  slug = models.SlugField(_('Slug'), max_length=100, null=True, blank=True, unique=True)
  phone = models.CharField(_('Phone'), max_length=30, null=True, blank=True)
  avatar = models.ForeignKey('ovp_uploads.UploadedImage', blank=False, null=True, related_name='avatar_user', verbose_name=_('avatar'))
  public = models.BooleanField(_('Public'), default=True)

  locale = models.CharField(_('Locale'), max_length=8, null=False, blank=True, default='en')

  is_staff = models.BooleanField(_('Staff'), default=False)
  is_superuser = models.BooleanField(_('Superuser'), default=False)
  is_active = models.BooleanField(_('Active'), default=True)
  is_email_verified = models.BooleanField(_('Email verified'), default=False)

  joined_date = models.DateTimeField(_('Joined date'), auto_now_add=True, null=True, blank=True)
  modified_date = models.DateTimeField(_('Modified date'), auto_now=True, null=True, blank=True)

  objects = UserManager()
  USERNAME_FIELD = 'email'

  class Meta:
    app_label = 'ovp_users'

  def __init__(self, *args, **kwargs):
    super(User, self).__init__(*args, **kwargs)
    self.__original_password = self.password

  def mailing(self, async_mail=None):
    return emails.UserMail(self, async_mail)

  def save(self, *args, **kwargs):
    hash_password = False

    if not self.pk:
      self.slug = encode_uuid(self.uuid)
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

  def get_full_name(self):
    return self.name

  def get_short_name(self):
    return self.name

  @property
  def profile(self):
    model = get_profile_model()
    related_field_name = model._meta.get_field('user').related_query_name()
    try:
      obj = getattr(self, related_field_name, None)
      if isinstance(obj, model):
        return obj
      else:
        return model.objects.get(user=self)
    except model.DoesNotExist:
      return None


@receiver(post_save, sender=User)
def update_history(sender, instance, raw=False, **kwargs):
  if raw: # pragma: no cover
    return

  last_password = PasswordHistory.objects.filter(user=instance).last()

  if not last_password or last_password.hashed_password != instance.password:
    PasswordHistory(hashed_password=instance.password, user=instance).save()
