from django.conf.urls.defaults import *
import views

urlpatterns = patterns('',
    url(
        regex   = '^$',
        view    = views.TEST,
        name    = 'graphs_test',
    ),
)
