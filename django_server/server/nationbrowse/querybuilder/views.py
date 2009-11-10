# coding=utf-8
from __future__ import division
from django.http import HttpResponse,Http404
from django.views.decorators.cache import cache_control
from django.db.models.loading import AppCache 

import string
import json
from querybuilder import APP_MAP

@cache_control(public=True,max_age=604800)
def get_columns(request,tables):
    # Strip leading/trailing whitespace and punctuation (so we only have
    # comma-delimited list)
    tables = tables.strip(string.whitespace + string.punctuation)
    if not tables:
        raise Http404
    
    tables = tables.split(",")
    
    app_loader = AppCache()
    
    tables2 = []
    real_tables = []
    columns = []
    for table in tables:
        try:
            real_table = APP_MAP[table]
            
            model = app_loader.get_model(*real_table.split("."))
            
            tables2.append(table)
            real_tables.append(real_table)
            columns.append(
                model.objects.all().values()[0].keys()
            )
        except:
            pass
    
    return HttpResponse(
        json.dumps({
            "tables":tables,
            "real_tables":real_tables,
            "columns":columns
        }, indent=4),
        mimetype="text/plain")
