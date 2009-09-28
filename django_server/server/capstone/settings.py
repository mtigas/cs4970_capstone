import os
# ../..
DJANGO_SERVER_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

DEBUG = True
TEMPLATE_DEBUG = DEBUG

ADMINS = (
    # ('Your Name', 'your_email@domain.com'),
)
MANAGERS = ADMINS

DATABASE_ENGINE = 'sqlite3'
DATABASE_NAME = 'site_database.db'

CACHE_BACKEND = 'dummy:///'
SESSION_ENGINE = 'django.contrib.sessions.backends.cached_db'

TIME_ZONE = 'America/Chicago'
LANGUAGE_CODE = 'en-us'
SITE_ID = 1
USE_I18N = False

MEDIA_ROOT = os.path.join(DJANGO_SERVER_DIR, 'static')
MEDIA_URL = '/static/'

ADMIN_MEDIA_ROOT = os.path.join(DJANGO_SERVER_DIR, 'third_party/django/contrib/admin/media')
ADMIN_MEDIA_PREFIX = '/admin_static/'

SECRET_KEY = '&(r^)05jawv58_e4hs2t@n(j&)tr@a6t_25xaq&e^+efy1e=zy'
INTERNAL_IPS = ('127.0.0.1',)

TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.load_template_source',
    'django.template.loaders.app_directories.load_template_source',
)
TEMPLATE_CONTEXT_PROCESSORS = (
    "django.core.context_processors.auth",
    "django.core.context_processors.media",
    #"django.core.context_processors.request",
)

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
)

ROOT_URLCONF = 'capstone.urls'

TEMPLATE_DIRS = (
    os.path.join(DJANGO_SERVER_DIR, 'templates'),
)

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    
    'places',
)

# Sqlite (the DB we use when we develop locally) is not GIS-aware, but our live
# server's database will be.
USE_GIS = False

# this one is valid for http://127.0.0.1:8000/
GOOGLE_MAPS_API_KEY = "ABQIAAAAFqOBQZEkQrzdpAXWWh2PJxTpH3CbXHjuCVmaTc5MkkU4wO1RRhQ4mYt9kZUlP0K8QbxrAaAdQVudOw"

# ----------

# See if there's an "extra_settings.py" file, containing server-specific settings.
# If there is, override settings here with the settings from there.
try:
    from extra_settings import *
except:
    pass
