# coding=utf-8
from django.conf.urls.defaults import *
import views

urlpatterns = patterns('',
    url(
        regex   = '^$',
        view    = views.race_piechart,
        name    = 'race_piechart',
    ),
)
