# coding=utf-8
from cacheutil import safe_get_cache,safe_set_cache
from django.shortcuts import get_object_or_404,render_to_response
from django.http import HttpResponse,Http404
from django.template import RequestContext
from django.db.models.loading import get_model
from django.contrib.contenttypes.models import ContentType

from mpl_render import histogram
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas

def scatterhist_test(request):
    cache_key = "scatterhist_test"
    response = safe_get_cache(cache_key)

    if not response:
        CrimeData = get_model("demographics","crimedata")
        DemographicData = get_model("demographics","placepopulation")
        SocioEco = get_model("demographics","socialcharacteristics")
        
        crime_ctype = ContentType.objects.get_for_model(CrimeData)
        demographic_ctype = ContentType.objects.get_for_model(DemographicData)
        socioeco_ctype = ContentType.objects.get_for_model(SocioEco)
        
        demographics = DemographicData.objects.filter(place_type__name="county").order_by("place_id").iterator()
        
        values = []
        for demo_data in demographics:
            if (demo_data.total == 0):
                continue
            
            try:
                crime_data = CrimeData.objects.get(
                    place_type=demo_data.place_type,
                    place_id=demo_data.place_id
                )
            except CrimeData.DoesNotExist:
                continue
            
            try:
                socioeco_data = SocioEco.objects.get(
                    place_type=demo_data.place_type,
                    place_id=demo_data.place_id
                )
            except SocioEco.DoesNotExist:
                continue
            
            var_a = float(socioeco_data.median_income)
            var_b = crime_data.violent_crime / (demo_data.total / 100000.0)
            
            if (var_a is 0) or (var_b is 0):
                continue
            
            values.append(
                (var_a, var_b)
            )
        
        fig = histogram(values,"Median Income","Crime Rate")
        canvas=FigureCanvas(fig)
        response=HttpResponse(content_type='image/png')
        canvas.print_png(response)

        safe_set_cache(cache_key,response,86400)
        
    return response
