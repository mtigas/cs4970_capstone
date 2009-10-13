# coding=utf-8
from django.conf.urls.defaults import *
import views

urlpatterns = patterns('',
    url(
        regex   = '^(?P<place_type>[-\w]+)/(?P<slug>[-\w]+)/(?P<graph_type>[-\w]+)/$',
        view    = views.render_graph,
        name    = 'render_graph',
    ),
    url(
        regex   = '^(?P<place_type>[-\w]+)/(?P<slug>[-\w]+)/(?P<graph_type>[-\w]+)/(?P<size>\d+)/$',
        view    = views.render_graph,
        name    = 'render_graph',
    ),
    url(
        regex   = '^county/(?P<state_abbr>[-\w]+)/(?P<name>[-\w]+)/(?P<graph_type>[-\w]+)/$',
        view    = views.render_graph_county,
        name    = 'render_graph_county',
    ),
    url(
        regex   = '^county/(?P<state_abbr>[-\w]+)/(?P<name>[-\w]+)/(?P<graph_type>[-\w]+)/(?P<size>\d{1,2,3,4})/$',
        view    = views.render_graph_county,
        name    = 'render_graph_county',
    ),
)
