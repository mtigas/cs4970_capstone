import os
DJANGO_SERVER_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

DEBUG = False
TEMPLATE_DEBUG = DEBUG

ADMINS = (
    ('Mike Tigas', 'mike.tigas+Debug@gmail.com'),
)
MANAGERS = ADMINS
INTERNAL_IPS = ('173.30.129.168',)

DATABASE_ENGINE = 'postgresql_psycopg2'
DATABASE_HOST = '' # in local_settings
DATABASE_NAME = '' # in local_settings
DATABASE_USER = '' # in local_settings
DATABASE_PASSWORD = '' # in local_settings
SECRET_KEY = '' # in local_settings

# Memcached has trouble accepting the large image files for matplotlib chart generation.
# TODO re-evaluate this (maybe switch from cmemcached to memcached.py)
#CACHE_BACKEND = 'memcached://172.21.0.41:11211/?timeout=300&max_entries=100000&cull_frequency=5'
CACHE_BACKEND = 'file:///tmp/django_cache?timeout=300&max_entries=100000&cull_frequency=5'
SESSION_ENGINE = 'django.contrib.sessions.backends.cached_db'

TIME_ZONE = 'America/Chicago'
LANGUAGE_CODE = 'en-us'
SITE_ID = 1
USE_I18N = False

# ===== Apps/app backend =====
USE_GIS = True
INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.gis',
    'django.contrib.sessions',
    'django.contrib.sites',
    #'debug_toolbar',
    'nationbrowse.places',
    'nationbrowse.demographics',
    'nationbrowse.graphs',
)
ROOT_URLCONF = 'nationbrowse.urls'

MIDDLEWARE_CLASSES = (
    #'nationbrowse.profiler.ProfileMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    #'debug_toolbar.middleware.DebugToolbarMiddleware',
)

# ===== Media =====
MEDIA_ROOT = os.path.join(DJANGO_SERVER_DIR, 'static')
MEDIA_URL = '/static/'
ADMIN_MEDIA_PREFIX = 'https://s3.amazonaws.com/django-admin/'

# ===== Templates =====
TEMPLATE_DIRS = (
    os.path.join(DJANGO_SERVER_DIR, 'templates'),
)
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.load_template_source',
    'django.template.loaders.app_directories.load_template_source',
)
TEMPLATE_CONTEXT_PROCESSORS = (
    "django.core.context_processors.auth",
    "django.core.context_processors.media",
)

# ===== Extra app-specifics =====
GOOGLE_MAPS_API_KEY = "" # in local_settings

DEBUG_TOOLBAR_CONFIG = {
    'INTERCEPT_REDIRECTS': False,
    'HIDE_DJANGO_SQL': False,
}

# ===== Settings that shouldn't be publically-readable in version control =====
from local_settings import *
