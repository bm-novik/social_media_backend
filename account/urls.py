# From Django
from django.urls import path, include

# From rest_framework
from rest_framework import routers


# 3rd Party
from knox.views import LogoutView

# From project
from account.views import LoginAPIView, RegisterAPIView, UserViewSet


app_name = 'account'
router = routers.DefaultRouter()
router.register(prefix='', viewset=UserViewSet, basename='profile_page')


urlpatterns = [
    path('', include('knox.urls')),
    path('register', RegisterAPIView.as_view(), name='register'),
    path('login', LoginAPIView.as_view(), name='login'),
    path('logout', LogoutView.as_view(), name='logout'),
]

urlpatterns += router.urls
