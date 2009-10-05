from django.http import HttpResponse
from datetime import datetime, timedelta
import random

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
    response = safe_get_cache()
    
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
