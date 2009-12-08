# coding=utf-8
"""
This app will provide the data models and API functionality on demographic(-esque) data.

App structure shortsightedness means that this app is not just a "demographics" data app.
Should be renamed in the future, but keeping this named as "demographics" for the semester.
"""
from django.contrib.contenttypes.models import ContentType
from django.db.models.loading import get_model
from django.db.models import Avg,Max,Min,StdDev,Variance
from cacheutil import cached_method

def get_data_aggregates(place,table,fieldname):
    if not (isinstance(table, basestring)):
        DataType = ContentType.objects.get_for_model(table).model_class()
    else:
        DataType = get_model('demographics',table)
    
    qs = DataType.objects.filter(
        place_id__in = place.children.values_list('id',flat=True),
        place_type   = ContentType.objects.get_for_model(place.children[0])
    )
    
    return qs.aggregate(
        avg=Avg(fieldname),
        max=Max(fieldname),
        min=Min(fieldname),
        stddev=StdDev(fieldname,sample=True),
        variance=Variance(fieldname,sample=True)
    )
get_data_aggregates = cached_method(get_data_aggregates, 15552000)
