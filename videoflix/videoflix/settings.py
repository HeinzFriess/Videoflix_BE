"""
Django settings for videoflix project.

Generated by 'django-admin startproject' using Django 4.2.5.

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
# SECRET_KEY = 'django-insecure-6)$p#nfo-^75&)405j!*6+csgnlr=0(m6sh@glf0@g1&mtv%(j'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True
#DEBUG = bool(os.environ.get("DEBUG", default=0))

ALLOWED_HOSTS = [
    'localhost',
    '127.0.0.1',
	'https://heinz-friess.developerakademie.org/admin/login/',
	'heinz-friess.developerakademie.org',
	'*',
    
]

CORS_ALLOWED_ORIGINS = [
    'http://localhost:4200',
    'https://localhost:4200',
    'https://videoflix.heinzfriess.com',
    'https://heinzfriess.com',
]


#ALLOWED_HOSTS = os.environ.get("DJANGO_ALLOWED_HOSTS").split(" ")
CSRF_COOKIE_SECURE = False
CSRF_COOKIE_HTTPONLY = False
SESSION_COOKIE_SECURE = True

CSRF_TRUSTED_ORIGINS = [
    'http://localhost:4200',
    'https://localhost:4200',
    'https://heinz-friess.developerakademie.org/*',
    'https://videoflix.heinzfriess.com',
    'https://heinzfriess.com',
]


# Application definition

INSTALLED_APPS = [
    'rest_framework',
    'rest_framework.authtoken',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    #'content.apps.ContentConfig',
    #'debug_toolbar',
    'django_rq',
    'import_export',
    'content',
    'users',
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

ROOT_URLCONF = 'videoflix.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            os.path.join(BASE_DIR, 'videoflix', 'templates'),
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

WSGI_APPLICATION = 'videoflix.wsgi.application'

AUTH_USER_MODEL = 'users.CustomUser'

# Database
# https://docs.djangoproject.com/en/4.2/ref/settings/#databases

import environ
env = environ.Env()
environ.Env.read_env()

#SECRET_KEY = env("SECRET_KEY")
SECRET_KEY = os.environ.get("SECRET_KEY")

DATABASES = {
    # 'default': {
    #     'ENGINE': 'django.db.backends.sqlite3',
    #     'NAME': BASE_DIR / 'db.sqlite3',
    # }
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': env("DB_NAME"), 
        'USER': env("DB_USER"),
        'PASSWORD': env("DB_PASSWORD"),
        'HOST': env("DB_HOST"), 
        'PORT': env("DB_PORT"),
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


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.2/howto/static-files/

STATIC_URL = '/static/'
#STATIC_ROOT = os.path.join(BASE_DIR, 'static/staticfiles')
STATIC_ROOT = '/var/www/static/'

#print(f"Static_ROOT directory is: {STATIC_ROOT}")

# Default primary key field type
# https://docs.djangoproject.com/en/4.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'


MEDIA_ROOT =  '/var/www/media/'
MEDIA_URL = '/media/'

CACHES = {
    "default": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": "rediss://127.0.0.1:6379/1",
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
            "ssl_cert_reqs": None,
        },
        "KEY_PREFIX": "videoflix"
    }
}

INTERNAL_IPS = [
    "127.0.0.1",
]

RQ_QUEUES = {
    'default': {
        'HOST': '127.0.0.1',
        'PORT': 6379,
        'DB': 0,
        #'USERNAME': 'some-user',
        'PASSWORD': 'foobared',
        'DEFAULT_TIMEOUT': 360,
        # 'REDIS_CLIENT_KWARGS': {    # Eventual additional Redis connection arguments
        #     'ssl_cert_reqs': None,
        # },
    },
}

CACHE_TTL = 60 * 15

IMPORT_EXPORT_USE_TRANSACTIONS = True

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'mail.gmx.net'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = 'friess.heinz@gmx.de'
EMAIL_HOST_PASSWORD = env("MAIL_PASSWORD")

import mimetypes
mimetypes.add_type("text/css", ".css", True)
mimetypes.add_type("text/javascript", ".js", True)

DATA_UPLOAD_MAX_MEMORY_SIZE = 5242880 # 100 MB
FILE_UPLOAD_MAX_MEMORY_SIZE = 5242880 # 100 MB


LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'file': {
            'level': 'DEBUG',
            'class': 'logging.FileHandler',
            'filename': '/var/log/django/videoflix.log',  # Replace with your log file path
        },
    },
    'loggers': {
        'videoflix': {
            'handlers': ['file'],
            'level': 'DEBUG',
            'propagate': True,
        },
    },
}
