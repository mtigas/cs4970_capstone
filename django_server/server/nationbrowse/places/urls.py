# coding=utf-8
from django.conf.urls.defaults import *
import views

urlpatterns = patterns('',
    url(
        regex   = '^$',
        view    = views.random_place,
        name    = 'random_place',
    ),
    url(
        regex   = '^state/(?P<slug>[-\w]+)/$',
        view    = views.state_detail,
        name    = 'state_detail',
    ),
    url(
        regex   = '^county/(?P<state_abbr>[-\w]+)/(?P<name>[-\s\w]+)/$',
        view    = views.county_detail,
        name    = 'county_detail',
    ),
)
