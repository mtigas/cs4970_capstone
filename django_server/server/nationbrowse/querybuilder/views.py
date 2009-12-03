# coding=utf-8
from __future__ import division
from django.http import HttpResponse,Http404
from django.views.decorators.cache import cache_control
from django.db.models.loading import AppCache 

import string
import json
from nationbrowse.querybuilder import APP_MAP

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
    
    json_string = json.dumps({
        "tables":tables,
        "real_tables":real_tables,
        "columns":columns
    })
    
    if request.GET.has_key("callback"):
        json_string = "%s(%s);" % (request.GET['callback'], json_string)
    
    return HttpResponse(
        json_string,
        mimetype="application/json"
    )

@cache_control(public=True,max_age=604800)
def get_results(request):
    if not (request.GET.has_key("tables") and request.GET.has_key("columns") and request.GET.has_key("filters")):
        raise Http404
    
    tables = request.GET['tables'].strip(string.whitespace + string.punctuation)
    columns = request.GET['columns'].strip(string.whitespace + string.punctuation)
    filters = request.GET['filters'].strip(string.whitespace + string.punctuation)
    
    # Strip leading/trailing whitespace and punctuation (so we only have
    # comma-delimited list)
    if not (tables or columns or filters):
        raise Http404
    
    tables = tables.split(",")
    columns = columns.split(",")
    filters = filters.split(",")
    
    
    app_loader = AppCache()
    """
    tables=state,placepopulation
    columns=state.name,placepopulation.total
    filters=state.name|contains|missouri,placepopulation.total|gt|100000


    /url/?tables=state,placepopulation&columns=state.name,placepopulation.total&filters=state.name|contains|missouri,placepopulation.total|gt|100000

    """
    models = []
    selected_fields = {}
    for table in tables:
        try:
            app = APP_MAP[table]
            
            model = app_loader.get_model(*app.split("."))
            
            models.append(model)
        except:
            pass
    
    return HttpResponse(
        "<p>Coming soon</p>"
    )
