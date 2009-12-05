# coding=utf-8
from __future__ import division
from django.http import HttpResponse,Http404
from django.views.decorators.cache import cache_control
from django.db.models.loading import AppCache 

import string
import json
from nationbrowse.querybuilder import APP_MAP,PLACES_MODELS,DATA_MODELS

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
            
            fieldlist = model.objects.all().values()[0].keys()
            fieldlist = filter(lambda x: not x.endswith("_err"), fieldlist)
            fieldlist.sort()
            
            columns.append(fieldlist)
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
    if not (tables or columns):
        raise Http404

    models = {}
    place_models = []
    data_models = []
    model_fields = {}
    selected_fields = {}
    qs_filters = {}
    
    app_loader = AppCache()
    
    tables = tables.split(",")
    for table in tables:
        app = APP_MAP[table]
        model = app_loader.get_model(*app.split("."))
        model_fields[table] = model.objects.all().values()[0].keys()
        models[table] = model
        if table in PLACES_MODELS:
            place_models.append(table)
        elif table in DATA_MODELS:
            data_models.append(table)

    columns = columns.split(",")
    for c in columns:
        c_model, c_column = c.split(".")
        if not selected_fields.has_key(c_model):
            selected_fields[c_model] = []
        selected_fields[c_model].append(c_column)
    
    if filters:
        filters = filters.split(",")
    
    test_output = "<table><tr>"
    for table,fields in selected_fields.iteritems():
        for f in fields:
            test_output += "<th>%s</th>" % f
    test_output += "</tr>\n"
    
    for table in place_models:
        AppModel = models[table]
        fields = selected_fields[table]
        
        for item in AppModel.objects.only(*fields):
            test_output += "<tr>"
            for field in fields:
                test_output += "<td>%s</td>" % getattr(item,field,None)
                
            # Fields that are in connected tables
            for join_table in data_models:
                if join_table == 'placepopulation':
                    dataset = item.population_demographics
                elif join_table == 'crimedata':
                    dataset = item.crime_data
                elif join_table == 'socialcharacteristics':
                    dataset = item.socioeco_data
                else:
                    continue
                
                data_fields = selected_fields[join_table]
                for data_field in data_fields:
                    test_output += "<td>%s</td>" % getattr(dataset,data_field,None)
                
            test_output += "</tr>\n"
    test_output += "</table>"
    
    return HttpResponse(
        test_output
    )
