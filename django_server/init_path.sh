#!/bin/sh

export DJANGO_SERVER_DIR=`pwd`

# For Windows machines, in case Python isn't in the path already.
export PATH=$PATH:/c/Python26

export PATH=$DJANGO_SERVER_DIR/third_party/django/bin:$PATH
export PYTHONPATH=$DJANGO_SERVER_DIR/server:$DJANGO_SERVER_DIR/third_party:$PYTHONPATH
export PYTHONOPTIMIZE=2

export DJANGO_SETTINGS_MODULE=capstone.settings
