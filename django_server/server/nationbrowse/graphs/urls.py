# coding=utf-8
from django.conf.urls.defaults import *
import views

urlpatterns = patterns('',
    url(
        regex   = '^age_bar/$',
        view    = views.age_bar,
        name    = 'age_bar',
    ),
    url(
        regex   = '^gender_pie/$',
        view    = views.gender_pie,
        name    = 'gender_pie',
    ),
    url(
        regex   = '^race_pie/(?P<place_type>[-\w]+)/(?P<slug>[-\w]+)/$',
        view    = views.race_pie,
        name    = 'race_pie',
    ),
    url(
        regex   = '^race_pie/county/(?P<state_abbr>[-\w]+)/(?P<name>[-\w]+)/$',
        view    = views.race_pie_county,
        name    = 'race_pie_county',
    ),
)
