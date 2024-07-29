import graphene
import graphql_jwt

from django.contrib.sites.models import Site
from django.utils import timezone
from graphql_jwt.shortcuts import get_token, create_refresh_token
from guardian.shortcuts import assign_perm

from utils.graphql import get_user_from_info
from utils import generate_reset_token, \
				  get_logger, \
				  retrieve_resource, \
				  send_email_template, \
				  Message as ErrorMessage

from apps.users.models import User
from apps.users.schema import UserTypeNode

from apps.auth.models import PasswordToken

log = get_logger("AUTH")

class RegisterMutation(graphene.Mutation):
	class Arguments:
		first_name = graphene.String(required=True)
		last_name = graphene.String(required=True)
		email = graphene.String(required=True)
		username = graphene.String(required=True)
		password = graphene.String(required=True)

	success = graphene.Boolean()
	error = graphene.String()
	user = graphene.Field(UserTypeNode)
	token = graphene.String()
	refresh_token = graphene.String()

	def mutate(self, info, *args, **kwargs):
		user = get_user_from_info(info)
		log.debug("User retrieved: %s", user)

		if user.is_authenticated:
			log.debug("User is already logged in")
			return RegisterMutation(
				success=False,
				error=ErrorMessage.ALREADY_SIGNED_IN,
				user=None,
				token=None,
				refresh_token=None
			)
		
		user, success = retrieve_resource(User, {"email": kwargs.get("email")})

		if success:
			log.debug("Account already exists: %s", user)
			return RegisterMutation(
				success=False,
				error=ErrorMessage.ACCOUNT_EXISTS,
				user=None,
				token=None,
				refresh_token=None
			)

		try:
			user = User.objects.create(**kwargs)
			log.debug("User created with email %s and username %s", user.email, user.username)
		except Exception as e:
			log.debug("Unable to create user: %s", str(e))
			return RegisterMutation(
				success=False,
				error=str(e),
				user=None,
				token=None,
				refresh_token=None
			)

		user.set_password(kwargs.get("password"))
		log.debug("Password set for user %s", user)
		user.save()

		assign_perm("change_user", user, user)
		assign_perm("delete_user", user, user)

		# Send email to user confirming account creation
		try:
			client_domain = Site.objects.get(name="client")
		except Site.DoesNotExist:
			client_domain = None

		login_url = f"{client_domain}/auth/login"
		context = {
            "name": user.name,
            "login_url": login_url
        }
		send_email_template(
            f"Welcome to TravelWithMe",
            "registration_confirmation",
            [user.email, ],
            **context
        )

		token = get_token(user)
		refresh_token = create_refresh_token(user)

		return RegisterMutation(
			success=True,
			error=None,
			user=user,
			token=token,
			refresh_token=refresh_token
		)


class LoginMutation(graphql_jwt.JSONWebTokenMutation):
	user = graphene.Field(UserTypeNode)
	
	@classmethod
	def resolve(cls, root, info, **kwargs):
		return cls(user=info.context.user)


class RecoverPasswordMutation(graphene.Mutation):
	class Arguments:
		email = graphene.String(required=True)

	success = graphene.Boolean()
	error = graphene.String()

	def mutate(self, info, *args, **kwargs):
		user, success = retrieve_resource(User, {"email": kwargs.get("email")})

		if not success:
			log.debug("No account found with email: %s", kwargs.get("email", None))
			return RecoverPasswordMutation(
				success=False,
				error=ErrorMessage.NO_ACCOUNT
			)
		
		token = generate_reset_token()
		recovery_token = PasswordToken.objects.create(user=user, token=token)

		try:
			client_domain = Site.objects.get(name="client")
		except Site.DoesNotExist:
			client_domain = None

		reset_url = f"{client_domain}/account/reset-password/{recovery_token.token}"

		context = {
            "name": user.name,
            "reset_url": reset_url
        }

		log.debug("Sending password reset email for %s", user.email)
		send_email_template(
            f"Password Reset for {user.email}",
            "password_reset",
            [user.email, ],
            **context
        )
		
		# Send reset email
		return RecoverPasswordMutation(success=True, error=None)


class ResetPasswordMutation(graphene.Mutation):
	class Arguments:
		email = graphene.String(required=True)
		new_password = graphene.String(required=True)
		token = graphene.String(required=True)

	success = graphene.Boolean()
	error = graphene.String()

	def mutate(self, info, *args, **kwargs):
		user, success = retrieve_resource(User, {"email": kwargs.get("email")})

		if not success:
			log.debug("No account found with email: %s", kwargs.get("email", None))
			return ResetPasswordMutation(
				success=False,
				error=ErrorMessage.NO_ACCOUNT
			)
		
		token, found_token = retrieve_resource(PasswordToken, {
			"user__pk": user.pk,
			"token": kwargs.get("token")
		})
		
		if not found_token:
			log.debug("Invalid token provided for user: %s", user)
			return ResetPasswordMutation(
				success=False,
				error=ErrorMessage.NO_TOKEN
			)

		current_date = timezone.now()

		total_seconds = (current_date - token.created_at).total_seconds()
		if total_seconds > 86400:
			token.delete()
			log.debug("Deleting expired token for %s", user)
			return ResetPasswordMutation(
				success=False,
				error=ErrorMessage.TOKEN_EXPIRED
			)
		
		log.debug("Resetting password for %s", user)
		user.set_password(kwargs.get("new_password"))
		user.save()
		
		token.delete()

        # Send Email       
		log.debug("Sending password reset confirmation email to user %s", user)
		context = {
            "name": user.name
        }
		send_email_template(
            f"Password update confirmation for {user.email}",
            "password_reset",
            [user.email, ],
            **context
        )
		
		# Send reset email
		return ResetPasswordMutation(success=True, error=None)


class AuthMutations(graphene.ObjectType):
	register = RegisterMutation.Field()
	login = LoginMutation.Field()
	recover_password = RecoverPasswordMutation.Field()
	reset_password = ResetPasswordMutation.Field()
	verify_token = graphql_jwt.Verify.Field()
	refresh_token = graphql_jwt.Refresh.Field()
	revoke_token = graphql_jwt.Revoke.Field()
