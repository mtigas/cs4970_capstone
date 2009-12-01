# coding=utf-8
from cacheutil import safe_get_cache,safe_set_cache
from django.shortcuts import get_object_or_404,render_to_response
from django.http import HttpResponse,Http404
from django.template import RequestContext
from django.db.models.loading import get_model
from mpl_render import histogram
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas

def scatterhist_test(request):
    cache_key = "scatterhist_test"
    response = safe_get_cache(cache_key)

    if not response:
        """
        # hella slow
        County = get_model("places","county")
        counties = County.objects.only('id',).all()
        values = []
        for county in counties:
            if county.crime_data and county.population_demographics:
                if (county.population_demographics.total > 0) and (county.crime_data.violent_crime > 0):
                    values.append(
                        (county.population_demographics.total, county.crime_data.violent_crime)
                    )
        """
        CrimeData = get_model("demographics","crimedata")
        DemographicData = get_model("demographics","placepopulation")
        
        total_pops = dict( DemographicData.objects.filter(place_type__name="county").order_by("place_id").values_list("place_id","total") )
        violent_crimes = dict( CrimeData.objects.filter(place_type__name="county").order_by("place_id").values_list("place_id","violent_crime") )
        
        # { place_id: population, place_id: population, ...}
        # { place_id: violent_crimes, place_id: violent_crimes, ...}
        
        values = []
        for place_id, population in total_pops.iteritems():
            if population == 0:
                continue
            if not violent_crimes.has_key(place_id):
                continue
            
            crime = violent_crimes[place_id]
            if crime == 0:
                continue

            values.append(
                (population, crime)
            )
        
        fig = histogram(values,"Total Population","Violent Crimes")
        canvas=FigureCanvas(fig)
        response=HttpResponse(content_type='image/png')
        canvas.print_png(response)

        safe_set_cache(cache_key,response,86400)
            
    return response

def scatterhist_test1(request,place_type,slug,source_id=None):
    cache_key = "scatterhist_test place_type=%s slug=%s source_id=%s" % (place_type, slug, source_id)
    response = safe_get_cache(cache_key)

    if not response:
        PlaceClass = get_model("places",place_type)
        if not PlaceClass:
            raise Http404
        
        place = get_object_or_404(PlaceClass,slug=slug)
        
        d = place.population_demographics
        
        male_ages = map(lambda f: getattr(d,f[0].replace('age','male')), d.age_fields)
        female_ages = map(lambda f: getattr(d,f[0].replace('age','female')), d.age_fields)            
        
        values = zip(
            male_ages,
            female_ages
        )
        
        fig = histogram(values,"Male","Female")
        canvas=FigureCanvas(fig)
        response=HttpResponse(content_type='image/png')
        canvas.print_png(response)

        safe_set_cache(cache_key,response,86400)
            
    return response