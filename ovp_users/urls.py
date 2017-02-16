from django.conf.urls import url, include
from rest_framework import routers
from rest_framework_jwt.views import obtain_jwt_token
from ovp_users import views

router = routers.DefaultRouter()
router.register(r'users', views.UserResourceViewSet, 'user')
router.register(r'users/recovery-token', views.RecoveryTokenViewSet, 'recovery-token')
router.register(r'users/recover-password', views.RecoverPasswordViewSet, 'recover-password')

urlpatterns = [
  url(r'^', include(router.urls)),
  url(r'^api-token-auth/', obtain_jwt_token),
]
