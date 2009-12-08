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
from django.views.decorators.cache import cache_control,never_cache

from nationbrowse.places.models import State,County

@never_cache
def random_place(request):
    """
    If a random place is in the cache, use it and return that to the user.
    If not, generate one right now.
    
    Before returning to the user, queue up a background task that generates
    the next random place, to save DB/CPU usage when responding to user. (Prevents
    this view from locking up while Django picks a suitable random object.)
    """
    response = None
    while not response:
        try:
            PlaceClass = rand_choice([State,County])
            
            # Cached list of all of the ID numbers for this place type.
            cache_key = "all_ids: %s" % (PlaceClass.__name__)
            all_ids = safe_get_cache(cache_key)
            if not all_ids:
                all_ids = PlaceClass.objects.only('id').order_by().values_list('pk') # [(0,),(1,),...]
                all_ids = map(lambda x: x[0], all_ids) # pull ID out of tuples for a "regular" list
                safe_set_cache(cache_key,all_ids,604800)
            
            rand_id = rand_choice(all_ids)
            
            if PlaceClass.__name__ == "County":
                place = PlaceClass.objects.get(pk=rand_id)
                url = reverse("places:county_detail",args=(place.state.abbr.lower(),urlencode(place.name.lower())),current_app="places")
            else:
                place = PlaceClass.objects.only('slug').get(pk=rand_id)
                url = reverse("places:state_detail",args=(place.slug,),current_app="places")
            response = HttpResponseRedirect(url)
        except:
            from traceback import print_exc
            print_exc()
            response = None
    return response

@cache_control(public=True,max_age=604800)
def state_detail(request,slug):
    cache_key = "state_detail slug=%s" % slug
    response = safe_get_cache(cache_key)
    
    if not response:
        place = get_object_or_404(State,slug=slug)
        
        response=render_to_response("places/state_detail.html",{
            'title':str(place.name),
            'place':place,
            'demographics':getattr(place.population_demographics,'__dict__',{}),
            'socioeco_data':getattr(place.socioeco_data,'__dict__',{}),
            'crime_data':getattr(place.crime_data,'__dict__',{}),
            'place_type':"state"
        },context_instance=RequestContext(request))
        
        safe_set_cache(cache_key,response,604800)

    return response

@cache_control(public=True,max_age=604800)
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
            'socioeco_data':getattr(place.socioeco_data,'__dict__',{}),
            'crime_data':getattr(place.crime_data,'__dict__',{}),
            'place_type':'county'
        },context_instance=RequestContext(request))
        
        safe_set_cache(cache_key,response,86400)
    
    return response
