import os
from pathlib import Path
import ctypes
import django.contrib.gis.gdal

BASE_DIR = Path(__file__).resolve().parent.parent
TEMPLATE_DIR = BASE_DIR / 'templates'
STATIC_DIR = BASE_DIR / 'static'
MEDIA_DIR = BASE_DIR / 'media'

try:
    GDAL_LIBRARY_PATH = ctypes.util.find_library('gdal') or django.contrib.gis.gdal.libgdal_path()
    GEOS_LIBRARY_PATH = ctypes.util.find_library('geos_c') or django.contrib.gis.gdal.libgdal_path()
except Exception:
    GDAL_LIBRARY_PATH = None
    GEOS_LIBRARY_PATH = None

SECRET_KEY = '7sww&gvkvd)ykx&kw3+u326n^s2jt#uz0f6bj1ttel$&p$ps*('

DEBUG = os.getenv('DJANGO_DEBUG', 'True') == 'True'

if DEBUG:
    ALLOWED_HOSTS = []
else:
    ALLOWED_HOSTS = ['your-pythonanywhere-username.pythonanywhere.com', 'localhost', '127.0.0.1']

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.gis',
    'registration',
    'dorm_guide_app',
    'django_bootstrap5',
    'leaflet'
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

ROOT_URLCONF = 'dorm_guide.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [TEMPLATE_DIR],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'django.template.context_processors.media',
                'django.template.context_processors.static'
            ],
        },
    },
]

WSGI_APPLICATION = 'dorm_guide.wsgi.application'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'your_db_name',
        'USER': 'your_db_user',
        'PASSWORD': 'your_db_password',
        'HOST': 'localhost',
        'PORT': '5432', 
    }
}

AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator', 'OPTIONS': {'min_length': 6}},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_L10N = True
USE_TZ = True

STATIC_URL = '/static/'
STATICFILES_DIRS = [STATIC_DIR]

LOGIN_REDIRECT_URL = '/dorm-guide/'  
LOGOUT_REDIRECT_URL = '/'
LOGIN_URL = '/accounts/login/'
ACCOUNT_ACTIVATION_DAYS = 7
REGISTRATION_AUTO_LOGIN = True

MEDIA_ROOT = MEDIA_DIR
MEDIA_URL = '/media/'
