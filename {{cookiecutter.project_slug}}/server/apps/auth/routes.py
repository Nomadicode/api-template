from django.conf.urls import include
from django.urls import path

APP_PREFIX = 'auth/'

urlpatterns = [
    path(APP_PREFIX, include('dj_rest_auth.urls')),
    path(f"{APP_PREFIX}register/", include('dj_rest_auth.registration.urls')),
]
