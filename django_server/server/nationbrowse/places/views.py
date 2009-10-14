# coding=utf-8
from __future__ import division
from django.http import HttpResponse
from cacheutil import safe_get_cache,safe_set_cache
from django.shortcuts import get_object_or_404,render_to_response
from django.http import HttpResponseRedirect,HttpResponsePermanentRedirect,Http404
from django.core.urlresolvers import reverse
from random import choice as rand_choice
from django.template import RequestContext
from django.template.defaultfilters import urlencode
from django.views.decorators.cache import never_cache

from nationbrowse.places.models import County

from django.db.models.loading import get_model

from nationbrowse.graphs.views import render_graph
from threadutil import call_in_bg
from traceback import print_exc
import sys

def seed_next_random():
    """
    Generates a redirect view to a random Place object (State, ZipCode, or County)
    and caches it. Picking a random place is expensive on the DB and CPU since there
    are over 40000 objects that it picks from, which strains the DB (since it causes
    an iteration over the objects to select the ID).
    
    See random_place() below, for notes on usage.
    """
    cache_key = "random_place"
    
    print >> sys.stderr, "PRE-CACHING random_place"
    
    response = None
    while not response:
        try:
            place_type = rand_choice(['state','county','zipcode'])
            PlaceClass = get_model("places",place_type)
            rand_id = rand_choice(PlaceClass.objects.order_by().values_list('pk'))[0]
            place = PlaceClass.objects.get(pk=rand_id)

            if place_type == "county":
                response = HttpResponsePermanentRedirect(
                    reverse("places:county_detail",args=(place.state.abbr.lower(),urlencode(place.name.lower())),current_app="places")
                )
                # Pre-cache this random view in the background, too.
                call_in_bg(county_detail,(None,place.state.abbr.lower(),urlencode(place.name.lower())))
            else:
                response = HttpResponseRedirect(
                    reverse("places:place_detail",args=(place_type,place.slug),current_app="places")
                )
                # Pre-cache this random view in the background, too.
                call_in_bg(place_detail,(None,place_type,place.slug))
        except:
            print_exc()
            response = None
    print >> sys.stderr, "PRE-CACHED random_place: %s" % getattr(response,'Location','')
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
    
    print >> sys.stderr, "CALL: random_place()"

    if not response:
        print >> sys.stderr, "GENERATING (was not in cache) random_place"
        response = seed_next_random()
    
    # THIS IS AWESOME: start pre-generating the race pie chart for this place before the user
    # even sees the page
    #call_in_bg(render_graph,(None,place_type,place.slug,"race_pie",200))
    
    # Pre-generate the next random location.
    call_in_bg(seed_next_random)
    
    print >> sys.stderr, "RETURN: random_place()"
    
    return response
    

    
def place_detail(request,place_type,slug):
    """
    /places/state/missouri/
    /places/zipcode/65201/
    /places/county/boone-missouri/
    """
    cache_key = "place_detail place_type=%s slug=%s" % (place_type, slug)
    response = safe_get_cache(cache_key)
    
    # If it wasn't cached, do all of this fancy logic and generate the image as a PNG
    if not response:
        print >> sys.stderr, "GENERATING (was not in cache) %s" % cache_key
        
        PlaceClass = get_model("places",place_type)
        if not PlaceClass:
            raise Http404        
        
        if place_type == "zipcode":
            place = get_object_or_404(PlaceClass,id=slug)
            # HORRENDOUSLY SLOW
            #title = u"ZIP Code %s in %s, %s" % (place, place.county.long_name, place.county.state)
            title = u"ZIP Code %s" % (place)
        elif place_type == "county":
            place = get_object_or_404(PlaceClass,slug=slug)
            response = HttpResponsePermanentRedirect(
                reverse("places:county_detail",args=(place.state.abbr.lower(),urlencode(place.name.lower())),current_app="places")
            )
        else:
            place = get_object_or_404(PlaceClass,slug=slug)
            title = u"%s" % (place.name)

        #call_in_bg(render_graph,(None,place_type,place.slug,"race_pie",200))

        response=render_to_response("places/place_detail.html",{
            'title':title,
            'place':place,
            'place_type':place_type
        },context_instance=RequestContext(request))
        
        safe_set_cache(cache_key,response,86400)
    else:
        print >> sys.stderr, "IN CACHE %s" % cache_key
    return response

def county_detail(request,state_abbr,name):
    cache_key = "county_detail state_abbr=%s name=%s" % (state_abbr, name)
    response = safe_get_cache(cache_key)
    
    if not response:
        print >> sys.stderr, "GENERATING (was not in cache) %s" % cache_key
        
        place = get_object_or_404(County,state__abbr__iexact=state_abbr,name__iexact=name)
        
        #call_in_bg(render_graph,(None,place_type,place.slug,"race_pie",200))

        title = u"%s, %s" % (place.long_name, place.state)
        
        response=render_to_response("places/place_detail.html",{
            'title':title,
            'place':place,
            'place_type':'county'
        },context_instance=RequestContext(request))

        safe_set_cache(cache_key,response,86400)
        
        # It's likely that the user will go to the State's page from here (since it's linked
        # from the County detail page). Call it right now to pre-cache it.
        call_in_bg(place_detail,(None,"state",place.state.slug))
    else:
        print >> sys.stderr, "IN CACHE %s" % cache_key

    return response
