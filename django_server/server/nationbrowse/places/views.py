# coding=utf-8
from __future__ import division
from django.http import HttpResponse
from cacheutil import safe_get_cache,safe_set_cache,USING_DUMMY_CACHE
from django.shortcuts import get_object_or_404,render_to_response
from django.http import HttpResponseRedirect,HttpResponsePermanentRedirect,Http404
from django.core.urlresolvers import reverse
from random import choice as rand_choice
from django.template import RequestContext
from django.template.defaultfilters import urlencode
from django.views.decorators.cache import never_cache

from nationbrowse.places.models import State,ZipCode,County

from nationbrowse.graphs.views import render_graph
from threadutil import call_in_bg

def seed_next_random():
    """
    Generates a redirect view to a random Place object (State, ZipCode, or County)
    and caches it. Picking a random place is expensive on the DB and CPU since there
    are over 40000 objects that it picks from, which strains the DB (since it causes
    an iteration over the objects to select the ID).
    
    See random_place() below, for notes on usage.
    """
    cache_key = "random_place"
    
    response = None
    while not response:
        try:
            PlaceClass = rand_choice([State,ZipCode,County])
            rand_id = rand_choice(PlaceClass.objects.only('id').order_by().values_list('pk'))[0]

            if PlaceClass.__name__ == "County":
                place = PlaceClass.objects.get(pk=rand_id)
                url = reverse("places:county_detail",args=(place.state.abbr.lower(),urlencode(place.name.lower())),current_app="places")
                call_in_bg(county_detail, (None, place.state.abbr.lower(),urlencode(place.name.lower())))
            elif PlaceClass.__name__ == "State":
                place = PlaceClass.objects.only('slug').get(pk=rand_id)
                url = reverse("places:state_detail",args=(place.slug,),current_app="places")
                call_in_bg(state_detail, (None, place.slug))
            else:
                place = PlaceClass.objects.only('slug').get(pk=rand_id)
                url = reverse("places:zipcode_detail",args=(place.slug,),current_app="places")
                call_in_bg(zipcode_detail, (None, place.slug))
            response = HttpResponseRedirect(url)
        except:
            from traceback import print_exc
            print_exc()
            response = None
    safe_set_cache(cache_key,response,604800)
    
    return response

@never_cache
def random_place(request):
    """
    If a random place is in the cache, use it and return that to the user.
    If not, generate one right now.
    
    Before returning to the user, queue up a background task that generates
    the next random place, to save DB/CPU usage when responding to user. (Prevents
    this view from locking up while Django picks a suitable random object.)
    """
    cache_key = "random_place"
    response = safe_get_cache(cache_key)
    
    if not response:
        response = seed_next_random()
    
    # Pre-generate the next random location.
    if not USING_DUMMY_CACHE:
        call_in_bg(seed_next_random)
    
    return response

def state_detail(request,slug):
    cache_key = "state_detail slug=%s" % slug
    response = safe_get_cache(cache_key)
    
    if not response:
        place = get_object_or_404(State,slug=slug)
        
        response=render_to_response("places/place_detail.html",{
            'title':str(place.name),
            'place':place,
            'demographics':getattr(place.population_demographics,'__dict__',{}),
            'place_type':"state"
        },context_instance=RequestContext(request))
        
        safe_set_cache(cache_key,response,86400)

    return response

def zipcode_detail(request,slug):
    cache_key = "zipcode_detail slug=%s" % slug
    response = safe_get_cache(cache_key)
    
    if not response:
        place = get_object_or_404(ZipCode,id=slug)
        
        #title = "ZIP Code %s in %s, %s" % (place, place.county.long_name, place.county.state)
        if place.state:
            title = "ZIP Code %s, %s" % (place, place.state)
        else:
            title = "ZIP Code %s" % place

        response=render_to_response("places/place_detail.html",{
            'title':title,
            'place':place,
            'demographics':getattr(place.population_demographics,'__dict__',{}),
            'place_type':"zipcode"
        },context_instance=RequestContext(request))
        
        safe_set_cache(cache_key,response,86400)

        # It's likely that the user will go to the State's page from here (since it's linked
        # from the detail page). Call it right now to pre-cache it.
        if (not USING_DUMMY_CACHE) and (place.state):
            call_in_bg(state_detail,(None,place.state.slug))

    return response

def county_detail(request,state_abbr,name):
    cache_key = "county_detail state_abbr=%s name=%s" % (state_abbr, name)
    response = safe_get_cache(cache_key)
    
    if not response:
        place = get_object_or_404(County,state__abbr__iexact=state_abbr,name__iexact=name)
        
        title = u"%s, %s" % (place.long_name, place.state)
        
        response=render_to_response("places/place_detail.html",{
            'title':title,
            'place':place,
            'demographics':getattr(place.population_demographics,'__dict__',{}),
            'place_type':'county'
        },context_instance=RequestContext(request))
        
        safe_set_cache(cache_key,response,86400)
        
        if (not USING_DUMMY_CACHE) and (place.state):
            call_in_bg(state_detail,(None,place.state.slug))

    return response
