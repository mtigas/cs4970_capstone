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

def is_numeric(value):
    try:
        x = float(value)
    except ValueError:
        return False
    else:
        return True

def process_op(value_a, op, value_b):
    if not value_a:
        return False
    if not value_b:
        raise Exception
    
    if is_numeric(value_a):
        value_b = float(value_b)
    
    if op == 'e':
        return value_a == value_b
    elif op == 'gt':
        return value_a > value_b
    elif op == 'gte':
        return value_a >= value_b
    elif op == 'lt':
        return value_a < value_b
    elif op == 'lte':
        return value_a <= value_b
    else:
        raise Exception
    
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
        for f in filters.split(","):
            filtercol,op,value = f.split("|")
            f_model, f_column = filtercol.split(".")
            if not qs_filters.has_key(f_model):
                qs_filters[f_model] = {}
            qs_filters[f_model][f_column] = (op, value)
    
    test_output = "<table><tr>"
    for table,fields in selected_fields.iteritems():
        for f in fields:
            test_output += "<th>%s</th>" % f
    test_output += "</tr>\n"
    
    for table in place_models:
        AppModel = models[table]
        fields = selected_fields[table]
        
        for item in AppModel.objects.only(*fields):
            row_output = "<tr>"
            for field in fields:
                row_output += "<td>%s</td>" % getattr(item,field,None)
                
            # ===== Check filters =====
            skip = False
            if qs_filters.has_key(table):
                for filter_field,f_op in qs_filters[table].iteritems():
                    op, value = f_op
                    print "%s, %s, %s, %s" % (item, filter_field, op, value)
                    if not process_op( getattr(item,filter_field,None), op, value ):
                        skip = True
                        break
            if not skip and qs_filters.has_key('placepopulation'):
                d = item.population_demographics
                for filter_field,f_op in qs_filters['placepopulation'].iteritems():
                    op, value = f_op
                    print "%s, %s, %s, %s, %s" % (d, getattr(d,filter_field,None), filter_field, op, value)
                    print "\t%s" % process_op( getattr(d,filter_field,None), op, value )
                    if not d or not process_op( getattr(d,filter_field,None), op, value ):
                        skip = True
                        break
            if not skip and qs_filters.has_key('crimedata'):
                d = item.crime_data
                for filter_field,f_op in qs_filters['crimedata'].iteritems():
                    op, value = f_op
                    print "%s, %s, %s, %s, %s" % (d, getattr(d,filter_field,None), filter_field, op, value)
                    print "\t%s" % process_op( getattr(d,filter_field,None), op, value )
                    if not d or not process_op( getattr(d,filter_field,None), op, value ):
                        skip = True
                        break
            if not skip and qs_filters.has_key('socialcharacteristics'):
                d = item.socioeco_data
                for filter_field,f_op in qs_filters['socialcharacteristics'].iteritems():
                    op, value = f_op
                    print "%s, %s, %s, %s, %s" % (d, getattr(d,filter_field,None), filter_field, op, value)
                    print "\t%s" % process_op( getattr(d,filter_field,None), op, value )
                    if not d or not process_op( getattr(d,filter_field,None), op, value ):
                        skip = True
                        break
            if skip:
                continue
            
            # ===== Perform fake join on PlacePopulation, CrimeData, SocialCharacteristics =====
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
                    row_output += "<td>%s</td>" % getattr(dataset,data_field,None)
            
            test_output += "%s</tr>\n" % row_output
    test_output += "</table>"
    
    return HttpResponse(
        test_output
    )
