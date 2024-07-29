import logging

from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.response import Response

from utils.mixins import CoreViewSet

from apps.users.models import UserProfile
from apps.users.serializers import UserSerializer, ProfileSerializer

User = get_user_model()
log = logging.getLogger("user")


# Create your views here.
class UserViewSet(CoreViewSet):
	require_auth = ['create', 'update', 'destroy']
	resource_class = User
	serializer_class = UserSerializer
	permissions = {
		"update": "change_user",
		"destroy": "delete_user"
	}

	def me(self, request):
		serializer = UserSerializer(request.user)
		return Response(
			data=serializer.data,
			status=status.HTTP_200_OK
		)

	def set_update_fields(self, request, *args, **kwargs):
		return {
			'username': kwargs.get('username')
		}

