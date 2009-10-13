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
        regex   = '^(?P<place_type>[-\w]+)/(?P<slug>[-\w]+)/$',
        view    = views.place_detail,
        name    = 'place_detail',
    ),
    url(
        regex   = '^county/(?P<state_abbr>[-\w]+)/(?P<name>[-\s\w]+)/$',
        view    = views.county_detail,
        name    = 'county_detail',
    ),
)
