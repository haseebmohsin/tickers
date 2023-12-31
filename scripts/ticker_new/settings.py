"""
Django settings for ticker_new project.

Generated by 'django-admin startproject' using Django 4.2.1.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.2/ref/settings/
"""
import os
from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-k=xpusre3dyjgvjw2s=m$tj#h#+j-y0ht*utccupk%oa@f(f5t'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['*']


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'celery',
    'django_celery_beat',  # Add django_celery_beat to the list of installed apps
    'polls',
    'corsheaders',

]

MIDDLEWARE = [

    'django.middleware.security.SecurityMiddleware',
            'whitenoise.middleware.WhiteNoiseMiddleware',

    'django.contrib.sessions.middleware.SessionMiddleware',
            "corsheaders.middleware.CorsMiddleware",

    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',

]

ROOT_URLCONF = 'ticker_new.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': ['templates'],
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

WSGI_APPLICATION = 'ticker_new.wsgi.application'


# Database
# https://docs.djangoproject.com/en/4.2/ref/settings/#databases

# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.sqlite3',
#         'NAME': BASE_DIR / 'db.sqlite3',
#     }
# }

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'postgres',
        'USER': 'postgres',
        'PASSWORD': 'ticker@1234',
        'HOST': '',  # Leave empty for localhost
        'PORT': '5432',  # Default port is 5432
    }
}


# Password validation
# https://docs.djangoproject.com/en/4.2/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/4.2/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True

# STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')  # Set your static root directory here

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.2/howto/static-files/
# STATIC_ROOT='root'
STATIC_URL = 'static/'

# Default primary key field type
# https://docs.djangoproject.com/en/4.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
STATICFILES_DIRS=[
    # 'extract',
    'image_detections',
    'Dunya_Ticker',
    'Ary_Ticker',
    'Samaa_Ticker',
    'Express_Ticker',
    'Geo_Ticker',
    'NinetyTwo_Ticker',
    'Collage',
    'HumNews_Ticker',





]
CORS_ALLOWED_ORIGINS = [
 
    "http://loclhost:3003",
]
STATICFILES_STORAGE = 'whitenoise.storage.StaticFilesStorage'

# Example configuration for RabbitMQ as the broker
# BROKER_URL='amqp://celeryuser@localhost:5672//'
# BROKER_VHOST='/celeryhost'
BROKER_URL = 'amqp://celeryuser@localhost:5672/celeryhost'
CELERY_RESULT_BACKEND = None
# if you want to use database uncomment this
# CELERY_RESULT_BACKEND = 'db+postgresql://postgres:ticker@1234@localhost/postgres'
# The redirection in mainly happening from view.py
LOGIN_REDIRECT_URL = "{% url 'index' %}"

# Set the logout redirect URL
LOGOUT_REDIRECT_URL = "{% url 'logout' %}"
CELERY_WORKER_HIJACK_ROOT_LOGGER = False
