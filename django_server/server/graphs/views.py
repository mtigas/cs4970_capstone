# coding=utf-8
from __future__ import division
from django.http import HttpResponse

from django.views.decorators.cache import cache_page
from cacheutil import safe_get_cache,safe_set_cache

import matplotlib
matplotlib.use('Agg')
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas

from demographics.models import PlacePopulation
from places.models import State,County,ZipCode
from graphutil import generate_race_piechart

def race_piechart(request):
    """
    Generates a png pie chart of the given location's racial breakdown. See
    graphutil.generate_race_piechart for the chart-generation bits.
    """    
    
    # Needs a 'place_type' request var.
    if (not request.REQUEST.has_key('place_type')) or (not request.REQUEST['place_type'] in ['state','county','zipcode']):
        return HttpResponse('"place_type" needs to be set', mimetype="text/plain")
    
    place = None
    if request.REQUEST['place_type'] == "zipcode":
        # Getting zipcode from the 'place_id' request var
        if request.REQUEST.has_key('id'):
            place = ZipCode.objects.get(id=request.REQUEST['id'])
    elif request.REQUEST['place_type'] == "state":
        # Getting state from 'abbr'
        if request.REQUEST.has_key('abbr'):
            place = State.objects.get(abbr__iexact=request.REQUEST['abbr'])
        # Getting state by 'name'
        elif request.REQUEST.has_key('name'):
            place = State.objects.get(name__iexact=request.REQUEST['name'])
    elif request.REQUEST['place_type'] == "county":
        # County requires both 'state_abbr' and 'name'
        if request.REQUEST.has_key('state__abbr') and request.REQUEST.has_key('name'):
            place = County.objects.get(name__iexact=request.REQUEST['name'],state__abbr__iexact=request.REQUEST['state__abbr'])
    if not place:
        return HttpResponse("A place object with the given request string could not be found.", mimetype="text/plain")
    
    # Check if we have a cache of this render, with the same parameters ...
    # Set the cache based on the specific object we got (place_type + place_id)
    cache_key = "race_piechart place_type=%s place_id=%s" % (request.REQUEST['place_type'], place.pk)
    response = safe_get_cache(cache_key)
    
    # If it wasn't cached, generate it, render it to a PNG, and cache that HTTP response.
    if not response:
        # Generate the chart
        fig = generate_race_piechart(place)
        
        # Add it to the HTTP response
        canvas=FigureCanvas(fig)
        response=HttpResponse(content_type='image/png')
        canvas.print_png(response)
        
        # save this to the cache.
        safe_set_cache(cache_key,response,86400)
        print "Saved to cache: %s" % cache_key
    else:    
        print "Got from cache: %s" % cache_key
    
    # Return the response that was either cached OR generated just now.
    return response
