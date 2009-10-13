# coding=utf-8
from __future__ import division
from django.http import HttpResponse
from django.db import connection
from cacheutil import safe_get_cache,safe_set_cache
from django.shortcuts import get_object_or_404,render_to_response
from django.http import HttpResponseRedirect,HttpResponsePermanentRedirect,Http404
from django.core.urlresolvers import reverse
from random import choice as rand_choice, sample as rand_sample
from django.template import RequestContext
from django.template.defaultfilters import urlencode

from nationbrowse.places.models import County

from django.db.models.loading import get_model

from nationbrowse.graphs import graph_maker
from threadutil import call_in_bg

def random_place(request):
    place_type = rand_choice(['state','county','zipcode'])
    PlaceClass = get_model("places",place_type)
    if not PlaceClass:
        raise Http404
    
    num = PlaceClass.objects.count()
    rand_nums = rand_sample(xrange(1,num), 20)
    place = PlaceClass.objects.filter(id__in=rand_nums)[0]
    
    # THIS IS AWESOME: start pre-generating the race pie chart for this place before the user
    # even sees the page
    call_in_bg(graph_maker.generate_race_pie,(place,200))
    
    if place_type == "county":
        return HttpResponsePermanentRedirect(
            reverse("places:county_detail",args=(place.state.abbr.lower(),urlencode(place.name.lower())),current_app="places")
        )
    else:
        return HttpResponseRedirect(
            reverse("places:place_detail",args=(place_type,place.slug),current_app="places")
        )
    
def place_detail(request,place_type,slug):
    """
    /places/state/missouri/
    /places/zipcode/65201/
    /places/county/boone-missouri/
    """
    cache_key = "place_detail place_type=%s slug=%s" % (place_type, slug)
    response = safe_get_cache(cache_key)
    connection.close()
    
    # If it wasn't cached, do all of this fancy logic and generate the image as a PNG
    if not response:
        PlaceClass = get_model("places",place_type)
        if not PlaceClass:
            raise Http404        
        
        if place_type == "zipcode":
            place = get_object_or_404(PlaceClass,id=slug)
            title = u"ZIP Code %s in %s, %s" % (place, place.county.long_name, place.county.state)
        elif place_type == "county":
            place = get_object_or_404(PlaceClass,slug=slug)
            response = HttpResponsePermanentRedirect(
                reverse("places:county_detail",args=(place.state.abbr.lower(),urlencode(place.name.lower())),current_app="places")
            )
        else:
            place = get_object_or_404(PlaceClass,slug=slug)
            title = u"%s" % (place.name)

        # THIS IS AWESOME: start pre-generating the race pie chart for this place before the user
        # even sees the page
        #call_in_bg(graph_maker.generate_race_pie,(place,200))

        response=render_to_response("places/place_detail.html",{
            'title':title,
            'place':place,
            'place_type':place_type
        },context_instance=RequestContext(request))
        
        safe_set_cache(cache_key,response,86400)
    
    return response

def county_detail(request,state_abbr,name):
    cache_key = "county_detail state_abbr=%s name=%s" % (state_abbr, name)
    response = safe_get_cache(cache_key)
    connection.close()
    
    if not response:
        place = get_object_or_404(County,state__abbr__iexact=state_abbr,name__iexact=name)

        title = u"%s, %s" % (place.long_name, place.state)
        
        # THIS IS AWESOME: start pre-generating the race pie chart for this place before the user
        # even sees the page
        #call_in_bg(graph_maker.generate_race_pie,(place,200))

        response=render_to_response("places/place_detail.html",{
            'title':title,
            'place':place,
            'place_type':'county'
        },context_instance=RequestContext(request))

        safe_set_cache(cache_key,response,86400)
    
    return response
