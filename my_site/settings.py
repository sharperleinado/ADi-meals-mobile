from pathlib import Path
import os
from info import *
#import environ

EMAIL_USE_TLS = EMAIL_USE_TLS
EMAIL_HOST = EMAIL_HOST
EMAIL_HOST_USER = EMAIL_HOST_USER
EMAIL_HOST_PASSWORD = EMAIL_HOST_PASSWORD
EMAIL_PORT = EMAIL_PORT

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent




# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-38w+yczvta+h61ca9jq6^&z%18)dd!g)ktznjmw)n5cw+qmhd7'

FLUTTERWAVE_PUBLIC_KEY = 'FLWPUBK_TEST-6b49e2a58d4f2cc37781d4d20c8a67c6-X'
FLUTTERWAVE_SECRET_KEY = 'FLWSECK_TEST-752480689d5aa127ba8cc6bfe6cd2b79-X'


# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = [
    'cart.apps.CartConfig',
    'review.apps.ReviewConfig',
    'phonenumber_field',
    'address.apps.AddressConfig',
    'payments.apps.PaymentsConfig',
    'search_box.apps.SearchBoxConfig',
    'food_app.apps.FoodAppConfig',
    'authentication.apps.AuthenticationConfig',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'corsheaders',
    'pyotp',
    'django.contrib.sites',#
    #3rd party
    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    #social providers
    'allauth.socialaccount.providers.twitter',
    'allauth.socialaccount.providers.facebook',
    'allauth.socialaccount.providers.google',
]


MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
]
CORS_ALLOW_ALL_ORIGINS = False 
CORS_ALLOWED_ORIGINS = ['https://checkout-v3-ui-prod-f4b-flutterwave.com']

ROOT_URLCONF = 'my_site.urls'


TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'my_site.context_processors.context_render',
            ],
        },
    },
]
#BEARER_TOKEN = 'AAAAAAAAAAAAAAAAAAAAAP8KuwEAAAAAp9KCHpswuRvjSomgep5OF3EY5dI%3DZ9PoqTcW66WWSjeIWYmtGOVBBmKTzOVlxWUR7x062SOWfPslRV'

AUTHENTICATION_BACKENDS = (
    'allauth.account.auth_backends.AuthenticationBackend',
)
SITE_ID = 1
ACCOUNT_EMAIL_VERIFICATION = "none"
LOGIN_REDIRECT_URL = 'home'
ACCOUNT_LOGOUT_ON_GET = True

#SMS_BACKEND = 'sms.backends.twilio.SmsBackend'
SMS_BACKEND = 'sms.backends.console.SmsBackend'

TWILIO_ACCOUNT_SID = 'AC979ee3b09821db405a907fb0b7b25648'

TWILIO_AUTH_TOKEN = '9e437ac82b2ba42782512d529de4191e'

WSGI_APPLICATION = 'my_site.wsgi.application'


# Database
# https://docs.djangoproject.com/en/4.0/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}


# Password validation
# https://docs.djangoproject.com/en/4.0/ref/settings/#auth-password-validators

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


# Internationalization
# https://docs.djangoproject.com/en/4.0/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.0/howto/static-files/
#This is for static files in root directory
STATIC_URL = 'static/'
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'static')
    ]

# Default primary key field type
# https://docs.djangoproject.com/en/4.0/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

AUTH_USER_MODEL = 'authentication.User'

MEDIA_URL = os.path.join(BASE_DIR, '/image/')
MEDIA_ROOT = '/image/'


USE_THOUSAND_SEPARATOR=True

THOUSAND_SEPARATOR=','

DECIMAL_SEPARATOR='.'

NUMBER_GROUPING=3


PHONENUMBER_DEFAULT_FORMAT = 'INTERNATIONAL'
PHONENUMBER_DEFAULT_REGION = 'NG'
