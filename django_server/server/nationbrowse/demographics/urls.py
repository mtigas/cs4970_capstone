# coding=utf-8
from django.conf.urls.defaults import *
import views

urlpatterns = patterns('',
    url(
        regex   = '^csv/(?P<place_type>[-\w]+)/(?P<slug>[-\w]+)/source_(?P<source_id>[-\w]+)/$',
        view    = views.demographics_csv,
        name    = 'demographics_csv',
    ),
)
