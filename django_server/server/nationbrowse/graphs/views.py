# coding=utf-8
from cacheutil import safe_get_cache,safe_set_cache
from django.shortcuts import get_object_or_404,render_to_response
from django.http import HttpResponse,Http404
from django.template import RequestContext
from django.db.models.loading import get_model
from django.contrib.contenttypes.models import ContentType

from mpl_render import boxplot,histogram,scatterplot,threed_bar_chart

from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas

def scatterhist_test(request):
    cache_key = "scatterhist_test"
    response = safe_get_cache(cache_key)
    
    if not response:
        County = get_model("places","county")
        
        values = []
        for county in County.objects.order_by("?")[:100].iterator():
            if (not county.population_demographics) or (not county.population_demographics.total) \
                or (not county.socioeco_data) or (not county.socioeco_data.median_income) or (not county.crime_data)\
                or (not county.crime_data.violent_crime):
                    continue
            
            var_a = float(county.socioeco_data.median_income)
            var_b = float(county.crime_data.violent_crimes_per100k)
            
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

def scatterplot_test(request):
    cache_key = "scatterplot_test"
    response = safe_get_cache(cache_key)

    if not response:
        State = get_model("places","state")
        
        values = []
        for state in State.objects.iterator():
            if (not state.population_demographics) or (not state.population_demographics.total) or (not state.area):
                continue
            
            pop_density = float(state.population_demographics.total)/float(state.area.sq_mi)
            
            # get rid of screwy outliers for the presentation demo
            if pop_density > 2000:
                continue
            if state.crime_data.violent_crime > 100000:
                continue
                        
            var_x = pop_density
            var_y = state.crime_data.violent_crime
            
            if (var_x is 0) or (var_y is 0):
                continue
            
            values.append(
                (var_x, var_y)
            )
        
        fig = scatterplot(values,"Population Density","Violent Crimes")
        canvas=FigureCanvas(fig)
        response=HttpResponse(content_type='image/png')
        canvas.print_png(response)

        safe_set_cache(cache_key,response,86400)
        
    return response

def threedee_test(request):
    cache_key = "threedee_test"
    response = safe_get_cache(cache_key)

    if not response:
        County = get_model("places","county")
        State = get_model("places","state")
        
        mo=State.objects.get(abbr="MO")

        
        values = []
        for county in County.objects.filter(state=mo)[:35].iterator():
            if (not county.population_demographics) or (not county.population_demographics.total) or (not county.area)\
                or (not county.socioeco_data) or (not county.socioeco_data.per_capita_income) or (not county.crime_data)\
                or (not county.crime_data.violent_crime):
                    continue
            
            pop_density = float(county.population_demographics.total)/float(county.area.sq_mi)
            if pop_density is 0:
                continue
            
            values.append(
                (pop_density, float(county.socioeco_data.per_capita_income), float(county.crime_data.violent_crime))
            )
        print values
        fig = threed_bar_chart(values,"Population Density","Per-Capita Income", "Violent Crimes")
        canvas=FigureCanvas(fig)
        response=HttpResponse(content_type='image/png')
        canvas.print_png(response)

        safe_set_cache(cache_key,response,86400)
        
    return response

def boxplot_test(request):
    cache_key = "boxplot_test"
    response = safe_get_cache(cache_key)

    if not response:
        CrimeData = get_model("demographics","crimedata")
        State = get_model("places","state")
        mo=State.objects.get(abbr="MO")

        data = CrimeData.objects.filter(place_type__name="county",place_id__in=mo.counties).exclude(assault__gt=200).values_list('assault','murder','rape')
        
        fig = boxplot(zip(*data),("Assault","Murder","Rape"))
        canvas=FigureCanvas(fig)
        response=HttpResponse(content_type='image/png')
        canvas.print_png(response)

        safe_set_cache(cache_key,response,86400)
        
    return response

