# coding=utf-8
from __future__ import division
from django.http import HttpResponse
from django.db import connection
from cacheutil import safe_get_cache,safe_set_cache
from django.shortcuts import get_object_or_404

from nationbrowse.demographics.models import PlacePopulation
from django.contrib.contenttypes.models import ContentType

from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from graph_maker import generate_race_pie

def age_bar(request):
    return HttpResponse("Not yet implemented", mimetype="text/plain")

gender_pie = age_bar


def race_pie(request,place_type,slug):
    """
    Generates a png pie chart of the given location's racial breakdown. See
    graph_maker.generate_race_pie for the chart-generation bits.
    /graphs/race_pie/state/missouri/
    /graphs/race_pie/zipcode/65201/
    /graphs/race_pie/county/boone-missouri/
    
    See race_pie_county, below, for a version with nicer URL arguments.
    """
    # Check if we have a cache of this render, with the same request parameters ...
    # Set the cache based on the specific object we got (place_type + place_id)
    cache_key = "race_pie place_type=%s slug=%s" % (place_type, slug)
    response = safe_get_cache(cache_key)
    connection.close()
    
    # If it wasn't cached, do all of this fancy logic and generate the image as a PNG
    if not response:
        ctype = get_object_or_404(ContentType,app_label="places",model=place_type)
        
        # Querying ZipCode by numeric ID is *MUCH* quicker than string
        if place_type.lower() == "zipcode":
            place = get_object_or_404(ctype.model_class(),id=slug)
        else:
            place = get_object_or_404(ctype.model_class(),slug=slug)
        
        # Generate the chart & render it as a PNG to the HTTP response
        fig = generate_race_pie(place)
        canvas=FigureCanvas(fig)
        response=HttpResponse(content_type='image/png')
        canvas.print_png(response)
        
        # Save the response to cache
        safe_set_cache(cache_key,response,86400)
        print "\nSaved to cache:\n\t%s\n" % cache_key
    else:        
        print "\nGot from cache:\n\t%s\n" % cache_key
    
    # Return the response that was either cached OR generated just now.
    return response

def race_pie_county(request,state_abbr,name):
    """
    An alternative view to above, with nicer URL structure for county browsing:
    /graphs/race_pie/county/mo/boone/
    """
    cache_key = "race_pie_county state_abbr=%s name=%s" % (state_abbr, name)
    response = safe_get_cache(cache_key)
    connection.close()
    
    if not response:
        County = ContentType.objects.get(app_label="places",model="county").model_class()
        place = get_object_or_404(County,state__abbr__iexact=state_abbr,name__iexact=name)

        fig = generate_race_pie(place)
        canvas=FigureCanvas(fig)
        response=HttpResponse(content_type='image/png')
        canvas.print_png(response)
        
        # Save the response to cache
        safe_set_cache(cache_key,response,86400)
        print "\nSaved to cache:\n\t%s\n" % cache_key
    else:        
        print "\nGot from cache:\n\t%s\n" % cache_key
    
    # Return the response that was either cached OR generated just now.
    return response
