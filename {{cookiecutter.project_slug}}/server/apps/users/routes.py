from django.urls import path, include

from apps.users.views import UserViewSet

from rest_framework.routers import SimpleRouter
from rest_framework_nested.routers import NestedSimpleRouter

APP_PREFIX = ''

router = SimpleRouter()
router.register(r'users', UserViewSet)

urlpatterns = [
    path(r'', include(router.urls)),
    path('users/me/', UserViewSet.as_view({
        'get': 'me'
	})),
    path('users/password/', UserViewSet.as_view({
        'put': 'update_password'
    })),
    path('users/<slug:username>/', UserViewSet.as_view({
        'get': 'retrieve',
        'put': 'update',
        'delete': 'destroy'
    })),
    path('users/', UserViewSet.as_view({
        'get': 'list'
    }))
]
