from django.conf.urls.defaults import *
from django.views.generic.simple import direct_to_template, redirect_to
from django.conf import settings

from django.contrib import admin
admin.autodiscover()

import nationbrowse.views as root_views

urlpatterns = patterns('',
    url(
        regex   = '^$',
        view    = root_views.nation_overview,
        name    = 'nation_overview',
    ),
    (r'^graphs/', include('nationbrowse.graphs.urls',namespace="graphs")),
    (r'^places/', include('nationbrowse.places.urls',namespace="places")),
    (r'^querybuilder/', include('nationbrowse.querybuilder.urls',namespace="querybuilder")),
    (r'^admin/', include(admin.site.urls)),
)

# If Django DEBUG is disabled, don't serve the static files -- it is
# assumed that the deployed server is handling that. (See settings.py)
if settings.DEBUG:
    urlpatterns += patterns('',
        (r'^static/(?P<path>.*)$', 'django.views.static.serve', {
            'document_root': settings.MEDIA_ROOT,
            'show_indexes': True
        }),
    )
urlpatterns += patterns('',
    (r'^sandbox/(?P<path>.*)$', 'django.views.static.serve', {
        'document_root': settings.SANDBOX_ROOT,
        'show_indexes': True
    }),
)
