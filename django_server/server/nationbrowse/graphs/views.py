# coding=utf-8
from __future__ import division
from django.http import HttpResponse
from django.db import connection
from cacheutil import safe_get_cache,safe_set_cache
from django.shortcuts import get_object_or_404
from django.http import Http404

from nationbrowse.demographics.models import PlacePopulation
from django.contrib.contenttypes.models import ContentType

from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
import graph_maker

def render_graph(request,place_type,slug,graph_type):
    """
    Generates a png pie graph of the given location's racial breakdown. Example
    URLs include:
    /graphs/state/missouri/race_pie/
    /graphs/zipcode/65201/race_pie/
    /graphs/county/boone-missouri/race_pie/
    
    See render_graph_county, below, for a version with nicer URL arguments.
    """
    # Check if we have a cache of this render, with the same request parameters ...
    # Set the cache based on the specific object we got (place_type + place_id)
    cache_key = "render_graph place_type=%s slug=%s graph_type=%s" % (place_type, slug, graph_type)
    response = safe_get_cache(cache_key)
    connection.close()
    
    # If it wasn't cached, do all of this fancy logic and generate the image as a PNG
    if not response:
        # 404 if graph_type is invalid
        if hasattr(graph_maker, 'generate_%s' % graph_type):
            graph_generator = getattr(graph_maker, 'generate_%s' % graph_type)
        else:
            raise Http404
        
        # 404 if the PlaceType is invalid
        ctype = get_object_or_404(ContentType,app_label="places",model=place_type)
        
        # 404 if place slug is invalid
        if place_type.lower() == "zipcode":
            # Querying ZipCode by numeric ID is *MUCH* quicker than string
            place = get_object_or_404(ctype.model_class(),id=slug)
        else:
            place = get_object_or_404(ctype.model_class(),slug=slug)
        
        # Generate the graph & render it as a PNG to the HTTP response
        fig = graph_generator(place)
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

def render_graph_county(request,state_abbr,name,graph_type):
    """
    An alternative view to above, with nicer URL structure for county browsing:
    /graphs/county/mo/boone/race_pie/
    """
    cache_key = "render_graph_county state_abbr=%s name=%s graph_type=%s" % (state_abbr, name, graph_type)
    response = safe_get_cache(cache_key)
    connection.close()
    
    if not response:
        if hasattr(graph_maker, 'generate_%s' % graph_type):
            graph_generator = getattr(graph_maker, 'generate_%s' % graph_type)
        else:
            raise Http404

        County = ContentType.objects.get(app_label="places",model="county").model_class()
        place = get_object_or_404(County,state__abbr__iexact=state_abbr,name__iexact=name)

        fig = graph_generator(place)
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

