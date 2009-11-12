# coding=utf-8
from cacheutil import safe_get_cache,safe_set_cache
from django.shortcuts import get_object_or_404,render_to_response
from django.http import Http404
from django.template import RequestContext
from models import PlacePopulation

def demographics_csv(request,place_type,slug,source_id):
    # Not complete yet.
    raise Http404
    """
    cache_key = "demographics_csv place_type=%s slug=%s source_id=%s" % (place_type, slug, source_id)
    response = safe_get_cache(cache_key)

    if not response:
        try:
            demographics = PlacePopulation.objects.get(
                place_type__name=place_type,
                
            )
        
        response=render_to_response("places/place_detail.html",{
            'title':title,
            'place':place,
            'demographics':getattr(place.population_demographics,'__dict__',{}),
            'place_type':place_type
        },context_instance=RequestContext(request))
        
        safe_set_cache(cache_key,response,86400)
    return response
    """