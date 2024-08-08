import os
import sys

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

PROJECT_APPS = ['app']

INSTALLED_APPS = PROJECT_APPS + [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.humanize',
    'django.contrib.messages',
    'django.contrib.redirects',
    'django.contrib.sessions',
    'django.contrib.sitemaps',
    'django.contrib.sites',
    'app.storages.CustomStaticFilesConfig',
    'django_extensions',
    'huey.contrib.djhuey',
    'tailwind',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.contrib.redirects.middleware.RedirectFallbackMiddleware',
]

ROOT_URLCONF = 'app.urls'

ASGI_APPLICATION = 'app.asgi.application'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
        'APP_DIRS': True,
        'OPTIONS': {
            'builtins': ['app.templatetags.meta'],
            'context_processors': [
                'django.template.context_processors.debug',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'django.template.context_processors.request',
            ],
        },
    },
]

LANGUAGE_CODE = 'en'

TIME_ZONE = 'America/Bogota'

USE_I18N = True

USE_TZ = True

SITE_ID = 1

STATIC_URL = '/static/'

STATIC_ROOT = os.path.join(BASE_DIR, 'static')

MEDIA_URL = '/uploads/'

MEDIA_ROOT = os.path.join(BASE_DIR, 'uploads')

LOGIN_URL = 'admin:login'

LOGOUT_URL = 'admin:logout'

CSRF_COOKIE_SECURE = True
SESSION_COOKIE_SECURE = True
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

AUTHENTICATION_BACKENDS = [
    'django.contrib.auth.backends.AllowAllUsersModelBackend',
]

STORAGES = {
    'default': {
        'BACKEND': 'django.core.files.storage.FileSystemStorage',
    },
    'staticfiles': {
        'BACKEND': 'app.storages.JSManifestStaticFilesStorage',
    },
}

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': 'mydatabase',
    }
}

CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
    }
}

SECRET_KEY = '' # add your Django secret key here
DEBUG = True
ALLOWED_HOSTS: list = []

# django-tailwind
TAILWIND_APP_NAME = 'app'

# openai
OPENAI_API_KEY = '' # add your OpenAI API key here
OPENAI_MODEL = 'gpt-4o-mini'
OPENAI_REQUEST_URL = 'https://api.openai.com/v1/chat/completions'
OPENAI_TIMEOUT = 10
OPENAI_TEMPERATURE = 1
OPENAI_REQUEST_MAX_TOKENS = 1024
OPENAI_DAILY_MAX_TOKENS = OPENAI_REQUEST_MAX_TOKENS * 1000
