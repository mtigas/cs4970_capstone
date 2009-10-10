# coding=utf-8
from __future__ import division
from django.http import HttpResponse
from django.db import connection
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
    # Check the 'place_type' GET variable.
    place_type = request.GET.get('place_type',None)
    if isinstance(place_type,basestring):
        place_type = str(place_type.lower())
    
    if (not place_type) or (not place_type in ['state','county','zipcode']):
        return HttpResponse('"place_type" needs to be set', mimetype="text/plain")
    
    # Get the rest of the request variables that we want.
    place_id = request.GET.get('place_id',None)
    abbr = request.GET.get('abbr',None)
    name = request.GET.get('name',None)
    state_abbr = request.GET.get('state__abbr',None)
    state_name = request.GET.get('state__name',None)

    # Check if we have a cache of this render, with the same request parameters ...
    # Set the cache based on the specific object we got (place_type + place_id)
    cache_key = "race_piechart place_type=%s place_id=%s abbr=%s name=%s state_abbr=%s state_name=%s" % (
        place_type, place_id, abbr, name, state_abbr, state_name
    )
    response = safe_get_cache(cache_key)

    # Explicitly reset DB connection
    connection.close()
    
    # If it wasn't cached, do all of this fancy logic and generate the image as a PNG
    if not response:
        place = None
        if (place_type == "zipcode") and place_id:
            # Get zipcode by place_id (which is the ZIP #)
            try:
                place = ZipCode.objects.get(id=place_id)
            except ZipCode.DoesNotExist:
                place = None
        elif place_type == "state":
            # State requires either name or abbr
            try:
                if abbr:
                    place = State.objects.get(abbr__iexact=abbr)
                elif name:
                    place = State.objects.get(name__iexact=name)
            except State.DoesNotExist:
                place = None
        elif (place_type == "county") and name:
            # County requires name and either state__name or state__abbr
            try:
                if state_abbr:
                    place = County.objects.get(name__iexact=name,state__abbr__iexact=state_abbr)
                elif state_name:
                    place = County.objects.get(name__iexact=name,state__name__iexact=state_name)
            except County.DoesNotExist:
                place = None
        
        # If we failed to get a location
        if not place:
            return HttpResponse("A %s object with the given request string could not be found." % place_type, mimetype="text/plain")

        # Explicitly reset DB connection
        connection.close()
            
        # Generate the chart
        fig = generate_race_piechart(place,place_type)
        
        # Add it to the HTTP response
        canvas=FigureCanvas(fig)
        response=HttpResponse(content_type='image/png')
        canvas.print_png(response)
        
        # save this to the cache.
        safe_set_cache(cache_key,response,86400)
        print "\nSaved to cache:\n\t%s\n" % cache_key
    else:        
        print "\nGot from cache:\n\t%s\n" % cache_key
    
    # Return the response that was either cached OR generated just now.
    return response
