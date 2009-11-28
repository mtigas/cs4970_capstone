# coding=utf-8
from django.conf.urls.defaults import *
import views

urlpatterns = patterns('',
    url(
        regex   = '^scatterhist_test\.png$',
        view    = views.scatterhist_test,
        name    = 'scatterhist_test',
    ),
    #/(?P<place_type>[-\w]+)/(?P<slug>[-\w]+)
)
