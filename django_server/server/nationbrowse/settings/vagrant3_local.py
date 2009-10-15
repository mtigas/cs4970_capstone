import os
DJANGO_SERVER_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

DEBUG = True
TEMPLATE_DEBUG = DEBUG

ADMINS = (
    ('Mike Tigas', 'mike.tigas+Debug@gmail.com'),
)
MANAGERS = ADMINS
INTERNAL_IPS = ('127.0.0.1',)

DATABASE_ENGINE = 'postgresql_psycopg2'
DATABASE_HOST = '127.0.0.1'
DATABASE_NAME = 'cs4970_capstone'
DATABASE_USER = 'mtigas'
DATABASE_PASSWORD = r''
SECRET_KEY = '&(r^)05jawv58_e4hs2t@n(j&)tr@a6t_25xaq&e^+efy1e=zy'

CACHE_BACKEND = 'dummy:///'

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
    'nationbrowse.graphs'
)
ROOT_URLCONF = 'nationbrowse.urls'

MIDDLEWARE_CLASSES = (
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
# http://127.0.0.1:8000/
GOOGLE_MAPS_API_KEY = "ABQIAAAAFqOBQZEkQrzdpAXWWh2PJxTpH3CbXHjuCVmaTc5MkkU4wO1RRhQ4mYt9kZUlP0K8QbxrAaAdQVudOw"
DEBUG_TOOLBAR_CONFIG = {
    'INTERCEPT_REDIRECTS': False,
    'HIDE_DJANGO_SQL': False,
}
