import os
from datetime import timedelta
import environ
from django.utils.translation import gettext_lazy as _

env = environ.Env()
ROOT_DIR = environ.Path(__file__) - 3

READ_DOT_ENV_FILE = env.bool('DJANGO_READ_DOT_ENV_FILE', default=True)

if READ_DOT_ENV_FILE:
	env_file = str(ROOT_DIR.path('.env'))
	print('Loading : {}'.format(env_file))
	env.read_env(env_file)
	print('The .env file has been loaded. See base.py for more information')

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SECRET_KEY = env('DJANGO_SECRET_KEY', default=env('DJANGO_SECRET', default='CHANGE THIS!!!'))
DEBUG = env('DEBUG', default=True)

ALLOWED_HOSTS = []

#region General Configurations
TEMPLATES = [
	{
		'BACKEND': 'django.template.backends.django.DjangoTemplates',
		'DIRS': [
			os.path.join(ROOT_DIR, 'templates/'),
		],
		'APP_DIRS': True,
		'OPTIONS': {
			'context_processors': [
				'django.template.context_processors.debug',
				'django.template.context_processors.request',
				'django.contrib.auth.context_processors.auth',
				'django.contrib.messages.context_processors.messages',
			],
		},
	},
]

WSGI_APPLICATION = 'config.wsgi.application'
FILE_UPLOAD_MAX_MEMORY_SIZE = 20 * 1024 * 1024

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
ADMIN_URL = r'^d-admin/'

STATIC_ROOT = os.path.join(ROOT_DIR, 'static')
STATIC_URL = '/static/'

MEDIA_ROOT = os.path.join(ROOT_DIR, 'media')
MEEDIA_URL = '/media/'

SITE_ID = 1
AUTH_USER_MODEL = 'users.User'

#region Email Settings
ADMINS = [
	('Nomadicode Dev Team', 'dev@travelwithme.app'),
]
MANAGERS = ADMINS
EMAIL_BACKEND = env('DJANGO_EMAIL_BACKEND', default='django.core.mail.backends.console.EmailBackend')
#endregion email settings

#region Internationalization
LANGUAGE_CODE = 'en-us'
USE_I18N = bool('True')
LANGUAGES = [
    ('en', _('English')),
    ('es', _('Spanish')),
]

TIME_ZONE = 'UTC'
USE_TZ = True
USE_L10N = True
#endregion Internationalization

#endregion

#region Logging Configuration
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler', 
        },
    },
    'root': {
        'handlers': ['console'],
        'level': "DEBUG" if DEBUG else 'INFO'
    }
}
#endregion

#region Django Apps definitions
DJANGO_APPS = [
	'django.contrib.admin',
	'django.contrib.auth',
	'django.contrib.contenttypes',
	'django.contrib.sessions',
	'django.contrib.sites',
	'django.contrib.messages',
	'django.contrib.staticfiles',
	'django.contrib.gis',
]

THIRD_PARTY_APPS = [
	'corsheaders',
	'rest_framework',
	'django_filters',
]

APPLICATION_APPS = [
	'apps.geo.apps.GeoConfig',
	'apps.auth.apps.AuthenticationConfig',
	'apps.users.apps.UsersConfig'
]

INSTALLED_APPS = DJANGO_APPS + THIRD_PARTY_APPS + APPLICATION_APPS
#endregion

#region Database Configuration
DATABASES = {
	'default': {
		'ENGINE': 'django.contrib.gis.db.backends.postgis',
		'NAME': env('POSTGRES_DB', default=''),
		'USER': env('POSTGRES_USER', default=''),
		'PASSWORD': env('POSTGRES_PASSWORD', default=''),
		'HOST': env('POSTGRES_HOST', default='database'),
		'PORT': env('POSTGRES_PORT', default='5432'),
	}
}
#endregion

#region Password Configuration
PASSWORD_HASHERS = [
	'django.contrib.auth.hashers.Argon2PasswordHasher',
	'django.contrib.auth.hashers.PBKDF2PasswordHasher',
	'django.contrib.auth.hashers.PBKDF2SHA1PasswordHasher',
	'django.contrib.auth.hashers.BCryptSHA256PasswordHasher',
	'django.contrib.auth.hashers.BCryptPasswordHasher',
]

AUTH_PASSWORD_VALIDATORS = [
	{
		'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
	},
	{
		'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
	},
	{
		'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
	},
	{
		'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
	},
]
#endregion

#region Request Settings
CORS_ORIGIN_ALLOW_ALL = True
ROOT_URLCONF = 'config.urls'

MIDDLEWARE = [
	'corsheaders.middleware.CorsMiddleware',
	'django.middleware.security.SecurityMiddleware',
	'django.contrib.sessions.middleware.SessionMiddleware',
	'django.middleware.common.CommonMiddleware',
	'django.middleware.csrf.CsrfViewMiddleware',
	'django.contrib.auth.middleware.AuthenticationMiddleware',
	'django.contrib.messages.middleware.MessageMiddleware',
	'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.middleware.locale.LocaleMiddleware',
]

AUTHENTICATION_BACKENDS = [
	'django.contrib.auth.backends.ModelBackend',
]
#endregion

#region REST Configuration

REST_FRAMEWORK = {
	'DEFAULT_FILTER_BACKENDS': (
        'django_filters.rest_framework.DjangoFilterBackend',
	),
	'DEFAULT_PERMISSION_CLASSES': (
		'rest_framework.permissions.AllowAny',
	)
}

# REST_AUTH = {
# 	'PASSWORD_RESET_USE_SITES_DOMAIN': True,
# 	'REGISTER_SERIALIZER': 'apps.auth.serializers.RegisterSerializer',
# 	'USE_JWT': True,
# 	'JWT_AUTH_HTTPONLY': False,
# 	'USER_DETAILS_SERIALIZER': 'apps.users.serializers.UserSerializer',
# 	'JWT_AUTH_REFRESH_COOKIE': 'refresh_token'
# }

#endregion

# #region All Auth Configurations
# ACCOUNT_AUTHENTICATION_METHOD = 'username_email'
# ACCOUNT_UNIQUE_EMAIL = True
# ACCOUNT_EMAIL_REQUIRED = True
# ACCOUNT_PRESERVE_USERNAME_CASING = False
# ACCOUNT_SIGNUP_PASSWORD_ENTER_TWICE = False
# #endregion

# #region 3rd Party Integration
# GOOGLE_API_KEY = env('GOOGLE_API_KEY')
# DEEPL_API_KEY = os.environ.get('DEEPL_API_KEY', None)
# #endregion
