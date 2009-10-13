# coding=utf-8
"""
This app will provide graph/chart rendering of statistical data, from MatPlotLib.
"""
from django.conf import settings

# Some default settings for this app. Can be overridden in settings.py.
BACKGROUND = getattr(settings,"GRAPHS_DEFAULT_BACKGROUND",'#ffffff')
COLORS6 = getattr(settings,"GRAPHS_DEFAULT_COLORS6",[
    '#0000FF',
    '#5555FF',
    '#999911',
    '#00FF00',
    '#FF00FF',
    '#FFFF00'
])
USE_PLAINFORMAT = getattr(settings,"GRAPHS_USE_PLAINFORMAT",True)
