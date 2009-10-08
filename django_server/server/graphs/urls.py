# coding=utf-8
from django.conf.urls.defaults import *
import views

urlpatterns = patterns('',
    url(
        regex   = '^3d/$',
        view    = views.TEST4,
        name    = 'graphs_test4',
    ),
    url(
        regex   = '^$',
        view    = views.TEST3,
        name    = 'graphs_test',
    ),
)
