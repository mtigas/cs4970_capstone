# coding=utf-8
"""
Settings for the Nationbrowse server.

Don't edit this file. If you need to change anything or add new
settings, create local_settings.py in this directory and set everything
there -- values in that file will override those in this one.

In particular, for a production setting, DATABASE_* values should be overridden
and SECRET_KEY should be changed so it's actually, you know, *secret*.
"""
import os
DJANGO_SERVER_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Note, when you disable DEBUG, you will have to serve the static files
# (from django_server/static) through your server. See MEDIA_ROOT and MEDIA_URL.
DEBUG = True
TEMPLATE_DEBUG = DEBUG

ADMINS = ()
MANAGERS = ()
INTERNAL_IPS = ('127.0.0.1',)

DATABASE_ENGINE = 'sqlite3'
DATABASE_NAME = os.path.join(DJANGO_SERVER_DIR, 'nationbrowse', 'site_database.db')
SECRET_KEY = '&(r^)05jawv58_e4hs2t@n(j&)tr@a6t_25xaq&e^+efy1e=zy'

CACHE_BACKEND = 'dummy:///'

TIME_ZONE = 'America/Chicago'
LANGUAGE_CODE = 'en-us'
SITE_ID = 1
USE_I18N = False

# ===== Apps/app backend =====
USE_GIS = False
INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.humanize',
    'django.contrib.sessions',
    'django.contrib.sites',
    'nationbrowse.places',
    'nationbrowse.demographics',
    'nationbrowse.graphs',
)
ROOT_URLCONF = 'nationbrowse.urls'

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
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
# http://127.0.0.1:8000/
GOOGLE_MAPS_API_KEY = "ABQIAAAAFqOBQZEkQrzdpAXWWh2PJxTpH3CbXHjuCVmaTc5MkkU4wO1RRhQ4mYt9kZUlP0K8QbxrAaAdQVudOw"

# ===== Import overrides =====

try:
    from local_settings import *
except:
    pass
