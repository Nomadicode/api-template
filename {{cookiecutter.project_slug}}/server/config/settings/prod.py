from .base import *
from .base import env

SECRET_KEY = env("DJANGO_SECRET")
DEBUG=env.bool("DEBUG", default=False)
ALLOWED_HOSTS = env.list("DJANGO_ALLOWED_HOSTS", default="")

# https://docs.djangoproject.com/en/dev/ref/settings/#csrf-cookie-secure
CSRF_COOKIE_SECURE = True

# Your stuff...
# ------------------------------------------------------------------------------

INSTALLED_APPS += ["storages"]

AWS_ACCESS_KEY_ID = env("AWS_ACCESS_KEY_ID")
AWS_SECRET_ACCESS_KEY = env("AWS_SECRET_ACCESS_KEY")
AWS_S3_REGION_NAME = env("AWS_S3_REGION_NAME", default="us-west-2")
AWS_STORAGE_BUCKET_NAME = env("AWS_STORAGE_BUCKET_NAME")
AWS_QUERYSTRING_AUTH = False
# DO NOT change these unless you know what you're doing.
_AWS_EXPIRY = 60 * 60 * 24 * 7
# https://django-storages.readthedocs.io/en/latest/backends/amazon-S3.html#settings
AWS_S3_OBJECT_PARAMETERS = {
    "CacheControl": f"max-age={_AWS_EXPIRY}, s-maxage={_AWS_EXPIRY}, must-revalidate"
}

AWS_S3_CUSTOM_DOMAIN = env("DJANGO_AWS_S3_CUSTOM_DOMAIN", default=None)
# AWS_S3_ENDPOINT_URL = f"{AWS_S3_REGION_NAME}.digitaloceanspaces.com"
storage_domain = AWS_S3_CUSTOM_DOMAIN or f"{AWS_STORAGE_BUCKET_NAME}.s3.amazonaws.com"


STATICFILES_STORAGE = "utils.storages.StaticRootS3Boto3Storage"
STATIC_URL = f"https://{storage_domain}/static/"

# MEDIA
# ------------------------------------------------------------------------------
DEFAULT_FILE_STORAGE = "utils.storages.MediaRootS3Boto3Storage"
MEDIA_URL = f"https://{storage_domain}/media/"


DEFAULT_FROM_EMAIL = env(
    "DJANGO_DEFAULT_FROM_EMAIL", default="TravelWithMe <no-reply@travelwithme.app>"
)
SERVER_EMAIL = env("DJANGO_SERVER_EMAIL", default=DEFAULT_FROM_EMAIL)

INSTALLED_APPS += ["anymail"]
EMAIL_BACKEND = "anymail.backends.sendinblue.EmailBackend"

ANYMAIL = {
    "SENDINBLUE_API_KEY": env("SENDINBLUE_API_KEY", default="")
}
