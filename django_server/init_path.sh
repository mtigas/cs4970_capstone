#!/bin/bash

export DJANGO_SERVER_DIR=`pwd`

# For Windows machines, in case Python isn't in the path already.
export PATH=$PATH:/c/Python26

export PATH=$DJANGO_SERVER_DIR/third_party/django/bin:$PATH
export PYTHONPATH=$DJANGO_SERVER_DIR/server:$DJANGO_SERVER_DIR/third_party:$PYTHONPATH
export PYTHONOPTIMIZE=1

export DJANGO_SETTINGS_MODULE=nationbrowse.settings

# Kill outdated Python temp files 
alias cleanpy='find $DJANGO_SERVER_DIR -name "*.pyc" -delete;find $DJANGO_SERVER_DIR -name "*.pyo" -delete'
cleanpy
