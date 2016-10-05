from django.conf.urls import url, include
from rest_framework import routers
from rest_framework_jwt.views import obtain_jwt_token
from ovp_users import views
from ovp_users import recover_password as rp

router = routers.DefaultRouter()
router.register(r'users', views.UserCreateViewSet, 'user')
router.register(r'users/current-user', views.CurrentUserViewSet, 'user-search')
router.register(r'users/recovery-token', rp.RecoveryTokenViewSet, 'user-search')
router.register(r'users/recover-password', rp.RecoverPasswordViewSet, 'user-search')

urlpatterns = [
  url(r'^', include(router.urls)),
  url(r'^api-token-auth/', obtain_jwt_token),
]
