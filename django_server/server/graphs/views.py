# coding=utf-8
from __future__ import division
from django.http import HttpResponse
from datetime import datetime, timedelta
import random
from django.contrib.contenttypes.models import ContentType

from matplotlib import pyplot as plt
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from matplotlib.figure import Figure
from matplotlib.dates import DateFormatter

from django.views.decorators.cache import cache_page
from cacheutil import safe_get_cache,safe_set_cache

@cache_page(86400)
def TEST(request):
    """
    This is a variation of the MatPlotLib/Django example from:
    http://www.scipy.org/Cookbook/Matplotlib/Django
    
    This one adds a bit of high-level caching. The @cache_page
    decorator above caches this view for one day (86400sec). The
    'key' to this cache is the URL that this was accessed under.
    If this needs more robust caching (using GET request string,
    for example), see below.
    """
    # Do stuff with data
    fig=Figure()
    ax=fig.add_subplot(111)
    x=[]
    y=[]
    now=datetime.now()
    delta=timedelta(days=1)
    for i in range(10):
        x.append(now)
        now+=delta
        y.append(random.randint(0, 1000))
    ax.plot_date(x, y, '-')
    ax.xaxis.set_major_formatter(DateFormatter('%Y-%m-%d'))
    fig.autofmt_xdate()

    # Set up a MatPlotLib Canvas to draw on.
    canvas=FigureCanvas(fig)

    # Canvas can do .print_png() to a Python file-like object (like
    # opening a local file with open() ). Django's HttpResponse object
    # works for this, so we can render directly to an HTTP response to
    # the user.
    response=HttpResponse(content_type='image/png')
    canvas.print_png(response)

    # And that's it. Send this reply back to the user the standard Django way.
    return response

def TEST2(request):
    """
    Variation of the above view. This one is an example of how we'd
    vary the cache if we use HTTP GET request variables (i.e.
    http://example.com/view/?var1=foo&var2=bar )
    
    Essentially the same, except it's wrapped around a block that
      1) Makes the cache key out of the parameters
      2) Tests to see whether a cached object exists under that key
    """
    # Get our query string
    if request.REQUEST.has_key('some_query_var'):
        d = request.REQUEST['some_query_var']
    else:
        d = 111
    
    # Check if we have a cache of this render, with the same parameters ...
    cache_key = "cache_page_2 d=%s" % d
    response = safe_get_cache(cache_key)
    
    if not response:
        # ... if we don't have this in cache, render the image like we did above...
        fig=Figure()
        ax=fig.add_subplot(111)
        x=[]
        y=[]
        now=datetime.now()
        delta=timedelta(days=1)
        for i in range(10):
            x.append(now)
            now+=delta
            y.append(random.randint(0, 1000))
        ax.plot_date(x, y, '-')
        ax.xaxis.set_major_formatter(DateFormatter('%Y-%m-%d'))
        fig.autofmt_xdate()

        canvas=FigureCanvas(fig)
        response=HttpResponse(content_type='image/png')
        canvas.print_png(response)
        
        # ... and then save this to the cache.
        safe_set_cache(cache_key,response,86400)

    # Return the response that was either cached OR generated just now.
    return response


def TEST3(request):
    from demographics.models import PlacePopulation
    from places.models import State,County,ZipCode

    try:
        place_type = ContentType.objects.get(app_label="places",model=request.REQUEST['place_type'])
    except:
        return HttpResponse('"place_type" needs to be set', mimetype="text/plain")

    place = None
    if request.REQUEST['place_type'] == "zipcode":
        if request.REQUEST.has_key('place_id'):
            print "zipcode, place_id"
            place = ZipCode.objects.get(id=request.REQUEST['place_id'])
    elif request.REQUEST['place_type'] == "state":
        if request.REQUEST.has_key('abbr'):
            print "state, abbr"
            place = State.objects.get(abbr=request.REQUEST['abbr'])
        elif request.REQUEST.has_key('name'):
            print "state, name"
            place = State.objects.get(name__iexact=request.REQUEST['name'])
    elif request.REQUEST['place_type'] == "county":
        if request.REQUEST.has_key('state__abbr') and request.REQUEST.has_key('name'):
            print "county, name, state__abbr"
            place = County.objects.get(name__iexact=request.REQUEST['name'],state__abbr__iexact=request.REQUEST['state__abbr'])
    if not place:
        return HttpResponse("wat", mimetype="text/plain")
    
    # Check if we have a cache of this render, with the same parameters ...
    cache_key = "cache_page_2 place_type=%s place_id=%s" % (request.REQUEST['place_type'], place.pk)
    response = safe_get_cache(cache_key)
    
    if not response:
        d = place.population_demographics
        
        bg = "#ffffff"
        fig = plt.figure(figsize=(7,7), facecolor=bg)
        ax = fig.add_subplot(111, axis_bgcolor=bg)
        
        labels = "White","Black","Native American","Asian","Pacific Islander","Other"
        fracs = [
            d.onerace_white/d.onerace*100,
            d.onerace_black/d.onerace*100,
            d.onerace_amerindian/d.onerace*100,
            d.onerace_asian/d.onerace*100,
            d.onerace_pacislander/d.onerace*100,
            d.onerace_other/d.onerace*100
        ]
        explode=(.1, .05, 0, 0, 0, 0)

        ax.pie(fracs, explode=explode, labels=labels, autopct='%1.2f%%', labeldistance=1.15, shadow=True)
        ax.set_title('Race in %s (total pop %s)' % (place,d.total))

        canvas=FigureCanvas(fig)
        response=HttpResponse(content_type='image/png')
        canvas.print_png(response)

        # ... and then save this to the cache.
        safe_set_cache(cache_key,response,86400)

    # Return the response that was either cached OR generated just now.
    return response


def TEST4(request):
    from mpl_toolkits.mplot3d import Axes3D
    import matplotlib.pyplot as plt
    import numpy as np
    
    cache_key = "cache_test4-a"
    
    response = None
    #response = safe_get_cache(cache_key)

    if not response:

        fig = plt.figure()
        ax = Axes3D(fig)
        x, y = np.random.rand(2, 100) * 4
        hist, xedges, yedges = np.histogram2d(x, y, bins=4)

        elements = (len(xedges) - 1) * (len(yedges) - 1)
        xpos, ypos = np.meshgrid(xedges[:-1]+0.25, yedges[:-1]+0.25)

        xpos = xpos.flatten()
        ypos = ypos.flatten()
        zpos = np.zeros(elements)
        dx = 0.5 * np.ones_like(zpos)
        dy = dx.copy()
        dz = hist.flatten()
        ax.bar3d(xpos, ypos, zpos, dx, dy, dz, color='b')
        
        canvas=FigureCanvas(fig)
        response=HttpResponse(content_type='image/png')
        canvas.print_png(response)

        # ... and then save this to the cache.
        safe_set_cache(cache_key,response,86400)

    # Return the response that was either cached OR generated just now.
    return response
