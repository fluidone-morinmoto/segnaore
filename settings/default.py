"""
Django settings for segna_ore project.

Generated by 'django-admin startproject' using Django 3.0.3.

For more information on this file, see
https://docs.djangoproject.com/en/3.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.0/ref/settings/
"""

import os

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'q#hs+j5dzym1gdll64lzq8gewg@iyc@_ehfp^e*r%0h81-25u%'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['localhost']


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    #'registro.apps.RegistroConfig',
    # because it's registered in 'registro' app __init_.py file
    'registro',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'segna_ore.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
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

WSGI_APPLICATION = 'segna_ore.wsgi.application'

# Password validation
# https://docs.djangoproject.com/en/3.0/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/3.0/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.0/howto/static-files/

STATIC_URL = '/static/'


# Since among loggers and handlers levels the one which wins is the highest,
# keep the 'base' logger level to DEBUG (low) and set the desired level in the
# handler to get just the needed logs on a per-handler basis
LOGGING = {
    'version': 1,
    'formatters': {
        'default': {
            'format': '%(asctime)s [%(process)d:%(levelname)s:%(module)s:%(lineno)d] %(message)s'
        },
        'json': {
            'format': '%(asctime)s %(levelname)s %(message)s',
            '()': 'pythonjsonlogger.jsonlogger.JsonFormatter'
        },
    },
    'handlers': {
        'file': {
            'level': 'WARNING',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': 'logs/sore.log',
            'formatter': 'default',
            'maxBytes': 1024 * 1024 * 1024 * 10,
            'backupCount': 7,
        },
        'console': {
            'level': 'INFO',
            'class': 'logging.StreamHandler'
        },
        'dev_file': {
            'level': 'DEBUG',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': 'logs/sore_dev.log',
            'formatter': 'json',
            'maxBytes': 1024 * 1024 * 10,
            'backupCount': 3
        },
        'file_json': {
            'level': 'INFO',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': 'logs/sore_json.log',
            'formatter': 'json',
            'maxBytes': 1024 * 1024 * 1024 * 10,
            'backupCount': 7,
        },
    },
    'loggers': {
        'base': {
            'handlers': ['file', 'file_json'],
            'level': 'DEBUG',
            'propagate': True,
        },
    },
    # 'filters': {
    #     'content_history_json' : {
    #         '()': 'registro.logstuff.ContentHistoryJsonFilter'
    #     }
    # }
}
