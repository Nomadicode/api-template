import deepl
from django.core.exceptions import ValidationError as DjangoValidationError
from django.contrib.auth import get_user_model
from allauth.account import app_settings as allauth_account_settings
from allauth.utils import email_address_exists, get_username_max_length
from allauth.account.adapter import get_adapter
from allauth.account.utils import setup_user_email
from rest_framework import serializers

from utils.mixins import AsymmetricRelatedField
from utils.translate import translate

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
	class Meta:
		model = User
		exclude = ('password', )


class RegisterSerializer(serializers.Serializer):
    first_name = serializers.CharField(max_length=30)
    last_name = serializers.CharField(max_length=150)
    username = serializers.CharField(
        max_length=get_username_max_length(),
        min_length=allauth_account_settings.USERNAME_MIN_LENGTH,
        required=allauth_account_settings.USERNAME_REQUIRED,
    )
    email = serializers.EmailField(required=allauth_account_settings.EMAIL_REQUIRED)
    password = serializers.CharField(write_only=True)
	
    def validate_username(self, username):
        username = get_adapter().clean_username(username)
        return username

    def validate_email(self, email):
        email = get_adapter().clean_email(email)
        if allauth_account_settings.UNIQUE_EMAIL:
            if email and email_address_exists(email):
                raise serializers.ValidationError(
                    _('A user is already registered with this e-mail address.'),
                )
        return email

    def validate_password1(self, password):
        return get_adapter().clean_password(password)

    def validate(self, data):
        return data

    def custom_signup(self, request, user):
        pass

    def get_cleaned_data(self):
        return {
            'first_name': self.validated_data.get('first_name', None),
            'last_name': self.validated_data.get('last_name', None),
            'username': self.validated_data.get('username', None),
            'password1': self.validated_data.get('password', None),
            'email': self.validated_data.get('email', None),
        }

    def save(self, request):
        adapter = get_adapter()
        user = adapter.new_user(request)
        self.cleaned_data = self.get_cleaned_data()
        user = adapter.save_user(request, user, self, commit=False)
        if "password1" in self.cleaned_data:
            try:
                adapter.clean_password(self.cleaned_data['password1'], user=user)
            except DjangoValidationError as exc:
                raise serializers.ValidationError(
                    detail=serializers.as_serializer_error(exc)
            )
        user.save()
        self.custom_signup(request, user)
        setup_user_email(request, user, [])
        return user