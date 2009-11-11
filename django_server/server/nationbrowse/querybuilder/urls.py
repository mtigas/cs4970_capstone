# coding=utf-8
from django.conf.urls.defaults import *
import views

urlpatterns = patterns('',
    url(
        regex   = '^get_columns/(?P<tables>.*).js$',
        view    = views.get_columns,
        name    = 'get_columns',
    ),
)
