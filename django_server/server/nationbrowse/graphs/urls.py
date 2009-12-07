# coding=utf-8
from django.conf.urls.defaults import *
import views

urlpatterns = patterns('',
    url(
        regex   = '^scatterhist_test\.png$',
        view    = views.scatterhist_test,
        name    = 'scatterhist_test',
    ),
    url(
        regex   = '^scatterplot_test\.png$',
        view    = views.scatterplot_test,
        name    = 'scatterplot_test',
    ),
    url(
        regex   = '^3d_test\.png$',
        view    = views.threedee_test,
        name    = 'threedee_test',
    ),
    url(
        regex   = '^boxplot_test\.png$',
        view    = views.boxplot_test,
        name    = 'boxplot_test',
    ),
    #/(?P<place_type>[-\w]+)/(?P<slug>[-\w]+)
)
