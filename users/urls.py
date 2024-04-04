from django.urls import path, include
from .views import UserViewSet, LoginViewSet, UserDataViewSet, LogoutViewset
from rest_framework.routers import DefaultRouter

router = DefaultRouter()

router.register('signup', UserViewSet, basename='users')
router.register('login', LoginViewSet, basename='login')
router.register('userdata', UserDataViewSet, basename='userdata')
router.register('logout', LogoutViewset, basename='logout')

urlpatterns = [
    path('', include(router.urls)),
]