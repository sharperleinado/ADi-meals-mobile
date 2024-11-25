from pathlib import Path
import os
from info import *
from django.contrib import messages
from dotenv import load_dotenv
load_dotenv()


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


# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

ALLOWED_HOSTS = ['adimeals.com', '13.60.195.70']


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
    'allauth.socialaccount.providers.github',
    'allauth.socialaccount.providers.twitter',
    'allauth.socialaccount.providers.facebook',
    'allauth.socialaccount.providers.google',
    'allauth.socialaccount.providers.instagram',
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

ROOT_URLCONF = 'my_site.urls'


TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates'),os.path.join(BASE_DIR, 'templates/allauth/')],
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

AUTHENTICATION_BACKENDS = [
    'allauth.account.auth_backends.AuthenticationBackend',
]

SITE_ID = 2
ACCOUNT_EMAIL_VERIFICATION = "none"
LOGIN_REDIRECT_URL = 'https://adimeals.com/address/register_address'#'home'
ACCOUNT_LOGOUT_ON_GET = True

SOCIALACCOUNT_PROVIDERS = {
    'twitter': {
        'APP': {
            'client_id': os.getenv('SOCIAL_AUTH_TWITTER_KEY'),  # Twitter API Key
            'secret': os.getenv('SOCIAL_AUTH_TWITTER_SECRET'),  # Twitter API Key Secret
            'key': os.getenv('SOCIAL_AUTH_TWITTER_KEY')  # Same as Twitter API Key
        }
    },
    'google': {
        'APP': {
            'client_id': os.getenv('SOCIAL_AUTH_GOOGLE_KEY'),  # Google API Key
            'secret': os.getenv('SOCIAL_AUTH_GOOGLE_SECRET'),  # Google API Key Secret
            'key': os.getenv('SOCIAL_AUTH_GOOGLE_KEY')  # Same as Google API Key
        }
    },
    'facebook': {
        'APP': {
            'client_id': os.getenv('SOCIAL_AUTH_FACEBOOK_KEY'),  # Facebook API Key
            'secret': os.getenv('SOCIAL_AUTH_FACEBOOK_SECRET'),  # Facebook API Key Secret
            'key': os.getenv('SOCIAL_AUTH_FACEBOOK_KEY')  # Same as Facebook API Key
        }
    },
    'instgram': {
        'APP': {
            'client_id': os.getenv('SOCIAL_AUTH_INSTAGRAM_KEY'),  # Instagram API Key
            'secret': os.getenv('SOCIAL_AUTH_INSTAGRAM_SECRET'),  # Instagram API Key Secret
            'key': os.getenv('SOCIAL_AUTH_INSTRAGRAM_KEY')  # Same as Instagram API Key
        }
    },
}

# In settings.py
ACCOUNT_EMAIL_REQUIRED = True                # Require an email address on signup
SOCIALACCOUNT_QUERY_EMAIL = True             # Request email from the social provider
ACCOUNT_EMAIL_VERIFICATION = "optional"      # Optional or "mandatory" if you want verification
SOCIALACCOUNT_STORE_TOKENS = True            # Store social provider tokens for API access


SMS_BACKEND = 'sms.backends.twilio.SmsBackend'
#SMS_BACKEND = 'sms.backends.console.SmsBackend'

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
STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles/')  # Directory to collect static files
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'static'),
]

MEDIA_URL = '/image/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'image/')


# Default primary key field type
# https://docs.djangoproject.com/en/4.0/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

AUTH_USER_MODEL = 'authentication.User'


USE_THOUSAND_SEPARATOR=True

THOUSAND_SEPARATOR=','

DECIMAL_SEPARATOR='.'

NUMBER_GROUPING=3


PHONENUMBER_DEFAULT_FORMAT = 'INTERNATIONAL'
PHONENUMBER_DEFAULT_REGION = 'NG'
