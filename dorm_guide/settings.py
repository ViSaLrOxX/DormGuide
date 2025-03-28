import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TEMPLATE_DIR = os.path.join(BASE_DIR, 'templates')
STATIC_DIR = os.path.join(BASE_DIR, 'static')
MEDIA_DIR = os.path.join(BASE_DIR, 'media')

GDAL_LIBRARY_PATH = '/opt/homebrew/Cellar/gdal/3.10.2_3/lib/libgdal.dylib'

GEOS_LIBRARY_PATH = '/opt/homebrew/Cellar/geos/3.13.1/lib/libgeos_c.dylib'

SECRET_KEY = '7sww&gvkvd)ykx&kw3+u326n^s2jt#uz0f6bj1ttel$&p$ps*('

DEBUG = True

ALLOWED_HOSTS = []

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.gis',  
    'dorm_guide_app',
    'django_registration',
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
        'DIRS': [TEMPLATE_DIR, ],
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
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
        'OPTIONS': {'min_length': 6},
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator', 
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


STATIC_URL = '/static/'
STATICFILES_DIRS = [STATIC_DIR, ]


REGISTRATION_OPEN = True


REGISTRATION_AUTO_LOGIN = True


LOGIN_REDIRECT_URL = '/dorm-guide/'


LOGIN_URL = 'auth_login'

REGISTRATION_FORM = 'dorm_guide_app.forms.CustomRegistrationForm'

MEDIAFILES_DIRS = [
    MEDIA_DIR,
]

MEDIA_ROOT = MEDIA_DIR
MEDIA_URL = '/media/'
