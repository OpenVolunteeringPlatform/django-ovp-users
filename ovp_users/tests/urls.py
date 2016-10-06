"""
This urlconf exists because Django expects ROOT_URLCONF to exist. URLs
should be added within the test folders, and use TestCase.urls to set them.
This helps the tests remain isolated.
"""
from django.conf.urls import url, include

from rest_framework import routers

from ovp_users import views
from ovp_users import recover_password as rp

router = routers.DefaultRouter()
router.register(r'users', views.UserCreateViewSet, 'user')
router.register(r'users/current-user', views.CurrentUserViewSet, 'current-user')
router.register(r'users/recovery-token', rp.RecoveryTokenViewSet, 'recovery-token')
router.register(r'users/recover-password', rp.RecoverPasswordViewSet, 'recover-password')

urlpatterns = [
  url(r'^', include(router.urls)),
]
